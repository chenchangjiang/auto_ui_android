#coding=utf-8
import time
import sys
import requests
import json
import case_account
import case_common
import case_group
import restHelper
import case_chat
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from testdata import *
from time import sleep

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
		print "Empty chatroom list!"
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

	print "<case start: get_chatroomlist >"
	case_common.gotoContact(driver)
	case_common.gotoChatroomlist(driver)

	roomlist = driver.find_elements_by_xpath("//android.widget.ListView[@index='2']/*") # 获取聊天室列表条目
	if len(roomlist) > 0:
		print "get chatroom list success!"
		print "< case end: pass. >"
		ret_status = True
	else:
		print "get chatroom list failed!"
		print "< case end: failed. >!"
		ret_status = False

		case_common.back(driver)
		case_common.gotoConversation(driver)
		
	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_join_chatroom(driver,testaccount,roomname):
	ret_status = False
	
	print "< case start: join_chatroom >"
	case_common.gotoChatroomlist(driver)
	if get_chatroomlist(driver):
		join_chatroom(driver,roomname)
		if join_sucess(roomname,testaccount):
			ret_status = True
			print "< case end: pass. >"
		else:
			print "< case end: failed. >"
	print "------------------------------------------------------------------------------------------------------------------"
	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_get_10_historymsg(driver):
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
# def testset_chatroom(driver1, driver2, accountA, accountB):
	# accountA join chatroom
	print "********************************************---Chatroom---********************************************"
	if test_get_chatroomlist(driver1):
		roominfo = restHelper.get_joinroominfo()
		roomid = roominfo[0]
		roomname = roominfo[1]
		restHelper.send10chatroommsg(roomid)
		if test_join_chatroom(driver1, testaccount = accountA, roomname = roomname):
			test_get_10_historymsg(driver1)
			print "------------------------------------------------------------------------------------------------------------------"
			case_chat.test_send_chatroomMsg_txt(driver1, msgcontent = "KK999")
			print "------------------------------------------------------------------------------------------------------------------"
			case_chat.test_send_chatroomMsg_audio(driver1)
			print "------------------------------------------------------------------------------------------------------------------"
			# test_add_admin(driver1, driver2, roomname, adm_name = accountB)
			# test_rm_admin(driver1, driver2, roomname, adm_name = accountB)
			# test_mute_chatroommember(driver1, driver2, roomname, mute_name = accountB)
			# test_unmute_chatroommember(driver1, driver2, roomname, unmute_name = accountB)
			# test_kick_out_chatroommember(driver1, driver2,roomname, member = accountB)
			# test_block_roommember(driver1, driver2, roomname, member = accountB)
			# test_unblock_roommember(driver1, driver2, roomname, member = accountB)

			test_leave_chatroom(driver1, testaccount = accountA, roomname = roomname)
			case_common.back(driver1)
			case_common.gotoConversation(driver1)

def chatroom_details(driver,roomname):
	driver.find_element_by_id('com.hyphenate.chatuidemo:id/right_image').click()

def chatroom_member_manage(driver,roomname,member):
	el = case_group.find_memberElement(driver1,member)
	el.click()

def chatroom_admin_manage(driver,roomname,adm_name):
	el = case_group.find_adminElement(driver1,adm_name)
	el.click()

# Add Member to Admin
def test_add_admin(driver1, driver2, roomname, adm_name):
	ret_status = False

	chatroom_details(driver1,roomname)
	chatroom_member_manage(driver1,roomname,adm_name)
	case_group.add_admin(driver1)
	sleep(5)

	mydic = case_group.get_group_roles(driver1)
	if adm_name in mydic["adminlist"]:
		ret_status = True
		print "%s received +admin notice sucess!" %(adm_name)
		print "< case end: pass >"
	else:
		print "%s not receive +admin notice, fail!" %(adm_name)
		print "< case end: fail >"

	str1 = 'chatroom'

	case_status[sys._getframe().f_code.co_name+':'+str1] = ret_status
	return ret_status

# Remove Member from Admin
def test_rm_admin(driver1, driver2, roomname, adm_name):
	ret_status = False

	chatroom_admin_manage(driver1,roomname,adm_name)
	case_group.rm_admin(driver1)
	sleep(5)

	mydic = case_group.get_group_roles(driver1)
	if adm_name not in mydic["adminlist"]:
		ret_status = True
		print "%s received -admin notice sucess!" %(adm_name)
		print "< case end: pass >"
	else:
		print "%s not receive -admin notice, fail!" %(adm_name)
		print "< case end: fail >"

	str1 = 'chatroom'

	case_status[sys._getframe().f_code.co_name+':'+str1] = ret_status
	return ret_status

# Mute a Chatroom Member
def test_mute_chatroommember(driver1,driver2,roomname,mute_name):
	ret_status = False

	chatroom_details(driver1,roomname)
	chatroom_member_manage(driver1,roomname,mute_name)
	case_group.mute(driver1)
	sleep(5)

	case_chat.send_chatroomMsg_txt(driver2,"test msg!")


	if not case_chat.send_chatroomMsg_txt(driver2,"test msg!"):
		print "mute %s sucess!" %(mute_name)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	str1 = 'chatroom'

	case_status[sys._getframe().f_code.co_name+':'+str1] = ret_status
	return ret_status

# Unmute a Chatroom Member
def test_unmute_chatroommember(driver1,driver2,roomname,unmute_name):
	ret_status = False

	chatroom_member_manage(driver1,roomname,unmute_name)
	case_group.unmute(driver1)
	sleep(5)

	case_chat.send_chatroomMsg_txt(driver2,'test msg!')

	if case_chat.send_chatroomMsg_txt(driver2,"test msg!"):
		print "unmute %s sucess!" %(unmute_name)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	str1 = "chatroom"
	case_status[sys._getframe().f_code.co_name+":"+str1] = ret_status
	return ret_status


# Kick Member out of Chatroom
def test_kick_out_chatroommember(driver1,driver2,roomname,member):
	ret_status = False

	chatroom_member_manage(driver1,roomname,member)
	case_group.del_member(driver1)
	sleep(5)

	if leave_sucess(member,roomname):
		print "kick %s out of chatroom sucess!" %(member)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	str1 = "chatroom"
	case_status[sys._getframe().f_code.co_name+":"+str1] = ret_status
	return ret_status

# Blcok Chatroom Member
def test_block_roommember(driver1,driver2,roomname,member):
	ret_status = False

	join_chatroom(driver2,roomname)

	chatroom_member_manage(driver1,roomname,member)
	case_group.add_group_blacklist(driver1)
	sleep(5)

	join_chatroom(driver2,roomname)


	if not join_sucess(roomname,member):
		print "Block %s sucess!" %(member)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	str1 = "chatroom"
	case_status[sys._getframe().f_code.co_name+":"+str1] = ret_status
	return ret_status

# Unblock Chatroom Member
def test_unblock_roommember(driver1,driver2,roomname,member):
	ret_status = False

	chatroom_member_manage(driver1,roomname,member)
	case_group.rm_group_blacklist(driver1)
	sleep(5)

	join_chatroom(driver2,roomname)

	if join_sucess(roomname,member):
		print "Unblock %s sucess!" %(member)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	str1 = "chatroom"
	case_status[sys._getframe().f_code.co_name+":"+str1] = ret_status
	return ret_status		

if __name__ == "__main__":
	device_list = case_common.device_info()

	driver1 = case_common.startDemo1(device_list[0],device_list[1])
	driver2 = case_common.startDemo2(device_list[2],device_list[3])
	case_account.test_login(driver1,"bob011","1")
	case_account.test_login(driver2,"bob022","1")

	testset_chatroom(driver1, accountA)

