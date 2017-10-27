# usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import xlwt
import os
import scipy.interpolate as itp
import matplotlib.pyplot as plt
import numpy as np
import json

def function(outImage):
	y = a * outImage - b
	atcImage = y / (1 + y * c)
	print(atcImage)

if __name__ == '__main__':
	fname = "lansat8SRF.xlsx"
	# print(fname)
	bk = xlrd.open_workbook(fname)
	shxrange=range(bk.nsheets)
	try:
		sh = bk.sheet_by_name("Sheet1")
	except:
		print("no sheet in %s named Sheet1" % fname)

	nrows = sh.nrows
	ncols = sh.ncols

	readdata = np.zeros((nrows,ncols))
	row_list=[]

	for i in range(0,nrows):
		row_data = sh.row_values(i)
		# print(type(row_data[1]))
		readdata[i,:]=row_data

	x = list(readdata[:,0]*1000)
	y1=list(readdata[:,1])
	y2=list(readdata[:,2])
	y3=list(readdata[:,3])
	y4=list(readdata[:,4])
	xnew=np.arange(420,2000,2.5)

	yinterp1 = itp.spline(x,y1,xnew)#调用样条插值函数
	plot1=plt.plot(x, y1, 'b*',label='original values')	
	plot12=plt.plot(xnew, yinterp1, 'r-x',label='interped values')

	yinterp2 = itp.spline(x,y2,xnew)#调用样条插值函数
	plot21=plt.plot(x, y2, 'g*',label='original values')	
	plot22=plt.plot(xnew, yinterp2, 'r-x',label='interped values')

	yinterp3 = itp.spline(x,y3,xnew)#调用样条插值函数
	plot31=plt.plot(x, y3, 'r*',label='original values')	
	plot32=plt.plot(xnew, yinterp3, 'r-x',label='interped values')

	yinterp4 = itp.spline(x,y4,xnew)#调用样条插值函数
	plot41=plt.plot(x, y4, 'c*',label='original values')	
	plot42=plt.plot(xnew, yinterp4, 'r-x',label='interped values')
	plt.xlabel('x axis')
	plt.ylabel('y axis')
	plt.legend()
	plt.show()
	plt.title('Spline')
	plt.savefig('c4.png')	
	#保存在当前目录文件夹


	#将插值结果写入excel
	wb = xlwt.Workbook()
	sheet = wb.add_sheet('sheet')
	row = len(xnew)
	inter = np.zeros((row,5))
	inter[:,0]=xnew
	inter[:,1]=yinterp1
	inter[:,2]=yinterp2
	inter[:,3]=yinterp3
	inter[:,4]=yinterp4

	for i in range(row):
		for j in range(0,5):
			sheet.write(i,j,inter[i,j])

	wb.save("Landsat8.xls")

	# jsonname="RadiometricCorrectionParameter.json"
	# config = json.load(open(jsonname))
	# band1 = []
	# band2 =[]
	# band3 =[]
	# band4 =[]
	# for i in range(row):
	# 	if inter[i][0]>=450 and inter[i][0]<=520:
	# 		band1.append(inter[i][1])
	# 	if inter[i][0]>=520 and inter[i][0]<=590:
	# 		band2.append(inter[i][2])
	# 	elif inter[i][0]>=630 and inter[i][0]<=690:
	# 		band3.append(inter[i][3])
	# 	elif inter[i][0]>=770 and inter[i][0]<=890:
	# 		band4.append(inter[i][4])

	# SensorID="WFV4"
	# newdir ={}
	# newdir['1']=band1
	# newdir['2']=band2
	# newdir['3']=band3
	# newdir['4']=band4
	# config['Parameter']['GF1'][SensorID]['SRF']=newdir


	# datastring =json.dumps(config,indent=4)
	# with open(jsonname, "w") as f3:
	# 	f3.write(datastring)











