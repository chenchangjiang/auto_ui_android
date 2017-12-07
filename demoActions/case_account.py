# coding = utf-8

import time
import sys
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from case_common import *
from testdata import *
import restHelper


def unread_msg_count(driver):
	mylist = []
	
	elems = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/unread_msg_number")
	for elem in elems:
		mylist.append(elem.get_attribute("text"))
	
	return mylist

def switch_user(driver, replacename):
	gotoSetting(driver)
	test_logout(driver)
	test_login(driver, replacename, password = "1")

def test_create_new_user(driver, username, password):
	print "< Case start: create new user: " + username + " | " + password +" >"
	ret_status = False
	
	driver.find_element_by_xpath("//android.widget.Button[@index='0']").click()
	driver.find_element_by_xpath("//android.widget.EditText[@text='User name']").send_keys("%s"%username)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/password").send_keys(password)
	pwd2 = driver.find_element_by_id("com.hyphenate.chatuidemo:id/confirm_password").send_keys("%s"%password)
	driver.find_element_by_xpath("//android.widget.Button[@text='Register']").click()
	
	mylist = driver.find_elements_by_id("android:id/progress")
	while mylist != []:
		mylist = driver.find_elements_by_id("android:id/progress")
	try:
		driver.find_element_by_xpath("//android.widget.Button[@text='Login']")
		print "< case end: pass! >"
		ret_status = True
	except:
		print "< case end: fail >"
		driver.press_keycode(4)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def  test_login(driver, username, password):
	print("< case start : login >")
	ret_status = False

	driver.find_element_by_id("com.hyphenate.chatuidemo:id/username").send_keys(username)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/password").send_keys(password)
	
	n = 1
	while ret_status == False and n <= 3:
		driver.find_element_by_xpath("//android.widget.Button[@text='Login']").click()
		for i in range(50):
			if i<49:
				cur_Activity = driver.current_activity
				if cur_Activity == ".ui.MainActivity":
					print "%s login successful." %username
					print "< case end: pass >"
					ret_status = True
					break
				else:
					time.sleep(1)
			else:
				print "%s login fail %s time." %(username, n)
				print "< case end: fail >"
		n = n + 1
		if driver.find_elements_by_id("android:id/progress") != []:
			back(driver)

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_logout(driver):
	print"< Case start: logout >"
	ret_status = False

	swipeUp(driver)
	xpath_id = "com.hyphenate.chatuidemo:id/btn_logout"
	text = "logout button."

	n = 1
	while ret_status == False and n <= 3:
		elem = findelem_swipe(driver, xpath_id, text)
		elem.click()

		mylist = driver.find_elements_by_id("android:id/progress")
		while mylist != []:
			mylist = driver.find_elements_by_id("android:id/progress")
		mylist = driver.find_elements_by_xpath("//android.widget.Button[@text='Login']")
		if mylist == []:
			print "logout fail %s time." %n
			print "< case end: fail >"
		else:
			print "< case end: pass >"
			ret_status = True
		n = n + 1

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_offline_msg(driver, fromname, toname, togroupid, msgnum):
	print "< case start: receive offline rest msg >"
	ret_status = False
	
	restHelper.sendmsg(toname, fromname, msgnum, msgtype='users')
	restHelper.sendmsg(togroupid, fromname, msgnum, msgtype='chatgroups')
	test_login(driver,toname,"1")
	
	mylist = unread_msg_count(driver)
	print mylist
	if mylist == ['6', '5', '11']:
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_online_msg(driver, fromname, toname, togroupid, msgnum):
	print "< case start: receive online rest msg >"
	ret_status = False
	
	del_conversation(driver)
	restHelper.sendmsg(toname, fromname, msgnum, msgtype='users')
	restHelper.sendmsg(togroupid, fromname, msgnum, msgtype='chatgroups')

	mylist = unread_msg_count(driver)
	print mylist
	if mylist == ['5', '5', '10']:
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def testset_account(driver):
	print "********************************************---Accounts---********************************************"
	registername = random_str(8)
	# registername = "my_autotest"

	print "------------------------------------------------------------------------------------------------------------------"
	test_create_new_user(driver, registername, "1")
	print "------------------------------------------------------------------------------------------------------------------"
	restHelper.create_group("offline_msg_Group", True, registername, memberlist = [])
	groupid = restHelper.get_groupid(registername, "offline_msg_Group")
	test_offline_msg(driver, fromname="rest", toname=registername, togroupid=groupid, msgnum=5)
	print "------------------------------------------------------------------------------------------------------------------"
	test_online_msg(driver, fromname="rest", toname=registername, togroupid=groupid, msgnum=5)
	print "------------------------------------------------------------------------------------------------------------------"
	gotoSetting(driver)
	test_logout(driver)

	restHelper.del_user(registername)
	print "------------------------------------------------------------------------------------------------------------------"

if __name__ == "__main__":
	device_list = device_info()
	print device_list
	for i in range(10):
		clearAppdata(device_list[0])
		clearAppdata(device_list[2])

		driver1 = startDemo(device_list[0], device_list[1], "4723")
		driver2 = startDemo(device_list[2], device_list[3], "4725")

		test_login(driver1, "on1", "asd")
		test_login(driver2, "on2", "asd")

		change_appkeyandserver(driver1, "easemob-demo#coco", "rest_server", "im_server", "ebs", "full")
		change_appkeyandserver(driver2, "easemob-demo#coco", "rest_server", "im_server", "ebs", "full")

		print "----------end %s times----------\n" %i



