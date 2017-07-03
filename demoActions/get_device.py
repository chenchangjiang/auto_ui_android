#coding=utf-8
import os
import re

def get_devicelist():
	patt = "\n(.+)\tdevice"
	text = os.popen("adb devices").read()
	devicelist = re.findall(patt,text)
	if devicelist == []:
		print "No device detected!\nplease check the connect!"

	return devicelist
	
def get_deviceinfo():
	mydic = {}
	patt = "\d\.\d[\.\d]?"
	dlist = get_devicelist()
	vlist = []
	for name in dlist:
		text = os.popen("adb -s %s shell getprop ro.build.version.release"%name).read()#获取系统版本
		cmd_api = os.popen('adb -s %s shell getprop ro.build.version.sdk'%name).read()# 获取系统api版本
		version = re.findall(patt,text)[0]
		mydic[name] = version

	return mydic
	
if __name__=="__main__":
	vlist = get_deviceinfo()
	
	print "mydic:"
	print vlist

	

