# -*- coding: utf-8 -*-

import json
import os
import operator

yuefenhuansuan={1:['1',0],2:['2',31],3:['3',59],4:['4',90],5:['5',120],6:['6',151],7:['7',181],8:['8',212],9:['9',243],10:['10',273],11:['11',304],12:['12',334]}


"""
d_user={}

kk=0
riqi=116
for mm in range(4,5):		
	for dd in range(26,27):	
		kk+=1
		if len(str(mm)) <2:
			mm='0'+str(mm)
		if len(str(dd))<2:
			dd='0'+str(dd)
		if kk==1:
			mm1=mm
			dd1=dd	
			#riqi=yuefenhuansuan[int(mm)][1]+int(dd)
		n=0	
		with open(r'D://广州//公交数据//公交刷卡数据//2018-'+str(mm)+'-'+str(dd)+'//folder//2018-'+str(mm)+'-'+str(dd)+'.txt','r+',encoding='UTF-8') as f:
			for line in f.readlines():
				n+=1
				if n%50000==0:
					print(str(mm),str(dd),':',n)
				line=json.loads(line)
				nyr=[line['data'][0]['tim'][:4],line['data'][0]['tim'][4:6],line['data'][0]['tim'][6:8]]
				shi=line['data'][0]['tim'][8:10]
				fen=line['data'][0]['tim'][10:12]
				miao=line['data'][0]['tim'][12:14]
				shiju = int(shi) * 3600 + int(fen) * 60 + int(miao) - 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2]))
				lineno=line['data'][0]['lineno'][-5:]
				busno=line['data'][0]['busno']
				if lineno not in d_user:
					d_user[lineno]={}
				if busno not in d_user[lineno]:
					d_user[lineno][busno]=[]
				d_user[lineno][busno].append((shiju,line['data'][0]['logiccardno']))
	

d_yz={}				#yz=已知,主支线对应

lis_1=os.listdir('D://广州//公交数据//公交分车//116')
for x in lis_1:
	xianlu=x[1:4]
	if xianlu not in d_yz:
		d_yz[xianlu]={}
	lis_2=os.listdir('D://广州//公交数据//公交分车//116//'+x)
	for xx in lis_2:
		with open(r'D://广州//公交数据//公交分车//116//'+x+'//'+xx,'r+',encoding='UTF-8')as f:
			for line in f.readlines():
				line=line.split(',')
				shijian=line[-2].strip('''"''').split(' ')
				nianyueri=shijian[0]
				nyr=nianyueri.split('-')
				shifenmiao=shijian[1].split(':')
				shi=shifenmiao[0]
				fen=shifenmiao[1]
				miao=shifenmiao[2]
				shiju = int(shi) * 3600 + int(fen) * 60 + int(miao)- 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2]))
				zhandian=line[-7]
				busno=xx[:-4]
				
				if busno not in d_yz[xianlu]:
					d_yz[xianlu][busno]=[]
				d_yz[xianlu][busno].append((shiju,zhandian))

d_bus={}
d_id={}			

w=0
n=0		
for k,v in d_user.items():											#对每一个线路做遍历
	lineno=k[1:4]
	if lineno not in d_yz:
		w+=1
	else:
		for kk,vv in v.items():											#对线路的每一个巴士做遍历,里面有一个巴士内所有乘客的乘车信息
			
			
			ddd_inf={}
			d_bus[kk]={}
			d_panduan={}
			d_bus_jishu={}
			for x in vv:												#对巴士内的每一个人做遍历，结果是要找出相应的已知巴士
				n+=1
				if n%50000==0:
					print(n)
				id=x[1]
				ddd={}
				for busno,bus_inf in d_yz[lineno].items():				#对已知里的同一个线路的所有车做遍历
				
					for vaa in bus_inf:									#对一辆车的所有运行时间做遍历，找出与此次刷卡最近的一个站点和时间
						if busno not in ddd:
							ddd[busno]=99999999
							ddd_inf[busno]={}
						if id not in ddd_inf[busno]:
							ddd_inf[busno][id]='null'
						sjj=abs(vaa[0]-x[0])			#时间距
						if sjj<ddd[busno]:
							ddd[busno]=sjj
							ddd_inf[busno][id]=(x[0],vaa[1])			#没考虑同一个人连续上同一辆车的异常情况
				final_bus=sorted(ddd.items(),key=lambda item:item[1])[0][0]
				if final_bus not in d_bus_jishu:
					d_bus_jishu[final_bus]=0
				d_bus_jishu[final_bus]+=1
			d_bus[kk]=sorted(d_bus_jishu.items(),key=lambda item:item[1])[-1][0]		
			
			for sc_id,sc_xx in ddd_inf[d_bus[kk]].items():				#输出以id为key的以时间为第二层key的字典
				if sc_id not in d_id:
					d_id[sc_id]={}
				d_id[sc_id][sc_xx[1]]=sc_xx[0]


with open('D:\广州\公交数据\match_cut.txt','w')as f:
	for k,v in d_bus.items():
		f.write(k)
		f.write(',')
		f.write(v)
		f.write(',')
		f.write('\n')
with open('D:\广州\公交数据\cuowu_cut.txt','w')as f:
	f.write(str(w))		
"""				
d_user={}
d_bus={}
l=[]
for k,v in d_id.items():
	sorted_kk=sorted(v.items(),key=operator.itemgetter(0))
	for x in sorted_kk:
		strrr=str(k)+','+str(x[0])+','+str(x[1])
		l.append(strrr)
		
		

lastID=''			#记录上一id，为写入zhongdian作准备
d_zgf={'':['null','null']}
d_wgf={'':['null','null']}
d_qt={'':['null','null']}
l_zgf_zd=['null']
l_wgf_zd=['null']
l_qt_zd=['null']
zgf_qsj=7*60		#早高峰起始时间
zgf_zsj=9*60		#早高峰终止时间
wgf_qsj=17.5*60		#晚高峰起始时间
wgf_zsj=19.5*60		#晚高峰终止时间
qt_qsj=0*60		#全天起始时间
qt_zsj=24*60		#全天终止时间
		
for line in l:
	line=line.split(',')
	fzj=int(line[2])//60
	zhandian=line[1]
	
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
			else:
				l_shuchu.append('0')
			l_shuchu.append(',')
		l_shuchu.append('\n')
	
	if os.path.exists('D:\广州\公交数据\shuchu_cut\\'+str(mm1)+str(dd1)) == False:
		os.mkdir('D:\广州\公交数据\shuchu_cut\\'+str(mm1)+str(dd1)+'\\')

	with open('D:\广州\公交数据\shuchu\\'+str(mm1)+str(dd1)+'\\'+sjd+'.csv','w')as f:
		for x in l_shuchu:
			f.write(x)
	n=0
	nn=0
	nnn=0
	with open('D:\广州\公交数据\shuchu\\'+str(mm1)+str(dd1)+'\\'+sjd+'.csv')as f:
		for hang in f.readlines():
			line=hang.split(',')
			if n!=0:
				nn+=int(line[n])
				nnn+=int(line[1])
			n+=1
	with open('D:\广州\公交数据\shuchu\\'+str(mm1)+str(dd1)+'\\'+sjd+'信息.txt','w')as f:
		f.write('对角线和：')
		f.write(str(nn))
		f.write('\n')
		f.write('未识别到终点数：')
		f.write(str(nnn))
		f.write('\n')
	

	
	
	