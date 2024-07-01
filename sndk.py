import pyautogui as  pg
import time
import sys
import math
import settings
import multiprocessing
import os
import keyboard
import signal

#функция завершения программы
def hook(pid):
    while True:
        if keyboard.is_pressed(settings.key_exit):
            os.kill(pid,signal.SIGTERM)
            os._exit(1)

def has(target):
    try:
        pg.center(pg.locateOnScreen(target,confidence=0.8))
        return 1
    except:
        return 0


#координаты расы вещей
all_items = [
    (113,189),
    (174,189),
    (235,189),
    (296,189),
    (357,189),
    (418,189),
    (479,189),
    (540,189),
    (601,189),
    (662,189),
    (723,189),
    (784,189),
    (845,189),
    (906,189),
    (967,189),
    (1028,189),
    (1089,189),
    (1150,189),
    (1211,189),
    (1272,189),
    (1333,189)
]
col_items = [
    (62, 176, 29), #эльф
    (197, 166, 210), #орк
    (252, 175, 23), #человек
    (88, 5, 6), #труп
    (26, 104, 129) #гном
]

def findAndClick(target,wait=0.4):
    try:
        pos = pg.center(pg.locateOnScreen(target,confidence=0.8))
        pg.moveTo(pos[0],pos[1])
        time.sleep(.1)
        pg.click()
        time.sleep(wait)
    except:
        print('cannot find ' + str(target))

choice = 'templates/choice.png'
plus = 'templates/plus.png'
menu = 'templates/menu.png'
accept = 'templates/accept.png'
exit_menu = 'templates/exit_menu.png'
deal = 'templates/deal.png'
market = 'templates/market.png'
doors = 'templates/doors.png'
market_items = 'templates/market_items.png'
ceif_i = 'templates/ceif.png'
chest = 'templates/chest.png'
already_open = 'templates/already_open.png'
defender = 'templates/defender.png'
money = 'templates/money.png'
health = 'templates/health.png'
pointer = 'templates/pointer.png'
ghosts = 'templates/ghosts.png'
annonce = 'templates/annonce.png'
non_target ='templates/non_target.png'
target = 'templates/target.png'
magic = 'templates/magic.png'
boost = 'templates/boost.png'
wait = 'templates/wait.png'
city_enter = 'templates/city_enter.png'
def ceif():
    im = pg.screenshot()
    count_n = 0
    for i in all_items:
        if im.getpixel((i[0],i[1]-26))==(217,184,84):
            if im.getpixel(i) not in col_items:
                try:
                    pg.moveTo(i)
                    time.sleep(.1)
                    pg.click()
                    time.sleep(.5)
                    findAndClick(choice)
                    findAndClick(plus)
                    count_n = count_n+1
                    print('+neutral')
                except Exception as e:
                    print(e)
                    exit()
        else:
            break
    findAndClick(menu)
    if count_n!=0:
        findAndClick(accept)
        while has(wait):
            time.sleep(1)
    else:
        findAndClick(exit_menu)

def sell_items():
    im = pg.screenshot()
    count_n = 0
    for i in all_items:
        if im.getpixel((i[0],i[1]-26))==(217,184,84):
            if im.getpixel(i) in col_items:
                try:
                    pg.moveTo(i)
                    time.sleep(.1)
                    pg.click()
                    time.sleep(.2)
                    #findAndClick(choice)
                    pg.press('enter')
                    # findAndClick(plus)
                    pg.press('right')
                    count_n = count_n+1
                except Exception as e:
                    print(e)
                    exit()
        else:
            break
    findAndClick(menu)
    if count_n!=0:
        findAndClick(deal)
        while has(wait):
            time.sleep(1)
    else:
        findAndClick(exit_menu)
   
def city():
    findAndClick(market)
    findAndClick(ceif_i)
    ceif()
    time.sleep(2)
    findAndClick(market_items)
    sell_items()
    time.sleep(2)
    findAndClick(exit_menu)
    findAndClick(doors)

def fight():
    k=0
    while has(annonce)==0:
        while has(pointer)==0 and k==0:
            time.sleep(.2)
        k=1
        if has(ghosts):#призраки
            for i in range(5):
                while has(pointer)==0:
                    time.sleep(.2)
                findAndClick(ghosts)
                while has(non_target):
                    pg.press('right')
                    pg.press('enter')
        else:#драконы
            findAndClick(menu)
            pg.moveTo(1160,640)
            pg.click()
            time.sleep(.2)
            pg.press('enter',2,.2)
            pg.press('up')
            pg.press('enter')
            while has(pointer)==0:
                time.sleep(.2)
            pg.press('up',5)
            pg.press('right',4)
            pg.press('enter')
        while has(annonce)==0:
            time.sleep(1)
    pg.press('enter')    

            

        

def sunduk(k):
    while k<19:
        pg.press('left')
        for i in range(2):
            pg.press('enter')
            time.sleep(.4)
        while has(defender)==0 and has(choice)==0 and has(money)==0:
            time.sleep(.4)
        if has(defender):
            pg.press('enter')
            while has(health)==0:
                pg.press('enter')
                time.sleep(.4)
            fight()
            k=k+1
        else:
            time.sleep(.7)
            if has(choice):
                findAndClick(menu)
                pg.press('enter')
                pg.press('right')
            else: #elif has(money)
                pg.press('enter')
                findAndClick(menu)
                pg.press('enter')
            while has(already_open):
                time.sleep(1)





def start_farm():
    all_k = 0
    findAndClick(chest,1.1)
    sunduk(all_k)
    findAndClick(city_enter)
    pg.press('enter')
    while has(market)==0:
        time.sleep(.4)
    city()
    



if __name__ == '__main__':
    pid = os.getpid()
    multiprocessing.Process(target=hook,args=[pid]).start()
    
    while True:
        #ceif()
        start_farm()



