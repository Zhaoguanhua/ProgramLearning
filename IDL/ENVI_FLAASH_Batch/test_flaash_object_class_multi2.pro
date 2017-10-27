PRO test_flaash_object_class_multi2
  COMPILE_OPT idl2
  e=envi(/HEADLESS)

  ;获取源码所在文件
  Path = FILE_DIRNAME(ROUTINE_FILEPATH())+PATH_SEP()
  
  ;批量读取原始数据,生成辐射亮度
  ;metedata = File_Search(path, '*_MTL.txt')
  metedata = 'E:\IDL\LC08_L1TP_118030_20150803_20170406_01_T1\LC08_L1TP_118030_20150803_20170406_01_T1_MTL.txt'
  outdataBIL='E:\IDL\radioCa\rai12.dat'
  
  
  Raster  = e.OpenRaster(metedata)

  ;调用辐射校正task
  Task = ENVITask('RadiometricCalibration')
  Task.INPUT_RASTER = Raster[0]
  Task.Output_Data_Type = 'Float'
  ;Task.Output_Raster_URI = e.GetTemporaryFilename()
  Task.SCALE_FACTOR = float(0.1000000)
  Task.Output_Raster_URI = outdataBIL
  Task.Execute
  
  BSQRaster = e.OpenRaster(outdataBIL)

  fid = ENVIRasterToFID(BSQRaster)
  ENVI_FILE_QUERY, fid, DIMS=dims
  print,fid,dims
  ;转换数据存储顺序
  pos=[0,1,2,3,4,5,6]
  ENVI_DOIT, 'CONVERT_INPLACE_DOIT',DIMS=dims,FID=fid,O_INTERLEAVE= 1,POS=pos
  ;DataColl = e.Data
  
  ;DataColl.Add,Task.Output_Raster
  
  
  ;radiance_file = FILEPATH('Landsat_8_OLI_Rad.dat', $
    ;root_dir=Path, subdirectory=['data'])
   
   radiance_file = outdataBIL
  ;大气校正输出结果文件路径
  reflect_file = FILEPATH('Landsat_8_OLI_flaash.dat', $
    root_dir=Path, subdirectory=['FLAASH'])

  ;打开栅格数据，获取元数据信息
  raster = e.OpenRaster(radiance_file)
  ;raster = e.OpenRaster(Task.Output_Raster_URI)

  ;数据信息
  nspatial = raster.nColumns   ;列数
  nlines = raster.nRows        ;行数
  fid = ENVIRasterToFID(raster)
  ENVI_FILE_QUERY, fid, data_type=data_type  ;数据类型

  ;获取输入文件后缀 （.dat）
  exten = stregex(radiance_file, '\..+$', /extract)
  ;对应 Rootname for FLAASH files 参数，设置为 Landsat_8_OLI_Rad_
  user_stem_name = FILE_BASENAME(radiance_file, exten)+'_'

  ;对应 Output Directory for FLAASH Files 参数
  ;使用输出路径作为临时路径（不建议使用系统临时路径）
  modtran_directory = Path+'FLAASH'

  ;获取光谱响应函数路径
  filter_func_filename = FILEPATH('landsat8_oli.sli', $
    root_dir=e.root_dir, subdirectory=['resource','filterfuncs'])

  ;获取时间信息
  IF OBJ_VALID(raster.Time) THEN BEGIN
    ;如果元数据中有时间信息，则自动获取
    tmpTimes = STRSPLIT(raster.Time.ACQUISITION, '-T:Z', /extract)
    year = FIX(tmpTimes[0])
    month = FIX(tmpTimes[1])
    day = FIX(tmpTimes[2])
    gmt = DOUBLE(tmpTimes[3]) + $
      DOUBLE(tmpTimes[4])/60D + DOUBLE(tmpTimes[5])/60D^2
  ENDIF ELSE BEGIN
    ;如果元数据中没有，则手动设置
    year = 2013
    month = 10
    day = 3
    gmt = 2.923418
  ENDELSE

  ;坐标信息
  ref = raster.SPATIALREF
  IF ref NE !NULL THEN BEGIN
    ;如果有坐标系，则自动获取经纬度、分辨率
    pixel_size = (ref.pixel_size)[0]
    ref.ConvertFileToMap, nspatial/2, nlines/2, MapX, MapY
    ref.ConvertMapToLonLat, MapX, MapY, longitude, latitude
  ENDIF ELSE BEGIN
    ;如果没有坐标系，则手动设置
    pixel_size = 30.0
    longitude = 117.08846
    latitude = 40.506906
  ENDELSE

  ;获取波长信息
  metadata = Raster.Metadata
  wavelength_units = metadata['WAVELENGTH UNITS']
  lambda = metadata['WAVELENGTH']
  ;fwhm如果没有，可设置值全部为-1，
  ;例如4个波段的多光谱数据，设置为[-1.0, -1.0, -1.0, -1.0]
  IF metadata.HasTag('FWHM') THEN $
    fwhm = metadata['FWHM'] $
  ELSE fwhm = DBLARR(raster.nBands)-1.0
  ;缩放系数，如果定标时设置了FLAASH Setting，则设置value=1.0即可。
  input_scale = MAKE_ARRAY(raster.nbands, value=1.0, /double)

  ;初始化FLAASH对象
  ;可选关键字如下：
  ; rad_remove FLAASH执行完毕后，自动关闭输入文件
  ; anc_remove FLAASH执行完毕后，自动关闭生成的辅助数据
  ; anc_delete FLAASH执行完毕后，自动关闭并删除辅助数据
  flaash_obj = obj_new('flaash_batch', /anc_delete)

  ;设置大量的输入参数
  flaash_obj->SetProperty, $
    hyper = 0, $ ;设置为1，表示高光谱；设置为0，表示多光谱
    ;
    ; FLAASH工程参数----
    radiance_file = radiance_file, $
    reflect_file = reflect_file, $
    filter_func_filename = filter_func_filename, $
    filter_func_file_index = 0, $
    water_band_choice = 1.13, $
    red_channel = 4, $   ;0表示undefined，LC8红波段为第4波段
    green_channel = 3, $ ;0表示undefined，LC8绿波段为第3波段
    blue_channel = 2, $  ;0表示undefined，LC8蓝波段为第2波段

    ;水汽反演，没有所需波段，所以设置为0，表示undefined
    ;分别对应Multispectral Setting中Water Retrieval选项卡中的两个参数
    water_retrieval = 0, $ ;Water Retrieval参数。0表示No，1表示Yes
    water_abs_channel = 0, $
    water_ref_channel = 0, $

    ;气溶胶反演----
    ;对应Multispectral Setting中Kaufman-Tanre Aerosol Retrieval选项卡中的参数
    kt_upper_channel = 6, $ ;设置短波红外2（SWIR 2）
    kt_lower_channel = 4, $ ;设置红波段（Red）
    kt_cutoff = 0.08, $ ;Maximum Upper Channel Reflectance
    kt_ratio = 0.500, $ ;Reflectance Ratio
    cirrus_channel = 0, $  ;0表示undefined

    ;前边已经定义
    user_stem_name = user_stem_name, $
    modtran_directory = modtran_directory, $
    ;
    ; MODTRAN参数---
    visvalue = 40.0000, $ ;能见度，默认40km

    ;为了进行水汽反演，需要如下3个波段范围中的一个：
    ; 1050-1210nm, 770-870nm, 870-1020nm
    ; 而且要求此范围的波段光谱分辨率最低为15nm
    f_resolution = 15.0000, $

    ;时间信息----
    day = day, $
    month = month, $
    year = year, $
    gmt = gmt, $
    latitude = latitude, $
    longitude = longitude, $
    sensor_altitude = 705.0000, $ ;传感器高度
    ground_elevation = 0.043, $ ;平均海拔，单位km

    ;分别对应 Advanced Setting 中的同名参数，默认即可
    view_zenith_angle = 180.0000, $
    view_azimuth = 0.0000, $

    ;大气模型：0-SAW；1-MLW；2-U.S. Standard；3-SAS；4-MLS；5-T
    atmosphere_model = 4, $
    ;气溶胶模型：0-No Aerosol；1-Rural；2-Maritime；3-Urban；4-Tropospheric
    aerosol_model = 3, $

    ;如下几个参数对应 Advanced Setting同名参数，默认即可。
    multiscatter_model = 0, $
    disort_streams = 8, $
    co2mix = 390.0000, $
    water_column_multiplier = 1.0000, $
    ;
    ;图像参数----
    nspatial = nspatial, $
    nlines = nlines, $
    data_type = data_type, $
    margin1 = 0, $
    margin2 = 0, $
    nskip = 0, $
    pixel_size = pixel_size, $
    sensor_name = 'Landsat-8 OLI', $

    ;分析参数----
    ;对应Advanced Setting中的 Aerosol Scale Height
    aerosol_scaleht = 2.0000, $
    ;对应Advanced Setting中的 Use Adjacency Correction
    ;中高分辨率设置为1，低分辨率（如Modis）设置为0
    use_adjacency = 1, $

    ;输出缩放系数，输出结果放大了10000倍，变为UINT数据类型。
    ;对应Advanced Setting中的Output Reflectance Scale Factor
    output_scale = 10000.0000, $ ;输出结果缩放系数

    ;对应 Width (number of bands) 参数，多光谱设置0即可。
    polishing_res = 0, $

    ;对应 Aerosol Retrieval 参数。
    ; 0 表示 None；1 表示 2-Band (K-T)；2 表示 2-Band Over Water
    aerosol_retrieval = 1, $

    ;对应FLAASH面板中的 Wavelength Recalibration，多光谱一般为0
    calc_wl_correction = 0, $
    reuse_modtran_calcs = 0, $
    use_square_slit_function = 0, $
    convolution_method = 'fft', $

    ;对应Advanced Setting中的 Use Tiled Processing
    ;1-Yes；0-No
    use_tiling = 0, $
    tile_size = 1024.0000, $

    ; Spectral Parameters
    wavelength_units = wavelength_units, $
    lambda = lambda, $
    fwhm = fwhm, $
    input_scale = input_scale

  ;重要！！！！！！重要！！！！！！重要！！！！！
  ;执行FLAASH之前，必须在ENVI中把输入文件关闭
  Raster.Close

  ;开始执行FLAASH
  flaash_obj->processImage

  ;获取输入输出文件的FID
  flaash_obj->getResults, rad_fid=rad_fid, reflect_fid=reflect_fid
END
