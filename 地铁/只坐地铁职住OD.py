# -*- coding: utf-8 -*-
import os
from pandas import DataFrame
df=  DataFrame(columns=['总人数', '非高峰搭车人数', '早搭晚不搭', '晚搭早不搭','确定OD'])

def getDayNumber(month, day):   #输入日期，输出是第几天
    L =  [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    return L[month-1]+day


#地铁刷卡文件中不含站点名称，要通过设备编号找到对应的站点
d_NumToStation={}   #key是编号 value是名称
with open(r'E:\广州公交\广州项目\地铁\\交易设备地铁站点对应.txt')as f:
    for lines in f.readlines():
        line=lines.split('	')   
        d_NumToStation[int(line[1].strip())] = line[0]
f.close()


#day=24
for day in range(30,31):
    month=4
    mm='0%s'%month
    dd='0%s'%day if day<10 else str(day)
    date=mm+dd
    dayPeak = range(630,900)       #早高峰时间段
    nightPeak = range(1730, 1930)   #晚高峰时间段
    n=0                             #刷卡记录条数
    stationNull=0                   #设备无对应站点
    notToday = 0                    #日期不是今天的刷卡量
    dayPeakNum, nightPeakNum=  0, 0    #count是有刷卡出站记录的人数，onlyNight晚搭早不搭,晚高峰出行人数
    onlyNight={}                    #晚搭早不搭
    bothPeak={}                     #长度为早晚总人数
    allCount={}                     #总人数
    #key是卡号，value是一个list，起点和终点
    ODNight, ODDay={}, {}
    ODTrue={}   #早晚高峰匹配成功的字典
    '''
    通过以下数据：
    line[0]本次交易设备编号
    line[2]本次交易时间
    line[3]卡号
    line[16]本次交易入口设备编号
    line[17]本次交易入口时间
    line[18]上次设备编号
    line[19]上次入口时间
    
    生成以下数据：
    人数、非高峰搭车人数、早搭晚不搭、晚搭早不搭
    
    筛选刷卡记录：
    第一遍读取，生成
    ODDay：含有全部早高峰的字典{key:卡号, value:[O, D]}
    早高峰出行总人数 len(ODDay)
    总刷卡记录n
    有进出站记录的总人数count
    找不到对应站点的总记录stationNull
    '''
    
    
    #只坐地铁，排除公交刷卡数据中的卡号
    busCard = {}
    with open('E:\广州公交\广州数据及脚本\shuchu//'+mm+'-'+dd+'//chenggong.csv','r+',encoding='UTF-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            busCard[line[0]] = ''

    
            
    print("生成全部早高峰卡号OD字典")
    for xmz in ['2688','3680','3690']:
        with open(r'E:\广州公交\广州项目\地铁\CX'+xmz+'0012018'+mm+dd+'08\JY'+xmz+'0012018'+mm+dd+'08.txt','r+', encoding='gbk') as f:
            for lines in f.readlines():
                n+=1
                line=lines.split('	')
                if line[17][4:8] == mm+dd and line[3] not in busCard: #只坐地铁，交易入口时间要是今天
                    enterTime = int(line[17][8:12])
                    if line[0] != line[16]:           #设备不同为出站
                        allCount[line[3]] = ''
                        if enterTime in dayPeak:                    #筛选早高峰出行   
                            dayPeakNum+=1
                            try:
                                if int(line[0]) in d_NumToStation and int(line[16]) in d_NumToStation:#能找到对应站点
                                        Ostation = d_NumToStation[int(line[16])]
                                        Dstation = d_NumToStation[int(line[0])]
                                        ODDay[line[3]] = [Ostation, Dstation]
                                else:
                                    stationNull+=1
                            except:
                                pass
                else:
                    notToday+=1
        f.close()
    print("出行总人数为:%s"%len(allCount))
    
    '''
    第二遍读取，生成
    ODNight：含有全部晚高峰的字典{key:卡号, value:[O, D]}
    晚高峰出行总人数nightPeakNum
    每个晚高峰出行OD，若在ODDay有对应记录，则ODTrue添加对应记录，无对应记录，则晚搭早不搭+1
    '''
    print("生成全部晚高峰卡号OD字典")
    for xmz in ['2688','3680','3690']:
        with open(r'E:\广州公交\广州项目\地铁\CX'+xmz+'0012018'+mm+dd+'08\JY'+xmz+'0012018'+mm+dd+'08.txt','r+', encoding='gbk') as f:
            for lines in f.readlines():
                line=lines.split('	')
                if line[17][4:8] == mm+dd and line[3] not in busCard:   #只坐地铁，交易入口时间要是今天
                    enterTime = int(line[17][8:12])
                    if line[0] != line[16]:           #设备不同为出站
                        if enterTime in nightPeak:                    #筛选晚高峰出行
                            nightPeakNum+=1
                            try:
                                if int(line[0]) in d_NumToStation and int(line[16]) in d_NumToStation:#能找到对应站点
                                    Ostation = d_NumToStation[int(line[16])]
                                    Dstation = d_NumToStation[int(line[0])]
                                    ODNight[line[3]] = [Ostation, Dstation]
                                    if line[3] in ODDay:                          #早晚都搭地铁    #OD完全匹配  and [Dstation, Ostation] == ODDay[line[3]]
                                        ODTrue[line[3]] = [Dstation, Ostation]    #长度是人数
                                        bothPeak[line[3]] = ''                    #早晚高峰都刷卡的次数，多文件匹配会重复不准
                                    else:
                                        onlyNight[line[3]] = ''                   #无对应早高峰OD，晚搭早不搭+1
                            except:
                                pass
        f.close()
    
    onlyDay =  len(ODDay) - len(bothPeak)                          #早搭晚不搭 = 早人数 - 早晚都搭
    print("早搭晚不搭的人数为：%s"%onlyDay)
    print("晚搭早不搭的人数为：%s"%len(onlyNight))
    notPeak = len(allCount) -onlyDay - len(bothPeak) - len(onlyNight)              #非高峰搭车人数 = 总人数-早全部-晚全部
    print('非高峰搭车人数：%s'%notPeak)
    print("仅匹配当天，职住匹配成功数%s"%len(ODTrue))
    
    
    
    '''
    筛选一周内的数据
    若当天早高峰的数据 在首日晚高峰ODNight里，则ODTrue更新数据
    若当天晚高峰的数据 在首日早高峰ODDay里，则ODTrue更新数据
    最后ODTrue的长度就是匹配成功的个数
    '''
    for i in range(2,8):
        print("验证第%s天"%i)
        day+=1
        if day>30:
            month, day = 5, 1 
        mm='0%s'%month
        dd='0%s'%day if day<10 else str(day)
        print('读取'+mm+dd+'文件')
        for xmz in ['2688','3680','3690']:
            if os.path.exists('E:\广州公交\广州项目\地铁\CX'+xmz+'0012018'+mm+dd+'08\JY'+xmz+'0012018'+mm+dd+'08.txt'):
                with open(r'E:\广州公交\广州项目\地铁\CX'+xmz+'0012018'+mm+dd+'08\JY'+xmz+'0012018'+mm+dd+'08.txt','r+', encoding='gbk') as f:
                    for lines in f.readlines():
                        line=lines.split('	')
                        if line[17][4:8] == mm+dd:      #交易入口时间要是今天
                            enterTime = int(line[17][8:12])
                            try:
                                if int(line[0]) != int(line[16]):                   #筛选出站刷卡数据
        
                                    if enterTime in nightPeak:                      #筛选晚高峰出行
        
                                        if line[3] in ODDay :                        #有首日早高峰数据
                                            Ostation = d_NumToStation[int(line[16])]
                                            Dstation = d_NumToStation[int(line[0])]
                                            if [Dstation, Ostation] == ODDay[line[3]]:
                                                ODTrue[line[3]] = [Dstation, Ostation]  #有则覆盖，无则添加，长度是人数
        
                                        elif line[3] in ODNight:                      #有首日晚高峰数据
                                            Ostation = d_NumToStation[int(line[16])]
                                            Dstation = d_NumToStation[int(line[0])]
                                        if [Ostation, Dstation] == ODNight[line[3]]:
                                            ODTrue[line[3]] = [Ostation, Dstation]  #有则覆盖，无则添加，长度是人数                               
        
        
                                    elif enterTime in dayPeak:                      #筛选早高峰出行
        
                                        if line[3] in ODDay :                        #有首日早高峰数据
                                            Ostation = d_NumToStation[int(line[16])]
                                            Dstation = d_NumToStation[int(line[0])]
                                            if [Dstation, Ostation] == ODDay[line[3]]:
                                                ODTrue[line[3]] = [Dstation, Ostation]  #有则覆盖，无则添加，长度是人数
        
        
                                        elif line[3] in ODNight:                      #有首日晚高峰数据
                                            Ostation = d_NumToStation[int(line[16])]
                                            Dstation = d_NumToStation[int(line[0])]
                                            if [Ostation, Dstation] == ODNight[line[3]]:
                                                ODTrue[line[3]] = [Ostation, Dstation]  #有则覆盖，无则添加，长度是人数
                            except:
                                pass
                f.close()
                                
    print("职住匹配成功数%s"%len(ODTrue))
    df.loc[date] = [len(allCount), notPeak, onlyDay, len(onlyNight), len(ODTrue)]


'''
地铁：当日匹配23万，结合后6天，匹配37万
仅坐地铁：单日匹配18.7万，结合后6天，匹配29.5万

说明7万左右的换乘的


早晚高峰都有搭地铁或者公交的刷卡是159232
换乘匹配成功数133243

'''