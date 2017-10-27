PRO test_RadiometricCalibrationTask
  COMPILE_OPT idl2
  e=envi()

  ;获取源码所在文件
  Path = FILE_DIRNAME(ROUTINE_FILEPATH())+PATH_SEP()
  
  ;批量读取原始数据,生成辐射亮度
  metedata = File_Search(path, '*_MTL.txt')
  raster  = e.OpenRaster(metedata)

  ;调用辐射校正task
  Task = ENVITask('RadiometricCalibrationTask')
  Task.INPUT_RASTER = Raster[0]
  Task.Output_Data_Type = 'Double'
  Task.OUTPUT_RASTER = Raster2
  
  Task.Execute
  
  fid = ENVIRasterToFID(Task.Output_Raster)
  ENVI_FILE_QUERY, fid, DIMS=dims
  print,fid,dims
  ;转换数据存储顺序
  pos=[0,1,2,3,4,5,6]
  ENVI_DOIT, 'CONVERT_INPLACE_DOIT',DIMS=dims,FID=fid,O_INTERLEAVE= 1,POS=pos
  
  DataColl = e.Data
  
  DataColl.Add,Task.Output_Raster
  
  e.Close
  
 END