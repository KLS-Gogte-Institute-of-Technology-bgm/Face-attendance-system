 
import face_recognition
import cv2
import numpy as np
import glob
import pickle
import datetime
from csv import writer

video_capture = cv2.VideoCapture(0)


def attendence(name):
    now=datetime.datetime.now()
    timestamp=f"{now.date()} {now.time()}"
    # print(timestamp)
    List=[name,timestamp]
    with open('attendence.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(List)
        f_object.close()

#--------------------------------------------------------------------------------------------------------------



try:
    pickle_in = open("data.pickle","rb")
    d = pickle.load(pickle_in)
    print(d)
except:
    d={}



# #--------------------------------------------------------------------------------------------------------------
images=glob.glob("images/*.jpg")
print(images)

for i in images:
    print(i)
    name=i.split("/")[1].split(".")[0]

    if name not in d.keys():
        image_file=face_recognition.load_image_file(f"{i}")
        encoding=face_recognition.face_encodings(image_file,num_jitters=50,model='large')[0]
        # print(encoding)
        
        # print(name)
        d[name]=encoding
        print(f"Encoding completed : {name}")
# print(d)
    
# #--------------------------------------------------------------------------------------------------------------

# Create arrays of known face encodings and their names
known_face_encodings = list(d.values())
known_face_names = list(d.keys())

# print(type(list(d.values())))
# print(type(list(d.keys())))

# print(known_face_names)
# print(known_face_encodings)

# # # #--------------------------------------------------------------------------------------------------------------


pickle_out = open("data.pickle","wb")
pickle.dump(d, pickle_out)
pickle_out.close()

# # #--------------------------------------------------------------------------------------------------------------

# # Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    small_frame=frame
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            # best_match_index = np.argmin(face_distances)
            # if matches[best_match_index]:
            #     name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        # top *= 4
        # right *= 4
        # bottom *= 4
        # left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if name!='Unknown':
            attendence(name)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

#--------------------------------------------------------------------------------------------------------------