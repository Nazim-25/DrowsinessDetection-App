# Driver Drowsiness Detection Application

## Overview
This repository contains a real-time computer vision application that uses facial landmark analysis and algorithms to detect driver drowsiness and fatigue. The app is designed to help prevent accidents caused by drowsy driving.

## Features

-Detects faces in video stream from webcam in real-time.

-Analyzes facial landmarks around eyes and mouth areas.

-Uses eye aspect ratio and mouth aspect ratio algorithms to detect blinking, yawning, and mouth opening.

-Classifies driver state as awake, yawning, asleep or no driver detected.

-Plays audio alerts if signs of fatigue or no driver is detected.

-Runs as a Flask web application for easy viewing of detection results.


The application is built using dlib and OpenCV libraries for facial landmark detection and computer vision tasks. Audio playback is handled using Pygame. Real-time video streaming and detection results are served using Flask.

## Installation

To install the app, follow these steps:

1. Clone the repository:

```
git clone https://github.com/Nazim-25/DrowsinessDetection-App.git
```

2. Install the dependencies:

```
pip install -r requirements.txt
```

3. Run the app:

```
python app.py
```

## Acknowledgements
* **OpenCV:** Open Source Computer Vision Library
* **Dlib:** Machine Learning Toolkit
* **Python:** Programming Language
* **NumPy:** Numerical Computing Library
* **Pygame:** Python library for game development (used for sound alerts)
* **Imutils:**  A series of convenience functions for image processing
* **Flask:** Web framework for building web applications in Python

## Usage

The app will start running and will monitor your face for signs of drowsiness and fatigue. If the app detects that you are drowsy or fatigued, it will alert you with a visual and audio alert.

## Customization

You can customize the app's settings to suit your needs. The following settings are available:

* **Alert threshold:** The threshold at which the app will alert you.
* **Alert type:** The type of alert that will be displayed.
* **Alert sound:** The sound that will be played when the app alerts you.

## Troubleshooting

If you are having trouble running the app, please check the following:

* Make sure that you have installed the dependencies correctly.
* Make sure that you are running the app in a Python 3 environment.
* Make sure that you have a webcam connected to your computer.
* Make sure that you have granted the app permission to access the webcam.

## Contributing

If you would like to contribute to the app, please feel free to submit a pull request.


