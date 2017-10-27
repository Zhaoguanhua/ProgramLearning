#! usr/bin/env python
# -*- coding:utf-8 -*-
# created by zhaoguanhua 2017/9/28
# bandmath

import os
import gdal
import numpy as np

def NDVIMODIS():
	Root_outname = "/Users/zhaoguanhua/2017/Project/fuyu/MOD09Q1/NDVI"
	Root_input_path = "/Users/zhaoguanhua/2017/Project/fuyu/MOD09Q1/chuli"
	for root,dirs,RSFiles in os.walk(Root_input_path):
		print(root)
		print(dirs)
		for tifFile in RSFiles:
			if tifFile[-7:] == 'b01.tif' or tifFile[-7:] == 'b02.tif':
				if tifFile[-7:] == 'b01.tif':
					RedDataSet = gdal.Open(os.path.join(root,tifFile))
					RedBand = RedDataSet.GetRasterBand(1)
					print(RedBand)
					continue
				if tifFile[-7:] == 'b02.tif':
					NirDataSet = gdal.Open(os.path.join(root,tifFile))
					NirBand = NirDataSet.GetRasterBand(1)

				cols = RedDataSet.RasterXSize
				rows = RedDataSet.RasterYSize
				print(cols)
				RedData = RedBand.ReadAsArray(0, 0, cols, rows)
				NirData = NirBand.ReadAsArray(0,0,cols,rows)

				NDVI = np.where(RedData!=-28672,(NirData-RedData)/(NirData+RedData),-9999)

				# mulu = root.split('/')
				# print(root)
				# print(mulu)
				# os.makedirs(os.path.join(Root_outname,mulu[-3],mulu[-2],mulu[-1]))
				# outname=os.path.join(Root_outname,mulu[-3],mulu[-2],mulu[-1])

				# 拷贝地图基础信息
				driver = RedDataSet.GetDriver()

				#设置输出文件路径
				mulu = tifFile.split('.')
				outFilename=os.path.join(Root_outname,"NDVI"+mulu[0]+mulu[1]+'.tif')

				#如果文件存在就删除
				if os.path.isfile(outFilename):
				    os.remove(outFilename)

				#输出栅格数据集
				outDataset = driver.Create(outFilename, cols, rows, 1, gdal.GDT_Float32)

				# 设置投影信息，与原数据一样
				geoTransform = RedDataSet.GetGeoTransform()
				outDataset.SetGeoTransform(geoTransform)
				proj = RedDataSet.GetProjection()
				outDataset.SetProjection(proj)
				outband = outDataset.GetRasterBand(1)
				outband.SetNoDataValue(-9999)
				outband.WriteArray(NDVI, 0, 0)
				print(outFilename + 'NDVI计算完成')
				RasterData = None

def NDVI6s():
	Root_outname = "/Users/zhaoguanhua/2017/Project/fuyu/MOD09Q1/chuli/NDVI"
	Root_input_path = "/Users/zhaoguanhua/2017/Project/fuyu/MOD09Q1/chuli"
	for root,dirs,RSFiles in os.walk(Root_input_path):
		print(root)
		print(dirs)
		for tifFile in RSFiles:
			if tifFile[-6:] == 'B4.TIF' or tifFile[-6:] == 'B5.TIF':
				if tifFile[-6:] == 'B4.TIF':
					RedDataSet = gdal.Open(os.path.join(root,tifFile))
					RedBand = RedDataSet.GetRasterBand(1)
					print(RedBand)
					continue
				if tifFile[-6:] == 'B5.TIF':
					NirDataSet = gdal.Open(os.path.join(root,tifFile))
					NirBand = NirDataSet.GetRasterBand(1)

				cols = RedDataSet.RasterXSize
				rows = RedDataSet.RasterYSize
				print(cols)
				RedData = RedBand.ReadAsArray(0, 0, cols, rows)
				NirData = NirBand.ReadAsArray(0,0,cols,rows)

				NDVI = np.where(RedData!=-9999,(NirData-RedData)/(NirData+RedData),-9999)

				mulu = root.split('/')
				print(root)
				print(mulu)
				os.makedirs(os.path.join(Root_outname,mulu[-3],mulu[-2],mulu[-1]))
				outname=os.path.join(Root_outname,mulu[-3],mulu[-2],mulu[-1])

				# 拷贝地图基础信息
				driver = RedDataSet.GetDriver()

				#设置输出文件路径
				outFilename=os.path.join(outname,"NDVI"+os.path.basename(tifFile))

				#如果文件存在就删除
				if os.path.isfile(outFilename):
				    os.remove(outFilename)

				#输出栅格数据集
				outDataset = driver.Create(outFilename, cols, rows, 1, gdal.GDT_Float32)

				# 设置投影信息，与原数据一样
				geoTransform = RedDataSet.GetGeoTransform()
				outDataset.SetGeoTransform(geoTransform)
				proj = RedDataSet.GetProjection()
				outDataset.SetProjection(proj)
				outband = outDataset.GetRasterBand(1)
				outband.SetNoDataValue(-9999)
				outband.WriteArray(NDVI, 0, 0)
				print(outFilename + 'NDVI6S计算完成')
				RasterData = None

def NDVIFLAASH():
	Root_outname = "/Users/zhaoguanhua/2017/Project/Data/AtmosphericCorrection/NDVI"
	Root_input_path = "/Users/zhaoguanhua/2017/Project/Data/AtmosphericCorrection/LC08/Landsat/Landsat8FLAASH"
	print(Root_input_path)
	for root,dirs,RSFiles in os.walk(Root_input_path):
		print(root)
		print(dirs)
		for tifFile in RSFiles:
			print(tifFile[-4:])
			if tifFile[-4:] == '.dat':
				IDataSet = gdal.Open(os.path.join(root,tifFile))
				RedBand = IDataSet.GetRasterBand(4)
				NirBand = IDataSet.GetRasterBand(5)


				cols = IDataSet.RasterXSize
				rows = IDataSet.RasterYSize
				print(cols)
				RedData = RedBand.ReadAsArray(0, 0, cols, rows)
				NirData = NirBand.ReadAsArray(0,0,cols,rows)

				NDVI = np.where(RedData!=0,(NirData-RedData)/(NirData+RedData),-9999)

				mulu = root.split('/')
				outname=os.path.join(Root_outname,mulu[-3],mulu[-2],mulu[-1][6:])

				# 拷贝地图基础信息
				driver = IDataSet.GetDriver()

				#设置输出文件路径
				outFilename=os.path.join(outname,"NDVI"+os.path.basename(tifFile)[:-4]+'.TIF')

				#如果文件存在就删除
				if os.path.isfile(outFilename):
				    os.remove(outFilename)

				#输出栅格数据集
				outDataset = driver.Create(outFilename, cols, rows, 1, gdal.GDT_Float32)

				# 设置投影信息，与原数据一样
				geoTransform = IDataSet.GetGeoTransform()
				outDataset.SetGeoTransform(geoTransform)
				proj = IDataSet.GetProjection()
				outDataset.SetProjection(proj)
				outband = outDataset.GetRasterBand(1)
				outband.SetNoDataValue(-9999)
				outband.WriteArray(NDVI, 0, 0)
				print(outFilename + 'NDVIFLAASH计算完成')
				RasterData = None

def Subtraction():
	Root_input_path = "/Users/zhaoguanhua/2017/Project/Data/AtmosphericCorrection/NDVI"
	Root_output_path = "/Users/zhaoguanhua/2017/Project/Data/AtmosphericCorrection/DifferenceNDVI"
	for root,dirs,NDVIfiles in os.walk(Root_input_path):
		if dirs:
			pass
		else:
			for NDVIfile in NDVIfiles:
				if NDVIfile[:6] == 'NDVI6s'and NDVIfile[-4:] == '.TIF':
					sixsNDVIfile = NDVIfile

				if NDVIfile[:6] == 'NDVIFL'and NDVIfile[-4:] == '.TIF':
					FLAASHNDVIfile = NDVIfile

			print(sixsNDVIfile)
			sixsIDataSet = gdal.Open(os.path.join(root,sixsNDVIfile))
			sixsNDVIband = sixsIDataSet.GetRasterBand(1)
			print(FLAASHNDVIfile)
			FLAASHIDataSet = gdal.Open(os.path.join(root,FLAASHNDVIfile))
			FLAASHNDVIband = FLAASHIDataSet.GetRasterBand(1)

			cols = sixsIDataSet.RasterXSize
			rows = sixsIDataSet.RasterYSize

			sixsNDVIData = sixsNDVIband.ReadAsArray(0, 0, cols, rows)
			FLAASHNDVIData = FLAASHNDVIband.ReadAsArray(0, 0, cols, rows)

			DifferenceNDVI = np.where(sixsNDVIData!=-9999,sixsNDVIData-FLAASHNDVIData,-9999)

			Driver = sixsIDataSet.GetDriver()

			outfilename = os.path.join(Root_output_path,'DifferenceNDVI'+sixsNDVIfile[6:])

			outDataset =Driver.Create(outfilename,cols,rows,1,gdal.GDT_Float32)

			geoTransform = sixsIDataSet.GetGeoTransform()
			outDataset.SetGeoTransform(geoTransform)
			proj = sixsIDataSet.GetProjection()
			outDataset.SetProjection(proj)

			outband = outDataset.GetRasterBand(1)
			outband.SetNoDataValue(-9999)
			outband.WriteArray(DifferenceNDVI,0,0)
			print('NDVI差值完成')

if __name__ == '__main__':
	NDVIMODIS()
	#NDVI6s()
	#NDVIFLAASH()
	#Subtraction()
