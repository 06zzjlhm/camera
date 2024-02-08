# 使用的多线程，但是视频流的速度太卡
# https://segmentfault.com/q/1010000042841961?sort=votes
import cv2
from collections import deque
from time import sleep, time
import threading

class camCapture:#声明了一个类
    def __init__(self, camID, buffer_size):
        self.Frame = deque(maxlen=buffer_size)
        self.status = False
        self.isstop = False
        self.capture = cv2.VideoCapture(camID,cv2.CAP_DSHOW)

    def start(self):
        print('camera started!')
        t1 = threading.Thread(target=self.queryframe, daemon=True, args=())
        t1.start()

    def stop(self):
        self.isstop = True
        print('camera stopped!')

    def getframe(self):
        print('current buffers : ', len(self.Frame))
        # return self.Frame.popleft()
        return self.Frame.pop()#pop和popleft都可以运行
    
    def queryframe(self):
        while (not self.isstop):
            start = time()
            self.status, tmp = self.capture.read()
            print('read frame processed : ', (time() - start) *1000, 'ms')
            self.Frame.append(tmp)

        self.capture.release()

cam = camCapture(camID=0, buffer_size=20) #定义了一个实例，buffersize越大好像越卡，应该要比FPS大，小了报错
# W, H = 1280, 720
W, H = 300, 200 #改变显示窗口的大小
cam.capture.set(cv2.CAP_PROP_FRAME_WIDTH, W)
cam.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
cam.capture.set(cv2.CAP_PROP_FPS,1)#帧率越大越卡，1、2差不多
cam.capture.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

# start the reading frame thread
cam.start()

# filling frames
sleep(1)#给初始化一点时间

while True:
  frame = cam.getframe() # numpy array shape (720, 1280, 3)

  cv2.imshow('video',frame)
  sleep( 40 / 1000) # mimic the processing time

  if cv2.waitKey(1) == 27:   #esc退出
        cv2.destroyAllWindows()
        cam.stop()
        break

# cmd 把电脑硬件的开启速度提高
#   https://blog.csdn.net/u013066730/article/details/129545155