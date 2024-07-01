from PIL import ImageGrab
import os
import time
import win32api, win32con
from PIL import ImageOps


import multiprocessing
import os
import keyboard
import signal
import settings

#функция завершения программы
def hook(pid):
    while True:
        if keyboard.is_pressed(settings.key_exit):
            os.kill(pid,signal.SIGTERM)
            os._exit(1)


x_pad = 0
y_pad = 0
kol_items = 0
# по 13пред.,чистим инвентарь (вмещается 15, 2 на магию защиты и ухудш.)

class Cord:
    rinok = (480,210)
    seif = (480,175)
    magaz = (480,265)
    vrata = (480,565)
    gorod = (525,710)

    ghost = (524,394)
    dragon = (572,394)

    sunduk = (413,505)
    sunduk_right = (457,311) #встаем справа сундука

    menuButton_left = (280,995)
    menuButton_left_smotr = (280,910)
    menuButton_confirmOrAtt = (280,820)

    menuButton_right = (685,995)
    menuButton_right_end = (685,910)
    menuButton_magic = (685,650)
    menuButton_centrOrEnd = (685,820)

    lvl_plus = (918,536)    #координаты плюса
    sinij_pix = (52,980)    #синий пиксель для гнома

    checkEnemy_right = (425,620) 
    checkEnemy_up = (380,575)
    checkMyself = (374,620)


    col_announcement = (225,197,152)    #цвет объявления
    col_checkEnemy_right = (48,48,48)   #цвет дракона справа
    col_checkEnemy_right_priz = (46,46,46)
    col_checkEnemy_up = (60,60,60)      #цвет дракона сверху
    col_checkEnemy_up_priz = (31,31,31)
    col_checkMyself = (221,122,0)       #цвет стрелки на своем юните

    col_sunduk_open = (60,0,67)
    col_sunduk_close = (168, 36, 0)

    col_ghost = (31,31,31)

    col_meshok_1 = (116, 108, 126)
    col_meshok_2 = (84, 78, 95)

    col_sunduk_svoboden_sprava = (54,54,54)
    col_sinij_pix = (32, 73, 137)


all_items = [ #каждые 61 пиксель
    (30,202),
    (91,202), 
    (152,202), 
    (213,202), 
    (274,202), 
    (335,202), 
    (396,202), 
    (457,202), 
    (518,202), 
    (579,202), 
    (640,202), 
    (701,202), 
    (762,202), 
    (823,202), 
    (884,202)
]

col_item = [
    (76,39,125), #ork
    (106, 199, 38), #elf
    (111, 157, 178), #gnom
    (255,243,62), #chel
    (88,5,6), #trup
    
]    

all_spells = [
    (60,205),
    (60,260),
    (60,315),
    (60,370),
    (60,425),
    (60,480),
    (60,535),
    (60,590),
]

bufSelf = (239, 155, 35)
debufEnemy = (131, 162, 176)

def screenGrab():
    box = (x_pad,y_pad,x_pad+960,y_pad+1040)
    im = ImageGrab.grab(box)
    ##im.save(os.getcwd()+'\scr' + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im 

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

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)

def centrov():
    mousePos(Cord.menuButton_right)
    leftClick()
    time.sleep(.2)
    mousePos(Cord.menuButton_centrOrEnd)
    leftClick()
    time.sleep(.2)
#!centrov

def sortItems():
    #рынок-хранилище-магазин-выйти из города
    #рынок
    mousePos(Cord.rinok)
    leftClick()
    time.sleep(.2)
    #хранилище
    mousePos(Cord.seif)
    leftClick()
    time.sleep(.2)
    s = screenGrab()
    kol_sr = 0
    for i in all_items:
        if (s.getpixel((i[0]+15,i[1]-10)) == Cord.col_meshok_1) and (s.getpixel((i[0]+25,i[1]-10)) == Cord.col_meshok_2):
            break 
        elif checkItemSeif(i,s):
            kol_sr=1
    if kol_sr == 1:
        mousePos(Cord.menuButton_right)
        leftClick()
        time.sleep(.2)
        mousePos(Cord.menuButton_centrOrEnd)
        leftClick()
        time.sleep(.2)
        print('Положил в сейф')
    else:
        mousePos(Cord.menuButton_right)
        leftClick()
        time.sleep(.2)
        mousePos(Cord.menuButton_right_end)
        leftClick()
        time.sleep(.2)
        print("Нечего класть")
    #магазин вещей
    mousePos(Cord.magaz)
    leftClick()
    time.sleep(.2)
    s = screenGrab()
    for i in all_items:
        if (s.getpixel((i[0]+15,i[1]-10)) == Cord.col_meshok_1) and (s.getpixel((i[0]+25,i[1]-10)) == Cord.col_meshok_2):
            break
        checkItemMagaz(i,s)
            
    mousePos(Cord.menuButton_right)
    leftClick()
    time.sleep(.2)
    mousePos(Cord.menuButton_centrOrEnd)
    leftClick()
    time.sleep(.2)
    # выход из рынка
    mousePos(Cord.menuButton_right)
    leftClick()
    time.sleep(.4)
    # выход из города
    mousePos(Cord.vrata)
    leftClick()
    time.sleep(.4)
    centrov()
    global kol_items
    kol_items = 0
#!sortItems

#для сейфа
def checkItemSeif(cords, image_s):
    if image_s.getpixel(cords) not in col_item:
        mousePos(cords)
        leftClick()
        time.sleep(.2)
        mousePos(Cord.menuButton_left)
        leftClick()
        time.sleep(.2)
        mousePos(Cord.lvl_plus)
        leftClick()
        time.sleep(.2)
        return True
    return False
        
#для магазина
def checkItemMagaz(cords,image_s):
    #если вещь имеет расу И нетрехзначное кол-во:
    if (image_s.getpixel(cords) in col_item) and (image_s.getpixel((cords[0]+35,cords[1]-3)) != (0,0,0)):
        mousePos(cords)
        leftClick()
        time.sleep(.2)
        mousePos(Cord.menuButton_left)
        leftClick()
        time.sleep(.2)
        mousePos(Cord.lvl_plus)
        leftClick()
        time.sleep(.2)
        leftClick()
        time.sleep(.2)
        leftClick()
        time.sleep(.2)

def startFarm():
    #стоим слева от входа в город Череп Аха
    s = screenGrab()
    while (s.getpixel(Cord.sunduk_right) != Cord.col_sunduk_svoboden_sprava):
        time.sleep(3)
        s = screenGrab()
    mousePos(Cord.sunduk_right)
    leftClick()
    time.sleep(1)
    centrov()
    global kol_items
    while kol_items<13: 
        sunduk()
    mousePos(Cord.gorod)
    leftClick()
    time.sleep(.2)
    mousePos(Cord.menuButton_left_smotr)
    leftClick()
    time.sleep(2)
    sortItems()
    


        
def sunduk():
    s = screenGrab()
    while s.getpixel(Cord.sunduk) != Cord.col_sunduk_close:
        time.sleep(3)
        s = screenGrab()
    mousePos(Cord.sunduk)
    leftClick()
    time.sleep(.2)
    mousePos(Cord.menuButton_left_smotr)
    leftClick()
    time.sleep(.4)
    s=screenGrab()
    time.sleep(.5)
    #если НЕ стражи
    if s.getpixel(Cord.sinij_pix) == Cord.col_sinij_pix:
        mousePos(Cord.menuButton_left)
        leftClick()
        time.sleep(.2)
        leftClick()
        time.sleep(.2)
        mousePos(Cord.menuButton_right)
        leftClick()
        time.sleep(.1)
        mousePos(Cord.menuButton_right_end)
        leftClick()
        time.sleep(.2)
        centrov()
    #если стражи
    else: 
        mousePos(Cord.menuButton_left)
        leftClick() #вы наткнулись на стражу
        time.sleep(.2)
        leftClick() #вы атакованы
        time.sleep(.2)
        fight()
        


def castMagic(enemy): #0-priz,1-dragon
    mousePos(Cord.menuButton_right)
    leftClick()
    time.sleep(.4)
    mousePos(Cord.menuButton_magic)
    leftClick()
    time.sleep(.4)
    s = screenGrab()
    time.sleep(.4) 
    if enemy == 0:
        for i in all_spells:
            if (s.getpixel(i) == (0,0,0)) and (s.getpixel((i[0],i[1]-10)) == bufSelf):
                if all_spells.index(i)!=0:
                    mousePos(i)
                    leftClick()
                    time.sleep(.2)
                mousePos(Cord.menuButton_left)
                leftClick()
                time.sleep(.2)
                mousePos(Cord.menuButton_left)
                leftClick()
                time.sleep(.3)
                mousePos(Cord.menuButton_confirmOrAtt)
                leftClick()
                time.sleep(.3)
                mousePos(Cord.menuButton_right)
                leftClick()
                time.sleep(.4)
                mousePos(Cord.menuButton_centrOrEnd)
                leftClick()
                time.sleep(.2)
                break
    else: 
        for i in all_spells:
            if (s.getpixel(i) == (0,0,0)) and (s.getpixel((i[0],i[1]-10)) == debufEnemy):
                mousePos(i)
                leftClick()
                time.sleep(.2)
                mousePos(Cord.menuButton_left)
                leftClick()
                time.sleep(.2)
                mousePos(Cord.dragon)
                leftClick()
                time.sleep(.3)
                mousePos(Cord.menuButton_confirmOrAtt)
                leftClick()
                time.sleep(.3)
                mousePos(Cord.menuButton_right)
                leftClick()
                time.sleep(.4)
                mousePos(Cord.menuButton_centrOrEnd)
                leftClick()
                time.sleep(.3)
                break

 

def fight():
    s = screenGrab()
    time.sleep(.2)
    #призраки
    if s.getpixel(Cord.ghost) == (Cord.col_ghost):
        castMagic(0)
    #драконы
    else:
        castMagic(1)
    time.sleep(.2)
    s = screenGrab()
    time.sleep(.1)
    while s.getpixel(Cord.checkMyself) != Cord.col_announcement:
        s = screenGrab()
        time.sleep(.3)
        while s.getpixel(Cord.checkMyself) != Cord.col_checkMyself:
            time.sleep(.53)
            s = screenGrab()
            time.sleep(.2)
            if s.getpixel(Cord.checkMyself) == Cord.col_announcement:
                break
        if (s.getpixel(Cord.checkEnemy_right) == Cord.col_checkEnemy_right) or (s.getpixel(Cord.checkEnemy_right) == Cord.col_checkEnemy_right_priz):
            mousePos(Cord.checkEnemy_right)
            leftClick()
            time.sleep(2)
        elif (s.getpixel(Cord.checkEnemy_up) == Cord.col_checkEnemy_up) or (s.getpixel(Cord.checkEnemy_up) == Cord.col_checkEnemy_up_priz):
            mousePos(Cord.checkEnemy_up)
            leftClick()
            time.sleep(2)
        else:
            time.sleep(2)
            s=screenGrab()
            time.sleep(.3)
        s = screenGrab()
        time.sleep(.3)
        
    mousePos(Cord.menuButton_left)
    leftClick()
    time.sleep(.3)
    centrov()
    global kol_items 
    kol_items = kol_items + 1
   
        



if __name__ == '__main__':
    pid = os.getpid()
    multiprocessing.Process(target=hook,args=[pid]).start()
    
    while True:
        startFarm()
        #nim()



#sortItems()

# a=((all_items[3][0]+35,all_items[3][1]-3))
# s=screenGrab()
# print(s.getpixel(a))
# mousePos(a)