import face_recognition

def is_face_matched(image1_path, image2_path):
    try:
        image1 = face_recognition.load_image_file(image1_path)
        image2 = face_recognition.load_image_file(image2_path)

        # Encode faces
        image1_encoding = face_recognition.face_encodings(image1)[0]
        image2_encoding = face_recognition.face_encodings(image2)[0]

        # Compare faces
        results = face_recognition.compare_faces([image1_encoding], image2_encoding)
        return results[0]
    except Exception as e:
        print(f"Error during face matching: {e}")
        return False
