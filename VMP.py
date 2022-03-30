import cv2
import numpy as np
import HandTrackingModule as htm
import autopy
import time
import pyautogui
import printapp as pa

#from autopy.mouse import LEFT_BUTTON, RIGHT_BUTTON

#veriables
widthC, heightC =648,488
pTime = 0
frameR = 150
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoot = 0.1
clickTime = 0
sstime = 0
downValue = 25
dragLeft = False
SSnumber = 0

#init
cap= cv2.VideoCapture(0)
cap.set(2,widthC)
cap.set(4,heightC)
detector = htm.handDetector(maxHands=1)
widthSc, heightSc = autopy.screen.size()
pa.window.withdraw()

while True:
    #find hand points
    success, VC = cap.read()
    VC = detector.findHands(VC)
    lmList, bbox = detector.findPosition(VC)
    
    if len(lmList) != 0:
        # get the tip of the index and middle finger
        xindex, yindex = lmList[8][1:]
        xmiddle, ymiddle = lmList[12][1:]

       # Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        
        #values which need to check alot index-middle finger distance and click distance
        lengthim = detector.findDistanceL(8, 12, VC)
        downValue = detector.findDistanceL(5, 6, VC) + 1
        #print(downValue1)

        # Only Index Finger : Moving & drag mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and lengthim > 40:

            # Convert Coordinates
            x1 = np.interp(xindex, (frameR, widthC - frameR), (0, widthSc))
            y1 = np.interp(yindex, (frameR, heightC - frameR), (0, heightSc))

            # Smoothen Values
            clocX = plocX + (x1 - plocX) * smoot
            clocY = plocY + (y1 - plocY) * smoot

            # Mouse move
            autopy.mouse.move(widthSc - clocX,clocY)

            # Mouse drag 
            if(pa.window.state() == "withdrawn"): 
                #select
                if fingers[0] == 1:
                    if dragLeft == False:
                        pyautogui.mouseDown(button='left')
                        dragLeft = True
                else:
                    if dragLeft == True:
                        pyautogui.mouseUp(button='left')
                        dragLeft = False
            else:
                #color
                if fingers[0] == 1:
                    pa.addLine(widthSc - plocX, plocY,widthSc - clocX, clocY )

            plocX, plocY = clocX, clocY 

        # Both Index and middle fingers are up : Clicking Mode (left & right)
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            
            # Click mouse if index-middle finger distance short
            if lengthim < 40 and clickTime == 0 and lmList[6][2] - yindex < downValue and lmList[10][2] - ymiddle < downValue:

                if fingers[0] == 1:
                    #right click
                    pyautogui.click(button='right')
                    clickTime= -12
                    #print('r')
                else:
                    #left click
                    pyautogui.click(button='left')
                    clickTime= -3
                    #print('l')

        #Thump finger : scolling mode
        elif fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 1:

            if yindex - lmList[4][2] > downValue and lmList[4][1] - xindex > downValue and clickTime == 0:
                # up scoll
                #print('up-scoll')
                pyautogui.scroll(300)
                clickTime= -15

            elif lmList[4][1] - xindex > downValue and lmList[4][2] - yindex > downValue and clickTime == 0:
                # down scoll
                #print('down-scoll')
                pyautogui.scroll(-300)
                clickTime= -15

        # All finger up : Screenshot mode
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[0] == 1 and sstime == 0:
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save("SS" + str(SSnumber) + ".jpg")
            SSnumber += 1
            sstime = -50

        # 4 finger up : mouse mode & drawing mode switch
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[0] == 0 :

            # getting distance for adjustent fingers
            lengthmr = detector.findDistanceL(12, 16, VC)
            lengthrs = detector.findDistanceL(16, 20, VC)

            # Click mouse if adjustent fingers distance short
            if lengthim < 40 and lengthmr < 40 and lengthrs < 40 and sstime == 0 and lmList[6][2] - yindex < downValue and lmList[10][2] - ymiddle < downValue and lmList[14][2] - lmList[16][2] < downValue and lmList[19][2] - lmList[20][2] < downValue:
                
                if(pa.window.state() == "withdrawn"):
                    # drawing mode
                    pa.window.deiconify()
                    pa.window.state('zoomed')
                else:
                    # mouse mode
                    pa.window.withdraw()

                sstime= -50
                 
    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #print(fps)

    # timers
    clickTime+= (1 if clickTime < 0 else 0)
    sstime+= (1 if sstime < 0 else 0)

    # tkinter window mainloop
    pa.window.update()
    pa.window.update_idletasks()

    # Display
    #cv2.imshow("VC",VC)
    cv2.waitKey(1)
