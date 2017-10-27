PRO save_file
  COMPILE_OPT idl2
  
  e=ENVI()
  
  reflect_file = 'E:\test\Landsat8FLAASH\025\030\FLAASHLC08_L1GT_025030_20170828_20170828_01_RT\FLAASHLC08_L1GT_025030_20170828_20170828_01_RT.dat'
  
  Greenbandfile = file_dirname(reflect_file)+'\'+file_basename(reflect_file)+'_B3.TIFF'
  Redbandfile = file_dirname(reflect_file)+'\'+file_basename(reflect_file)+'_B4.TIFF'
  Nirbandfile = file_dirname(reflect_file)+'\'+file_basename(reflect_file)+'_B5.TIFF'
  ;print,Greenbandfile
  
  
  
  ;分别保存3、4、5波段影像
  Raster = E.OpenRaster(reflect_file)
  ;print,outRaster
  newFile = e.GetTemporaryFilename('TIFF')

  ;GreenRaster = ENVISubsetRaster(outRaster,SUB_RECT=[200,200,299,299], BANDS=1)
  ;View = e.GetView()
  ;Layer1 = view.CreateLayer(outRaster)
  ;Layer2 = view.CreateLayer(GreenRaster)
  
  origData1 = raster.GetData(BANDS=2)
  newRaster1 = ENVIRaster(origData1, URI=Greenbandfile, NBANDS=1)
  newRaster1.Save
  
  origData2 = raster.GetData(BANDS=3)
  newRaster2 = ENVIRaster(origData2, URI=Redbandfile, NBANDS=1)
  newRaster2.Save
  
  origData3 = raster.GetData(BANDS=4)
  newRaster3 = ENVIRaster(origData3, URI=Nirbandfile, NBANDS=1)
  newRaster3.Save
  
  View = e.GetView()
  layer = view.CreateLayer(newRaster1)
  layer = view.CreateLayer(newRaster2)
  layer = view.CreateLayer(newRaster3)
 
END