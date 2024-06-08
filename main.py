import keyboard
from PIL import ImageGrab
import os
import time
import win32api, win32con
from PIL import ImageOps
import signal
import multiprocessing
import settings
import cv2 as cv
import numpy as np


x_pad = 0
y_pad = 0
#===============СИСТЕМНЫЕ ФУНКЦИИ===============
#получение скриншота
def screenGrab():
    box = (x_pad,y_pad,x_pad+1920,y_pad+1080) #размеры окна
    im = ImageGrab.grab(box)
    #im.save(os.getcwd()+'/results' + '/full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im 

#функции клика
def leftClick():
   win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
   time.sleep(.1)
   win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print("left Down")
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print("left release")

#функция перемещения мыши
def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))

#получения координатов мыши
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)

#функция завершения программы
def hook(pid):
    while True:
        if keyboard.is_pressed(settings.key_exit):
            os.kill(pid,signal.SIGTERM)
            os._exit(1)

#===============!СИСТЕМНЫЕ ФУНКЦИИ===============



temp_troll = cv.imread('templates/troll.png',cv.IMREAD_GRAYSCALE)
w,h = temp_troll.shape[::-1]

ImageGrab.grab(bbox=(0,0,1920,1080)).save(os.getcwd()+'/results' + '/full_snap_' + '.png', 'PNG')
base_screen = ()
img_rgb = cv.imread('results/full_snap_.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

res = cv.matchTemplate(img_gray, temp_troll, cv.TM_CCOEFF_NORMED)
loc=np.where(res>=0.7)

for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)


cv.imwrite('res.png',img_rgb)













#основная функция            
def main():
    while True:
        time.sleep(500)

        
if __name__ == '__main__':
    # pid = os.getpid()
    # multiprocessing.Process(target=hook,args=[pid]).start()
    
    # main()
    pass

    #screenGrab()