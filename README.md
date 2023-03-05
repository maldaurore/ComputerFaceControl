# ComputerFaceControl
Python program to control the computer with face and head movements using Google Mediapipe, pyautogui and a webcam.


This program uses the webcam and MediaPipe library to find a face and its landmarks, uses these landmarks to detect gestures and movements, and execute some actions 
with the gestures using pyautogui. It is necessary to have MediaPipe, OpenCV, pyautogui, math and numpy installed. 

The actions available at this moment are: scroll up, scroll down, scroll left, scroll right, zoom in, and travel between windows us you would do with alt+tab macro. 
This first version was made for Windows 10.

In order to execute the actions, you have to raise your eyebrows. This will put the program into the "observing" state, where it gets ready to detect a gesture.
This is done as a sort of protection for capturing gestures when the user doesn't want it to capture them. 
Once you have raised your eyebrows, any of the following gestures will be detected and the program will make the corresponding actions:

1. Move the face up: this will scroll down the screen.
2. Move the face down: this will scroll up the screen.
3. Move the face to the right: this will scroll the screen to the left.
4. Move the face to the left: this wil scroll the screen to the right.
5. Open the mouth: this will zoom in.
6. Tilt the head to the right: this will open the window menu. If you relax your eyebrows, this will just travel to the next windox. But if you keep your eyebrows raised and tilt your head again, you can travel within the window menu from left to right as you would do with Windows 10 alt+tab macro, and once you are in the window you want, relax your eyebrows to select it and close the window menu. 

These are the options available for now, the goal is to keep adding gestures and options, hand gestures, speech recognition for automatic writing, and more. 
The program has some bugs and issues that I will be fixing in future versions.
