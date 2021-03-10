import pyautogui
import numpy as np
import  cv2
import base64
import threading
import time

delay = .5

class VideoStream(threading.Thread):

    def __init__(self,mode= 'test'):
        threading.Thread.__init__(self)
        self.mode = mode
        self.frame = self.capture2()
        self.frame_used = False
        self.count = 0

    def run(self):
        while self.count <999:
            if self.frame_used == True:
                self.frame = self.capture2()
            time.sleep(delay)

    def get_frame(self):
        self.frame_used = True
        return self.frame

    def capture(self):
        capture = pyautogui.screenshot()
        cv2cap = cv2.cvtColor(np.array(capture), cv2.COLOR_RGB2BGR)
        shape = cv2cap.shape
        #print(cv2cap)
        resized = cv2.resize(cv2cap, (int(shape[0]/40),int(shape[1]/40)),interpolation = cv2.INTER_AREA)
        bytes = resized.tobytes()
        print(resized.shape)
        #print(len(bytes))
        a2 = np.frombuffer(bytes, dtype=resized.dtype)
        a2 = a2.reshape(resized.shape)
        #upscaled = cv2.resize(a2, (int(shape[1]/1.2), int(shape[0]/1.2)),interpolation = cv2.INTER_CUBIC)
        #cv2.imshow("image", upscaled)
        #cv2.waitKey(0)
        #print(a2)
        return bytes

    def capture2(self):
        # capture = pyautogui.screenshot()
        # cv2cap = cv2.cvtColor(np.array(capture), cv2.COLOR_RGB2BGR)
        cv2cap = cv2.imread('/home/pi/Downloads/RcMain-main/GroundStation/test.png')
        frame = cv2.resize(cv2cap, (150, 150))  # resize the frame
        buffer = cv2.imencode('.png', frame)[1]
        jpg_as_text = base64.b64encode(buffer)
        print(jpg_as_text)
        print(len(jpg_as_text))
        # cv2.startWindowThread()
        # img = base64.b64decode(jpg_as_text.strip())
        # npimg = np.fromstring(img,dtype=np.uint8)
        # source = cv2.imdecode(npimg,1)
        # cv2.imshow('stream',source)
        # cv2.waitKey()

        # print(img)

        return jpg_as_text


V = VideoStream().capture2()