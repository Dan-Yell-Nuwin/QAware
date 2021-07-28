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