## Overview
Facial recognition roll call system using deep metric learning, i.e., deep learning-based facial recognition

## Requirement
* Python >= 3.5

## Installation and Execution
```
$ git clone https://github.com/aesophor/pyrollcall.git && cd pyrollcall
$ source venv/bin/activate
$ ./pyrollcall.py
```

## Dependencies (Already bundled in virtualenv)
* PyGTK **[2.24.0-r4](https://gitweb.gentoo.org/repo/gentoo.git/tree/dev-python/pygtk/pygtk-2.24.0-r4.ebuild)**
* OpenCV 3.4.5
* imutils
* dlib
* face_recognition

## Features
* Manage (add/edit/remove) your own courses and students; each course may contains a list of students. This program can be reused throughout different classes you teach
* Take photos of  each student and train the program so that it can recognize faces correctly
* Start a roll call session, let student sign in to the class by taking photos (a webcam is needed)
* Information about students' arrival will be displayed on-the-fly (e.g., arrival rate, who has and has not arrived)
* Export reports to a text file by clicking the `End` button in `roll call` tab. These files can be found under `logs/` (relative to project's root directory).

## References
* [Face recognition with OpenCV, Python, and deep learning](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/) by [Adrian Rosebrock](https://www.pyimagesearch.com/author/adrian/) for the usage of dlib and face_recognition

## License
Available under the [MIT License](https://github.com/aesophor/pyrollcall/blob/master/LICENSE)
