#coding=utf-8
import case_common
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
	try:
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_answer_call").click()
		print "B received call from A."
	except:
		raise Exception("B not receive call from A, can not find answer button on screen.")
	try:
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/tv_call_state")
		print "B awnswered call, now B is in call state"
	except:
		raise Exception("some error occurs when answering call.")

def mute_unmute(driver):
	try:
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/iv_handsfree").click()
	except:
		raise Exception("not find answer button.")
	
def hangup(driver, name):
	try:
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_hangup_call").click()
		print "%s ended the call." %name
	except:
		raise Exception("not find hang up button.")

def receive_hangup(driver, name):
	if driver.find_elements_by_id("com.hyphenate.chatuidemo:id/tv_call_state") == []:
		print "%s received hangup notice." %name
	else:
		print "%s not receive hangup notice" %name
	
#////////////////////////////////////////////////////////////////////
def test_video_call(driver1, driver2, userA, userB):
	print "-----------------------------------------------------------"
	print "<case start: voice_call >"

	ret_status = False

	try:
		dial_video(driver1)
		sleep(3)
		answer_call(driver2)
		hangup(driver2, userB)
		sleep(5)
		receive_hangup(driver1, userA)
		print "<case end: pass.>"
		ret_status = True
	except Exception, e:
		print traceback.print_exc()
		print "<case end: fail.>"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_voice_call(driver1, driver2, userA, userB):
	print "-----------------------------------------------------------"
	print "<case start: voice_call >"

	ret_status = False

	try:
		dial_voice(driver1)
		sleep(3)
		answer_call(driver2)
		hangup(driver2, userB)
		sleep(5)
		receive_hangup(driver1, userA)
		print "<case end: pass.>"
		ret_status = True
	except Exception, e:
		print traceback.print_exc()
		print "<case end: fail.>"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status
	

def testset_call(driver1, driver2, userA = accountA, userB = accountB):
	case_common.gotoContact(driver1)
	if case_common.find_name(driver1, userB):
		case_common.click_name(driver1, userB)

	test_video_call(driver1, driver2, userA, userB)
	test_voice_call(driver1, driver2, userA, userB)
	
	
if __name__ == "__main__":
	driver1 = case_common.startDemo1()
	driver2 = case_common.startDemo2()

	testset_call(driver1, driver2, userA = accountA, userB = accountB)