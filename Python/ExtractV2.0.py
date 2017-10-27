# -*- coding: UTF-8 -*-
#create by zhaoguanhua on 2017/5/11
# -*- coding: UTF-8 -*-

import os,sys
import glob
# import geojson
import gdal


def Extract(mask,file):
	maskname = os.path.basename(mask)
	OutputFile = maskname[:-4]+os.path.basename(file)
	strCmd = "gdalwarp --config GDALWARP_IGNORE_BAD_CUTLINE YES -cutline" +' '+ str(mask)+' '+ "-crop_to_cutline"+' '+ str(file)+' '+ OutputFile
	#print "裁剪成功"
	os.system(strCmd)


if __name__ == '__main__':
	#获取所有的栅格图像
	files = glob.glob(os.getcwd()+"/*.tif")
	#获取矢量边界
	mask = "/Users/zhaoguanhua/2017/Project/fuyu/fuyu/fuyu.shp"
	for file in files:
		#print file
		Extract(mask,file)

