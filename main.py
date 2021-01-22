#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pygame, sys
import pickle
import random
import time
import os

##copyright()

# In[2]:

def main(ss, isDarkMode=False, language="Chinese"):
    """
ss:你可以试试看ss的效果你就知道了 建议开启
isDarkMode:如果开启黑暗模式的话就是黑底白字 否则是白底黑字
language:只有两种可能:"Chinese"或者"English" 调节语言
    """
    assert language == "Chinese" or language == "English"
    pygame.init()
    ##pygame.freetype.init()
    font = pygame.font.Font(r"C:\Windows\fonts\msyh.ttc",90)
    if isDarkMode:
        TextColor = (255,255,255)
    else:
        TextColor = (0,0,0)
    pos = 0
    line_height = font.get_linesize()
    if isDarkMode:
        bg = (0,0,0)
    else:
        bg = (255,255,255)
    res = width, height = 1920, 1080

    if language == "Chinese":
        GameOverMessage = "游戏结束"
        RandomMessage = "勿轻举妄动"
        PressMessage = "请按下Enter键"
        FPSMessage = "帧速率"
        ResponseMessage = ["反应时间", "毫秒"]
    elif language == "English":
        GameOverMessage = "Game over."
        RandomMessage = "Don't do anything."
        PressMessage = "Press Enter."
        FPSMessage = "FPS"
        ResponseMessage = ["Response time","ms."]
    else:
        print("非法字符:", language)
        print("默认设置为\"Chinese\"")
        GameOverMessage = "游戏结束"
        RandomMessage = "勿轻举妄动"
        PressMessage = "请按下Enter键"
        FPSMessage = "帧速率"
        ResponseMessage = ["反应时间", "毫秒"]
        
    # In[3]:

    dfont = pygame.font.Font(r"C:\Windows\fonts\msyh.ttc",20)

    screen = pygame.display.set_mode(res, pygame.FULLSCREEN | pygame.HWSURFACE)
    pygame.display.set_caption("beta test")


    twait = random.randint(1000,5000)
    tbegin = time.time()

    if os.path.exists(r".\time.log"):
        lfile = open(r".\time.log", "rb+")
    else:
        _ = open(r".\time.log", "w")
        _.close()
        del _
        lfile = open(r".\time.log", "rb+")

    try:
        write_data = pickle.load(lfile)
        lfile.seek(0)
    except Exception as e:
        print(repr(e))
        write_data = []


    clock = pygame.time.Clock()
    draw = False
    drawed = False
    draw_result = False
    drawed_result = False
    draw_another = 0
    drawed_another = False
    screen.fill(bg)
    while True:
        time_now = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pickle.dump(write_data, lfile)
                lfile.close()
                pygame.quit()
                return 0
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pickle.dump(write_data, lfile)
                    lfile.close()
                    pygame.quit()
                    return 0
                elif event.key == pygame.K_c:
                    bg = (255-bg[0], 255-bg[1], 255-bg[2])
                    TextColor = (255-TextColor[0], 255-TextColor[1], 255-TextColor[2])
                    screen.fill(bg)
                    drawed = False
                    drawed_result = False
                    drawed_another = False
                elif event.key == pygame.K_l:
                    if language == "Chinese":
                        GameOverMessage = "Game over."
                        RandomMessage = "Don't do anything."
                        PressMessage = "Press Enter."
                        FPSMessage = "FPS"
                        ResponseMessage = ["Response time","ms."]
                        language = "English"
                    elif language == "English":
                        GameOverMessage = "游戏结束"
                        RandomMessage = "勿轻举妄动"
                        PressMessage = "请按下Enter键"
                        FPSMessage = "帧速率"
                        ResponseMessage = ["反应时间", "毫秒"]
                        language = "Chinese"
                    screen.fill(bg)
                    drawed = False
                    drawed_result = False
                    drawed_another = False
                        
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not draw:
                        print(GameOverMessage)
                        pickle.dump(write_data, lfile)
                        lfile.close()
                        pygame.quit()
                        return 0
                    if not draw_result:
                        
                        result = time_now - start
                        #print(write_data)
                        print("%s:%.2f %s"%(ResponseMessage[0], result*1000, ResponseMessage[1]))
                        write_data.append((time_now, result))
                        #print(write_data)
                        draw_result = True
                        timeleft = time_now
        
            pos += line_height

        if time_now - tbegin >= (twait/1000) and not draw:
            draw = True
            start = time_now
        
        screen.fill(bg,(0,0,150,50))

        if not draw and not draw_result and not drawed_another:
            if random.randint(1,100) == 13 or draw_another:
                draw_another = time_now
                stext= font.render(RandomMessage, ss, TextColor)
                rtext = stext.get_rect()
                screen.blit(stext, (width/2 - rtext.width/2, height/2 - rtext.height/2))
                drawed_another = True
        if time_now - draw_another >= 1 and draw_another and not draw:
            screen.fill(bg)
            
            draw_another = 0
            drawed_another = False

        
        if draw and not draw_result and not drawed:
            screen.fill(bg)
##            print("enter")
            stext= font.render(PressMessage, ss, TextColor)
            rtext = stext.get_rect()
            screen.blit(stext, (width/2 - rtext.width/2, height/2 - rtext.height/2))
            drawed = True
        elif drawed and not draw and draw_result:
            screen.fill(bg)
            drawed = False

        if draw_result and not drawed_result:
            screen.fill(bg)
            stext= font.render("%s:%.2f%s"%(ResponseMessage[0], result*1000, ResponseMessage[1]), ss, TextColor)
            rtext = stext.get_rect()
            screen.blit(stext, (width/2 - rtext.width/2, height/2 - rtext.height/2))
            drawed_result = True
            
        if (draw_result) and (time_now - timeleft >= 2):
            screen.fill(bg)
            drawed = False
            draw = False
            drawed_result = False
            draw_result = False
            twait = random.randint(1000,5000)
            tbegin = time_now



        dstext = dfont.render(FPSMessage+":%.2f"%clock.get_fps(), ss, (0,255,0))
        screen.blit(dstext, (0,0))

        pygame.display.flip()
        clock.tick(75)
if __name__ == "__main__":
    main(ss=True,
         isDarkMode=True,
         language="Chinese")
