#coding=utf-8
import time
import sys
import requests
import json
import case_account
import case_common
import restHelper
import case_chat
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from testdata import *

def create_chatroom(driver,roomname):
	ret_status = False
	
	els = driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/android.widget.RelativeLayout")
	els[0].click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/edit_chat_room_name").sendkeys(roomname)
	driver.find_element_by_xpath("//android.widget.Button").click()
	ret_status = True
	
	return ret_status
	
def get_chatroomlist(driver):
	ret_status = False

	mylist = driver.find_elements_by_xpath("//android.widget.ListView/*")
	if mylist == []:
		print """No chatroom got!
please check your network and refresh chatroomlist again!"""
		driver.find_element_by_xpath("//android.widget.ImageView").click()
		return
	elif mylist != []:
		print "refresh chatroomlist successfully!"
		ret_status = True

	return ret_status

def join_chatroom(driver,roomname):
	driver.find_element_by_xpath("//android.widget.TextView[@text='%s']" %roomname).click()
	time.sleep(3)
	
def join_sucess(roomname,testaccount):
	ret_status = False

	roomid = restHelper.get_roomid(roomname)
	mylist = restHelper.get_roommember(roomid)

	if testaccount in mylist:
		print "join chatroom %s success!" %roomid
		ret_status=True

	else:
		print "join chatroom %s failed!" %roomid
		
	return ret_status

def leave_chatroom(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/left_layout").click()
	time.sleep(3)

def leave_sucess(testaccount,roomname):
	ret_status = False

	roomid = restHelper.get_roomid(roomname)
	mylist = restHelper.get_roommember(roomid)
	time.sleep(3)
	if testaccount not in mylist:
		print "Leave chatrrom %s success!" %roomid
		ret_status = True

	elif testaccount in mylist:
		print "leave chatroom %s failed!" %roomid

	return ret_status

def get_10_historymsg(driver):
	ret_status = False

	case_common.swipeDown(driver)
	msglist1 = case_common.historymsg_on_screen(driver)
	case_common.swipeUp(driver)
	msglist2 = case_common.historymsg_on_screen(driver)
	
	msglist = []
	for i in msglist1:
		msglist.append(i)

	for i in msglist2:
		if i not in msglist:
			msglist.append(i)

	for i in msglist:
		print "txt msg: %s" %i
	
	print "txt msg count: %s" %(len(msglist))
	if len(msglist) >= 10:
		print "10 history msg got success!"
		ret_status = True
		# driver.press_keycode(4)#退出聊天室
		# driver.find_element_by_xpath("//android.widget.ImageView").click()
	elif len(msglist)<10:
		print"""10 history msg got failed!
Or this room has less than 10 history msg, please check and retry again!"""

	return ret_status

def get_first_roomname(driver):
	els = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")
	roomname = els[1].get_attribute("text")
	return roomname

# ///////////////////////////////////////////

def test_get_chatroomlist(driver):
	ret_status = False

	print "------------------------------------------------------------------------------------------------------------------"
	print "<case start: get_chatroomlist >"
	case_common.gotoContact(driver)
	case_common.gotoChatroomlist(driver)

	roomlist = driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/*") # 获取聊天室列表条目
	if len(roomlist) > 0:
		print "get chatroomlist success!"
		print "< case end: pass. >"
		ret_status = True
	else:
		print "get chatroomlist failed!"
		print "< case end: failed. >!"
		ret_status = False

		case_common.back(driver)
		case_common.gotoConversation(driver)
		
	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_join_chatroom(driver,testaccount,roomname):
	ret_status = False
	
	print "------------------------------------------------------------------------------------------------------------------"
	print "< case start: join_chatroom >"
	case_common.gotoChatroomlist(driver)
	if get_chatroomlist(driver):
		join_chatroom(driver,roomname)
		if join_sucess(roomname,testaccount):
			ret_status = True
			print "< case end: pass. >"
		else:
			print "< case end: failed. >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_get_10_historymsg(driver):
	print "------------------------------------------------------------------------------------------------------------------"
	print "< case start: get_10_historymsg >"
	ret_status = get_10_historymsg(driver)

	if ret_status == True:
		print "< case end: pass. >"
	else:
		print "< case end: failed. >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

# Leave a chatroom
def test_leave_chatroom(driver,testaccount,roomname): 
	ret_status = False

	print "------------------------------------------------------------------------------------------------------------------"
	print "< case start: leave_chatroom >"
	leave_chatroom(driver)
	if leave_sucess(testaccount,roomname):
		ret_status = True
		print "< case end: pass. >"
	else:
		print "< case end: failed. >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

# def test_create_chatroom(driver,roomname):
# 	create_chatroom(driver,roomname)
# 	if restHelper
	
def testset_chatroom(driver1, accountA):
	# accountA join chatroom
	print "*************---testset chatroom---*************"
	if test_get_chatroomlist(driver1):
		roomname = get_first_roomname(driver1)
		roomid = restHelper.get_roomid(roomname)
		restHelper.send10chatroommsg(roomid)
		if test_join_chatroom(driver1, testaccount = accountA, roomname = roomname):
			test_get_10_historymsg(driver1)
			case_chat.test_send_chatroomMsg_txt(driver1, msgcontent = "KK999")
			case_chat.test_send_chatroomMsg_audio(driver1)
			test_leave_chatroom(driver1, testaccount = accountA, roomname = roomname)
			case_common.back(driver1)
			case_common.gotoConversation(driver1)
	

if __name__ == "__main__":
	driver1 = case_common.startDemo1()
	# case_account.test_login(driver1,"no1","1")
	testset_chatroom(driver1,"no1")


