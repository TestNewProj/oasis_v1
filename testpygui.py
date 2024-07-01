import pyautogui as  pg
import time
import sys
import math
import settings
import multiprocessing
import os
import keyboard
import signal

#4 loc OI
oi_1_1 = 'templates/oi_1_1.png'
oi_1_2 = 'templates/oi_1_2.png'
oi_1_2_0 = 'templates/oi_1_2_0.png'
oi_1_2_1 = 'templates/oi_1_2_1.png'
oi_1_3 = 'templates/oi_1_3.png'
oi_1_tp = 'templates/oi_1_tp.png'
oi_2_tp = 'templates/oi_2_tp.png'
oi_3_1 = 'templates/oi_3_1.png'
oi_3_2 = 'templates/oi_3_2.png'
oi_3_3 = 'templates/oi_3_3.png'
oi_3_4 = 'templates/oi_3_4.png'
oi_3_tp = 'templates/oi_3_tp.png'
oi_4_1 = 'templates/oi_4_1.png'
oi_4_2 = 'templates/oi_4_2.png'
oi_4_3 = 'templates/oi_4_3.png'
oi_4_4 = 'templates/oi_4_4.png'
oi_4_4_1 = 'templates/oi_4_4_1.png'
oi_4_5 = 'templates/oi_4_5.png'
oi_4_tp = 'templates/oi_4_tp.png'
oi_final = 'templates/oi_final.png'

troll_map = 'templates/troll.png'
troll_fight = 'templates/troll_fight.png'
elf_map_f = 'templates/elf_map_f.png'
elf_map_s = 'templates/elf_map_s.png'
elf_fight = 'templates/elf_fight.png'

game_close='templates/game_close.png'
game_fullscreen='templates/game_fullscreen.png'
game_play = 'templates/game_play.png'
game_open = 'templates/game_open.png'
oasis = 'templates/oasis.png'

accept = 'templates/accept.png'

new_lvl = 'templates/new_lvl.png'
xitr = 'templates/xitr.png'
lovk = 'templates/lovk.png'
must_not = 'templates/must_not.png'
no_exp = 'templates/no_exp.png'
plus = 'templates/plus.png'

menu = 'templates/menu.png'
attack = 'templates/atack.png'
health = 'templates/health.png'
close = 'templates/close.png'
pointer = 'templates/pointer.png'
time_fight = 'templates/time.png'
magic = 'templates/magic.png'
boost = 'templates/boost.png'
boost_unact = 'templates/boost_unact.png'
mag = 'templates/mag.png'
action = 'templates/action.png'
choice = 'templates/choice.png'
annonce = 'templates/annonce.png'
yes = 'templates/yes.png'
centr = 'templates/centr.png'


rg_fight = (800,360,300,290)
rg_time = (40,25,900,30)
rg_annonce = (20,150,570,470)
rg_menu = (600,950,745,100)
rg_pannel = (45,1040,870,40)
rg_attack = (570,790,388,64)

#функция завершения программы
def hook(pid):
    while True:
        if keyboard.is_pressed(settings.key_exit):
            os.kill(pid,signal.SIGTERM)
            os._exit(1)



def has(target,rg=None):
    try:
        pg.center(pg.locateOnScreen(target,confidence=0.8,region=rg,grayscale=True))
        return 1
    except:
        return 0

def findAndClick(target,wait=0.01, rg=None):
    try:
        # st_time = time.time()
        pos = pg.center(pg.locateOnScreen(target,confidence=0.8, region=rg,grayscale=True))
        pg.moveTo(pos[0],pos[1])
        pg.click()
        time.sleep(wait)
        # end_time = time.time()
        # print(end_time-st_time)
    except:
        print('cannot find ' + str(target))

def hit(enemy):
    try:

        
        m=10000
        i = 0
        pos_pointer= pg.locateCenterOnScreen(pointer, confidence=0.8,region=rg_fight,grayscale=True)
        all_enemy = list(pg.locateAllOnScreen(enemy, confidence=0.8,region=rg_fight,grayscale=True))
        closest=i
        for pos_enemy in all_enemy:
            if m > math.fabs(pos_enemy[0]-pos_pointer[0])+math.fabs(pos_enemy[1]-pos_pointer[1]):
                m = math.fabs(pos_enemy[0]-pos_pointer[0])+math.fabs(pos_enemy[1]-pos_pointer[1])
                closest=i
            i=i+1
        pg.moveTo(all_enemy[closest][0]+15,all_enemy[closest][1]+15)
        pg.click()
        time.sleep(0.3)
        
    except Exception as err:
        print(err)
        
def fight(enemy):
    k=0
    while True:
        try:
            pg.locateOnScreen(time_fight,confidence=0.8) #пока на экране есть таймер
            if (k==0 and has(pointer,rg_fight)):
                castMagic()
                k = k+1

            while has(annonce,rg_annonce)!=1:
                if (has(pointer,rg_fight)):
                    hit(enemy)
                else:
                    time.sleep(.3)
            
        except Exception as e:
            print(e)
            return False
        finally:
            
            return False

def castMagic():
    try:
        findAndClick(menu,rg=rg_menu)
        pg.moveTo(1160,640)
        pg.click()
        time.sleep(.2)
        pg.press('enter',2,.2)
        pg.press('up')
        pg.press('enter')
        while has(pointer,rg_fight)==0:
            time.sleep(.2)
    except Exception as err:
        print(err)


def lvlUp(xar):
    if has(new_lvl):
        findAndClick(xar)
        findAndClick(choice)
        for i in range(3):
            findAndClick(plus)
        time.sleep(.3)
        findAndClick(accept)
        time.sleep(.3)
        findAndClick(yes)
        time.sleep(3)
        print('NEW LEVEL')
        findAndClick(close)
        time.sleep(1)


def reOpen():
    findAndClick(game_close)
    time.sleep(.4)
    findAndClick(game_open)
    while has(game_play)!=1:
        time.sleep(1.5)
    findAndClick(game_fullscreen)
    time.sleep(.4)
    findAndClick(game_play)
    time.sleep(.4)
    while has(oasis):
        time.sleep(1)
    while has(close,rg_menu):
        findAndClick(close,rg=rg_menu)
        time.sleep(1)
    
        

def atack(enemy,proverka,rgg=None):
    
    findAndClick(enemy,rg=rgg)
    if has(attack,rg=rg_attack):
        findAndClick(attack,rg=rg_attack)
        while (has(health,rg_time)==0) and (has(must_not)==0):
                time.sleep(.2)  

        if enemy == troll_map:
                enemy = troll_fight
        else:
                enemy = elf_fight

    try: 
        pg.center(pg.locateOnScreen('templates/health.png',confidence=0.8,region=rg_time))
        while (has(pointer,rg_fight)==0):
            time.sleep(.2)
        fight(enemy)
        time.sleep(.2)
        if has(no_exp,rg_annonce):
            proverka=1
        findAndClick(close,rg=rg_menu)
        lvlUp(settings.xar)
        if proverka == 1:
            reOpen()
            
    except:
        findAndClick(close,rg=rg_menu)

nim_1 = 'templates/nim_1.png'
rg_nim = (700,160,690,640)

def nim():
    pr = 0
    findAndClick(menu,rg=rg_menu)
    findAndClick(centr)
    k=0
    while has(troll_map,rg_nim):
        atack(troll_map,pr,rg_nim)
        k=k+1
    if pr==1:
        return
    #findAndClick(nim_1,2)





def OI():
    pr = 0
    findAndClick(menu)
    findAndClick(centr)
    findAndClick(oi_1_1,1)
    while has(troll_map):
        atack(troll_map,pr)
    if pr==1:
        return
    findAndClick(oi_1_2_0,1)
    findAndClick(oi_1_2_1,1)
    findAndClick(oi_1_2,2)
    findAndClick(oi_1_3,1)
    findAndClick(oi_1_tp,1)
    while (has(oasis)):
        time.sleep(1)

    while has(troll_map):
        atack(troll_map,pr)
    if pr==1:
        return
    findAndClick(oi_2_tp,1.5)
    while (has(oasis)):
        time.sleep(2)

    while has(troll_map):
        atack(troll_map,pr)
    if pr==1:
        return
    findAndClick(oi_3_1,1)
    while has(troll_map):
        atack(troll_map,pr)
    if pr==1:
        return
    findAndClick(oi_3_2,1)
    while has(troll_map):
        atack(troll_map,pr)
    if pr==1:
        return
    findAndClick(oi_3_3,1)
    while has(troll_map):
        atack(troll_map,pr)
    if pr==1:
        return
    findAndClick(oi_3_4,1)
    findAndClick(oi_3_tp,1)
    while (has(oasis)):
        time.sleep(2)

    while has(troll_map):
        atack(troll_map,pr)
    if pr==1:
        return
    findAndClick(oi_4_1,2)
    while has(troll_map):
        atack(troll_map,pr)

    # =========
    reOpen()
    pr=1
    # =========
    if pr==1:
        return




#основная функция            
# def main():
#     while True:
#         OI()
     


if __name__ == '__main__':
    pid = os.getpid()
    multiprocessing.Process(target=hook,args=[pid]).start()
    
    while True:
        OI()
        # nim()
    
    