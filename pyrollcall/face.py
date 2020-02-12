# -*- encoding: utf-8 -*-

""" Most of the code in this module were borrowed from this tutorial on pyimagesearch By Adrian Rosebrock.
https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
"""

import os
import cv2
import face_recognition
import time

import pyrollcall.utils as utils

class FaceEncoding:
    """ This class is a wrapper of a face encoding and the student's id """
    def __init__(self, encoding, student_id: str):
        self.encoding = encoding
        self.student_id = student_id


def collect_faces(student=None, img_count=1, capture_key=0x20):
    """ Collect several images of a person's face via webcam
    :param student: The student of which we'll take photos
    :param img_count: Number of images to take
    :param capture_key: Keycode of the key which captures images (default=SPACE)
    :return: A list of paths to the photos taken
    """
    current_img_no = 0
    taken_photo_paths = []

    photo_dir = "photos/" if student is None else student.get_photo_dir()
    photo_filename = utils.get_datetimestamp().replace('/', '_') if student is None else student.name
    webcam_title = "Face Collector" if student is None else "Face Collector ({})".format(student.name)

    cv2.namedWindow(webcam_title)
    cam = cv2.VideoCapture(0)

    if cam.isOpened():
        rval, img = cam.read()
    else:
        rval = False

    while rval:
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(image_rgb)

        # Loop over the recognized faces.
        for top, right, bottom, left in boxes:
            # Draw the predicted face id on the image.
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow(webcam_title, img)
        rval, img = cam.read()
        key = cv2.waitKey(20)

        if key == capture_key:
            utils.mkdir(photo_dir)
            img_path = photo_dir + photo_filename + '_' + str(current_img_no) + '.png'

            taken_photo_paths.append(img_path)
            cv2.imwrite(img_path, img)

            current_img_no += 1
            if current_img_no >= img_count:
                break
        elif key == 27: # esc
            break

    cv2.destroyWindow(webcam_title)
    del cam
    return taken_photo_paths


def encode_faces(db, faces_dir: str, encoding_model="cnn"):
    """ (Re-)encode all students faces in the specified directory and subdirectories.
    Each photo should only contain a single face.
    :param course: Faces of each student in this course will be processed
    :param encoding_model: Use `hog` for speed, `cnn` for accuracy
    """
    db.face_encodings.clear()
    db.encoded_face_img_paths.clear()

    image_paths = list(utils.list_images(faces_dir))
    time_start = time.perf_counter()

    for (i, image_path) in enumerate(image_paths):
        print("[INFO] processing image {} {current}/{total}".format(
            image_path, current=i+1, total=len(image_paths)))

        # Extract student ID from image's directory name.
        student_id = image_path.split(os.path.sep)[-2].split('_')[0]

        # Load input img and convert it from BGR(OpenCV) to RGB(dlib).
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

        # Detect the (x, y) of the bounding box of each face in input image.
        boxes = face_recognition.face_locations(image, model=encoding_model)

        # Compute the facial embedding for the face.
        encodings = face_recognition.face_encodings(image, boxes)

        # Export all face encodings in the photo to our database.
        db.face_encodings += [FaceEncoding(e, student_id) for e in encodings]
        db.encoded_face_img_paths.append(image_path)

    time_end = time.perf_counter()
    print(f"[INFO] faces encoded in {time_end - time_start:0.4f} seconds")


def encode_new_faces(db, faces_dir: str, encoding_model="cnn"):
    """ Encode new students' faces which have not been encoded before.
    Each photo should only contain a single face.
    :param course: Faces of each student in this course will be processed
    :param encoding_model: Use `hog` for speed, `cnn` for accuracy
    """
    image_paths = list(utils.list_images(faces_dir))
    time_start = time.perf_counter()

    for (i, image_path) in enumerate(image_paths):

        # Skip this image if it has already been processed before.
        if image_path in db.encoded_face_img_paths:
            continue

        print("[INFO] processing image {} {current}/{total}".format(
            image_path, current=i+1, total=len(image_paths)))

        # Extract student ID from image's directory name.
        student_id = image_path.split(os.path.sep)[-2].split('_')[0]

        # Load input img and convert it from BGR(OpenCV) to RGB(dlib).
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

        # Detect the (x, y) of the bounding box of each face in input image.
        boxes = face_recognition.face_locations(image, model=encoding_model)

        # Compute the facial embedding for the face.
        encodings = face_recognition.face_encodings(image, boxes)

        # Export all face encodings in the photo to our database.
        db.face_encodings += [FaceEncoding(e, student_id) for e in encodings]
        db.encoded_face_img_paths.append(image_path)

    time_end = time.perf_counter()
    print(f"[INFO] faces encoded in {time_end - time_start:0.4f} seconds")


def recognize_faces(db, img_path: str, encoding_model="cnn"):
    """ Recognize the faces in the specified image
    :param img_path: Image which contains the face of a student
    :param encoding_model: Use `hog` for speed, `cnn` for accuracy
    :return: A list of ids of the students recognized
    """
    print("[INFO] recognizing face in {}".format(img_path))

    # Initialize the list of ids for each face detected.
    db_encodings = [e.encoding for e in db.face_encodings]
    student_ids = []

    # Load the input image and convert it from BGR to RGB.
    image = cv2.imread(img_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect the (x, y) of the bounding box of each face in input image.
    boxes = face_recognition.face_locations(image_rgb, model=encoding_model)

    # Compute the facial embeddings for each face.
    encodings = face_recognition.face_encodings(image_rgb, boxes)


    for encoding in encodings:
        # Attempt to match each face in the input image to our known encodings.
        matches = face_recognition.compare_faces(db_encodings, encoding)
        student_id = "Unknown"

        # Check if we've found a match
        if True in matches:
            # find the indices of all matched faces, and initialize a dict
            # to count the total number of times each face was matched.
            matchedIndices = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # Loop over the matched indices and maintain a count for each
            # recognized face.
            for i in matchedIndices:
                student_id = db.face_encodings[i].student_id
                counts[student_id] = counts.get(student_id, 0) + 1

            # Determine the recognized face with the largest number of votes
            # (note: in the event of an unlikely tie Python will select the
            # first entry in the dict)
            student_id = max(counts, key=counts.get)

        # Update the list of student ids
        if student_id != "Unknown":
            student_ids.append(student_id)
        else:
            print("[INFO] Unable to recognize this person")


    # Loop over the recognized faces.
    for ((top, right, bottom, left), student_id) in zip(boxes, student_ids):
        # Draw the predicted face id on the image.
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, db.get_student(student_id).name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(20)

    return student_ids
