# -*- coding: utf-8 -*-

import json
import os
import operator

yuefenhuansuan={1:['1',0],2:['2',31],3:['3',59],4:['4',90],5:['5',120],6:['6',151],7:['7',181],8:['8',212],9:['9',243],10:['10',273],11:['11',304],12:['12',334]}
line_match={'3':'C','4':'E','5':'H','6':'N','7':'P','8':'R'}


d_dz={}
n=0
with open(r'E:\广州公交\广州数据及脚本//cldz.csv','r+',encoding='UTF-8')as f:
	for line in f.readlines():
		n+=1
		line=line.split(',')
		if n!=1:
			if line[1][-4:] not in d_dz:
				d_dz[line[1][-4:]]=[]
			d_dz[line[1][-4:]].append(line[2])
d={}
l=[]
ll=[]

kk=0
date=21
for mm in range(5,6):
	dd=date
	kk+=1
	if len(str(mm)) <2:
		mm='0'+str(mm)
	if len(str(dd))<2:
		dd='0'+str(dd)
	if kk==1:
		mm1=mm
		dd1=dd
	riqi=yuefenhuansuan[int(mm)][1]+int(dd)
	line_list=os.listdir('E:\广州公交\yjt/公交分车//'+str(riqi))
	n=0
	for line_no in line_list:
		n+=1
		if n%300==0:
			print(mm,dd,n)
		bus_list=os.listdir('E:\广州公交\yjt/公交分车//'+str(riqi)+'//'+line_no)
		for bus_no in bus_list:
			with open(r'E:\广州公交\yjt/公交分车//'+str(riqi)+'//'+line_no+'//'+bus_no,'r+',encoding='UTF-8') as f:
				for line in f.readlines():
					line=line.split(',')
					shijian=line[-2:-1][0].strip('''"''').split(' ')
					shifenmiao=shijian[1].split(':')
					shi=shifenmiao[0]
					fen=shifenmiao[1]
					miao=shifenmiao[2]
					nianyueri=shijian[0]
					nyr=nianyueri.split('-')
					shiju = int(shi) * 3600 + int(fen) * 60 + int(miao) - 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2])) #将时间换成以某一天零点为基准，为以后做排序准备
					
					obuid=line[1].strip('''"''')
					lineid_jilu=line[4].strip('''"''')[-5:]
					lineid=line[4].strip('''"''')[-5:-1]
					if lineid[0] in line_match:
						lineid=line_match[lineid[0]]+lineid[1:]
					linename=line[5].strip('''"''')
					stationname= line[13].strip('''"''')
					intime= line[-2].strip('''"''')
					if obuid not in d:
						d[obuid]={}
					if lineid not in d[obuid]:
						d[obuid][lineid]={}
					d[obuid][lineid][shiju]=lineid_jilu+','+linename+','+obuid+','+stationname+','+intime+',\n'

						
for mm in range(5,6):	
	for dd in range(date,date+2):
		if len(str(mm)) <2:
			mm='0'+str(mm)
		if len(str(dd))<2:
			dd='0'+str(dd)
		
					
		try:		
			n=0
			with open(r'E:\广州公交\广州项目\公交刷卡//2018-'+str(mm)+'-'+str(dd)+'//folder//2018-'+str(mm)+'-'+str(dd)+'.txt','r+',encoding='UTF-8') as f:
				for line in f.readlines():
					
					line=json.loads(line)
					for xl in range(len(line['data'])):
						n+=1
						if n%50000==0:
							print(str(mm),str(dd),':',n)
						nyr=[line['data'][xl]['tim'][:4],line['data'][xl]['tim'][4:6],line['data'][xl]['tim'][6:8]]
						shi=line['data'][xl]['tim'][8:10]
						fen=line['data'][xl]['tim'][10:12]
						miao=line['data'][xl]['tim'][12:14]
						shiju = int(shi) * 3600 + int(fen) * 60 + int(miao) - 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2]))
						lineno_jilu=line['data'][xl]['lineno'][-5:]
						lineno=line['data'][xl]['lineno'][-5:-1]
						busno=line['data'][xl]['busno'][-4:]
						strr=line['data'][xl]['logiccardno']+','+line['data'][xl]['cardtype']+','+line['data'][xl]['tf']+','+busno+','+lineno_jilu+','+line['data'][xl]['tim']+','
						#if line['data'][xl]['lineno'][-1] =='0':				#只对规则的进行分析
						kn=0
						knn=0
						knnn=0
						if busno in d_dz:
							

							ll_kn=len(d_dz[busno])
							for x in d_dz[busno]:								#x为车辆运行的obuid
								

								if x in d:										
									kn+=1
									if lineno in ['C000','C0020','N060','N600']:
										knn+=1
										continue
										
									
									elif lineno in d[x]:
										ss=sorted(d[x][lineno].items(),key=operator.itemgetter(0))
										leee=len(ss)
										knlk=0
										for xx in ss:
											knlk+=1
											if abs(xx[0]-shiju)<60:
												l.append(strr+xx[1])
												break
											if	knlk==leee:
												ll.append(strr+'\n')
												
									
									
									else:
										knn+=1
								else:									#obuid在公交运行文件中找不到
									knnn+=1		
										
							if ll_kn==knn or ll_kn==knnn :		#obuid在公交运行文件中是有问题的巴士编号找不到或者在公交运行文件中找不到obuid
								ll.append(strr+'\n')
						else:									#busno在匹配文件里找不到
							ll.append(strr+'\n')
						#else:
							#ll.append(strr+'\n')
		except Exception as e:
			print(e)
'''						
for mm in range(5,6):		
	for dd in range(2,3):	

		if len(str(mm)) <2:
			mm='0'+str(mm)
		if len(str(dd))<2:
			dd='0'+str(dd)
				
						
		n=0
		with open(r'D://广州//公交数据//公交刷卡数据//2018-'+str(mm)+'-'+str(dd)+'//folder//2018-'+str(mm)+'-'+str(dd)+'.txt','r+',encoding='UTF-8') as f:
			for line in f.readlines():
				
				line=json.loads(line)
				for xl in range(len(line['data'])):
					n+=1
					if n%50000==0:
						print(str(mm),str(dd),':',n)
					nyr=[line['data'][xl]['tim'][:4],line['data'][xl]['tim'][4:6],line['data'][xl]['tim'][6:8]]
					shi=line['data'][xl]['tim'][8:10]
					fen=line['data'][xl]['tim'][10:12]
					miao=line['data'][xl]['tim'][12:14]
					shiju = int(shi) * 3600 + int(fen) * 60 + int(miao) - 86400 * (riqi - yuefenhuansuan[int(nyr[1])][1]-int(nyr[2]))
					lineno_jilu=line['data'][xl]['lineno'][-5:]
					lineno=line['data'][xl]['lineno'][-5:-1]
					busno=line['data'][xl]['busno'][-4:]
					strr=line['data'][xl]['logiccardno']+','+line['data'][xl]['cardtype']+','+line['data'][xl]['tf']+','+busno+','+lineno_jilu+','+line['data'][xl]['tim']+','
					#if line['data'][xl]['lineno'][-1] =='0':				#只对规则的进行分析
					kn=0
					knn=0
					knnn=0
					if busno in d_dz:
						

						ll_kn=len(d_dz[busno])
						for x in d_dz[busno]:								#x为车辆运行的obuid
							

							if x in d:										
								kn+=1
								if lineno in ['C000','C0020','N060','N600']:
									knn+=1
									continue
									
								
								elif lineno in d[x]:
									ss=sorted(d[x][lineno].items(),key=operator.itemgetter(0))
									leee=len(ss)
									knlk=0
									for xx in ss:
										knlk+=1
										if abs(xx[0]-shiju)<60:
											l.append(strr+xx[1])
											break
										if	knlk==leee:
											ll.append(strr+'\n')
											
								
								
								else:
									knn+=1
							else:									#obuid在公交运行文件中找不到
								knnn+=1		
									
						if ll_kn==knn or ll_kn==knnn :		#obuid在公交运行文件中是有问题的巴士编号找不到或者在公交运行文件中找不到obuid
							ll.append(strr+'\n')
					else:									#busno在匹配文件里找不到
						ll.append(strr+'\n')
					#else:
						#ll.append(strr+'\n')
						
'''						
						
print("Start Write")						
if os.path.exists('E:\广州公交\广州数据及脚本\shuchu//'+str(mm1)+'-'+str(dd1))== False:
	os.makedirs('E:\广州公交\广州数据及脚本\shuchu//'+str(mm1)+'-'+str(dd1)+'/') 
with open(r'E:\广州公交\广州数据及脚本\shuchu//'+str(mm1)+'-'+str(dd1)+'//chenggong.csv','w+',encoding='UTF-8') as f:
	for x in l:
		f.write(x)
		
with open(r'E:\广州公交\广州数据及脚本\shuchu//'+str(mm1)+'-'+str(dd1)+'//shibai.csv','w+',encoding='UTF-8') as f:
	for x in ll:
		f.write(x)
		
		
			
			
			