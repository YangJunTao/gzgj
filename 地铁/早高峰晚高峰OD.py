# -*- coding: utf-8 -*-

from collections import deque #提高list删除插入速度
import operator
import time
import os
'''
以下需要说明下，全称和作用
nn								#用来做统计的，进了地铁站但四小时内没出来的人数 fourHourNotOut
nnn								#用来做统计的，总过刷卡进站人数 enterCount
nnnn							#用来做统计的，总过刷卡出站人数 outCount
jz_n							#进站闸机无对应的数量，识别不出的数量 enter_Null
cz_n							#出站闸机无对应的数量，识别不出的数量 out_Null
d_zd							#闸机和站点的对应关系，存储在字典里
d_zgf							#早高峰od的字典，key是od对，value是人流 morningPeak
d_wgf							#晚高峰od的字典，key是od对，value是人流 eveningPeak
zgf_zd							#早高峰站点列表，把早高峰内出现的早高峰站点都记录 morningPeak_Station
wgf_zd							#晚高峰站点列表，把晚高峰内出现的早高峰站点都记录 eveningPeak_Station
d_tm=							#tm指同名，指进出站同名的站点统计 
d_zdtj_jz						#进站站点统计，每半小时统计一次，双层字典，key是站点，value是以时间的字典，二层字典key是每半小时（如00：30，07：00），value是客流
d_zdtj_cz						#出战站点统计，参照上面
d_zgf_xf						#和d_zgf一样，只是统计的是xf文件，d_zgf统计的是cx文件
d_wgf_xf						#晚高峰，同上
xmz								#文件名不一样，同一天的CX文件由三个文件组成，可以观察一下文件名
enterInterval outInterval
jinshiju，chushiju是进时距，出时距吗				#是的,以需要做统计的那一天的00：00为0，每加一秒加以，比如00：30为1800
line[0],line[16]代表什么？文件里是010000029922
sc_lis												#列表，是为了输出统计信息用的
'''
date ='0424'
dt_List, gj_List  = [], []
def dt_path(date):
    path = 'E:\广州公交\广州项目\地铁\\'
    path1 = path + 'CX26880012018'+ date + '08\JY26880012018'+date+'08.txt'
    path2 = path + 'CX36800012018'+ date + '08\JY36800012018'+date+'08.txt'
    path3 = path + 'CX36900012018'+ date + '08\JY36900012018'+date+'08.txt'
# =============================================================================
#     path4 = path + 'XF26880012018'+ date + '\JY26880012018'+date+'.txt'
#     path5 = path + 'XF36800012018'+ date + '\JY36800012018'+date+'.txt'
#     path6 = path + 'XF36900012018'+ date + '\JY36900012018'+date+'.txt'
# =============================================================================
    return [path1, path2, path3]

for path in dt_path(date):
    with open(path) as f:
        for line in f.readlines():
            line=line.split('	')
            dt_List.append(line[3])
    f.close()
dt_num = set(dt_List)

with open(r'E:\广州公交\广州项目\公交刷卡\2018-%s-%s\folder\\2018-%s-%s.txt'%(date[:2], date[2:], date[:2], date[2:])) as f:
    for line in f.readlines():
        line = line.split('logiccardno":"')
        gj_List.append(line[1][:16])
gj_num = set(gj_List)
f.close()


def both():
	#4.24 403725
    return len(gj_num.intersection(dt_num))

def onlyBus():
	#4.24 1825002
    return gj_num - gj_num.intersection(dt_num)

def onlyMetro():
	#4.24 1466670
    return dt_num - gj_num.intersection(dt_num)
dt_List = onlyMetro()

yuefenhuansuan={1:['1',0],2:['2',31],3:['3',59],4:['4',90],5:['5',120],6:['6',151],7:['7',181],8:['8',212],9:['9',243],10:['10',273],11:['11',304],12:['12',334]}
d_zd={}

with open(r'E:\广州公交\广州数据及脚本\羊城通sam2018.txt') as f:
	for line in f.readlines():
		line=line.split('	')
		d_zd[int(line[1].strip())]=line[0]

n=0
nn=0
nnn=0
nnnn=0
jz_n=0
cz_n=0
d_zgf={}
d_wgf={}
zgf_zd=deque([])
wgf_zd=deque([])
d_tm={}
d_zdtj_jz={}
d_zdtj_cz={}

d_zgf_xf={}
d_wgf_xf={}
jinzhandian='lllllllll'
chuzhandian='llllllldd'

for mm in range(4,5):		
	for dd in range(24,25):		
		riqi=yuefenhuansuan[int(mm)][1]+dd #dateNumber
		if len(str(mm)) <2:
			mm='0'+str(mm)
		if len(str(dd))<2:
			dd='0'+str(dd)
		d_zgf={}
		d_wgf={}
		d_zdtj_jz={}
		d_zdtj_cz={}
		jz_n=0
		cz_n=0
		n=0
		nn=0
		nnn=0
		nnnn=0
		for path in dt_path(date):
			with open(path) as f:
				print('luruwancheng')
				print('aa'+str(mm)+str(dd)+':',n)
				for line in f.readlines():
					line=line.split('	')
					n+=1	
					if n%50000==0:				#每处理50000条显示一次
						print('aa'+str(mm)+str(dd)+':',n)
					#try:#CX卡			
					if line[0]!=line[16]:
						jinshijian=line[17]
						jintianshu=yuefenhuansuan[int(jinshijian[4:6])][1]+int(jinshijian[6:8])#dayNumber
						jinshiju = int(jinshijian[8:10]) * 3600 + int(jinshijian[10:12]) * 60 + int(jinshijian[12:14]) + 86400 * (jintianshu-riqi)
						chushijian=line[2]
						chutianshu=yuefenhuansuan[int(chushijian[4:6])][1]+int(chushijian[6:8])
						chushiju = int(chushijian[8:10]) * 3600 + int(chushijian[10:12]) * 60 + int(chushijian[12:14]) + 86400 * (chutianshu-riqi)
						try:
							if int(line[16]) in d_zd:
								jinzhandian=d_zd[int(line[16])]
							else:
								jinzhandian=str(line[16])
								jz_n+=1
						except:
							jinzhandian=str(line[16])
							jz_n+=1
						
						try:
							if int(line[0]) in d_zd:
								chuzhandian=d_zd[int(line[0])]
							else:
								chuzhandian=str(line[0])
								cz_n+=1
						except:
							chuzhandian=str(line[0])
							cz_n+=1
						if chushijian[:4]==jinshijian[:4] and 0<(chushiju-jinshiju)<14401:		#进出站时间超过4个小时的去除
							nnnn+=1
							if 23400<jinshiju<32400 and 25200<chushiju<34200:
								od = (jinzhandian,chuzhandian)
								if od in d_zgf:
									d_zgf[od]+=1
								else:
									d_zgf[od]=1
									for x in od:
										if x not in zgf_zd:
											zgf_zd.append(x)
								if jinzhandian==chuzhandian:
									d_tm[n]=line				
							if 61200<jinshiju<70200 and 63000<chushiju<72000:
								od = (jinzhandian,chuzhandian)
								if od in d_wgf:
									d_wgf[od]+=1
								else:
									d_wgf[od]=1
									for x in od:
										if x not in wgf_zd:
											wgf_zd.append(x)
								if jinzhandian==chuzhandian:
									d_tm[n]=line
						else:
							nn+=1
						
						#以下为统计站点客流所用
						if jintianshu==riqi:
							if jinzhandian not in d_zdtj_jz:
								d_zdtj_jz[jinzhandian]={}
								for st in range(1,49):
									stt=st*30
									d_zdtj_jz[jinzhandian][stt]=0
							fenshiju=int(jinshijian[8:10])*60+int(jinshijian[10:12])
							for st in range(1,49):
								stt=st*30
								if fenshiju<=stt:
									d_zdtj_jz[jinzhandian][stt]+=1
									break
									
						if chutianshu==riqi:
							if chuzhandian not in d_zdtj_cz:
								d_zdtj_cz[chuzhandian]={}
								for st in range(1,49):
									stt=st*30
									d_zdtj_cz[chuzhandian][stt]=0
							fenshiju=int(chushijian[8:10])*60+int(chushijian[10:12])
							for st in range(1,49):
								stt=st*30
								if fenshiju<=stt:
									d_zdtj_cz[chuzhandian][stt]+=1
									break	
							
					else:
						nnn+=1
# =============================================================================
# 					XF卡
# 					except:
# 					
# 						if line[4]==line[17]:	
# 							jinshijian=line[4]
# 							if int(jinshijian[4:6]) in yuefenhuansuan:
# 								jintianshu=yuefenhuansuan[int(jinshijian[4:6])][1]+int(jinshijian[6:8])
# 							else:
# 								jintianshu=0
# 							jinshiju = int(jinshijian[8:10]) * 3600 + int(jinshijian[10:12]) * 60 + int(jinshijian[12:14]) + 86400 * (jintianshu-riqi)
# 							chushijian=line[6]
# 							if int(chushijian[4:6]) in yuefenhuansuan:
# 								chutianshu=yuefenhuansuan[int(chushijian[4:6])][1]+int(chushijian[6:8])
# 							else:
# 								chutianshu=0
# 							chushiju = int(chushijian[8:10]) * 3600 + int(chushijian[10:12]) * 60 + int(chushijian[12:14]) + 86400 * (chutianshu-riqi)
# 							jinzhandian=line[3]
# 							chuzhandian=line[5]
# 							if chushijian[:4]==jinshijian[:4] and 0<(chushiju-jinshiju)<14401:		#进出站时间超过4个小时的去除
# 								nnnn+=1
# 								if 23400<jinshiju<32400 and 25200<chushiju<34200:
# 									od = (jinzhandian,chuzhandian)
# 									if od in d_zgf:
# 										d_zgf[od]+=1
# 									else:
# 										d_zgf[od]=1
# 										for x in od:
# 											if x not in zgf_zd:
# 												zgf_zd.append(x)
# 									if jinzhandian==chuzhandian:
# 										d_tm[n]=line				
# 								if 61200<jinshiju<70200 and 63000<chushiju<72000:
# 									od = (jinzhandian,chuzhandian)
# 									if od in d_wgf:
# 										d_wgf[od]+=1
# 									else:
# 										d_wgf[od]=1
# 										for x in od:
# 											if x not in wgf_zd:
# 												wgf_zd.append(x)
# 									if jinzhandian==chuzhandian:
# 										d_tm[n]=line
# 							else:
# 								nn+=1
# 						
# 							#以下为统计站点客流所用
# 							if jintianshu==riqi:
# 								if jinzhandian not in d_zdtj_jz:
# 									d_zdtj_jz[jinzhandian]={}
# 									for st in range(1,49):
# 										stt=st*30
# 										d_zdtj_jz[jinzhandian][stt]=0
# 								fenshiju=int(jinshijian[8:10])*60+int(jinshijian[10:12])
# 								for st in range(1,49):
# 									stt=st*30
# 									if fenshiju<=stt:
# 										d_zdtj_jz[jinzhandian][stt]+=1
# 										break
# 										
# 							if chutianshu==riqi:
# 								if chuzhandian not in d_zdtj_cz:
# 									d_zdtj_cz[chuzhandian]={}
# 									for st in range(1,49):
# 										stt=st*30
# 										d_zdtj_cz[chuzhandian][stt]=0
# 								fenshiju=int(chushijian[8:10])*60+int(chushijian[10:12])
# 								for st in range(1,49):
# 									stt=st*30
# 									if fenshiju<=stt:
# 										d_zdtj_cz[chuzhandian][stt]+=1
# 										break	
# 					
#						else:
#							nnn+=1
# =============================================================================						
		if os.path.exists('E:\广州公交\yjt\CX\\'+str(mm)+str(dd)) == False:
			os.mkdir('E:\广州公交\yjt\CX\\'+str(mm)+str(dd)+'/')
		
		for mz in ['jz','cz']:		
			#输出站点客流信息
			with open(r'E:\广州公交\yjt\CX\\'+str(mm)+str(dd)+'\\train_'+mz+'.csv','w')as f:
				for kk,vv in locals()['d_zdtj_'+mz].items():
					sss=sorted(zip(vv.keys(),vv.values()))
					for x in sss:
						f.write(kk+','+str(x[0])+','+str(x[1])+',\n')
						
			sc_lis=['zhandian']
			strr=','

			for x in range(5,24):
				rr=0
				for xx in [':30',':00']:
					if rr==0:
						strrr=str(x-1)+xx+'-'+str(x)+':00,'
					if rr==1:
						strrr=str(x)+xx+'-'+str(x)+':30,'
					rr+=1
					strr=strr+strrr
					

			strr=strr+'23:30-24:00,'
			sc_lis.append(strr)


			with open(r'E:\广州公交\yjt\CX\\'+str(mm)+str(dd)+'\\train_'+mz+'.csv')as f:
				for line in f.readlines():
					line=line.split(',')	
					if int(line[1])/30==10:
						sc_lis.append('\n')
						sc_lis.append(line[0])
						sc_lis.append(',')
						sc_lis.append(line[2])
						sc_lis.append(',')
					elif 10<int(line[1])/30<=48:
						sc_lis.append(line[2])
						sc_lis.append(',')
					elif int(line[1])/30==48:
						sc_lis.append(line[2])
						sc_lis.append(',')

						
			with open(r'E:\广州公交\yjt\CX\\'+str(mm)+str(dd)+'\\train_statics_'+mz+'.csv','w')as f:
				for x in sc_lis:
					f.write(x)

		
		OD_zgf=deque(['null,'])				#早高峰OD						
		for x in zgf_zd:
			OD_zgf.append(x)
			OD_zgf.append(',')
		OD_zgf.append('\n')
		for x in zgf_zd:
			OD_zgf.append(x)
			OD_zgf.append(',')
			for xx in zgf_zd:
				if (x,xx) in d_zgf:
					OD_zgf.append(str(d_zgf[(x,xx)]))
					OD_zgf.append(',')
				else:
					OD_zgf.append('0')
					OD_zgf.append(',')
			OD_zgf.append('\n')

		OD_wgf=deque(['null,'])			#晚高峰OD
		for x in wgf_zd:
			OD_wgf.append(x)
			OD_wgf.append(',')
		OD_wgf.append('\n')
		for x in wgf_zd:
			OD_wgf.append(x)
			OD_wgf.append(',')
			for xx in wgf_zd:
				if (x,xx) in d_wgf:
					OD_wgf.append(str(d_wgf[(x,xx)]))
					OD_wgf.append(',')
				else:
					OD_wgf.append('0')
					OD_wgf.append(',')
			OD_wgf.append('\n')	
		
		with open(r'E:\广州公交\yjt\CX\\'+str(mm)+str(dd)+'\\zaogaofeng_'+str(mm)+str(dd)+'.csv','w') as f :
			for x in OD_zgf:
				f.write(x)
		with open(r'E:\广州公交\yjt\CX\\'+str(mm)+str(dd)+'\\wangaofeng_'+str(mm)+str(dd)+'.csv','w') as f :
			for x in OD_wgf:
				f.write(x)				
		with open('E:\广州公交\yjt\CX\\'+str(mm)+str(dd)+'\\tongji_'+str(mm)+str(dd)+'_CX.txt','w') as f:
			f.write('总共:')
			f.write(str(n))
			f.write('\n')
			f.write('四小时内出站:')
			f.write(str(nnnn))
			f.write('\n')
			f.write('超过四小时:')
			f.write(str(nn))
			f.write('\n')
			f.write('刷卡进站:')
			f.write(str(nnn))
			f.write('\n')
			f.write('刷卡出站:')
			f.write(str(n-nnn))
			f.write('\n')
			f.write('进站闸机无对应:')
			f.write(str(jz_n))
			f.write('\n')
			f.write('出站闸机无对应:')
			f.write(str(cz_n))
			f.write('\n')
			
"""


		
zgf_zd_xf=deque([])
wgf_zd_xf=deque([])
gg=0
ggg=0	
gggg=0	
for mm in range(5,6):		#确定输入文件时间月份，这里是2
	for dd in range(3,12):		#确定输入文件时间天，这里是25
		riqi=yuefenhuansuan[int(mm)][1]+dd
		if len(str(mm)) <2:
			mm='0'+str(mm)
		if len(str(dd))<2:
			dd='0'+str(dd)
		d_zgf_xf={}
		d_wgf_xf={}
		n=0
		nn=0
		nnn=0
		nnnn=0
		gg=0
		ggg=0
		
		for xmz in ['2688','3680','3690']:									
			with open(r'F:\shuakashuju\新数据\广州\4.30-5.13地铁数据\bak_dt_input_20180501-20180509\XF'+xmz+'0012018'+str(mm)+str(dd)+'\JY'+xmz+'0012018'+str(mm)+str(dd)+'.txt','r+') as f:
				print('luruwancheng')
				print('aa'+str(mm)+str(dd)+':',n)
				for line in f.readlines():
					n+=1	
					if n%50000==0:				#每处理50000条显示一次
						print('aa'+str(mm)+str(dd)+':',n)
					line=line.split('	')
					if line[4]==line[17]:	
						jinshijian=line[4]
						if int(jinshijian[4:6]) in yuefenhuansuan:
							jintianshu=yuefenhuansuan[int(jinshijian[4:6])][1]+int(jinshijian[6:8])
						else:
							jintianshu=0
						jinshiju = int(jinshijian[8:10]) * 3600 + int(jinshijian[10:12]) * 60 + int(jinshijian[12:14]) + 86400 * (jintianshu-riqi)
						chushijian=line[6]
						if int(chushijian[4:6]) in yuefenhuansuan:
							chutianshu=yuefenhuansuan[int(chushijian[4:6])][1]+int(chushijian[6:8])
						else:
							chutianshu=0
						chushiju = int(chushijian[8:10]) * 3600 + int(chushijian[10:12]) * 60 + int(chushijian[12:14]) + 86400 * (chutianshu-riqi)
						jinzhandian=line[3]
						chuzhandian=line[5]
						if chushijian[:4]==jinshijian[:4] and 0<(chushiju-jinshiju)<14401:
							nnnn+=1
							if 23400<jinshiju<32400 and 25200<chushiju<34200:
								gg+=1
								od = (jinzhandian,chuzhandian)
								if od in d_zgf_xf:
									d_zgf_xf[od]+=1
								else:
									d_zgf_xf[od]=1
									for x in od:
										if x not in zgf_zd_xf:
											zgf_zd_xf.append(x)
								if jinzhandian==chuzhandian:
									d_tm[n]=line
											
							if 61200<jinshiju<70200 and 63000<chushiju<72000:
								ggg+=1
								od = (jinzhandian,chuzhandian)
								if od in d_wgf_xf:
									d_wgf_xf[od]+=1
								else:
									d_wgf_xf[od]=1
									for x in od:
										if x not in wgf_zd_xf:
											wgf_zd_xf.append(x)
							
						else:
							nn+=1
							
						
						
					else:
						nnn+=1											
		print('ggggggggggggggggggggggggggggggggggg',gg)									
		print('goooooooooooooooooooooooooooooooooo',ggg)									
		print('gaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',gggg)									
		OD_zgf_XF=deque(['null,'])				#早高峰OD						
		for x in zgf_zd_xf:
			OD_zgf_XF.append(x)
			OD_zgf_XF.append(',')
		OD_zgf_XF.append('\n')
		for x in zgf_zd_xf:
			OD_zgf_XF.append(x)
			OD_zgf_XF.append(',')
			for xx in zgf_zd_xf:
				if (x,xx) in d_zgf_xf:
					OD_zgf_XF.append(str(d_zgf_xf[(x,xx)]))
					OD_zgf_XF.append(',')
				else:
					OD_zgf_XF.append('0')
					OD_zgf_XF.append(',')
			OD_zgf_XF.append('\n')

		OD_wgf_XF=deque(['null,'])			#晚高峰OD
		for x in wgf_zd_xf:
			OD_wgf_XF.append(x)
			OD_wgf_XF.append(',')
		OD_wgf_XF.append('\n')
		for x in wgf_zd_xf:
			OD_wgf_XF.append(x)
			OD_wgf_XF.append(',')
			for xx in wgf_zd_xf:
				if (x,xx) in d_wgf_xf:
					OD_wgf_XF.append(str(d_wgf_xf[(x,xx)]))
					OD_wgf_XF.append(',')
				else:
					OD_wgf_XF.append('0')
					OD_wgf_XF.append(',')
			OD_wgf_XF.append('\n')								
		
		if os.path.exists('F:\shuakashuju\新数据\试验文件夹\shuchu\XF\\'+str(mm)+str(dd)) == False:
			os.mkdir('F:/shuakashuju/新数据/试验文件夹/shuchu/XF//'+str(mm)+str(dd)+'/')
		
		with open(r'F:\shuakashuju\新数据\试验文件夹\shuchu\XF\\'+str(mm)+str(dd)+'\\zaogaofeng_'+str(mm)+str(dd)+'.csv','w') as f :
			for x in OD_zgf_XF:
				f.write(x)
			
		with open(r'F:\shuakashuju\新数据\试验文件夹\shuchu\XF\\'+str(mm)+str(dd)+'\\wangaofeng_'+str(mm)+str(dd)+'.csv','w') as f :
			for x in OD_wgf_XF:
				f.write(x)
				
		with open('F:\shuakashuju\新数据\试验文件夹\shuchu\XF\\'+str(mm)+str(dd)+'\\tongji_'+str(mm)+str(dd)+'_XF.txt','w') as f:
			f.write('总共:')
			f.write(str(n))
			f.write('\n')
			f.write('超过四小时:')
			f.write(str(nn))
			f.write('\n')
			f.write('刷卡进站:')
			f.write(str(nnn))
			f.write('\n')
			f.write('刷卡出站:')
			f.write(str(nnnn))
			f.write('\n')
"""