import cv2 as cv
import mediapipe as mp
import pyautogui

cap  = cv.VideoCapture(0)
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
model = mp_hands.Hands(static_image_mode=True,
               max_num_hands=1,
               model_complexity=1,
               min_detection_confidence=0.3,
               min_tracking_confidence=0.3)
screenWidth, screenHeight = pyautogui.size()
i_x = 0;i_y = 0;pre_x = 0;pre_y = 0
while True:
    success,img = cap.read()
    img = cv.flip(img,1)
    imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)

    result = model.process(imgRGB)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            landmarks = hand.landmark
            for idx,pos in enumerate(landmarks):
                if idx == 12:
                    t_x = (pos.x)*img.shape[1]
                    t_y = pos.y*img.shape[0]
                    cv.circle(img,(int(t_x),int(t_y)),10,(255,0,255),3)
                    print(((t_x - i_x)**2+(t_y - i_y)**2)**0.5)
                    if ((t_x - i_x)**2+(t_y - i_y)**2)**0.5 < 30:
                        pyautogui.click()
                if idx == 8:
                    i_x = (pos.x)*img.shape[1]
                    i_y = pos.y*img.shape[0]
                    index_x = int((screenWidth/(img.shape[1]-100))*i_x)
                    index_y = int((screenHeight/(img.shape[0]-100))*i_y)
                    # if pre_x - index_x + pre_y - index_y > 3:
                    pyautogui.moveTo(index_x,index_y)
                    pre_x = index_x 
                    pre_y = index_y
                    
                    cv.circle(img,(int(i_x),int(i_y)),10,(255,0,255),3)
                
    cv.imshow("output",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break;