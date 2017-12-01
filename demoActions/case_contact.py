#coding=utf-8
from appium import webdriver
from time import sleep
from appium.webdriver.webelement import WebElement
from appium.webdriver.common.touch_action import TouchAction
import sys
import os
import hashlib
import json
import urllib2
import requests
from datetime import datetime
import case_common
import case_account
import case_chat
import restHelper
from testdata import *

def add_friend(driver, name):
	ret_status = False
	
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/right_image").click()
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/edit_note").send_keys(name)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/search").click()
	sleep(2)
	add = driver.find_element_by_id("com.hyphenate.chatuidemo:id/indicator").click()
	ret_status = True
	
	return ret_status

def get_friendList(driver):
	friendList = []
	mylist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")
	for elem in mylist:
		friendList.append(elem.get_attribute("text"))	
		
	nonContactlist = ["Invitation and notification","Group chat","Channel","Robot chat"]
	for elem in nonContactlist:
		friendList.remove(elem)
	
	return friendList	
	
def del_friend(driver, name):
	ret_status = False
	
	friendlist = get_friendList(driver)
	if name not in friendlist:
		print "%s Not in friend list, so cannot delete this contact!" %name
		return
	
	action1 = TouchAction(driver)
	elem = driver.find_element_by_xpath("//android.widget.TextView[@text='%s']"%name)
	action1.long_press(elem).wait(3000).perform() 

	driver.find_element_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']").click()
	sleep(3)
	
	nowlist = get_friendList(driver)
	if name not in nowlist:
		print "delete friend success!"
		ret_status=True
	
	return ret_status

def block_friend(driver, name):
	ret_status = False
	
	case_common.long_click(driver, name)
	driver.find_element_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='1']").click()
	case_common.gotoSetting(driver)
	case_common.gotoBlacklist(driver)
	
	try:
		driver.find_element_by_xpath("//android.widget.TextView[@text='%s']" %name)
	except:
		print "Add contact blacklist failed!"
		return
	else:
		print "Move to contact blacklist success!"
		ret_status = True
		
	return ret_status

def unblock_friend(driver, name): 
	ret_status = False
	
	blacklist = get_friendBlacklist(driver)
	if name not in blacklist:
		print "%s not in blacklist so cannot unblock this contact!" %name
		return
	
	case_common.long_click(driver, name)
	driver.find_element_by_xpath("//android.widget.TextView[@text='Remove from blacklist']").click()
	sleep(3)
	newblacklist = get_friendBlacklist(driver)
	if name not in newblacklist:
		print "remove %s from blacklist success!" %name
		ret_status = True	
	
	return ret_status
	
def get_friendBlacklist(driver):
	elems = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")
	friendBlacklist = []
	for elem in elems:
		friendBlacklist.append(elem.get_attribute("text"))
	
	return friendBlacklist
	
def accept_friend_invite(driver, fromname):

	mylist = driver.find_elements_by_xpath("//android.widget.TextView[@text='%s']/../android.widget.RelativeLayout/*" %fromname)
	if mylist == []:
		print "cannot find any notice!"
		raise
	for elem in mylist:
		print elem.get_attribute("text")
		if elem.get_attribute("text") == "Agree":
			print "now B try to agree"
			elem.click()
			print "B agreed!"
			sleep(2)
			break
	
def refuse_friend_invite(driver, fromname):
	driver2.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()

	mylist = driver2.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@text='%s']/../*"%contact)
	if mylist == []:
		print "cannot find any notice!"
		raise
	for elem in mylist:
		if elem.get_attribute("text") == "Refuse":
			print "now B try to refuse"
			elem.click()
			print "B refused!"
			sleep(2)
			break
			
#///////////////////////////////////////////////////////////////////////////////////
def test_add_friend(driver1, driver2, fromname, toname):
	ret_status = False
	print "< case start: add frined >"
	
	case_common.gotoContact(driver1)
	add_friend(driver1, toname)
	case_common.gotoContact(driver2)
	case_common.find_notice(driver2, fromname)
	accept_friend_invite(driver2, fromname)

	case_common.back(driver1)
	case_common.back(driver2)

	isContactScreen = case_common.isContactScreen(driver2) #检查是否回到了contact_list界面，如果没有回到contact list界面则：loop(等待1s，再执行一次back)
	while not isContactScreen:
		sleep(1)
		case_common.back(driver2)
		isContactScreen = case_common.isContactScreen(driver2)
	
	mylist1 = get_friendList(driver1)
	mylist2 = get_friendList(driver2)
	if toname in mylist1 and fromname in mylist2:
		ret_status = True
		print "add friend success!"
		print "< case end: pass >"
	else:
		print "add friend failed!"
		print "< case end: fail >"
		
	case_common.gotoConversation(driver1)
	case_common.gotoConversation(driver2)
	
	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_del_friend(driver1, driver2, fromname, toname):
	ret_status = False
	print "< case start: del friend >"

	case_common.gotoContact(driver1)
	case_common.gotoContact(driver2)
	del_friend(driver1,toname)
	
	mylist1 = get_friendList(driver1)
	mylist2 = get_friendList(driver2)
	if toname not in mylist1 and fromname not in mylist2:
		ret_status = True
		print "del friend success!"
		print "< case end: pass >"
	else:
		print "del friend failed!"
		print "< case end: fail >"

	case_common.gotoConversation(driver1)
	case_common.gotoConversation(driver2)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_block_friend(driver, friendname):
	ret_status = False
	print "< case start: block friend >"

	case_common.gotoContact(driver)
	if block_friend(driver,friendname):
		ret_status = True
		print "< case end: pass >"
	else:
		print "< case end: fail >"

	case_common.back(driver)
	case_common.gotoConversation(driver)
	
	case_status[sys._getframe().f_code.co_name] = ret_status	
	return ret_status
	
def test_unblock_friend(driver, friendname):
	ret_status = False
	print "< case start: unblock friend >"
	
	case_common.gotoSetting(driver)
	case_common.gotoBlacklist(driver)
	if unblock_friend(driver,friendname):
		ret_status = True
		print "< case end: pass>"
	else:
		print "< case end: fail>"
		
	case_common.back(driver)
	case_common.gotoConversation(driver)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_msg_block(driver1, driver2, fromname, blockname):
	ret_status = False
	print "< case start: check msg after blocking friend >"

	case_common.gotoContact(driver2)
	case_common.click_name(driver2, fromname)
	case_chat.clear_msg(driver2)
	msgcontent = "test msg"
	msgtype = "text"

	if not case_chat.send_msg_txt(driver2, msgcontent):
		ret_status = True
		print "< case end: pass>"
	else:
		print "< case end: fail>"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_msg_unblock(driver1, driver2, fromname, blockname):
	ret_status = False
	print "< case start: check msg after unblocking friend >"	

	case_common.del_conversation(driver1)
	case_chat.clear_msg(driver2)
	msgcontent = "test msg"
	msgtype = "text"
	chattype = "single_chat"

	if case_chat.send_msg_txt(driver2, msgcontent):
		if case_chat.test_rcv_msg(driver1, blockname, msgcontent, msgtype, chattype):
			ret_status = True
			print "< case end: pass>"
		else:
			print "< case end: fail>"
	else:
		print "< case end: fail>"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status
	
def test_msg_restblock(driver1, driver2, fromname, blockname):
	ret_status = False
	print "< case start: check msg after after rest block friend >"

	restHelper.add_friend_blacklist(fromname, blockname)
	case_chat.clear_msg(driver2)
	msgcontent = "test msg"
	msgtype = "text"

	if not case_chat.send_msg_txt(driver2, msgcontent):
		ret_status = True
		print "< case end: pass>"
	else:
		print "< case end: fail>"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_msg_restunblock(driver1, driver2, fromname, blockname):
	ret_status = False
	print "< case start: check msg after after rest unblock friend >"

	restHelper.del_friend_blacklist(fromname, blockname)
	case_common.del_conversation(driver1)
	case_chat.clear_msg(driver2)
	msgcontent = "test msg"
	msgtype = "text"
	chattype = "single_chat"

	if case_chat.send_msg_txt(driver2, msgcontent):
		if case_chat.test_rcv_msg(driver1, blockname, msgcontent, msgtype, chattype):
			ret_status = True
			print "< case end: pass>"
		else:
			print "< case end: fail>"
	else:
		print "< case end: fail>"

	case_common.back(driver2)
	case_common.gotoConversation(driver2)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

#///////////////////////////////////////////////////////////
def testset_friend(driver1, driver2, userA = accountA, userB = accountB, userC = accountC):
	print "********************************************---Friends---********************************************"
	fromname = userA
	addname = userC
	delname = userC
	blockname = userB
	unblockname = userB
	
	case_account.switch_user(driver2, replacename = addname)
	case_common.del_conversation(driver2)
	print "------------------------------------------------------------------------------------------------------------------"
	test_add_friend(driver1, driver2, fromname, addname)
	print "------------------------------------------------------------------------------------------------------------------"
	test_del_friend(driver1, driver2, fromname, delname)
	print "------------------------------------------------------------------------------------------------------------------"
	case_account.switch_user(driver2, replacename=blockname)
	test_block_friend(driver1, blockname)
	print "------------------------------------------------------------------------------------------------------------------"
	test_msg_block(driver1, driver2, fromname, blockname)
	print "------------------------------------------------------------------------------------------------------------------"
	test_unblock_friend(driver1, unblockname)
	print "------------------------------------------------------------------------------------------------------------------"
	test_msg_unblock(driver1, driver2, fromname, blockname)
	print "------------------------------------------------------------------------------------------------------------------"
	test_msg_restblock(driver1, driver2, fromname, blockname)
	print "------------------------------------------------------------------------------------------------------------------"
	test_msg_restunblock(driver1, driver2, fromname, blockname)
	
if __name__ == "__main__":
	device_list = case_common.device_info()

	driver1 = case_common.startDemo(device_list[0], device_list[1], "4723")
	driver2 = case_common.startDemo(device_list[2], device_list[3], "4725")
	# case_account.test_login(driver1, "bob011", "1")
	# case_account.test_login(driver2, "bob022", "1")

	testset_friend(driver1, driver2, userA = accountA, userB = accountB, userC = accountC)