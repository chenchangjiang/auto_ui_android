#coding=utf-8
from appium import webdriver
from time import sleep
from appium.webdriver.webelement import WebElement
from appium.webdriver.common.touch_action import TouchAction
# import getdevice
import sys
import os
import hashlib
import json
import urllib2
import requests
from datetime import datetime
import case_common
import case_account
from testdata import *

def add_friend(driver,name):
	ret_status = False
	
	addcontactButton = driver.find_element_by_id("com.hyphenate.chatuidemo:id/right_image")
	addcontactButton.click()
	
	addName = driver.find_element_by_id("com.hyphenate.chatuidemo:id/edit_note")
	addName.send_keys(name)
	findButton = driver.find_element_by_id("com.hyphenate.chatuidemo:id/search")
	findButton.click()

	sleep(2)
	add = driver.find_element_by_id("com.hyphenate.chatuidemo:id/indicator")
	add.click()
	ret_status = True
	
	return ret_status
		

def get_friendList(driver):
	# list1 = driver.find_elements_by_xpath("//android.widget.LinearLayout[@index = '1']/android.widget.LinearLayout[@index = '0']/android.widget.TextView[@index = '0']")
	friendList = []
	list1 = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")
	for i in list1:
		friendList.append(i.get_attribute("text"))	
		
	nonContactlist = ["Invitation and notification","Group chat","Channel","Robot chat"]
	
	for i in nonContactlist:
		friendList.remove(i)
	
	return friendList	
	
def del_friend(driver,name):
	ret_status = False
	
	friendlist = get_friendList(driver)
	if name not in friendlist:
		print "%s Not in friend list, so cannot delete this contact!" %name
		return
	
	action1 = TouchAction(driver)
	el = driver.find_element_by_xpath("//android.widget.TextView[@text='%s']"%name)
	action1.long_press(el).wait(3000).perform() 

	delbutton = driver.find_element_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='0']")
	delbutton.click()
	sleep(3)
	
	nowlist = get_friendList(driver)
	if name not in nowlist:
		print "delete friend success!"
		ret_status=True
	
	return ret_status

def block_friend(driver,name):
	ret_status = False
	
	case_common.long_click(driver,name)
	blacklistbutton = driver.find_element_by_xpath("//android.widget.ListView[@index='0']/android.widget.LinearLayout[@index='1']")
	blacklistbutton.click()

	case_common.gotoSetting(driver)
	case_common.gotoBlacklist(driver)
	
	try:
		driver.find_element_by_xpath("//android.widget.TextView[@text='%s']"%name)
	except:
		print "Add contact blacklist failed!"
		return
	else:
		print "Move to contact blacklist success!"
		ret_status = True
		
	return ret_status

def unblock_friend(driver,name): 
	ret_status = False
	
	blacklist = get_friendBlacklist(driver)
	if name not in blacklist:
		print "%s not in blacklist so cannot unblock this contact!"
		return
	
	case_common.long_click(driver,name)
	driver.find_element_by_xpath("//android.widget.TextView[@text='Remove from blacklist']").click()
	sleep(3)
	
	newblacklist = get_friendBlacklist(driver)
	if name not in newblacklist:
		print "remove %s from blacklist success!" %name
		ret_status = True	
	
	return ret_status
	
def get_friendBlacklist(driver):
	elelist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")
	friendBlacklist = []
	for i in elelist:
		friendBlacklist.append(i.get_attribute("text"))
	
	return friendBlacklist
	
	
def accept_friend_invite(driver,fromname):

	list = driver.find_elements_by_xpath("//android.widget.TextView[@text='%s']/../android.widget.RelativeLayout/*"%fromname)
	if list == []:
		print "cannot find any notice!"
		raise
	for i in list:
		print i.get_attribute("text")
		if i.get_attribute("text") == "Agree":
			print "now B try to agree"
			i.click()
			print "B agreed!"
			sleep(2)
			break
	
def refuse_friend_invite(driver,fromname):
	driver2.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()

	list = driver2.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@text='%s']/../*"%contact)
	if list == []:
		print "cannot find any notice!"
		raise
	for i in list:
		if i.get_attribute("text") == "Refuse":
			print "now B try to refuse"
			i.click()
			print "B refused!"
			sleep(2)
			break
			
#///////////////////////////////////////////////////////////////////////////////////
def test_add_friend(driver1,driver2,fromname,toname):
	ret_status = False
	print "< case start: add frined >"
	
	case_common.gotoContact(driver1)
	add_friend(driver1,toname)
	case_common.gotoContact(driver2)
	case_common.find_notice(driver2,fromname)
	accept_friend_invite(driver2,fromname)

	case_common.back(driver1)
	case_common.back(driver2)

	isContactScreen = case_common.isContactScreen(driver2) #检查是否回到了contact_list界面，如果没有回到contact list界面则：loop(等待1s，再执行一次back)
	while not isContactScreen:
		sleep(1)
		case_common.back(driver2)
		isContactScreen = case_common.isContactScreen(driver2)
	
	list1 = get_friendList(driver1)
	list2 = get_friendList(driver2)
	if toname in list1 and fromname in list2:
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

def test_del_friend(driver1,driver2,fromname,toname):
	ret_status = False
	print "< case start: del friend >"
	case_common.gotoContact(driver1)
	case_common.gotoContact(driver2)
	del_friend(driver1,toname)
	
	list1 = get_friendList(driver1)
	list2 = get_friendList(driver2)
	if toname not in list1 and fromname not in list2:
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

def test_block_friend(driver,friendname):
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
	
def test_unblock_friend(driver,friendname):
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
	test_add_friend(driver1, driver2, fromname, addname)
	print "------------------------------------------------------------------------------------------------------------------"
	test_del_friend(driver1, driver2, fromname, delname)
	print "------------------------------------------------------------------------------------------------------------------"

	case_account.switch_user(driver2, replacename = blockname)
	test_block_friend(driver1, blockname)
	print "------------------------------------------------------------------------------------------------------------------"
	test_unblock_friend(driver1, unblockname)
	print "------------------------------------------------------------------------------------------------------------------"
	case_account.switch_user(driver2, replacename = accountB)
	
if __name__ == "__main__":
	device_list = case_common.device_info()

	driver1 = case_common.startDemo1(device_list[0],device_list[1])
	driver2 = case_common.startDemo2(device_list[2],device_list[3])
	case_account.test_login(driver1,"bob011","1")
	case_account.test_login(driver2,"bob022","1")

	testset_friend(driver1, driver2, userA = accountA, userB = accountB, userC = accountC)