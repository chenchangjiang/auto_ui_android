#coding=utf-8

import requests
import sys
import json
import random
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
	mylist = ['camera', 'image', 'location', 'video', 'file', 'voicecall', 'videocall', 'redpacket']
	mydic = dict(zip(mylist, multimediabuttonlist))	
	print mydic.keys()
	return mydic

def record_audio(driver, duration):
	case_common.long_press_by_id(driver, "com.hyphenate.chatuidemo:id/btn_press_to_speak", duration)

def send_msg_txt(driver, content):
	ret_status = False
	
	edit=driver.find_element_by_id("com.hyphenate.chatuidemo:id/et_sendmessage")
	edit.send_keys(content)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_send").click()
	sleep(1)
	
	mylist = driver.find_elements_by_xpath("//android.widget.ListView/android.widget.LinearLayout")
	send_index = len(mylist)-1
	print "send_index", send_index

	mylist = driver.find_elements_by_xpath("//android.widget.ListView/android.widget.LinearLayout[@index='%s']/android.widget.LinearLayout/android.widget.RelativeLayout/*" %send_index)
	while mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
		mylist=driver.find_elements_by_xpath("//android.widget.ListView/android.widget.LinearLayout[@index='%s']/android.widget.LinearLayout/android.widget.RelativeLayout/*" %send_index)
	if mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/bubble':
		print "txt message sent sucess!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
		print "txt message sent success and got Read ACK!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
		print "txt message sent failed!"
	
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

	ack_elems = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/tv_ack")
	if ack_elems != []:
		print "Received ACK! case pass"
		ret_status = True
	else:
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
	elem = case_common.findelem_swipe(driver, xpath_id, text)
	elem.click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_ok").click()
	driver.press_keycode(4)
	
def send_msg_audio(driver, duration):
	ret_status = False

	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_set_mode_voice").click()
	sleep(1)
	record_audio(driver, duration)
	sleep(1)
	
	list1 = driver.find_elements_by_xpath("//android.widget.ListView/android.widget.LinearLayout")
	send_index = len(list1)-1
	print "send index:", send_index
	
	list1 = driver.find_elements_by_xpath("//android.widget.ListView/android.widget.LinearLayout[@index='%s']/android.widget.LinearLayout/android.widget.RelativeLayout/*" %send_index)
	try:
		while list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
			list1 = driver.find_elements_by_xpath("//android.widget.ListView/android.widget.LinearLayout[@index='%s']/android.widget.LinearLayout/android.widget.RelativeLayout/*" %send_index)
		if list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_length':
			print "Audio message sent success!"
			ret_status = True
		elif list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_ack':
			print "Audio message sent success and got Read ACK!"
			ret_status = True
		elif list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
			print "Audio Messaage sent failed! please retry!"
	except:
		print "audio not send at all."	
	
	return ret_status

def send_chatroommsg_txt(driver, msgcontent):
	ret_status = False
	
	edit=driver.find_element_by_id("com.hyphenate.chatuidemo:id/et_sendmessage")
	edit.send_keys(msgcontent)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_send").click()
	sleep(3)
	
	msglist = driver.find_elements_by_xpath("//android.widget.ListView[@index = '0']/*")
	myindex = str(len(msglist)-1)
	mylist=driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '%s']/android.widget.LinearLayout[@index = '0']/android.widget.RelativeLayout/*" %myindex)
	print mylist[0].get_attribute("resourceId")
	while mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
		sleep(3)
		mylist=driver.find_elements_by_xpath("//android.widget.TextView[@text = 'chatroom test msg']/../../*")
	if mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/bubble':
		print "txt message sent sucess!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_delivered':
		print " message delivered sucess!"
		ret_status = True
	elif mylist[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/msg_status':
		print "txt message sent failed!"
		return
	# 发送文本消息结束
	return ret_status

def send_chatroommsg_audio(driver):
	ret_status = False
	#加入聊天室成功后开始发送录音消息
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_set_mode_voice").click()
	record_audio(driver, 3000)
	
	msglist = driver.find_elements_by_xpath("//android.widget.ListView[@index = '0']/*")
	myindex = str(len(msglist)-1)
	list1 = driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '%s']/android.widget.LinearLayout[@index = '0']/android.widget.RelativeLayout/*" %myindex)
	print list1[0].get_attribute("resourceId")
	while list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/progress_bar':
		sleep(1)
		list1 = driver.find_elements_by_xpath("//android.widget.LinearLayout[index = myindex]/android.widget.LinearLayout[@index = '0']/android.widget.RelativeLayout[@index = '1']/*")
	if list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_length':
		print "Audio message sent success!"
		ret_status = True
	elif list1[0].get_attribute("resourceId") == 'com.hyphenate.chatuidemo:id/tv_delivered':
		print " message delivered sucess!"
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
	
def get_last_msg_content(driver, content):
	last_msg_elems = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/tv_chatcontent")[-1]
	content = last_msg_elems.get_attribute("text")
	return content

def get_conversation_list(driver):
	name_elems= driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout/android.widget.TextView[@index='1']")
	msg_elems= driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout/android.widget.TextView[@index='3']")
	
	namelist = []
	msglist = []
	for elem in name_elems:
		namelist.append(elem.get_attribute("text"))
	for elem in msg_elems:
		msglist.append(elem.get_attribute("text"))

	mydic = dict(zip(namelist, msglist))
	print mydic
	return mydic

def check_if_receivemsg(driver, fromname, msgcontent):
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

def click_conversation(driver, fromname):
	name_elems= driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout/android.widget.TextView[@index='1']")
	
	namelist = []
	for el in name_elems:
		namelist.append(el.get_attribute("text"))

	myindex = namelist.index(fromname)
	target_elem = driver.find_element_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout[@index='%s']"%myindex)
	target_elem.click()

def read_msg(driver, msgtype):
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

def recall_message(driver1, driver2, fromname, msgcontent):
	ret_status = False

	case_common.long_click(driver1, msgcontent)
	driver1.find_element_by_id("com.hyphenate.chatuidemo:id/recall").click()
	sleep(1)

	xpath_id = "//android.widget.TextView[@text='This message has been recalled by %s']" %fromname
	if case_common.findelem(driver2, xpath_id, "by_xpath"):
		print "message recall succssful."
		ret_status = True
	else:
		print "message recall fail."

	return ret_status

def message_roaming(driver, msgcontent1, msgcontent2):
	ret_status = False

	case_common.swipeDown(driver)
	sleep(5)
	xpath_id1 = "//android.widget.TextView[@text='%s']" %msgcontent1
	xpath_id2 = "//android.widget.TextView[@text='%s']" %msgcontent2
	find_type = "by_xpath"

	if case_common.findelem(driver, xpath_id1, find_type) and case_common.findelem(driver, xpath_id2, find_type):
		print "find roaming message."
		ret_status = True
	else:
		print "not find roaming message."

	return ret_status

def kick_by_other(driver):
	ret_status = False

	try:
		driver.find_element_by_xpath("//android.widget.TextView[@text='The same account was loggedin in other device']")
		print "kicked by other device, appkey support multi device."
		ret_status = True
	except:
		print "not kicked by other device, appkey support multi device."
	else:
		driver.find_element_by_xpath("//android.widget.Button[@text='OK']").click()

	return ret_status
	
# ///////////////////////////////////////////////////////////////////////////////////////////

def test_send_msg_txt(driver, chattype, msgcontent="test msg!"):
	print "< case start: send txt msg >"
	ret_status = False
	
	if send_msg_txt(driver, msgcontent):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status
	return ret_status

def test_send_msg_location(driver, chattype):
	print "< case start: send location msg >"
	ret_status = False
	
	if send_msg_location(driver, chattype):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status
	return ret_status

def test_send_msg_pic(driver, chattype, msgcontent):
	print "< case start: send picture msg >"
	ret_status = False
	
	if send_msg_pic(driver):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status
	return ret_status

def test_send_msg_audio(driver, chattype, duration=3000):
	print "< case start: send audio msg >"
	ret_status = False
	
	if send_msg_audio(driver, duration):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"
	
	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status
	return ret_status

def test_send_chatroommsg_txt(driver, msgcontent):
	print "< case start: send chatroom txt_msg >"
	ret_status = False
	
	if send_chatroommsg_txt(driver, msgcontent):
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"
	
	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_send_chatroommsg_audio(driver):
	print "< case start: send chatroom audio_msg >"
	ret_status = False
	
	if send_chatroommsg_audio(driver):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"
	
	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_rcv_chatroommsg_txt(driver, msgcontent):
	print "< case start: receive chatroom msg >"
	ret_status = False

	xpath_id = "//android.widget.TextView[@text='%s']" %msgcontent
	if case_common.findelem(driver, xpath_id, find_type="by_xpath"):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"
	case_chatroom.leave_a_chatroom(driver)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_rcv_msg(driver, fromname, msgcontent, msgtype, chattype):
	print "< case start: receive online msg >"
	ret_status = False

	ret_status =  check_if_receivemsg(driver, fromname, msgcontent)
	if ret_status == True:
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+msgtype+"_"+chattype] = ret_status
	return ret_status

def test_read_msg(driver, fromname, msgtype):
	print "< caes start: read msg >"
	ret_status = False
	
	click_conversation(driver, fromname)
	read_msg(driver, msgtype)
	ret_status = True

	if ret_status == True:
		print "< case end: pass > "
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_rcv_readAck(driver, msgtype):
	print "< case start: receive msg readAck. >"
	ret_status = find_msgReadAck(driver)
	
	if ret_status == True:
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+msgtype] = ret_status
	
def test_recall_message(driver1, driver2, fromname, msgcontent, chattype):
	print "< case start: recall message. >"
	ret_status = False

	if recall_message(driver1, driver2, fromname, msgcontent):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status

def test_roaming_message(driver, msgcontent1, msgcontent2, chattype):
	print "< case start: message roaming. >"
	ret_status = False

	if message_roaming(driver, msgcontent1, msgcontent2):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status

def test_multidev_rcv(driver1, driver2, fromname, msgcontent, msgtype, chattype):
	print "< case start: multi devices receive %s >" %chattype
	ret_status = False

	if test_rcv_msg(driver1, fromname, msgcontent, msgtype, chattype) and test_rcv_msg(driver2, fromname, msgcontent, msgtype, chattype):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status

def test_multidev_send(driver, fromname, msgcontent, msgtype, chattype):
	print "< case start: multi devices send %s >" %chattype
	ret_status = False

	if test_rcv_msg(driver, fromname, msgcontent, msgtype, chattype):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name+"_"+chattype] = ret_status


def testset_single_chat(driver1, driver2, fromname, toname):
	print "********************************************---Single Chat---********************************************"
	chattype = "single_chat"

	case_common.gotoContact(driver1)
	case_common.click_name(driver1, toname)
	clear_msg(driver1)
	msgcontent = case_common.random_str(8)
	msgtype = "text"
		
	if test_send_msg_txt(driver1, chattype, msgcontent):
		print "------------------------------------------------------------------------------------------------------------------"
		test_rcv_msg(driver2, fromname, msgcontent, msgtype, chattype)
		print "------------------------------------------------------------------------------------------------------------------"
		test_read_msg(driver2, fromname, msgtype)
		print "------------------------------------------------------------------------------------------------------------------"
		test_rcv_readAck(driver1, msgtype)
		print "------------------------------------------------------------------------------------------------------------------"
		test_recall_message(driver1, driver2, fromname, msgcontent, chattype)
		clear_msg(driver2)
		case_common.back(driver2)
		print "------------------------------------------------------------------------------------------------------------------"
	msgcontent = u"[语音]"
	msgtype = "audio"

	clear_msg(driver1)
	sleep(2)
	case_common.back(driver1)
	sleep(2)
	case_common.click_name(driver1, toname)
	if test_send_msg_audio(driver1, chattype):
		print "------------------------------------------------------------------------------------------------------------------"
		test_rcv_msg(driver2, fromname, msgcontent, msgtype, chattype)
		print "------------------------------------------------------------------------------------------------------------------"
		test_read_msg(driver2, fromname, msgtype)
		print "------------------------------------------------------------------------------------------------------------------"
		case_common.back(driver2)
		test_rcv_readAck(driver1, msgtype)
		print "------------------------------------------------------------------------------------------------------------------"

	case_common.switch_messageroaming(driver2)
	msgcontent1 = case_common.random_str(8)
	msgcontent2 = case_common.random_str(8)
	case_common.mode_keyboard(driver1)
	
	if send_msg_txt(driver1, msgcontent1) and send_msg_txt(driver1, msgcontent2):
		click_conversation(driver2, fromname)
		clear_msg(driver2)
		test_roaming_message(driver2, msgcontent1, msgcontent2, chattype)
		case_common.back(driver2)

	case_common.switch_messageroaming(driver2)
	case_common.back(driver1)
	case_common.gotoConversation(driver1)

def testset_group_chat(driver1, driver2, fromname, groupname):
	chattype = "group_chat"
	print "********************************************---Group Chat---********************************************"
	case_common.gotoContact(driver1)
	case_common.gotoGroup(driver1)
	case_group.find_group(driver1, groupname)
	case_common.click_name(driver1, groupname)
	
	print "------------------------------------------------------------------------------------------------------------------"
	msgcontent = case_common.random_str(8)
	msgtype = "text"
	clear_groupmsg(driver1)
	if test_send_msg_txt(driver1, chattype, msgcontent):
		print "------------------------------------------------------------------------------------------------------------------"
		test_rcv_msg(driver2, groupname, msgcontent, msgtype, chattype)
		print "------------------------------------------------------------------------------------------------------------------"
		case_common.click_name(driver2, groupname)
		test_recall_message(driver1, driver2, fromname, msgcontent, chattype)
		case_common.back(driver2)	
	print "------------------------------------------------------------------------------------------------------------------"
	msgcontent = u"[语音]"
	msgtype = "audio"

	clear_groupmsg(driver1)
	if test_send_msg_audio(driver1, chattype):
		print "------------------------------------------------------------------------------------------------------------------"
		test_rcv_msg(driver2, groupname, msgcontent, msgtype, chattype)
		print "------------------------------------------------------------------------------------------------------------------"

	case_common.switch_messageroaming(driver2)
	msgcontent1 = case_common.random_str(8)
	msgcontent2 = case_common.random_str(8)
	case_common.mode_keyboard(driver1)

	if test_send_msg_txt(driver1, chattype, msgcontent1) and test_send_msg_txt(driver1, chattype, msgcontent2):
		click_conversation(driver2, groupname)
		clear_groupmsg(driver2)
		sleep(2)
		case_common.swipeUp(driver2)
		print "------------------------------------------------------------------------------------------------------------------"
		test_roaming_message(driver2, msgcontent1, msgcontent2, chattype)
		case_common.back(driver2)
	
	case_common.switch_messageroaming(driver2)
	case_common.back(driver1)
	sleep(1)
	case_common.back(driver1)
	sleep(1)
	case_common.gotoConversation(driver1)

def multi_devices_chat(driver1, driver2, fromname, toname, groupname):
	print "********************************************---Multi devices Chat---********************************************"
	chattype = "single_chat"
	msgtype = "text"
	msgnum = 1
	groupid = restHelper.get_groupid(fromname, groupname)
	case_account.switch_user(driver2, fromname)
	
	if not kick_by_other(driver1):

		case_common.del_conversation(driver2)

		restHelper.sendmsg(fromname, "rest", msgnum, msgtype='users')
		print "------------------------------------------------------------------------------------------------------------------"
		test_multidev_rcv(driver1, driver2, "rest", "testmsg0", msgtype, chattype)

		chattype = "group_chat"
		restHelper.sendmsg(groupid, "rest", msgnum, msgtype="chatgroups")
		print "------------------------------------------------------------------------------------------------------------------"
		test_multidev_rcv(driver1, driver2, "rest", "testmsg0", msgtype, chattype)

		case_common.gotoContact(driver1)
		case_common.click_name(driver1, toname)
		msgcontent = case_common.random_str(8)
		chattype = "single_chat"
		msgtype = "text"

		if test_send_msg_txt(driver1, chattype, msgcontent):
			print "------------------------------------------------------------------------------------------------------------------"
			test_multidev_send(driver2, toname, msgcontent, msgtype, chattype)
			print "------------------------------------------------------------------------------------------------------------------"

		case_common.back(driver1)
		case_common.gotoGroup(driver1)
		case_group.find_group(driver1, groupname)
		case_common.click_name(driver1, groupname)
		chattype = "group_chat"
		msgcontent = case_common.random_str(8)

		if test_send_msg_txt(driver1, chattype, msgcontent):
			test_multidev_send(driver2, groupname, msgcontent, msgtype, chattype)

		case_common.back(driver1)
		sleep(1)
		case_common.back(driver1)
		sleep(1)
		case_common.gotoConversation(driver1)
		case_account.switch_user(driver2, toname)
	else:
		case_account.switch_user(driver2, toname)
		case_account.test_login(driver1, fromname, password="1")

if __name__ == "__main__":
	device_list = case_common.device_info()

	# case_common.clearAppdata(device_list[0])
	# case_common.clearAppdata(device_list[2])
	case_common.setappiumimput(device_list[0])
	case_common.setappiumimput(device_list[2])

	driver1 = case_common.startDemo(device_list[0], device_list[1], "4723")
	driver2 = case_common.startDemo(device_list[2], device_list[3], "4725")
	case_account.test_login(driver1, "bob011", "1")
	case_account.test_login(driver2, "bob022", "1")

	testset_single_chat(driver1, driver2, "bob011", "bob022")

	testset_group_chat(driver1, driver2, "bob011", "GK1")

	multi_devices_chat(driver1, driver2, "bob011", "bob022", "GK1")




