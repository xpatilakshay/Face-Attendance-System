import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
from datetime import datetime
from db_config import connect_db
from PIL import Image
import pandas as pd


# Database Connection
conn = connect_db()
if conn is None:
    print("❌ Error: Failed to connect to the database.")
    exit()
cursor = conn.cursor()

# Initialize Webcam (DroidCam / Local Camera)
# cap = cv2.VideoCapture("http://192.168.1.100:4747/video")  # Change to 0 for built-in webcam
cap = cv2.VideoCapture(1)

cap.set(3, 640)
cap.set(4, 480)

# Load Background Image
imgBackground = cv2.imread('Resources/background.png')

# Load Mode Images
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Load Encodings
print("🔹 Loading Encode File ...")
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds
print("✅ Encode File Loaded")

# Variables
modeType = 0
counter = 0
id = -1
imgStudent = []

# Function to export attendance data to Excel
def export_to_excel():
    try:
        cursor.execute("SELECT * FROM attendance ORDER BY id ASC")
        attendance_data = cursor.fetchall()

        df = pd.DataFrame(attendance_data, columns=["ID", "Student ID", "Name", "Major", "Attendance Date"])
        df["ID"] = df["ID"].astype(int)  # Ensure ID is treated as an integer

        excel_file = "attendance_data.xlsx"
        df.to_excel(excel_file, index=False)
        print(f"✅ Attendance data exported to {excel_file}")
    except Exception as e:
        print(f"❌ Error exporting attendance data: {e}")

# Function to add new student face
def add_new_student_face():
    print("Adding new student face...")
    ret, frame = cap.read()
    if ret:
        student_id = input("Enter new student ID: ")
        student_name = input("Enter new student name: ")
        student_major = input("Enter new student major: ")
        student_year = input("Enter new student starting year: ")
        student_standing = input("Enter new student standing: ")
        student_year_level = input("Enter new student year level: ")

        # Save the captured image
        image_path = f"Images/{student_id}.png"
        cv2.imwrite(image_path, frame)
        print(f"Image saved as {image_path}")

        # Add student to database
        cursor.execute("""
            INSERT INTO students (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (student_id, student_name, student_major, student_year, 0, student_standing, student_year_level, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()

        # Update encodings
        img = Image.open(image_path).convert("RGB")
        img = np.array(img)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encodeListKnown.append(encodings[0])
            studentIds.append(student_id)
            with open("EncodeFile.p", "wb") as file:
                pickle.dump((encodeListKnown, studentIds), file)
            print(f"✅ New student face encoding added for {student_name} (ID: {student_id})")
        else:
            print("❌ No face found in the captured image.")
    else:
        print("❌ Failed to capture image.")

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Fetch student data from MySQL
                cursor.execute(f"SELECT * FROM students WHERE id={id}")
                studentInfo = cursor.fetchone()

                if studentInfo:
                    imgStudent = cv2.imread(f"Images/{id}.png")

                    # Fix last_attendance_time format
                    try:
                        last_attendance_time = datetime.strptime(str(studentInfo[7]), "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        last_attendance_time = datetime(2000, 1, 1, 0, 0, 0)  # Default old date

                    secondsElapsed = (datetime.now() - last_attendance_time).total_seconds()

                    if secondsElapsed > 30:
                        new_attendance_count = int(studentInfo[4]) + 1  # Convert to `int`

                        # Update students table
                        cursor.execute(f"UPDATE students SET total_attendance={new_attendance_count}, "
                                       f"last_attendance_time='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' "
                                       f"WHERE id={id}")
                        conn.commit()

                        # Insert into attendance table
                        cursor.execute("INSERT INTO attendance (student_id, name, major, attendance_date) "
                                       "VALUES (%s, %s, %s, %s)",
                                       (id, studentInfo[1], studentInfo[3],
                                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                        conn.commit()

                        # ✅ Print confirmation in console
                        print("==========================================")
                        print(f"✅ Attendance Recorded Successfully!")
                        print(f"Student Name : {studentInfo[1]}")
                        print(f"Student ID   : {id}")
                        print(f"Major        : {studentInfo[3]}")
                        print(f"Timestamp    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        print("==========================================")


                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    if studentInfo:  # Check if studentInfo is not None
                        cv2.putText(imgBackground, str(studentInfo[4]), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo[2]), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo[5]), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo[6]), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo[3]), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo[1], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, studentInfo[1], (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        imgStudent = cv2.resize(imgStudent, (216, 216))  # Resize to match the target area
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    # Check for key press to export to Excel
    key = cv2.waitKey(1)
    if key == ord('e'):  # Press 'e' to export to Excel
        export_to_excel()
    if key == ord('i'):  # Press 'i' to add new student face
        add_new_student_face()
    if key == ord('q'):  # Press 'q' to exit
        exit()
    cv2.imshow("Face Attendance", imgBackground)
