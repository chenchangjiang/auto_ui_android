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

def create_chatroom(driver, roomname):
	ret_status = False
	
	driver.find_element_by_xpath("//android.widget.TextView[@text='Create new Chat Room']").click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/edit_chat_room_name").send_keys(roomname)
	driver.find_element_by_xpath("//android.widget.Button[@text='Save']").click()
	if create_chatroom_success(driver,roomname):
		ret_status = True
	
	return ret_status

def create_chatroom_success(driver, roomname):
	ret_status = False

	try:
		sleep(2)
		driver.find_element_by_xpath("//android.widget.TextView[@text='%s']" %roomname)
		print "create chatroom successful."
		ret_status = True
	except:
		print "create chatroom fail."
		case_common.back(driver)
	else:
		leave_chatroom(driver)
	finally:
		sleep(1)
		case_common.back(driver)
		case_common.gotoConversation(driver)

	return ret_status

def dismiss_chatroom(driver):
	ret_status = False

	xpath_id = "com.hyphenate.chatuidemo:id/btn_destroy_chatroom"
	text = "destroy chatroom button"
	elem = case_common.findelem_swipe(driver,xpath_id,text)
	elem.click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_exit").click()

	if chatroom_list_view(driver):
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

def join_chatroom(driver, roomname):
	xpath_id = "//android.widget.TextView[@text='%s']" %roomname
	find_type = "by_xpath"
	text = "chatroom named %s" %roomname
	case_common.findelem_swipe(driver, xpath_id, text, find_type)
	driver.find_element_by_xpath(xpath_id).click()

	mylist = driver.find_elements_by_id("android:id/progress")
	while mylist != []:
		mylist = driver.find_elements_by_id("android:id/progress")
	
def join_sucess(roomid,testaccount):
	ret_status = False

	mylist = restHelper.get_roommember(roomid)
	if testaccount in mylist:
		print "user in chatroom memberlist, join chatroom %s success!" %roomid
		ret_status=True
	else:
		print "user in chatroom memberlist, join chatroom %s failed!" %roomid
		
	return ret_status

def leave_chatroom(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/left_layout").click()

def leave_sucess(testaccount, roomid):
	ret_status = False

	time.sleep(3)
	mylist = restHelper.get_roommember(roomid)
	
	if testaccount not in mylist:
		print "user not in chatroom member list, leave chatrrom %s success!" %roomid
		ret_status = True
	else:
		print "user still in chatroom member list, leave chatroom %s failed!" %roomid

	return ret_status

def chatroom_list_view(driver):
	ret_status = False

	try:
		driver.find_element_by_xpath("//android.widget.TextView[@text='Create new Chat Room']")
		print "in chatroom lis view"
		ret_status = True
	except:
		print "not in chatroom list view"

	return ret_status

def chatroom_view(driver,roomname):
	ret_status = False

	if not chatroom_list_view(driver):
		try:
			driver.find_element_by_xpath("//android.widget.TextView[@text='%s']" %roomname)
			print "in chatroom view"
			ret_status = True
		except:
			pass

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
	
	print "get msg count: %s" %(len(msglist))
	if len(msglist) >= 10:
		print "10 history msg got success!"
		ret_status = True
	elif len(msglist)<10:
		print "less than 10 history msg got!"

	return ret_status

# ///////////////////////////////////////////

def test_get_chatroomlist(driver):
	ret_status = False

	print "<case start: get_chatroomlist >"
	case_common.gotoContact(driver)
	case_common.gotoChatroomlist(driver)
	mylist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/progressBar") #ensure refresh chatroom list complete.
	while mylist != []:
		mylist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/progressBar")

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

def test_join_chatroom(driver, testaccount, roomname, roomid):
	ret_status = False
	
	print "< case start: join_chatroom >"
	join_chatroom(driver, roomname)
	if join_sucess(roomid, testaccount):
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
def test_leave_chatroom(driver, testaccount, roomname, roomid): 
	ret_status = False

	print "< case start: leave_chatroom >"
	leave_chatroom(driver)
	if leave_sucess(testaccount,roomid):
		ret_status = True
		print "< case end: pass. >"
	else:
		print "< case end: failed. >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_create_chatroom(driver, roomname):
	ret_status = False

	print "< case start: create chatroom >"
	case_common.gotoContact(driver)
	case_common.gotoChatroomlist(driver)
	if create_chatroom(driver, roomname):
		ret_status = True
		print "< case end: pass. >"
	else:
		print "< case end: failed. >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_dismiss_chatroom(driver, roomname):
	ret_status = False

	print "< case start: dismiss chatroom>"
	join_a_chatroom(driver,roomname)
	chatroom_details(driver,roomname)

	if dismiss_chatroom(driver):
		print "dismiss chatroom successful."
		case_common.back(driver)
		case_common.gotoConversation
		ret_status = True
		print "< case end: pass. >"
	else:
		print "dismiss chatroom fail."
		case_common.back(driver)
		leave_a_chatroom
		print "< case end: failed. >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def chatroom_details(driver, roomname):
	driver.find_element_by_id('com.hyphenate.chatuidemo:id/right_image').click()
	mylist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/progressBar")
	while mylist != []:
		mylist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/progressBar")

def chatroom_member_manage(driver, roomname, member):
	case_group.find_memberElement(driver, member).click()

def chatroom_admin_manage(driver, roomname, adm_name):
	case_group.find_adminElement(driver, adm_name).click()

def join_a_chatroom(driver,roomname):
	case_common.gotoContact(driver)
	case_common.gotoChatroomlist(driver)

	xpath_id = "//android.widget.TextView[@text='%s']" %roomname
	find_type = "by_xpath"
	text = "chatroom named %s" %roomname
	case_common.findelem_swipe(driver, xpath_id, text, find_type)
	driver.find_element_by_xpath(xpath_id).click()
	mylist = driver.find_elements_by_id("android:id/progress")
	while mylist != []:
		mylist = driver.find_elements_by_id("android:id/progress")

def leave_a_chatroom(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/left_layout").click()
	sleep(1)
	case_common.back(driver)
	case_common.gotoConversation(driver)

# Add Member to Admin
def test_add_admin_chatroom(driver1, driver2, roomname, adm_name):
	ret_status = False

	print "< case start: add chatroom admin>"
	join_a_chatroom(driver2,roomname)
	join_a_chatroom(driver1,roomname)

	chatroom_details(driver1,roomname)
	chatroom_member_manage(driver1,roomname,adm_name)
	case_group.add_admin(driver1)
	sleep(3)

	mydic = case_group.get_group_roles(driver1)
	if adm_name in mydic["adminlist"]:
		ret_status = True
		print "%s received +admin notice sucess!" %(adm_name)
		print "< case end: pass >"
	else:
		print "%s not receive +admin notice, fail!" %(adm_name)
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

# Remove Member from Admin
def test_rm_admin_chatroom(driver1, driver2, roomname, adm_name):
	ret_status = False

	print "< case start: remove chatroom admin>"

	chatroom_admin_manage(driver1,roomname,adm_name)
	case_group.rm_admin(driver1)
	sleep(3)

	mydic = case_group.get_group_roles(driver1)
	if adm_name not in mydic["adminlist"]:
		ret_status = True
		print "%s received -admin notice sucess!" %(adm_name)
		print "< case end: pass >"
	else:
		print "%s not receive -admin notice, fail!" %(adm_name)
		print "< case end: fail >"

	case_common.back(driver1)
	leave_a_chatroom(driver1)
	leave_a_chatroom(driver2)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

# Mute a Chatroom Member
def test_mute_chatroommember(driver1, driver2, roomname, mute_name):
	ret_status = False

	print "< case start: mute a chatroom member>"
	join_a_chatroom(driver2, roomname)
	join_a_chatroom(driver1, roomname)

	chatroom_details(driver1, roomname)
	chatroom_member_manage(driver1, roomname, mute_name)
	case_group.mute(driver1)
	sleep(3)

	if not case_chat.send_chatroomMsg_txt(driver2,"test msg!"):
		print "mute %s sucessful!" %(mute_name)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

# Unmute a Chatroom Member
def test_unmute_chatroommember(driver1, driver2, roomname, unmute_name):
	ret_status = False

	print "< case start: unmute a chatroom member>"

	chatroom_member_manage(driver1, roomname, unmute_name)
	case_group.unmute(driver1)
	sleep(3)

	if case_chat.send_chatroomMsg_txt(driver2,"test msg!"):
		print "unmute %s sucessful!" %(unmute_name)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	case_common.back(driver1)
	leave_a_chatroom(driver1)
	leave_a_chatroom(driver2)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

# Kick Member out of Chatroom
def test_remove_chatroommember(driver1, driver2, roomname, member):
	ret_status = False

	print "< case start: remove a chatroom member>"
	join_a_chatroom(driver2, roomname)
	join_a_chatroom(driver1, roomname)

	chatroom_details(driver1,roomname)
	chatroom_member_manage(driver1, roomname, member)
	case_group.del_member(driver1)
	sleep(3)

	if chatroom_list_view(driver2):
		print "kick %s out of chatroom sucess!" %(member)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"
		case_common.back(driver2)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

# Blcok Chatroom Member
def test_block_chatroommember(driver1, driver2, roomname, member):
	ret_status = False
	print "< case start: block a chatroom member>"

	join_chatroom(driver2, roomname)
	sleep(3)
	chatroom_member_manage(driver1, roomname, member)
	case_group.add_group_blacklist(driver1)
	sleep(3)

	join_chatroom(driver2, roomname)

	if not chatroom_view(driver2, roomname):
		print "Block %s sucess!" %(member)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

# Unblock Chatroom Member
def test_unblock_chatroommember(driver1, driver2, roomname, member):
	ret_status = False

	print "< case start: unblock a chatroom member>"

	chatroom_member_manage(driver1, roomname, member)
	case_group.rm_group_blacklist(driver1)
	sleep(3)

	join_chatroom(driver2, roomname)

	if chatroom_view(driver2, roomname):
		print "Unblock %s sucess!" %(member)
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	case_common.back(driver1)
	leave_a_chatroom(driver1)
	leave_a_chatroom(driver2)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def testset_chatroom(driver1, driver2, accountA, accountB):
	print "********************************************---Chatroom---********************************************"
	newroomname = "my_autotest_chatroom"
	restHelper.del_chatroom_vianame(newroomname)
	restHelper.chatroom_superadmin(accountA)

	if test_get_chatroomlist(driver1):
		roominfo = restHelper.get_joinroominfo()
		roomid = roominfo[0]
		roomname = roominfo[1]
		print "------------------------------------------------------------------------------------------------------------------"
		restHelper.send10chatroommsg(roomid)
		if test_join_chatroom(driver1, accountA, roomname, roomid):
			test_get_10_historymsg(driver1)
			print "------------------------------------------------------------------------------------------------------------------"
			case_chat.test_send_chatroomMsg_txt(driver1, msgcontent="chatroom autotest msg")
			print "------------------------------------------------------------------------------------------------------------------"
			case_chat.test_send_chatroomMsg_audio(driver1)
			print "------------------------------------------------------------------------------------------------------------------"
			test_leave_chatroom(driver1, accountA, roomname, roomid)
			print "------------------------------------------------------------------------------------------------------------------"
			case_common.back(driver1)
			case_common.gotoConversation(driver1)

	if test_create_chatroom(driver1, newroomname):
		print "------------------------------------------------------------------------------------------------------------------"
		test_add_admin_chatroom(driver1, driver2, newroomname, adm_name = accountB)
		print "------------------------------------------------------------------------------------------------------------------"
		test_rm_admin_chatroom(driver1, driver2, newroomname, adm_name = accountB)
		print "------------------------------------------------------------------------------------------------------------------"
		test_mute_chatroommember(driver1, driver2, newroomname, mute_name = accountB)
		print "------------------------------------------------------------------------------------------------------------------"
		test_unmute_chatroommember(driver1, driver2, newroomname, unmute_name = accountB)
		print "------------------------------------------------------------------------------------------------------------------"
		test_remove_chatroommember(driver1, driver2,newroomname, member = accountB)
		print "------------------------------------------------------------------------------------------------------------------"
		test_block_chatroommember(driver1, driver2, newroomname, member = accountB)
		print "------------------------------------------------------------------------------------------------------------------"
		test_unblock_chatroommember(driver1, driver2, newroomname, member = accountB)
		print "------------------------------------------------------------------------------------------------------------------"
		test_dismiss_chatroom(driver1, newroomname)
		print "------------------------------------------------------------------------------------------------------------------"

if __name__ == "__main__":
	device_list = case_common.device_info()

	driver1 = case_common.startDemo(device_list[0], device_list[1], "4723")
	driver2 = case_common.startDemo(device_list[2], device_list[3], "4725")
	# case_account.test_login(driver1, "bob011", "1")
	# case_account.test_login(driver2, "bob022", "1")

	testset_chatroom(driver1, driver2, accountA, accountB)

