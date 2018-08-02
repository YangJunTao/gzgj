# -*- coding: utf-8 -*-

from pandas import DataFrame
df=  DataFrame(columns=['总人数', '非高峰搭车人数', '早搭晚不搭', '晚搭早不搭','确定OD'])
'''
总体思路：
通过羊城通ID匹配，在早晚高峰都一次以上出行的为换乘
黄家俊已经可以根据每天的公交数据  l_inforid {id, 家, 晚上乘车点}
我可以根据地铁刷卡数据生成 id, 地铁早晚高峰的上车点下车点

在黄家俊的代码中添加一个value，即白天刷卡上车时间，和地铁早高峰刷卡时间对比
地铁早高峰刷卡时间 < 公交刷卡时间，O为地铁上车站，D为公交下车站，地铁换乘公交
公交刷卡时间 < 地铁早高峰刷卡时间，O为公交上车站，D为地铁下车站，公交换乘地铁
'''
'''
新加：从只坐了公交的
'''
def getDayNumber(month, day):   #输入日期，输出是第几天
    L =  [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    return L[month-1]+day


#地铁刷卡文件中不含站点名称，要通过设备编号找到对应的站点
d_NumToStation={}   #key是编号 value是名称
with open(r'E:\广州公交\广州项目\地铁\\交易设备地铁站点对应.txt')as f:
    for lines in f.readlines():
        line=lines.split('	')   
        d_NumToStation[int(line[1].strip())] = line[0]


for day in range(1,7):
    month=5
    mm='0%s'%month
    dd='0%s'%day if day<10 else str(day)
    date=mm+dd
    dayPeak = range(630,930)        #早高峰时间段
    nightPeak = range(1730, 1930)   #晚高峰时间段
    allPassengers=set()             #所有乘客
    dayPassengers, nightPassengers = set(), set()  
    notPeak=set()
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
    
    
    
    
    #---------------以下是生成地铁匹配成功的ODTrue{key:卡号, value:[刷卡时间, [O,D]]}------------------#
    
    print("生成地铁当日早、晚高峰卡号OD字典")
    for xmz in ['2688','3680','3690']:
        with open(r'E:\广州公交\广州项目\地铁\CX'+xmz+'0012018'+mm+dd+'08\JY'+xmz+'0012018'+mm+dd+'08.txt','r+', encoding='gbk') as f:
            for lines in f.readlines():
                line=lines.split('	')
                if line[17][4:8] == mm+dd:                       #交易入口时间要是今天
                    enterTime = int(line[17][8:12])                
                    if line[0] != line[16]:           #设备不同为出站
                        allPassengers.add(line[3])
                        if enterTime in dayPeak:                    #筛选早高峰出行   
                            dayPassengers.add(line[3])
                            try:
                                if int(line[0]) in d_NumToStation and int(line[16]) in d_NumToStation:#能找到对应站点
                                        Ostation = d_NumToStation[int(line[16])]
                                        Dstation = d_NumToStation[int(line[0])]
                                        ODDay[line[3]] = [enterTime, [Ostation, Dstation]]
                            except:
                                pass
                        elif enterTime in nightPeak:                    #筛选晚高峰出行
                            nightPassengers.add(line[3])   
                            try:
                                if int(line[0]) in d_NumToStation and int(line[16]) in d_NumToStation:#能找到对应站点
                                    Ostation = d_NumToStation[int(line[16])]
                                    Dstation = d_NumToStation[int(line[0])]
                                    ODNight[line[3]] = [Ostation, Dstation]	
                            except:
                                pass
                        else:
                            notPeak.add(line[3])
        f.close()
    
    OD_Transfer={}
    transfer=set()
    #换乘匹配：首先生成地铁当日早高峰ODDay和晚高峰ODNight
    #从公交当日所有刷卡数据中，判断时间在早高峰且ODNight或者ODDay有对应卡号的，匹配换乘
    #判断时间在晚高峰且ODNight或者ODDay有对应卡号的，匹配换乘
    with open('E:\广州公交\广州数据及脚本\shuchu//'+mm+'-'+dd+'//chenggong.csv','r+',encoding='UTF-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            time=int(line[-2].split(' ')[1].split(':')[0]+line[-2].split(' ')[1].split(':')[1])
            allPassengers.add(line[3])
            if time in dayPeak:
                dayPassengers.add(line[3])
                if line[0] in ODNight:
                    transfer.add(line[0])
                    OD_Transfer[line[0]] = [line[-3], ODNight[line[0]][0]]
                elif line[0] in ODDay:
                  transfer.add(line[0])
                  OD_Transfer[line[0]] = [ODDay[line[0]][1][0], line[-3]]
    
            elif time in nightPeak:
                nightPassengers.add(line[3])
                if line[0] in ODDay:
                    transfer.add(line[0])
                    OD_Transfer[line[0]] = [ODDay[line[0]][1][0], line[-3]]
                elif line[0] in ODNight:
                    transfer.add(line[0])
                    OD_Transfer[line[0]] = [line[-3], ODNight[line[0]][0]]
            else:
                notPeak.add(line[0])
    print("出行总人数%s"%len(allPassengers))	   
    print("早高峰出行人数：%s"%len(dayPassengers))
    print("晚高峰出行人数：%s"%len(nightPassengers))
    onlyDay=len(dayPassengers)-len(transfer)
    print("早搭晚不搭人数：%s"%onlyDay)
    onlyNight=len(nightPassengers)-len(transfer)
    print("晚搭早不搭人数：%s"%onlyNight)
    print('早晚高峰都有搭地铁或者公交的人数是%s'%len(transfer))
    print('换乘匹配成功数%s'%len(OD_Transfer))
    print('非高峰搭车人数%s\n'%len(notPeak))
    
    '''	
    for lines in l_inforid:
        line = lines.split(',')
        if line[0] not in ODTrue:
            continue
        else:
            transferNum+=1
            if int(ODTrue[line[0]][0]) < int(line[-1][:4]):
                OD_Transfer[line[0]] = [ODTrue[line[0]][1][0], line[-2]]
                
            elif int(ODTrue[line[0]][0]) > int(line[-1][:4]):
                OD_Transfer[line[0]] = [line[1], ODTrue[line[0]][1][1]]
    '''
    
    df.loc[date] = [len(allPassengers), len(notPeak), onlyDay, onlyNight, len(OD_Transfer)]    
    

    
    
    
    '''
    筛选一周内的数据
    若当天早高峰的数据 在首日晚高峰ODNight里，则ODTrue更新数据
    若当天晚高峰的数据 在首日早高峰ODDay里，则ODTrue更新数据
    最后ODTrue的长度就是匹配成功的个数
    
    for i in range(2,8):
        print("验证第%s天"%i)
        day+=1
        if day>30:
            month, day = 5, 1 
        mm='0%s'%month
        dd='0%s'%day if day<10 else str(day)
        for xmz in ['2688','3680','3690']:
            with open(r'E:\广州公交\广州项目\地铁\CX'+xmz+'0012018'+mm+dd+'08\JY'+xmz+'0012018'+mm+dd+'08.txt','r+', encoding='gbk') as f:
                for lines in f.readlines():
                    line=lines.split('	')
                    if line[17][4:8] == mm+dd:                              #交易入口时间要是今天
                        enterTime = int(line[17][8:12])
                        try:
                            if int(line[0]) != int(line[16]):                   #筛选出站刷卡数据
    
                                if enterTime in nightPeak:                      #筛选晚高峰出行
                                    if line[3] in ODDay :                        #有首日早高峰数据
                                        Ostation = d_NumToStation[int(line[16])]
                                        Dstation = d_NumToStation[int(line[0])]
                                        if [Dstation, Ostation] == ODDay[line[3]][1]:
                                            ODTrue[line[3]] = [ODDay[line[3]][0], [Dstation, Ostation]] #有则覆盖，无则添加，长度是人数
    
    
                                if enterTime in dayPeak:                      #筛选早高峰出行
                                    if line[3] in ODNight:                      #有首日晚高峰数据
                                        Ostation = d_NumToStation[int(line[16])]
                                        Dstation = d_NumToStation[int(line[0])]
                                        if [Ostation, Dstation] == ODNight[line[3]][1]:
                                            ODTrue[line[3]] = [enterTime, [Ostation, Dstation]]  #有则覆盖，无则添加，长度是人数
                        except:
                            pass
            f.close()
                                
    print("职住匹配成功数%s"%len(ODTrue))
    '''
    #---------------以上是生成地铁匹配成功的ODTrue{key:卡号, value:[刷卡时间, [O,D]]}------------------#
    
    
    
    #---------------以下生成公交匹配成功的l_inforid [id,家,晚上乘车点,上车刷卡时间]------------------#
    """
    yuefenhuansuan={1:['1',0],2:['2',31],3:['3',59],4:['4',90],5:['5',120],6:['6',151],7:['7',181],8:['8',212],9:['9',243],10:['10',273],11:['11',304],12:['12',334]}
    
    d={}
    
    n=0
    day=24
    mm='0%s'%month
    dd='0%s'%day if day<10 else str(day)
    riqi=getDayNumber(month, day)
    if len(str(mm)) <2:
    	mm='0'+str(mm)
    if len(str(dd))<2:
    	dd='0'+str(dd)
    d={}
    d_add={}		#add=address
    d_od={}
    l_inforid=deque([])
    
    n=0
    try:
    	with open('E:\广州公交\广州数据及脚本\shuchu//'+str(mm)+'-'+str(dd)+'//chenggong.csv','r+',encoding='UTF-8')as f:
    		for hang in f.readlines():
    			n+=1
    			if n%50000==0:
    				print(str(mm),str(dd),':',n)
    			if n!=1:
    				line=hang.split(',')
    				if line[0] not in d:
    					d[line[0]]={}
    				shijian=line[-2].split(' ')
    				nianyueri=shijian[0]
    				nyr=nianyueri.split('-')
    				shifenmiao=shijian[1].split(':')
    				shi=shifenmiao[0]
    				fen=shifenmiao[1]
    				miao=shifenmiao[2]
    				sfm=str(shifenmiao[0]+':'+shifenmiao[1]+':'+shifenmiao[2])
    				shiju = int(shi) * 3600 + int(fen) * 60 + int(miao) - 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2])) #将时间换成以某一天零点为基准，为以后做排序准备
    				d[line[0]][shiju]=hang
    except:
    	with open('E:\广州公交\广州数据及脚本\shuchu//'+str(int(mm)+1)+'-'+str(1)+'//chenggong.csv','r+',encoding='UTF-8')as f:
    		for hang in f.readlines():
    			n+=1
    			if n%50000==0:
    				print(str(mm),str(dd),':',n)
    			if n!=1:
    				line=hang.split(',')
    				if line[0] not in d:
    					d[line[0]]={}
    				shijian=line[-2].split(' ')
    				nianyueri=shijian[0]
    				nyr=nianyueri.split('-')
    				shifenmiao=shijian[1].split(':')
    				shi=shifenmiao[0]
    				fen=shifenmiao[1]
    				miao=shifenmiao[2]
    				sfm=str(shifenmiao[0]+':'+shifenmiao[1]+':'+shifenmiao[2])
    				shiju = int(shi) * 3600 + int(fen) * 60 + int(miao) - 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2])) #将时间换成以某一天零点为基准，为以后做排序准备
    				d[line[0]][shiju]=hang
    
    l=[]
    
    for k,v in d.items():
    	sorted_kk=sorted(v.items(),key=operator.itemgetter(0))
    	for x in sorted_kk:
    		l.append(x[1])
    
    
    		
    d={'':{'day':{'qidian':{},'zhongdian':{}},'night':{'qidian':{},'zhongdian':{}}}}
    	
    y=0					#是否进行判断早高峰起点依据,0为判断，1为不判断
    yy=0				#是否进行判断晚高峰起点依据,0为判断，1为不判断
    z=1					#是否录入早高峰终点依据,0为录入，1为不录入
    zz=1				#是否录入晚高峰终点依据,0为录入，1为不录入
    day_zd='null'		#白天终点
    night_zd='null'		#晚上终点
    lastID=''			#记录上一id，为写入zhongdian作准备
    
    
    for line in l:
    	line=line.split(',')
    	shijian=line[-2].split(' ')
    	nyr=nianyueri.split('-')
    	shijian=shijian[1].split(':')
    	fzj=int(shijian[0])*60+int(shijian[1])		#fenzhongju，以分钟为单位距0点
    	riqi=yuefenhuansuan[int(nyr[1])][1]+int(nyr[2])
    	zhandian=line[-3]
    	startTime = shijian[0]+ shijian[1]
    	if line[0] != lastID:
    		rizi=riqi
    		y=0					#是否进行判断早高峰起点依据
    		yy=0				#是否进行判断晚高峰起点依据
    		#创建起点和终点的字典，并各自有上班与下班时段字典
    		if line[0] not in d:
    			d[line[0]]={'day':{'qidian':{},'zhongdian':{}},'night':{'qidian':{},'zhongdian':{}}}	
    		#将上一ID的早晚时间段的终点录入
    		if z==0:
    			z=1
    			if day_zd in d[lastID]['day']['zhongdian']:
    				d[lastID]['day']['zhongdian'][day_zd]+=1
    			else:
    				d[lastID]['day']['zhongdian'][day_zd]=1	
    		if zz==0:
    			z=1
    			if night_zd in d[lastID]['night']['zhongdian']:
    				d[lastID]['night']['zhongdian'][night_zd]+=1
    			else:
    				d[lastID]['night']['zhongdian'][night_zd]=1
    		lastID=line[0]
    		
    		#判断早高峰起点，并记录有可能的终点
    		if fzj >=420 and fzj <=540 :		#因为限制了时间，有可能开始的起点不在这里，如果只是想知道其家庭工作地点可放宽时间段，但不能掌握其是否在高峰时段出行
    			d[line[0]]['day']['time'] = startTime	
    			if y==0  :
    				y=1
    				if zhandian in d[line[0]]['day']['qidian']:
    					d[line[0]]['day']['qidian'][zhandian]+=1
    				else :
    					d[line[0]]['day']['qidian'][zhandian]=1
    			
    		#判断晚高峰起点，并记录有可能的终点
    		elif fzj >=1050 and fzj <=1170: 								
    			if yy==0 :
    				#yy=1
    				if zhandian in d[line[0]]['night']['qidian']:
    					d[line[0]]['night']['qidian'][zhandian]+=1
    				else :
    					d[line[0]]['night']['qidian'][zhandian]=1
    			
    	if line[0] == lastID:	
    		if riqi==rizi:
    			#判断早高峰起点，并记录有可能的终点
    			if fzj >=420 and fzj <=540 :
    				d[line[0]]['day']['time'] = startTime	
    				if y==0 :
    					y=1
    					if zhandian in d[line[0]]['day']['qidian']:
    						d[line[0]]['day']['qidian'][zhandian]+=1
    					else :
    						d[line[0]]['day']['qidian'][zhandian]=1
    				
    			#判断晚高峰起点，并记录有可能的终点
    			elif fzj >=1050 and fzj <=1170:						
    				if yy==0 :
    					#yy=1
    					if zhandian in d[line[0]]['night']['qidian']:
    						d[line[0]]['night']['qidian'][zhandian]+=1
    					else :
    						d[line[0]]['night']['qidian'][zhandian]=1
    				
    		
    		if riqi>rizi:
    			rizi=riqi
    			#将上一天的早晚时间段的终点录入
    			if z==0:
    				z=1
    				if day_zd in d[lastID]['day']['zhongdian']:
    					d[lastID]['day']['zhongdian'][day_zd]+=1
    				else:
    					d[lastID]['day']['zhongdian'][day_zd]=1
    			if zz==0:
    				zz=1
    				if night_zd in d[lastID]['night']['zhongdian']:
    					d[lastID]['night']['zhongdian'][night_zd]+=1
    				else:
    					d[lastID]['night']['zhongdian'][night_zd]=1
    				
    			#判断早高峰起点，并记录有可能的终点
    			if fzj >=420 and fzj <=540 :	
    				d[line[0]]['day']['time'] = startTime		
    				if y==0 :
    					y=1
    					if zhandian in d[line[0]]['day']['qidian']:
    						d[line[0]]['day']['qidian'][zhandian]+=1
    					else :
    						d[line[0]]['day']['qidian'][zhandian]=1
    				
    			#判断晚高峰起点，并记录有可能的终点
    			elif fzj >=1050 and fzj <=1170: 								
    				if yy==0 :
    					#yy=1
    					if zhandian in d[line[0]]['night']['qidian']:
    						d[line[0]]['night']['qidian'][zhandian]+=1
    					else :
    						d[line[0]]['night']['qidian'][zhandian]=1
    				
    
    d.pop('')				
    
    
    #判断家，工作地点
    d_add={}		#add=address
    li=['day_qd_max','day_zd_max','night_qd_max','night_zd_max']
    l_ri=['day','night']
    l_qz=['qidian','zhongdian']
    for k,v in d.items():
    	d_add[k]={}
    	if 'time' in d[k]['day']:
    		d_add[k]['time'] = d[k]['day']['time']
    	for x in li:
    		locals()[x]=''
    	nn=0
    	#给li里的变量赋值，分别表示早晚起终点的最大值的站点
    	for t in l_ri:
    		for tt in l_qz:
    			if v[t][tt]:
    				locals()[li[nn]]=sorted(v[t][tt],key=lambda x:v[t][tt][x])[-1]
    			else:
    				locals()[li[nn]]='null'
    			nn+=1
    	if 'jia' not in d_add[k]:
    		d_add[k]['jia']= day_qd_max
    
    	if 'gongsi' not in d_add[k]:
    		d_add[k]['gongsi']= night_qd_max
    
    	if d_add[k]['jia']!='null' and d_add[k]['gongsi']!='null' and 'time' in d_add[k]:
    		strr=k+','+d_add[k]['jia']+','
    		for key,value in v['night']['qidian'].items():
    			strr+=(key+',')
    		strr+=d_add[k]['time']
    		strr+='\n'				
    		l_inforid.append(strr)
    print("公交匹配成功数%s"%len(l_inforid))
    """
    
    
    
    
    
    
    #---------------以上生成公交匹配成功的l_inforid [id,家,晚上乘车点,上车刷卡时间]------------------#
    
    '''
    公交匹配数据 列表结构 [id,家,晚上乘车点,上车刷卡时间]
    地铁匹配数据 字典结构 {key:卡号, value:[早高峰刷卡时间, [O,D]]}
    
    公交人数<地铁人数，所以匹配换乘从公交匹配数据遍历
    取出公交匹配数据卡号id，检索地铁匹配数据里是否存在相同卡号，无则跳下一条数据，有则继续下面的步骤
    比较公交匹配数据 和地铁匹配数据的刷卡时间
    地铁早高峰刷卡时间 < 公交刷卡时间，O为地铁上车站，D为公交晚上乘车点，地铁换乘公交
    公交刷卡时间 < 地铁早高峰刷卡时间，O为公交家，D为地铁下车站，公交换乘地铁
    最后生成换乘的数据 {key:卡号, value:[O, D]}
    
    地铁晚高峰刷卡时间 < 公交刷卡时间，O为地铁上车站，D为公交晚上下车点，地铁换乘公交
    公交刷卡时间 < 地铁晚高峰刷卡时间，O为公交家，D为地铁下车站，公交换乘地铁
    '''
    
   

