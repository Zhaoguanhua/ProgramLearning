#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-13 10:06:28
# @Author  : zhaoguanhua
# @Email   : zhaoguanhua@gagogroup.com

import gdal
import os
import numpy as np 

def ReadHDF1():

	#设置输入文件路径、输出文件路径
	TMFilePath = "/Users/zhaoguanhua/2017/Project/Data/ATO550"
	outFilePath = "/Users/zhaoguanhua/2017/Project/Data/AC"

	for root,dirs,Files in os.walk(TMFilePath):

		AOTlist = []

		for file in Files:
			if file[-4:] == ".hdf":
				inputfile = os.path.join(root,file)
				outname = os.path.join(root,"aot"+file[:-4]+".tif")
				os.system("""gdalwarp -geoloc -t_srs EPSG:4326 HDF4_EOS:EOS_SWATH:"%s":mod04:Optical_Depth_Land_And_Ocean %s""" %(inputfile,outname))
				AOTlist.append(outname)

		if len(AOTlist) > 0:
			outname2 = " ".join(AOTlist)
			outnamesplit = root.split('/')
			#创建以年份命名的文件夹，存在合成的每天全国气溶胶数据
			try:
				os.mkdir(os.path.join(outFilePath,outnamesplit[-3])) #-3:分割后的年份
			except Exception as e:
				pass

			outnameMerge1 = os.path.join(outFilePath,outnamesplit[-3],"ATO"+outnamesplit[-2]+".tif") #-2:分割后的天数，一年的第几天
			os.system("""gdalwarp %s %s -srcnodata -9999 -dstnodata -9999""" %(outname2,outnameMerge1))

def ReadHDF2():
	ds = gdal.Open('MOD04_L2.A2011232.0215.006.2015054122726.hdf')
	print(ds)
	# print(ds.GetSubDatasets())

	# get the path for a specific subdataset
	subds = [sd for sd, descr in ds.GetSubDatasets() if descr.endswith('Solar_Azimuth mod04 (16-bit integer)')][0]

	# open and read it like normal
	dssub = gdal.Open(subds)
	data = dssub.ReadAsArray()
	dssub = None

	ds = None
	pass

if __name__ == '__main__':
	ReadHDF1()





