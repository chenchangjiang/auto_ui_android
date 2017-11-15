#coding=utf-8
import case_common
import case_account
import traceback
import sys
from time import sleep
from testdata import *


def dial_voice(driver):
	print "A dailed a voice call."
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_more").click()
	driver.find_element_by_xpath("//android.widget.TextView[@text='Voice call']").click()

def dial_video(driver):
	print "A dailed a video call."
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_more").click()
	driver.find_element_by_xpath("//android.widget.TextView[@text='Video call']").click()

def answer_call(driver):
	i = 1
	ret_status = False
	while ret_status == False and i<=2:
		try:
			driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_answer_call").click()
			print "B received call from A."
			ret_status = True
		except:
			return ret_status
			print "B not receive call from A, can not find answer button on screen."
	return ret_status
	
def check_in_call(driver):
	i = 1
	ret_status = False
	while ret_status == False and i<=3:
		try:
			driver.find_element_by_id("com.hyphenate.chatuidemo:id/tv_call_state")
			print "in call state"
			ret_status = True
		except:
			print "not in call state."
		i = i+1

def mute_unmute(driver):
	try:
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/iv_handsfree").click()
	except:
		print "not find mute/unmute button."
	
def hangup(driver, name):
	try:
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_hangup_call").click()
		print "%s ended the call." %name
	except:
		print "not find hang up button."

def receive_hangup(driver, name):
	sleep(3)
	if driver.find_elements_by_id("com.hyphenate.chatuidemo:id/tv_call_state") == []:
		print "%s received hangup notice." %name
	else:
		print "%s not receive hangup notice" %name
	
#////////////////////////////////////////////////////////////////////
def test_video_call(driver1, driver2, userA, userB):
	print "<case start: voideo_call >"

	ret_status = False

	try:
		dial_video(driver1)
		sleep(3)
		if answer_call(driver2):
			check_in_call(driver2)
			mute_unmute(driver2)
			check_in_call(driver1)
			mute_unmute(driver1)
			sleep(5)		
			hangup(driver2, userB)
			sleep(5)
			receive_hangup(driver1, userA)
			print "< case end: pass >"
			ret_status = True
		else:
			hangup(driver1, userA)
			print "< case end: fail >"
	except Exception, e:
		print traceback.print_exc()
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_voice_call(driver1, driver2, userA, userB):
	print "<case start: voice_call >"

	ret_status = False

	try:
		dial_voice(driver1)
		sleep(3)
		if answer_call(driver2):
			check_in_call(driver1)
			check_in_call(driver2)
			sleep(5)
			hangup(driver2, userB)
			sleep(5)
			receive_hangup(driver1, userA)
			print "<case end: pass >"
			ret_status = True
		else:
			hangup(driver1, userA)
			print "< case end: fail >"
	except Exception, e:
		print traceback.print_exc()
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status
	
def testset_call(driver1, driver2, userA = accountA, userB = accountB):
	print "********************************************---Voice/Video call---********************************************"
	case_common.gotoContact(driver1)
	case_common.click_name(driver1, userB)

	print "------------------------------------------------------------------------------------------------------------------"
	test_voice_call(driver1, driver2, userA, userB)
	print "------------------------------------------------------------------------------------------------------------------"
	test_video_call(driver1, driver2, userA, userB)
	print "------------------------------------------------------------------------------------------------------------------"
	
	case_common.back(driver1)
	case_common.gotoConversation(driver1)


if __name__ == "__main__":

	device_list = case_common.device_info()

	driver1 = case_common.startDemo1(device_list[0],device_list[1])
	driver2 = case_common.startDemo2(device_list[2],device_list[3])
	# case_account.test_login(driver1,"bob011","1")
	# case_account.test_login(driver2,"bob022","1")

	testset_call(driver1, driver2, userA = accountA, userB = accountB)
