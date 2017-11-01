#coding=utf-8

import requests
import sys
import json
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import case_account
import restHelper
import case_common
import case_group
import case_chatroom
from time import sleep
from testdata import *

def open_richMsglist(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_more").click()

def get_richmedia_msg_buttons(driver):
	multimediabuttonlist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/image")
	# print "multimediabuttonlist lenth is: %s" %len(multimediabuttonlist)
	mylist = ['camera','image','location','video','file','voicecall','videocall','redpacket']
	mydic = dict(zip(mylist,multimediabuttonlist))	
	print mydic.keys()
	return mydic

def record_audio(driver,duration):
	case_common.long_press_by_id(driver,"com.hyphenate.chatuidemo:id/btn_press_to_speak",5000)

def send_msg_txt(driver,content):
	ret_status = False
	
	edit=driver.find_element_by_id("com.hyphenate.chatuidemo:id/et_sendmessage")
	edit.send_keys(content)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_send").click()
	sleep(3)
	mylist=driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
	print "lenth of mylist is: %s" %len(mylist)
	while mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
		sleep(3)
		mylist=driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
	if mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/bubble':
		print "txt message sent sucess!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
		print "txt message sent success and got Read ACK!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
		print "txt message sent failed!"
		ret_status = False
	
	return ret_status

def send_msg_pic(driver):
	ret_status = False

	mydic = get_richmedia_msg_buttons(driver)
	mydic['camera'].click()
	
	# 小米5手机拍照
	driver.find_element_by_id("//com.android.gallery3d:id/shutter_button").click() 
	sleep(3)
	driver.find_element_by_id("com.android.gallery3d:id/camera_switcher").click()
	
	## 夜神模拟器拍照
	# driver.find_element_by_id("com.android.camera:id/shutter_button").click()
	# sleep(3)
	# driver.find_element_by_id("com.android.camera:id/btn_done").click()
	
	#发送照片消息
	sleep(3)
	list1=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
	print "lenth of list1 is: %s" %len(list1)
	
	if len(list1) == 3:
		list2=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/android.widget.LinearLayout[@index='0']/*")
		while len(list2) == 2:
			sleep(1)
			list2=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/android.widget.LinearLayout[@index='0']/*")
		
		list1=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
		print "list1 lenth: %d" %len(list1)
		
		if len(list1) == 4:
			if list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
				print "msg sent failed!"
				case_common.back(driver)
				return ret_status
			elif list1[1].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
				print "msg sent success and got Read ACK!"
				case_common.back(driver)
				ret_status = True
		elif len(list1) == 3:
			print "msg sent success!"
			case_common.back(driver)
			ret_status = True
			
	elif len(list1) == 4:
		print list1[1].get_attribute('resourceId')
		if list1[1].get_attribute('resourceId') == 'com.hyphenate.chatuidemo:id/tv_ack':
			print "msg sent success and got Read ACK!"
			case_common.back(driver)
			ret_status = True
		elif list1[0].get_attribute('resourceId') == 'com.hyphenate.chatuidemo:id/msg_status':
			print "msg send failed!"
			case_common.back(driver)
			return
	
	return ret_status

			
def send_msg_videoRecord(driver):
	ret_status = False
	
	mydic = get_richmedia_msg_buttons(driver)
	mydic['video'].click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/video_data_area").click()
	sleep(1)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/recorder_start").click()
	sleep(5)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/recorder_stop").click()
	driver.find_element_by_name("OK").click()
	#发送视频消息
	sleep(3)
	list1=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
	print "lenth of list1 is: %s" %len(list1)
	
	if len(list1) == 3:
		list2=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/android.widget.LinearLayout[@index='0']/*")
		while len(list2) == 2:
			sleep(3)
			list2=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/android.widget.LinearLayout[@index='0']/*")
		
		list1=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
		print "list1 lenth: %d" %len(list1)
		
		if len(list1) == 4:
			if list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
				print "msg sent failed!"
				return ret_status
			elif list1[1].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
				print "msg sent success and got Read ACK!"
				ret_status = True
		elif len(list1) == 3:
			print "msg sent success!"
			ret_status = True
	
	elif len(list1) == 4:
		print list1[1].get_attribute('resourceId')
		if list1[1].get_attribute('resourceId') == 'com.hyphenate.chatuidemo:id/tv_ack':
			print "msg sent success and got Read ACK!"
			ret_status = True
		elif list1[0].get_attribute('resourceId') == 'com.hyphenate.chatuidemo:id/msg_status':
			print "msg send failed!"
			return ret_status

	return ret_status

def find_msgReadAck(driver):
	ret_status = False

	ack_el = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/tv_ack")
	if ack_el != []:
		print "Received ACK! case pass"
		ret_status = True
	elif ack_el == []:
		print "Not receive ACK! Failed!"

	return ret_status
	
def send_msg_location(driver):
	ret_status = False
	
	mydic = get_richmedia_msg_buttons(driver)
	mydic['location'].click()
	sleep(3)
	driver.find_element_by_xpath("//android.widget.Button[@text='Send']").click()
	# driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_location_send").click()
	#发送位置
	sleep(5)
	if driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/*") == []:
		print "Cannot get your logcation, please check network connection and try again latter!"
		return ret_status
	else:
		mylist=driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
		print "lenth of mylist is: %s" %len(mylist)
		while mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
			sleep(3)
			mylist=driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
		if mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/bubble':
			print " location sent sucess!"
			case_common.back(driver)
			ret_status = True
		elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
			print "location sent success and got Read ACK!"
			case_common.back(driver)
			ret_status = True
		elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
			print "location sent failed!"
			case_common.back(driver)
			return ret_status
	
	return ret_status
	
def send_msg_emoji():
	driver.find_element_by_id('com.hyphenate.chatuidemo:id/rl_face').click()
	emojiList = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/iv_expression")
	emojiList[0].click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_send").click()
	sleep(3)
	mylist=driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
	print "lenth of mylist is: %s" %len(mylist)
	while mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
		sleep(3)
		mylist=driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
	if mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/bubble':
		print "txt message sent sucess!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
		print "txt message sent success and got Read ACK!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
		print "txt message sent failed!"
		return ret_status
	
def clear_msg(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/right_image").click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_ok").click()
	
def clear_groupmsg(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/right_image").click()
	text = "clear group conversaion"
	xpath_id = "com.hyphenate.chatuidemo:id/clear_all_history"
	elem = case_common.findelem_swipe(driver,xpath_id,text)
	elem.click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_ok").click()
	driver.press_keycode(4)
	
def send_msg_audio(driver,duration):
	ret_status = False

	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_set_mode_voice").click()
	sleep(1)
	
	record_audio(driver,duration)
	# action1.release()
	sleep(3)
	# record audio
	list1 = driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
	sleep(1)
	e1 = list1[0].get_attribute("resourceId")
	print "element0 is: %s" %e1
	while list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
		sleep(1)
		list1 = driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
	if list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_length':
		print "Audio message sent success!"
		ret_status = True
	elif list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
		print "Audio message sent success and got Read ACK!"
		ret_status = True
	elif list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
		print "Audio Messaage sent failed! please retry!"
		
	return ret_status

def send_chatroomMsg_txt(driver,msgcontent):
	ret_status = False
	
	#开始发送文本消息
	edit=driver.find_element_by_id("com.hyphenate.chatuidemo:id/et_sendmessage")
	edit.send_keys(msgcontent)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_send").click()
	sleep(3)
	msglist = driver.find_elements_by_xpath("//android.widget.ListView[@index = '0']/*")
	print "msglist lenth: %s" %len(msglist)
	myindex = str(len(msglist)-1)
	mylist=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '%s']/android.widget.LinearLayout[@index = '0']/android.widget.RelativeLayout/*" %myindex)
	print "lenth of mylist is: %s" %len(mylist)
	while mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
		sleep(3)
		mylist=driver.find_elements_by_xpath("//android.widget.TextView[@text = 'chatroom test msg']/../../*")
	if mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/bubble':
		print "txt message sent sucess!"
		ret_status = True
		# driver.find_element_by_id("com.hyphenate.chatuidemo:id/left_image").click()
		# driver.find_element_by_xpath("//android.widget.ImageView[@index = '0']").click()
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_delivered':
		print " message delivered sucess!"
		case_common.back(driver)
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
		print "txt message sent failed!"
		# driver.find_element_by_id("com.hyphenate.chatuidemo:id/left_image").click()
		# driver.find_element_by_xpath("//android.widget.ImageView[@index = '0']").click()
		return
	# 发送文本消息结束
	return ret_status

def send_chatroomMsg_audio(driver):
	ret_status = False
	#加入聊天室成功后开始发送录音消息
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_set_mode_voice").click()
	record_audio(driver,5000)
	
	msglist = driver.find_elements_by_xpath("//android.widget.ListView[@index = '0']/*")
	myindex = str(len(msglist)-1)
	print "myindex: %d" %int(myindex)
	
	list1 = driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '%s']/android.widget.LinearLayout[@index = '0']/android.widget.RelativeLayout/*" %myindex)
	print "lenth of list1: %s" %len(list1)
	print list1[0].get_attribute("resourceId")
	while list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
		sleep(1)
		list1 = driver.find_elements_by_xpath("//android.widget.LinearLayout[index = myindex]/android.widget.LinearLayout[@index = '0']/android.widget.RelativeLayout[@index = '1']/*")
	if list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_length':
		print "Audio message sent success!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_delivered':
		print " message delivered sucess!"
		case_common.back(driver)
		ret_status = True
	elif list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
		print "Audio message sent success and got Read ACK!"
		ret_status = True
	elif list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
		print "Audio Messaage sent failed! please retry!"
		return
		#录音消息发送完成

	return ret_status
	
def send_chatroomMsg_location(driver):
	ret_status = False
	
	mydic = get_richmedia_msg_buttons(driver)
	
	mydic['location'].click()
	sleep(3)
	driver.find_element_by_id('com.hyphenate.chatuidemo:id/btn_location_send').click()
	#发送位置
	
	msglist = driver.find_elements_by_xpath("//android.widget.ListView[@index = '0']/*")
	myindex = str(len(msglist)-1)
	print "myindex: %d" %int(myindex)
	
	sleep(3)
	if driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/*") == []:
		print "Cannot get your logcation, please check network connection and try again latter!"
		return
	else:
		mylist=driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='%s']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout/*"%myindex)
		print "lenth of mylist is: %s" %len(mylist)
		while mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
			sleep(3)
			mylist=driver.find_elements_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*")
		if mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/bubble':
			print " message sent sucess!"
			case_common.back(driver)
			ret_status = True
		elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_delivered':
			print " message delivered sucess!"
			case_common.back(driver)
			ret_status = True
		elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
			print "message sent success and got Read ACK!"
			case_common.back(driver)
			ret_status = True
		elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
			print "message sent failed!"
			case_common.back(driver)
	
	return ret_status

def send_chatroomMsg_pic(driver):
	ret_status = False

	mydic = get_richmedia_msg_buttons(driver)
	
	mydic['camera'].click()
	# driver.find_element_by_id("com.android.gallery3d:id/shutter_button").click()
	driver.find_element_by_id("com.android.camera:id/shutter_button").click()
	sleep(3)
	# driver.find_element_by_id("com.android.gallery3d:id/camera_switcher").click()
	driver.find_element_by_id("com.android.camera:id/btn_done").click()
	#发送照片消息
	sleep(3)
	
	msglist = driver.find_elements_by_xpath("//android.widget.ListView[@index = '0']/*")
	myindex = str(len(msglist)-1)
	print "myindex: %d" %int(myindex)
	
	list1=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '%s']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*"%myindex)
	print "lenth of list1 is: %s" %len(list1)
	
	if len(list1) == 3:
		list2=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '%s']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/android.widget.LinearLayout[@index='0']/*"%myindex)
		while len(list2) == 2:
			sleep(1)
			list2=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '%s']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/android.widget.LinearLayout[@index='0']/*"%myindex)
		
		list1=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '%s']/android.widget.LinearLayout[@index='0']/android.widget.RelativeLayout[@index='1']/*"%myindex)
		print "list1 lenth: %d" %len(list1)
		
		if len(list1) == 4:
			if list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
				print "msg sent failed!"
				case_common.back(driver)
				return 
			elif list1[1].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
				print "msg sent success and got Read ACK!"
				ret_status = True
				print "back1-0"
				case_common.back(driver)
				print "back1-1"
				sleep(0.5)
		elif len(list1) == 3:
			print "msg sent success!"
			ret_status = True
			case_common.back(driver)
			sleep(0.5)
	elif len(list1) == 4:
		print list1[1].get_attribute('resourceId')
		if list1[1].get_attribute('resourceId') == 'com.hyphenate.chatuidemo:id/tv_ack':
			print "msg sent success and got Read ACK!"
			case_common.back(driver)
			ret_status = True
			sleep(0.5)
		elif list1[0].get_attribute('resourceId') == 'com.hyphenate.chatuidemo:id/msg_status':
			print "msg send failed!"
			case_common.back(driver)
			sleep(0.5)
			return
	
	return ret_status
	
def get_last_msg_content(driver,content):
	last_msg_el = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/tv_chatcontent")[-1]
	content = last_msg_el.get_attribute("text")
	return content

def get_conversation_list(driver):
	name_els= driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout/android.widget.TextView[@index='1']")
	msg_els= driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout/android.widget.TextView[@index='3']")
	
	namelist = []
	msglist = []
	for el in name_els:
		namelist.append(el.get_attribute("text"))
	print "name list:", namelist
	for el in msg_els:
		msglist.append(el.get_attribute("text"))
	print "msg list:", msglist

	mydic = dict(zip(namelist,msglist))
	print mydic
	return mydic

def check_if_receivemsg(driver,fromname,msgcontent):
	ret_status = False

	sleep(5)
	mydic = get_conversation_list(driver)
	if fromname not in mydic.keys():
		print "no conversaion from ", fromname
		return ret_status
	elif msgcontent == mydic[fromname]:
		print "receive msg success!"
		ret_status = True
	else:
		print "not receive test msg!"

	return ret_status

def click_conversation(driver,fromname):
	name_els= driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout/android.widget.TextView[@index='1']")
	
	namelist = []
	for el in name_els:
		namelist.append(el.get_attribute("text"))
	print namelist

	myindex = namelist.index(fromname)
	target_el = driver.find_element_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout[@index='%s']"%myindex)
	target_el.click()

def read_msg(driver,msgtype):
	ret_status = False

	if msgtype == "audio":
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/bubble").click()
		sleep(2)

	elif msgtype != "text":
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/bubble").click()
		sleep(2)
		driver.press_keycode(4)
	ret_status = True
	print "msg read done!"

	return ret_status
		
	
# ///////////////////////////////////////////////////////////////////////////////////////////

def test_send_msg_txt(driver,chattype,msgcontent="test msg!"):
	print "< case start: send txt msg >"
	ret_status = False
	
	if send_msg_txt(driver,msgcontent):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status
	return ret_status

def test_send_msg_location(driver,chattype):
	print "< case start: send location msg >"
	ret_status = False
	
	if send_msg_location(driver, chattype):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status
	return ret_status

def test_send_msg_pic(driver,chattype,msgcontent):

	print "< case start: send picture msg >"
	ret_status = False
	
	if send_msg_pic(driver):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status
	return ret_status

def test_send_msg_audio(driver,chattype,duration=8000):
	
	print "< case start: send audio msg >"
	ret_status = False
	
	if send_msg_audio(driver,duration):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"
	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status
	return ret_status

def test_send_chatroomMsg_txt(driver,msgcontent):
	
	print "< case start: send chatroom txt_msg >"
	ret_status = False
	
	if send_chatroomMsg_txt(driver,msgcontent):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"
	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_send_chatroomMsg_audio(driver):
	print "< case start: send chatroom audio_msg >"
	ret_status = False
	
	if send_chatroomMsg_audio(driver):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"
	
	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_rcv_msg(driver,fromname,msgcontent,msgtype,chattype):

	print "< case start: receive online msg >"

	ret_status = False

	ret_status =  check_if_receivemsg(driver,fromname,msgcontent)
	if ret_status == True:
		print "< case end: pass > "
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+msgtype+"_"+chattype] = ret_status
	return ret_status

def test_read_msg(driver,fromname,msgtype):

	print "< caes start: read msg >"
	ret_status = False
	click_conversation(driver,fromname)
	read_msg(driver,msgtype)
	ret_status = True

	if ret_status == True:
		print "< case end: pass > "
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_rcv_readAck(driver,msgtype):
	print "< case start: receive msg readAck. >"
	ret_status = find_msgReadAck(driver)
	if ret_status == True:
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+msgtype] = ret_status
	
def testset_single_chat(driver1,driver2,fromname,toname):
	print "********************************************---Single Chat---********************************************"
	chattype = "single_chat"

	case_common.gotoContact(driver1)
	case_common.click_name(driver1,toname)
	msgcontent = "test msg"
	msgtype = "text"

	clear_msg(driver1)
	
	test_send_msg_txt(driver1,chattype,msgcontent)
	print "------------------------------------------------------------------------------------------------------------------"
	test_rcv_msg(driver2,fromname,msgcontent,msgtype,chattype)
	print "------------------------------------------------------------------------------------------------------------------"
	test_read_msg(driver2,fromname,msgtype)
	print "------------------------------------------------------------------------------------------------------------------"
	clear_msg(driver2)
	case_common.back(driver2)
	test_rcv_readAck(driver1,msgtype)
	
	print "------------------------------------------------------------------------------------------------------------------"
	msgcontent = u"[语音]"
	msgtype = "audio"

	clear_msg(driver1)
	sleep(2)
	case_common.back(driver1)
	sleep(2)
	case_common.click_name(driver1,toname)
	test_send_msg_audio(driver1,chattype)
	print "------------------------------------------------------------------------------------------------------------------"
	test_rcv_msg(driver2,fromname,msgcontent,msgtype,chattype)
	print "------------------------------------------------------------------------------------------------------------------"
	test_read_msg(driver2,fromname,msgtype)
	print "------------------------------------------------------------------------------------------------------------------"
	case_common.back(driver2)
	test_rcv_readAck(driver1,msgtype)
	print "------------------------------------------------------------------------------------------------------------------"


	# print "----------------------------------------------------------------------------------------------"

	# msgcontent = "[%s location]" %fromname
	# msgtype = "location"

	# clear_msg(driver1)
	# sleep(2)
	# case_common.back(driver1)	
	# sleep(2)
	# case_common.click_name(driver1,toname)
	# sleep(1)
	# open_richMsglist(driver1)
	# test_send_msg_location(driver1,chattype)
	# test_rcv_msg(driver2,fromname,msgcontent,msgtype,chattype)
	# test_read_msg(driver2,fromname,msgtype)
	# clear_msg(driver2)
	# case_common.back(driver2)
	# find_msgReadAck(driver1)

	# print "----------------------------------------------------------------------------------------------"
	# msgcontent = "[Picture]"
	# msgtype = "Picture"

	# clear_msg(driver1)
	# sleep(2)
	# case_common.back(driver1)
	# sleep(2)
	# case_common.click_name(driver1, toname)
	# open_richMsglist(driver1)
	# test_send_msg_pic(driver1,chattype,msgcontent)
	# test_rcv_msg(driver2, fromname, msgcontent,msgtype,chattype)
	# test_read_msg(driver2, fromname, msgtype)
	# clear_msg(driver2)
	# case_common.back(driver2)
	# find_msgReadAck(driver1)

	case_common.back(driver1)
	case_common.gotoConversation(driver1)


def testset_group_chat(driver1, driver2, fromname, groupname):
	chattype = "group_chat"
	print "********************************************---Group Chat---********************************************"
	case_common.gotoContact(driver1)
	case_common.gotoGroup(driver1)
	case_group.find_group(driver1,groupname)
	case_common.click_name(driver1,groupname)
	
	print "------------------------------------------------------------------------------------------------------------------"
	msgcontent = "group test msg"
	msgtype = "text"
	clear_groupmsg(driver1)
	test_send_msg_txt(driver1,chattype,msgcontent)
	print "------------------------------------------------------------------------------------------------------------------"
	test_rcv_msg(driver2,groupname,msgcontent,msgtype,chattype)
	
	print "------------------------------------------------------------------------------------------------------------------"
	msgcontent = u"[语音]"
	msgtype = "audio"

	clear_groupmsg(driver1)
	test_send_msg_audio(driver1,chattype,msgcontent)
	print "------------------------------------------------------------------------------------------------------------------"
	test_rcv_msg(driver2,groupname,msgcontent,msgtype,chattype)	
	
	# print "-------------------------------------------------------------------------------------------------"
	# msgcontent = "[%s location]" %fromname
	# msgtype = "location"
	# case_common.gotoContact(driver1)
	# case_common.gotoGroup(driver1)
	# case_common.click_name(driver1,groupname)
	# clear_groupmsg(driver1)
	# open_richMsglist(driver1)
	# test_send_msg_location(driver1,msgcontent)
	# test_rcv_msg(driver2,groupname,msgcontent,msgtype,chattype)

	# print "-------------------------------------------------------------------------------------------------"
	# msgcontent = "[Picture]"
	# msgtype = "Picture"
	# case_common.gotoContact(driver1)
	# case_common.gotoGroup(driver1)
	# case_common.click_name(driver1,groupname)
	# clear_groupmsg(driver1)
	# open_richMsglist(driver1)
	# test_send_msg_pic(driver1,chattype,msgcontent)
	# test_rcv_msg(driver2,groupname,msgcontent,msgtype,chattype)

	
	case_common.back(driver1)
	sleep(1)
	case_common.back(driver1)
	sleep(1)
	case_common.gotoConversation(driver1)
	

# def testset_offline_msg(driver,fromname,toname,togroupid,msgnum):
# 	ret_status = False
# 	tonamelist = [toname,togroupid]
# 	if test_offline_msg(driver,fromname,tonamelist,msgnum):
# 		ret_status =True
# 		print "offline msg received successfully."
# 	else:
# 		print "offline msg not received."

# 	case_status[sys._getframe().f_code.co_name] = ret_status
	

if __name__ == "__main__":
	driver1 = case_common.startDemo1()

	case_account.test_login(driver1,"hxt001","asd")
	# case_common.gotoContact(driver1)
	# case_common.gotoGroup(driver1)
	# case_common.click_name(driver1,"coco")





