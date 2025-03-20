
# Face-Attendance-System
An automated attendance system using real-time face recognition with Python, OpenCV, and MySQL. It securely captures and matches facial features to mark attendance. Features include a user-friendly GUI, real-time logging, and data export. Ideal for institutions and organizations seeking efficient attendance tracking.


**Project Title:** Face Recognition Attendance System

**1. Introduction:**
The Face Recognition Attendance System is an advanced, automated solution designed to streamline attendance management. Using real-time face recognition technology, the system eliminates manual attendance tracking, ensuring efficiency, accuracy, and security.

**2. Objectives:**
- Automate the attendance marking process.
- Enhance security and accuracy using facial recognition.
- Reduce time consumption compared to traditional methods.
- Store attendance data in a structured MySQL database.
- Provide interactive GUI features for user convenience.

**3. Technologies Used:**
- **Programming Language:** Python
- **Database:** MySQL (XAMPP)
- **Libraries:** OpenCV, face_recognition, NumPy, pickle, cvzone
- **Hardware:** Webcam (DroidCam or local camera)

**4. System Architecture:**
- **Face Encoding:** The system captures and encodes facial features from images and stores them in a database.
- **Real-Time Recognition:** The camera captures a live image, detects faces, and matches them with stored encodings.
- **Database Integration:** Attendance records are stored and managed in MySQL.
- **User Interface:** A highly interactive GUI displays real-time attendance updates and allows data export to CSV and printing.

**5. Features:**
- **Automated Face Detection & Recognition**
- **Real-Time Attendance Logging**
- **Integration with MySQL Database**
- **User-Friendly GUI with Export & Print Features**
- **Attendance History Tracking**

**6. Working Mechanism:**
- The system connects to a webcam (DroidCam or local camera) to capture real-time images.
- It preprocesses the images and extracts facial encodings.
- The extracted features are compared with stored encodings for identification.
- If a match is found, attendance is recorded in MySQL.
- The system updates the GUI to reflect attendance status.

**7. Database Design:**
- **Students Table:** Stores student details (ID, Name, Major, Attendance Count, etc.).
- **Attendance Table:** Stores attendance records with timestamps.

**8. Expected Outcomes:**
- Reduction in manual attendance errors.
- Faster and more efficient attendance tracking.
- Secure and tamper-proof attendance records.

**9. Conclusion:**
The Face Recognition Attendance System provides a seamless, efficient, and secure way to manage attendance using cutting-edge facial recognition technology. With its integration into MySQL and a user-friendly interface, it is a robust and reliable solution for institutions and organizations.

# working

**- Press i :** insert new student and Enter student data in console.
**- press e :** To record Attendance to excel file i.e, xlsx file.
**- press q :** to quite

# Project Screenshots / Graphical User Interface (GUI)

![attendance](https://github.com/xpatilakshay/Face-Attendance-System/blob/cc9013e83076c96a3b96a9037c9a68406db1484a/Face%20Attendance%20System/Face%20Attendance%20System%20Screenshots/1.jpeg)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
![attendance](https://github.com/xpatilakshay/Face-Attendance-System/blob/00c60dbe4d33bf0de78d54708ea815bf031c8d4e/Face%20Attendance%20System/Face%20Attendance%20System%20Screenshots/2.jpeg)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
![Attendance](https://github.com/xpatilakshay/Face-Attendance-System/blob/c6025481c4af6fa3555a97d2e0212c889632705f/Face%20Attendance%20System/Face%20Attendance%20System%20Screenshots/3.jpeg)
