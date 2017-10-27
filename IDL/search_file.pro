PRO search_file
  COMPILE_OPT idl2
  
  ;获取源码所在文件
  Root_inputfile_path = 'E:\Landsat8'
  Root_outputfile_path = 'E:\IDL\landsat8FLAASH'
  
  r=file_search(Root_inputfile_path,'*_MTL.txt',count=num,/test_regular)
  
  FOREACH file,r,i DO BEGIN
    print,i,'--',file
    b=strsplit(file_dirname(file),'\',ESCAPE='.txt',/extract)
    
    outfilepath = strjoin(['E:\IDL\landsat8FLAASH',b[-3],b[-2],b[-1]],'\')
    print,outfilepath
    
    file_mkdir,outfilepath
    
    outfile = outfilepath+'\'+strmid(file_basename(file),0,40)
    print,outfile
    
    
  ENDFOREACH
  
  
  
END