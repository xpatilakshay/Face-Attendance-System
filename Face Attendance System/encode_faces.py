import os
import face_recognition
import numpy as np
import pickle
from PIL import Image

def find_encodings(images):
    encode_list = []
    for img_path in images:
        try:
            img = Image.open(img_path).convert("RGB")
            img = np.array(img)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                encode_list.append(encodings[0])
            else:
                print(f"⚠ No face found in {img_path}")
        except Exception as e:
            print(f"❌ Error processing {img_path}: {e}")
    return encode_list

if __name__ == "__main__":
    path = "E:/Face Attendance System/images"
    images = []
    student_ids = []

    for file in os.listdir(path):
        if file.lower().endswith((".jpeg", ".jpg", ".png")):
            images.append(os.path.join(path, file))
            student_ids.append(os.path.splitext(file)[0])

    print(f"📂 Images Found: {len(images)}")
    print(f"✅ Student IDs: {student_ids}")

    print("🔹 Encoding Started ...")
    encode_list_known = find_encodings(images)

    if encode_list_known:
        with open("EncodeFile.p", "wb") as file:
            pickle.dump((encode_list_known, student_ids), file)
        print(f"✅ Encoding Completed. {len(encode_list_known)} face encodings saved.")
    else:
        print("❌ No valid face encodings found. Check the images.")
