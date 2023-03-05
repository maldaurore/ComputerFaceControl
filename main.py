import cv2
import mediapipe as mp
import math
import numpy as np
import guiControl as control

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mp_drawing_styles = mp.solutions.drawing_styles

# This variable holds the initial face measurements values when eyebrows are raised to 
# determine when a gesture is done
initial_state = {"initial_z_face_angle" : 0,
                 "initial_x_face_angle" : 0,
                 "initial_x_nosetip" : 0,
                 "observing" : False,
                 "window_traveling" : False}

# This allows to ignore the next frame after making an operation
# to prevent this operation repeating unwantedly.
ignore_frame = False

print("Iniciando")

with mp_face_mesh.FaceMesh(
    static_image_mode = False,
    max_num_faces = 1,
    min_detection_confidence = 0.5,
    refine_landmarks = True
    ) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        
        if not success:
            continue
        
        elif ignore_frame == True:
            # If ignore frame is True, continues to the next frame and ignores the actual. 
            # Sets ignore frame to False so it doesn't ignore the next frame.
            ignore_frame = False
            continue
        
        image_height = image.shape[0]
        image_width = image.shape[1]
        image.flags.writeable = False
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = face_mesh.process(image)
        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(150, 150, 150), thickness=1, circle_radius=1)
                )
                
                # Saves the coordinates of the left eyebrow landmark (landmark 107) 
                # that moves up when eyebrows are raised.
                left_eyebrow = (int(face_landmarks.landmark[107].x * image_width), 
                            int(face_landmarks.landmark[107].y * image_height))
                
                # Same as with left eyebrow
                right_eyebrow = (int(face_landmarks.landmark[336].x * image_width), 
                            int(face_landmarks.landmark[336].y * image_height))
                
                # Saves the coordinates of the landmark above the left eyebrow landmark 
                # to measure the distance between them.
                left_eyebrow_top = (int(face_landmarks.landmark[109].x * image_width), 
                           int(face_landmarks.landmark[109].y * image_height))
                
                # Same sa with left eyebrow top
                right_eyebrow_top = (int(face_landmarks.landmark[338].x * image_width), 
                           int(face_landmarks.landmark[338].y * image_height))
                
                # Saves the coordinates of the landmark corresponding to the top of the face (landmark 10)
                # Includes Z coordinate in order to calculate the face angle with the face bottom landmark.
                face_top = (int(face_landmarks.landmark[10].x * image_width), 
                            int(face_landmarks.landmark[10].y * image_height), 
                            int(face_landmarks.landmark[10].z * image_width))
                
                # Saves the coordinates of the landmark corresponding to the nose tip (landmark 1)
                nose_tip = (int(face_landmarks.landmark[1].x * image_width), 
                            int(face_landmarks.landmark[1].y * image_height))
                
                # Distance and relative eyebrow distances calculations
                face_top_to_nose_distance = math.dist((face_top[0], face_top[1]), nose_tip)
                relative_left_eyebrow_distance = math.dist(left_eyebrow, left_eyebrow_top) / face_top_to_nose_distance
                relative_right_eyebrow_distance = math.dist(right_eyebrow, right_eyebrow_top) / face_top_to_nose_distance
                
                cv2.putText(image, ("rel left eyebrow dist: " + str(relative_left_eyebrow_distance)), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                cv2.putText(image, ("rel reight eyebrow dist: " + str(relative_right_eyebrow_distance)), (50,100), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    
                # If the relative distance between the eyebrows and the top is < 0.26, then the eyebrows are raised.
                if relative_left_eyebrow_distance < 0.28 and relative_right_eyebrow_distance < 0.28:
                    
                    print("observando")
                    
                    # Same as with face top.
                    face_bottom = (int(face_landmarks.landmark[152].x * image_width), 
                                int(face_landmarks.landmark[152].y * image_height),
                                int(face_landmarks.landmark[152].z * image_width))

                    # Angle calculations
                    face_z_angle = np.rad2deg(math.atan2((face_bottom[1] - face_top[1]), (face_top[2]-face_bottom[2])))
                    face_x_angle = np.rad2deg(math.atan2((face_bottom[1] - face_top[1]), (face_top[0] - face_bottom[0])))
                    
                    # Calculate distance between face top and nose tip in the X axis
                    nose_tip_face_top_distance = face_top[0] - nose_tip[0]
                    
                    cv2.putText(image, ("Angulo de la cara: " + str(face_x_angle)), (50,150), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    
                    # If it's the first time eyebrow raise is detected:
                    if initial_state["observing"] == False:
                        
                        # This is to capture the values at the start of the gesture and
                        # make calculations with posterior values to detect the gestures.
                        initial_state["initial_z_face_angle"] = face_z_angle
                        initial_state["initial_x_face_angle"] = face_x_angle
                        initial_state["initial_x_nosetip"] = nose_tip_face_top_distance

                        # Changes observing state to True
                        initial_state["observing"] = True
                        
                    # Saves the coordinates of the landmark corresponding to the superior lip (landmark 13) 
                    superior_lip = (int(face_landmarks.landmark[13].x * image_width),
                                    int(face_landmarks.landmark[13].y * image_height))
                
                    # Same as with superior lip. This is to calculate the mouth opening.
                    lower_lip = (int(face_landmarks.landmark[14].x * image_width),
                                 int(face_landmarks.landmark[14].y * image_height))
                    
                    # Mouth opening calculations
                    mouth_opening = (lower_lip[1] - superior_lip[1])
                    # Calculates difference in the initial Z face angle and the actual angle
                    face_z_angle_difference = initial_state["initial_z_face_angle"] - face_z_angle
                    # Same as with above
                    face_x_angle_difference = initial_state["initial_x_face_angle"] - face_x_angle
                    # Calculate difference between face top and nose tip in the X axis
                    face_nosetip_x_difference = initial_state["initial_x_nosetip"] - nose_tip_face_top_distance
                    
                    cv2.putText(image, ("Ladeo de la cara: " + str(face_nosetip_x_difference)), (50,200), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    
                    # Gesture detections
                    if face_z_angle_difference > 10:
                        control.scrollDown()
                        
                    elif face_z_angle_difference < -10:
                        control.scrollUp()
                        
                    elif mouth_opening > 10:
                        control.zoomIn()
                        
                    elif face_x_angle_difference > 10:
                        
                        if initial_state["window_traveling"] == False:
                            
                            control.windowMenu()
                            initial_state["window_traveling"] = True
                            
                        else:
                            
                            control.nextWindow()
                            
                    elif face_nosetip_x_difference > 20:
                        
                        control.scrollLeft()
                    
                    elif face_nosetip_x_difference < -20:
                        
                        control.scrollRight()
                        
                    ignore_frame = True
                        
                else:
                    initial_state["observing"] = False
                    initial_state["initial_x_face_angle"] = 0
                    initial_state["initial_z_face_angle"] = 0
                    if initial_state["window_traveling"] == True:
                        
                        initial_state["window_traveling"] = False
                        control.releaseMenu()
                        print("Release menu")

                        
        cv2.imshow("Frame", image)       
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
    
cap.release()
cv2.destroyAllWindows()
print("Terminando programa.")