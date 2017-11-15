# coding = utf-8

import time
import sys
import random
import string
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from case_common import *
from testdata import *
import restHelper


def unread_msg_count(driver):
	mylist = []
	
	els = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/unread_msg_number")
	for el in els:
		mylist.append(el.get_attribute("text"))
	
	return mylist

# Register new user
def switch_user(driver, replacename ):
	gotoSetting(driver)
	test_logout(driver)
	test_login(driver, replacename, password = "1")


def test_create_new_user(driver, username, password):
	ret_status = False
	
	print "< Case start: create new user: " + username + " | " + password +" >"
	driver.find_element_by_xpath("//android.widget.Button[@index='0']").click()
	driver.find_element_by_xpath("//android.widget.EditText[@text='User name']").send_keys("%s"%username)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/password").send_keys(password)
	pwd2 = driver.find_element_by_id("com.hyphenate.chatuidemo:id/confirm_password").send_keys("%s"%password)
	driver.find_element_by_xpath("//android.widget.Button[@text='Register']").click()
	
	for i in range(2):
		try:
			driver.find_element_by_xpath("//android.widget.Button[@text='Login']")
			print "< case end: pass! >"
			ret_status = True
			break
		except:	
			pass
	if ret_status == False:
		print "< case end: fail >"
		driver.press_keycode(4)

	case_status[sys._getframe().f_code.co_name] = ret_status

	return ret_status

# Login
def test_login(driver, username, password):
	print("< case start : login >")
	ret_status = False

	driver.find_element_by_id("com.hyphenate.chatuidemo:id/username").send_keys(username)
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/password").send_keys(password)

	login_button = driver.find_element_by_xpath("//android.widget.LinearLayout/android.widget.Button[2][@index = 1]")
	login_button.click()

	for i in range(50):
		if i<50:
			cur_Activity = driver.current_activity
			if cur_Activity == ".ui.MainActivity":
				print "case end: pass"
				ret_status = True
				break
			else:
				time.sleep(1)
		elif i==49:
			print "< case end: fail >"
			return ret_status

	case_status[sys._getframe().f_code.co_name] = ret_status

	return ret_status

# Logout
def test_logout(driver):
	print"< Case start: logout >"
	ret_status = False

	swipeUp(driver)
	time.sleep(1)
	swipeUp(driver)
	logout = driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_logout")
	logout.click()

	mylist = driver.find_elements_by_id("android:id/progress")
	while mylist != []:
		mylist = driver.find_elements_by_id("android:id/progress")

	listA = driver.find_elements_by_xpath("//android.widget.Button[@text='Login']")
	if listA == []:
		print "case end: fail"
		driver.press_keycode(4)
		return ret_status
	else:
		print "case end: pass"
		ret_status = True
	case_status[sys._getframe().f_code.co_name] = ret_status

	return ret_status

def random_str(strlenth):
	list1 = []
	for i in range(strlenth):
		letter = (random.choice(string.ascii_letters))
		list1.append(letter)
	rdstr = ''.join(list1)
	return rdstr

def test_offline_msg(driver,fromname,toname,togroupid,msgnum):
	ret_status = False
	
	print "< case start: receive offline rest msg >"
	restHelper.sendmsg(fromname,toname,msgnum,msgtype='users')
	restHelper.sendmsg(fromname,togroupid,msgnum,msgtype='chatgroups')
	test_login(driver,toname,"1")
	
	mylist = unread_msg_count(driver)
	print mylist
	if mylist == ['6','5','11']:
		print "< case end: pass > "
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	
	return ret_status

def test_online_msg(driver,fromname,toname,togroupid,msgnum):
	ret_status = False

	print "< case start: receive online rest msg >"
	del_conversation(driver)
	restHelper.sendmsg(fromname,toname,msgnum,msgtype='users')
	restHelper.sendmsg(fromname,togroupid,msgnum,msgtype='chatgroups')

	mylist = unread_msg_count(driver)
	print mylist
	if mylist == ['5','5','10']:
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
	test_create_new_user(driver,registername,"1")
	print "------------------------------------------------------------------------------------------------------------------"
	restHelper.create_group("offline_msg_Group", True, registername, memberlist = [])
	groupid = restHelper.get_groupid(registername, "offline_msg_Group")
	test_offline_msg(driver, fromname = "rest", toname = registername, togroupid = groupid, msgnum = 5)
	print "------------------------------------------------------------------------------------------------------------------"
	test_online_msg(driver, fromname = "rest", toname = registername, togroupid = groupid, msgnum = 5)
	print "------------------------------------------------------------------------------------------------------------------"
	gotoSetting(driver)
	test_logout(driver)

	restHelper.del_user(registername)
	print "------------------------------------------------------------------------------------------------------------------"

if __name__ == "__main__":
	device_list = device_info()

	driver1 = startDemo1(device_list[0],device_list[1])
	driver2 = startDemo2(device_list[2],device_list[3])

	testset_account(driver1)

