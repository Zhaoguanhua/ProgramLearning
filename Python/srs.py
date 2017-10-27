from osgeo import ogr, osr
source = osr.SpatialReference()
source.ImportFromEPSG(4326)
target = osr.SpatialReference()
target.ImportFromEPSG(32615) 

coordTrans = osr.CoordinateTransformation(target,source)
# print(source)
# print(target)
point1,point2= coordTrans.TransformPoints([(300000,4300020),(300000,4800020)])
print(point1)
# print(x2,y2)
