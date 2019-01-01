<div align="center">
<h3>py-rollcall</h3>
<img src="https://i.imgur.com/f4yYQB2.png">
1071 Image Processing Semester Project
</div>

## Overview
Automate traditional roll calls using deep metric learning, i.e., deep learning-based facial recognition.

Please note that this project was developed on Gentoo **Linux** and has not been tested on other platforms!

## Dependencies
* Python >= 3.5
* PyGTK **[2.24.0-r4](https://gitweb.gentoo.org/repo/gentoo.git/tree/dev-python/pygtk/pygtk-2.24.0-r4.ebuild)**
* OpenCV 3.4.5
* imutils
* dlib
* face_recognition

## Installation
Please Make sure you have all dependencies installed. The installation commands can vary between different distros
```
$ sudo emerge -av python pygtk
$ pip3 install --user python-opencv imutils dlib face_recognition
```

Clone this repo and run `pyrollcall.py` in the project's root directory.
```
$ git clone https://github.com/aesophor/pyrollcall
$ cd pyrollcall && python pyrollcall.py
```

## Features
* Manage (add/edit/remove) your own courses and students, each course may contains a list of students. This program can be reused throughout different classes you teach
* Take photos of  each student and train the program so that it can recognize faces correctly
* Start a roll call session, let student sign in to the class by taking photos (a webcam is needed)
* Information about student arrival will be displayed in the window on-the-fly (e.g., arrival rate, who has and has not arrived)
* Export reports to a text file by clicking the `End` button in `roll call` tab. These files can be found under `logs/` (relative to project's root directory).

## References
* [Face recognition with OpenCV, Python, and deep learning](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/) by [Adrian Rosebrock](https://www.pyimagesearch.com/author/adrian/) for the usage of dlib and face_recognition

## License
Available under the [MIT License](https://github.com/aesophor/pyrollcall/blob/master/LICENSE)
