

from collections import deque #提高list删除插入速度
import operator
import os
import time

yuefenhuansuan={1:['1',0],2:['2',31],3:['3',59],4:['4',90],5:['5',120],6:['6',151],7:['7',181],8:['8',212],9:['9',243],10:['10',273],11:['11',304],12:['12',334]}

d={}

n=0
q_sj=24
z_sj=24
yue=4
for mm in range(yue,yue+1):		
	for dd in range(q_sj,z_sj+1):		
		riqi=yuefenhuansuan[int(mm)][1]+dd
		if len(str(mm)) <2:
			mm='0'+str(mm)
		if len(str(dd))<2:
			dd='0'+str(dd)
		d={}
		d_add={}		#add=address
		d_od={}
		l_inforid=deque(['id,家,晚上乘车点,\n'])
		
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
			date=nianyueri.split('-')
			shijian=shijian[1].split(':')
			fzj=int(shijian[0])*60+int(shijian[1])		#fenzhongju，以分钟为单位距0点
			riqi=yuefenhuansuan[int(date[1])][1]+int(date[2])
			zhandian=line[-3]
			
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

			"""#如果家庭工作地点都是地铁站
			if day_qd_max == night_zd_max:
				d_add[k]['jia']= day_qd_max
			if day_zd_max==night_qd_max:
				d_add[k]['gongsi']= day_zd_max"""
				
			#如果不是家或公司旁没有地铁站或BRT站，简单的认为白天起点最多的是家，晚上起点最多的是工作地点
			if 'jia' not in d_add[k]:
				d_add[k]['jia']= day_qd_max

			if 'gongsi' not in d_add[k]:
				d_add[k]['gongsi']= night_qd_max

			"""#也可以按比例最大的估算家或地点,以下是示例
			if 'jia' not in d_add[k]:
				dq_he=0
				d_add[k]['jia']=[]
				for x in v['day']['qidian'].values():
					dq_he+=x
				for kk,vv in v['day']['qidian'].items():
					if vv/dq_he>0.25:
						d_add[k]['jia'].append(kk)	"""
			if d_add[k]['jia']!='null' and d_add[k]['gongsi']!='null':
				strr=k+','+d_add[k]['jia']+','
				for key,value in v['night']['qidian'].items():
					strr+=(key+',')
                    
				strr+='\n'
				l_inforid.append(strr)
			
		d_od={}
		l_jg=['jia','gongsi']
		l_zd=['null']
		for k,v in d_add.items():
			od=(v['jia'],v['gongsi'])
			if od not in d_od:
				d_od[od]=0
				for x in od:
					if x not in l_zd:
						l_zd.append(x)
			d_od[od]+=1

		l_shuchu=[' ,']

		for x in l_zd:
			l_shuchu.append(x)
			l_shuchu.append(',')
		l_shuchu.append('\n')
		rzs=0										#人总数
		zdwbd=0										#早搭晚不搭
		wdzbd=0										#晚搭早不搭
		for x in l_zd:
			l_shuchu.append(x)
			l_shuchu.append(',')
			if x !='null':
				if (x,'null') in d_od:
					zdwbd+=d_od[(x,'null')]								#统计早搭晚不搭
				if ('null',x) in d_od:
					wdzbd+=d_od[('null',x)]								#统计晚搭早不搭
			for xx in l_zd:
				if (x,xx) in d_od:
					l_shuchu.append(d_od[(x,xx)])
					rzs+=d_od[(x,xx)]
					l_shuchu.append(',')
				else:
					l_shuchu.append('0')
					l_shuchu.append(',')
			
			l_shuchu.append('\n')
		
		
		
		if os.path.exists('E:\广州公交\yjt\人_od\\'+str(mm)+str(dd)) == False:
			os.mkdir('E:\广州公交\yjt\人_od\\'+str(mm)+str(dd)+'/')
		
		with open(r'E:\广州公交\yjt\人_od\\'+str(mm)+str(dd)+'\\shuchu'+str(mm)+str(dd)+'.csv','w+',encoding='utf-8')as f:
			for x in l_shuchu:
				f.write(str(x))
		
		
		with open(r'E:\广州公交\yjt\人_od\\'+str(mm)+str(dd)+'\\id_information.csv','w+',encoding='utf-8')as f:
			for x in l_inforid:
				f.write(str(x))
		
		gg=0
		l_xinxi=['人数:',rzs,'\n高峰内公交换乘的人数:']
		with open(r'E:\广州公交\yjt\人_od\\'+str(mm)+str(dd)+'\\id_information.csv','r+',encoding='utf-8')as f:
			for line in f.readlines():
				line=line.split(',')
				if len(line)>4:
					gg+=1
		l_xinxi.append(gg)
		
		with open(r'E:\广州公交\yjt\人_od\\'+str(mm)+str(dd)+'\\xinxi.txt','w+',encoding='utf-8')as f:
			for x in l_xinxi:
				f.write(str(x))
			f.write('\n非高峰搭车人数:')
			f.write(str(d_od[('null','null')]))
			f.write('\n早搭晚不搭:')
			f.write(str(zdwbd))
			f.write('\n晚搭早不搭:')
			f.write(str(wdzbd))
		
		



