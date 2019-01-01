# -*- encoding: utf-8 -*-

from pathlib import Path
from imutils import paths
import face_recognition
import cv2
import os

class FaceEncoding:
    """ This class is a wrapper of a face encoding and the person's name """
    def __init__(self, encoding, name: str):
        self.encoding = encoding
        self.name = name


def collect_face(student=None, img_count=1, capture_key=0x20):
    """ Collect several images of a person's face via webcam
    :param student: The student of which we'll take photos
    :param img_count: Number of images to take
    :param capture_key: Keycode of the key which captures images (default=SPACE)
    :return: A list of paths to the photos taken
    """
    current_img_no = 0
    photo_dir = "faces/temp/" if student is None else student.photo_dir
    webcam_title = "Face Collector" if student is None else "Face Collector ({})".format(student.name)

    cv2.namedWindow(webcam_title)
    cam = cv2.VideoCapture(0)

    if cam.isOpened():
        rval, img = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(webcam_title, img)
        rval, img = cam.read()
        key = cv2.waitKey(20)

        if key == capture_key:
            # mkdir -p on config_location and datafile_location.
            Path(photo_dir).mkdir(parents=True, exist_ok=True)
            cv2.imwrite(photo_dir + str(current_img_no) + '.png', img)
            current_img_no += 1
            if current_img_no >= img_count:
                break
        elif key == 27:
            break

    cv2.destroyWindow(webcam_title)
    del cam
    return list(paths.list_images(photo_dir))


def encode_faces(db, faces_dir: str):
    """ Encode all students faces in the specified course 
    :param course: Faces of each student in this course will be processed
    """
    image_paths = list(paths.list_images(faces_dir))

    for (i, image_path) in enumerate(image_paths):
        # Extract the person name from the image path.
        print("[INFO] processing image {} {current}/{total}".format(
            image_path, current=i + 1, total=len(image_paths)))
        student_name = image_path.split(os.path.sep)[-2].split('_')[1] # get directory name

        # Load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB).
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

        # Detect the (x, y) of the bounding boxes corresponding to
        # each face in the input image.
        boxes = face_recognition.face_locations(image, model="hog")

        # Compute the facial embedding for the face.
        encodings = face_recognition.face_encodings(image, boxes)

        # Add all face encodings in the photo to our database.
        db.face_encodings = [FaceEncoding(e, student_name) for e in encodings]


def recognize_face(db, img_path: str):
    """ Recognize the faces in the specified image
    :param img_path: Image which contains the face of a student
    """
    # Load the input image and convert it from BGR to RGB
    image = cv2.imread(img_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect the (x, y) of the bounding boxes corresponding to
    # each face in the input image, then compute the facial embeddings
    # for each face.
    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)

    # Initialize the list of names for each face detected
    names = []

    # Loop over the facial embeddings
    for encoding in encodings:
        # Attempt to match each face in the input image to our known encodings
        db_encodings = [e.encoding for e in db.face_encodings]
        matches = face_recognition.compare_faces(db_encodings, encoding)
        name = "Unknown"

        # Check if we've found a match
        if True in matches:
            # find the indices of all matched faces, and initialize a dict
            # to count the total number of times each face was matched.
            matchedIndices = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # Loop over the matched indicies and maintain a count for each
            # recognized face.
            for i in matchedIndices:
                name = db.face_encodings[i].name
                counts[name] = counts.get(name, 0) + 1

            # Determine the recognized face with the largest number of votes
            # (note: in the event of an unlikely tie Python will select the
            # first entry in the dict)
            name = max(counts, key=counts.get)

        # Update the list of names
        if name != "Unknown":
            names.append(name)


    # Loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # Draw the predicted face name on the images
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)

    # Show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    return names
