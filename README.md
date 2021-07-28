# QAware
Visualization for awareness on sleepy drivers.

`pip install pygame`

then run the car_game.py to see the demon

notes from Allan:
	ideally use openCV to make SleepDetector(), so I can call it in the game
	It needs these functions:
		detect()
		get_eye_closed_time()

	see how I call them from line 60 - 77
	Feel free to change these design choices :)

`python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav`

# Description

This project QAware is a AI/ML recognition simulation software for detecting if drivers are falling asleep on the road and pulls over the driver. To show this, we created a UI game for drivers to move around while we monitor the eye awareness level on the driver. Using OpenCV and facial recognition, we use these algorithms to detect if their eyes fall underneath a certain threshold to take hold of their car and pull them over. Check out our demo to visually see how this works!

By Allan, Momen, and Daniel
