# !usr/bin/env python
# -*- coding:utf-8 -*-

import xml.dom.minidom
import numpy

XmlData = '/Users/zhaoguanhua/2017/Project/Data/AtmosphericCorrection/sentinel/15SUC/tiles/15/S/UC/2017/1/7/0/metadata.xml'
dom = xml.dom.minidom.parse(XmlData)

#读取日期
Date = dom.getElementsByTagName('SENSING_TIME')[0].firstChild.data.split('T')[0]
month = int(Date.split('-')[1])
day = int(Date.split('-')[2])


#读取太阳高度角
Sun = dom.getElementsByTagName('Mean_Sun_Angle')
ZENITHANGLE = Sun[0].getElementsByTagName('ZENITH_ANGLE')


#读取观测方位角、高度角

#View = dom.getElementsByTagName('Mean_Viewing_Incidence_Angle_List')
ViewAngles = dom.getElementsByTagName('Mean_Viewing_Incidence_Angle')

for angle in ViewAngles:
	ViewAngle = angle.getAttribute('bandId')
	if ViewAngle == '0':
		Zenith_Angle = angle.getElementsByTagName('ZENITH_ANGLE')[0].firstChild.data
		Azimuth_Angle = angle.getElementsByTagName('AZIMUTH_ANGLE')[0].firstChild.data
		print(Zenith_Angle,Azimuth_Angle)
		print(ViewAngle)
# print(ZENITHANGLE[0].getAttribute('unit'))

meter = 4300020
cilometer= meter/(2*3.1415926*6371004)*360
print(cilometer)