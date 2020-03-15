import face_recognition
import os

def do_recognition(base_picture, new_picture):
    picture_of_me = face_recognition.load_image_file(base_picture)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    unknown_picture = face_recognition.load_image_file(new_picture)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

    if results[0] == True:
        base = os.path.basename(base_picture)
        return(os.path.splitext(base)[0], True)
    else:
        return("User not identified", False)
    
