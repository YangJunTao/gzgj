# -*- coding: utf-8 -*-
from collections import deque #提高list删除插入速度
import operator
import os
import time

yuefenhuansuan={1:['1',0],2:['2',31],3:['3',59],4:['4',90],5:['5',120],6:['6',151],7:['7',181],8:['8',212],9:['9',243],10:['10',273],11:['11',304],12:['12',334]}

d_zgf={}
d_wgf={}
d_qt={}
d={}
n=0
zgf_qsj=7*60		#早高峰起始时间
zgf_zsj=9*60		#早高峰终止时间
wgf_qsj=17.5*60		#晚高峰起始时间
wgf_zsj=19.5*60		#晚高峰终止时间
qt_qsj=0*60		#全天起始时间
qt_qsj=0*60		#全天起始时间
qt_zsj=24*60		#全天终止时间



kk=0
#card_type = ['56']#卡类别筛选
mm=5
day =14
for dd in range(day,day+2):	
	kk+=1
	if len(str(mm)) <2:
		mm='0'+str(mm)
	if len(str(dd))<2:
		dd='0'+str(dd)
	if kk==1:
		mm1=mm
		dd1=dd
		riqi=yuefenhuansuan[int(mm)][1]+int(dd)
	
	n=0
	try:
		with open(r'E:\广州公交\广州数据及脚本\shuchu//'+str(mm)+'-'+str(dd)+'//chenggong.csv','r+',encoding='UTF-8')as f:
			for hang in f.readlines():
				n+=1
				if n%50000==0:
					print(str(mm),str(dd),':',n)
				if n!=1:
					line=hang.split(',')
					#if line[1] in card_type:
					if line[0] not in d:
						d[line[0]]={}
					shijian=line[-2].split(' ')
					nianyueri=shijian[0]
					nyr=nianyueri.split('-')
					shifenmiao=shijian[1].split(':')
					shi=shifenmiao[0]
					fen=shifenmiao[1]
					miao=shifenmiao[2]
					shiju = int(shi) * 3600 + int(fen) * 60 + int(miao) - 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2])) #将时间换成以某一天零点为基准，为以后做排序准备
					d[line[0]][shiju]=hang
	except:
		with open(r'E:\广州公交\广州数据及脚本\shuchu//'+'0'+str(int(mm)+1)+'-'+'01'+'//chenggong.csv','r+',encoding='UTF-8')as f:
			for hang in f.readlines():
				n+=1
				if n%50000==0:
					print(str(int(mm)+1),'01',':',n)
				if n!=1:
					line=hang.split(',')
					#if line[1] in card_type:
					if line[0] not in d:
						d[line[0]]={}
					shijian=line[-2].split(' ')
					nianyueri=shijian[0]
					nyr=nianyueri.split('-')
					shifenmiao=shijian[1].split(':')
					shi=shifenmiao[0]
					fen=shifenmiao[1]
					miao=shifenmiao[2]
					shiju = int(shi) * 3600 + int(fen) * 60 + int(miao) - 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2])) #将时间换成以某一天零点为基准，为以后做排序准备
					d[line[0]][shiju]=hang

	l=[]
		
	for k,v in d.items():
		sorted_kk=sorted(v.items(),key=operator.itemgetter(0))
		for x in sorted_kk:
			l.append(x[1])
			

	lastID=''			#记录上一id，为写入zhongdian作准备


	#d={}

	d_zgf={'':['null','null']}
	d_wgf={'':['null','null']}
	d_qt={'':['null','null']}
	l_zgf_zd=['null']
	l_wgf_zd=['null']
	l_qt_zd=['null']


	for line in l:
		line=line.split(',')
		shijian=line[-2].split(' ')
		nianyueri=shijian[0]
		nyr=nianyueri.split('-')
		shijian=shijian[1].split(':')
		fzj=int(shijian[0])*60+int(shijian[1])- 1440 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2]))	#fenzhongju，以分钟为单位距0点
		
		zhandian=line[-3]
		if line[0] != lastID:
			for sjd in ['zgf','wgf','qt']:
				if lastID in locals()['d_'+sjd]:
					if len(locals()['d_'+sjd][lastID])%2==1:
						locals()['d_'+sjd][lastID].append('null')
				if fzj >=locals()[sjd+'_qsj'] and fzj <=locals()[sjd+'_zsj'] :
					locals()['d_'+sjd][line[0]]=[zhandian]
					if zhandian not in locals()['l_'+sjd+'_zd']:
						locals()['l_'+sjd+'_zd'].append(zhandian)	
						
			lastID=line[0]
			
		else:
			for sjd in ['zgf','wgf','qt']:
				if fzj >=locals()[sjd+'_qsj'] and fzj <=locals()[sjd+'_zsj']:
					if lastID in locals()['d_'+sjd]:
						if len(locals()['d_'+sjd][lastID])%2==1:
							locals()['d_'+sjd][lastID].append(zhandian)
							locals()['d_'+sjd][lastID].append(zhandian)
							if zhandian not in locals()['l_'+sjd+'_zd']:
								locals()['l_'+sjd+'_zd'].append(zhandian)
						else:
							locals()['d_'+sjd][lastID].append(zhandian)
							if zhandian not in locals()['l_'+sjd+'_zd']:
								locals()['l_'+sjd+'_zd'].append(zhandian)
					else:
						locals()['d_'+sjd][lastID]=[zhandian]	
						if zhandian not in locals()['l_'+sjd+'_zd']:
							locals()['l_'+sjd+'_zd'].append(zhandian)
				else:
					if lastID in locals()['d_'+sjd]:
						if len(locals()['d_'+sjd][lastID])%2==1:
							locals()['d_'+sjd][lastID].append(zhandian)
							if zhandian not in locals()['l_'+sjd+'_zd']:
								locals()['l_'+sjd+'_zd'].append(zhandian)
	for sjd in ['zgf','wgf','qt']:
		locals()['d_'+sjd].pop('')
		
		di_shuchu={}
		nn=0
		od_o=0
		od_d=0
		for k,v in locals()['d_'+sjd].items():
			nn=0
			for x in v:
				nn+=1
				if nn%2==1:
					od_o=x
				if nn%2==0:
					od_d=x
					if (od_o,od_d) not in di_shuchu:
						di_shuchu[(od_o,od_d)]=0
					di_shuchu[(od_o,od_d)]+=1
		zrc=0								#总人次
		qdrc=0								#确定人次
		l_shuchu=[' ,']
		for x in locals()['l_'+sjd+'_zd']:
			l_shuchu.append(x)
			l_shuchu.append(',')
		l_shuchu.append('\n')
		for x in locals()['l_'+sjd+'_zd']:
			l_shuchu.append(x)
			l_shuchu.append(',')
			for xx in locals()['l_'+sjd+'_zd']:
				if (x,xx) in di_shuchu:
					l_shuchu.append(str(di_shuchu[(x,xx)]))
					zrc+=di_shuchu[(x,xx)]
					if x!='null' and xx!='null':
						qdrc+=di_shuchu[(x,xx)]
				else:
					l_shuchu.append('0')
				l_shuchu.append(',')
			l_shuchu.append('\n')
		print('start Writing')
		if os.path.exists('E:\广州公交\yjt\od\\'+str(mm1)+str(dd1)) == False:
			os.makedirs('E:\广州公交\yjt\od\\'+str(mm1)+str(dd1)+'\\')

		with open('E:\广州公交\yjt\od\\'+str(mm1)+str(dd1)+'\\'+sjd+'.csv','w+',encoding='UTF-8')as f:
			for x in l_shuchu:
				f.write(x)
		n=0
		nn=0
		nnn=0
		with open(r'E:\广州公交\yjt\od\\'+str(mm1)+str(dd1)+'\\'+sjd+'.csv','r+',encoding='UTF-8')as f:
			for hang in f.readlines():
				line=hang.split(',')
				if n!=0:
					nn+=int(line[n])
					nnn+=int(line[1])
				n+=1
		with open('E:\广州公交\yjt\od\\'+str(mm1)+str(dd1)+'\\'+sjd+'信息.txt','w+',encoding='UTF-8')as f:
			f.write('总人次：')
			f.write(str(zrc))
			f.write('\n')
			f.write('对角线和：')
			f.write(str(nn))
			f.write('\n')
			f.write('未识别到终点数：')
			f.write(str(nnn))
			f.write('\n')
			f.write('确定人次：')
			f.write(str(qdrc))
			f.write('\n')
	print('done')
				
		
		
				



