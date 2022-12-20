# -*- coding: utf-8 -*-
#!/usr/local/bin/python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import math
import time
import json
import sys
import pygame

st=[
        "hour","day","temp","tmx","tmn","sky","pty","wfkor",
        "wfen","pop","r12","s12","ws","wd","wdkor","wden",
        "reh","r06","s06"
]

def Split(inp,A,B):
    return inp.split(A)[1].split(B)[0]

def data_crolling(inp,A,B):
    P=Split(inp,A,B)
    re={}
    for i in range(len(st)):
        data=Split(P,"<"+st[i]+">","</"+st[i]+">")
        re[st[i]]=data
    return re

def answer(V):
    prt=[]
    pr=[]
    #print(V)
    t=float(V["temp"])
    if float(V["tmx"])!=-999.0 and float(V["tmn"])!=-999.0:
        prt.append("현재 기온은 "+str(t)+"도 이며 최고 기온은 "+V["tmx"]+"도, 최저 기온은 "+V["tmn"]+"도 입니다.")
        #print("현재 기온은 "+str(t)+"도 이며 최고 기온은 "+V["tmx"]+"도, 최저 기온은 "+V["tmn"]+"도 입니다.")
    else:
        if float(V["tmx"])!=-999.0:
            prt.append("현재 기온은 "+str(t)+"도 이며 최고 기온은 "+V["tmx"]+"도 입니다.")
            #print("현재 기온은 "+str(t)+"도 이며 최고 기온은 "+V["tmx"]+"도 입니다.")
        elif float(V["tmn"])!=-999.0:
            prt.append("현재 기온은 "+str(t)+"도 이며 최저 기온은 "+V["tmn"]+"도 입니다.")
            #print("현재 기온은 "+str(t)+"도 이며 최저 기온은 "+V["tmn"]+"도 입니다.")
        else:
            prt.append("현재 기온은 "+str(t)+"도 입니다.")
            #print("현재 기온은 "+str(t)+"도 입니다.")
    if t<6:
        pr.append(["겨울 옷","방한용품"])
    elif 6<=t<10:
        pr.append(["코트","가죽 자켓"])
    elif 10<=t<12:
        pr.append(["트렌치 코트,야상 여러겹 껴입는 것"])
    elif 12<=t<17:
        pr.append(["자켓","셔츠","가디건","야상","살색 스타킹"])
    elif 17<=t<20:
        pr.append(["니트","가디건","청바지","면바지","맨투맨"])
    elif 20<=t<23:
        pr.append(["긴팔","후드티","면바지","슬랙스","스키니","가디건"])
    elif 23<=t<27:
        pr.append(["반팔","얇은 셔츠","반바지","면바지","긴팔"])
    else:
        pr.append(["민바지","반바지","원피스","바람이 잘통하는 옷"])

    S=""
    S+="이 기온에서는 "
    #print("이 기온에서는",end=" ")
    for i in range(len(pr[0])-1):
        S+=pr[0][i]+", "
        #print(pr[0][i],end=", ")
    S+=str(pr[0][len(pr[0])-1])+"을 추천합니다."
    #print(str(pr[0][len(pr[0])-1])+"을 추천합니다.")
    prt.append(S)

    w=V["wfen"]
    if w=="Rain" or w=="Shower" or w=="Raindrop":
        prt.append("지금 또는 곧 비가 내릴 예정입니다.")
        #print("지금 또는 곧 비가 내릴 예정입니다.")

        S=""
        S+="예상 강수량은 "+V["r12"]+"로 "
        #print("예상 강수량은 "+V["r12"]+"로 ",end="")
        if float(V["r12"])>=2.5:
            S+="옷이 젖는 것은 신경쓰지 않아도 될 정도입니다."
            prt.append(S)
            #print("옷이 젖는 것은 신경쓰지 않아도 될 정도입니다.")
            prt.append("필요하신 경우에만 우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
            #print("필요하신 경우에만 우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
        else:
            S+="상황에 따라 옷이 많이 젖을 수도 있습니다.\n"
            prt.append(S)
            #print("상황에 따라 옷이 많이 젖을 수도 있습니다.")
            prt.append("우산을 가지고 가거나 우비를 챙기는걸 추천합니다.")
            #print("우산을 가지고 가거나 우비를 챙기는걸 추천합니다.")
        
    elif w=="Snow" or w=="Snow Drifting":
        prt.append("지금 또는 곧 눈이 내릴 예정입니다.")
        #print("지금 또는 곧 눈이 내릴 예정입니다.")
        prt.append("예상 적설량은 "+V["s12"]+"로 필요하신 경우에만 우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
        #print("예상 적설량은 "+V["s12"]+"로 필요하신 경우에만 우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
    elif w=="Rain/Snow" or w==" Raindrop/Snow Drifting":
        prt.append("지금 또는 곧 비와 눈이 내릴 예정입니다.")
        #print("지금 또는 곧 비와 눈이 내릴 예정입니다.")
        prt.append("우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
        #print("우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
    else:
        if float(V["pop"])!=0:
            prt.append("비나 눈이 올 확률이 "+V["pop"]+"% 입니다.")
            #print("비나 눈이 올 확률이 "+V["pop"]+"% 입니다.")
            if float(V["pop"])>=40:
                prt.append("우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
                #print("우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
            else:
                prt.append("필요하신 경우에만 우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
                #print("필요하신 경우에만 우산을 가지고 가거나 우비를 챙기는 걸 추천합니다.")
    return prt





def run():

    print("지금 있는 위치를 추가해야 합니다.")
    print("(초기 설정은 충청북도 청주시 흥덕구 가경동으로 되어있습니다.)")
    print("https://www.weather.go.kr/w/pop/rss-guide.do")
    print("링크를 타고 들어가서 지금 현재 있는 지역을 설정한 뒤 링크를 복사해주세요.")
    print("그 다음에 링크를 cmd(명령프롬프트)에 붙여넣기 해주세요.")
    aa=input()
    url=aa#"http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4311374700"#aa



    width=700
    height=700
    color={"black":(0,0,0),"white":(255,255,255),"dark_green":(0,100,0),"green":(0,255,0),"blue":(3,37,126)}

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SURFACE = pygame.display.set_mode((width, height))
    pygame.display.set_caption('weather')

    #B=A.split('<data seq=\"0\">')[1].split('<data seq=\"1\">')[0]
    #print(B)


    font=pygame.font.SysFont("malgungothic",30)

    text=font.render("지금 시간대 추천",True,color["black"],color["green"])

    text2=font.render("확인",True,color["black"],color["green"])

    text3=font.render("지역 설정",True,color["black"],color["green"])

    text4=font.render("링크를 타고 들어가서 지금 현재 있는 지역을 설정한 뒤 링크를 복사해주세요.",True,color["black"])

    #text1=font.render(" 추천",True,color["white"],color["blue"])

    #print(pygame.font.get_fonts())

    while 1:
        SURFACE.fill(color["white"])

        SURFACE.blit(text,(250,350))

        SURFACE.blit(text3,(250,450))

        event = pygame.event.poll()
        if event.type == pygame.QUIT:break

        if pygame.mouse.get_pressed()[0]:
            Mouse=pygame.mouse.get_pos()
            #print(Mouse)

            if 251<=Mouse[0]<=381 and 451<=Mouse[1]<=489:
                pygame.quit()
                return 123

            if 249<=Mouse[0]<=482 and 352<=Mouse[1]<=391:
                # 오늘
            
                resp = requests.get(url)
                soup = BeautifulSoup(resp.text, 'lxml')
                A=str(soup)
                V=data_crolling(A,'<data seq=\"0\">','<data seq=\"1\">')
                A=answer(V)
                #print("##########")
                while 1:
                    SURFACE.fill(color["white"])
                    event = pygame.event.poll()
                    if event.type == pygame.QUIT:break
                    q=200
                    font=pygame.font.SysFont("malgungothic",20)
                    for i in range(len(A)):
                        text1=font.render(A[i],True,color["black"])
                        text_rect=text1.get_rect()
                        text_rect.centerx=350
                        text_rect.centery=q
                        SURFACE.blit(text1,text_rect)
                        #print(A[i])
                        q+=60

                    text_rect=text2.get_rect()
                    text_rect.centerx=350
                    text_rect.centery=500
                    SURFACE.blit(text2,text_rect)

                    if pygame.mouse.get_pressed()[0]:
                        Mouse=pygame.mouse.get_pos()
                        if 320<=Mouse[0]<=382 and 481<=Mouse[1]<=522:
                            break

                    pygame.display.update()
                        #FPSCLOCK.tick(100)
                    


        pygame.display.update()
        FPSCLOCK.tick(100)
    return 0

while 1:
    asd=run()
    if asd!=123:break