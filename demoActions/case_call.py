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
			print "B not receive call from A, can not find answer button on screen."
			return ret_status
		i = i+1
	
	return ret_status
	
def check_in_call(driver, name):
	i = 1
	ret_status = False
	
	while ret_status == False and i<=3:
		try:
			driver.find_element_by_xpath("//android.widget.TextView[@text='In the call..']")
			print "%s in call state" %name
			ret_status = True
		except:
			print "%s not in call state." %name
		i = i+1

	return ret_status

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
	ret_status = False

	if driver.find_elements_by_id("com.hyphenate.chatuidemo:id/tv_call_state") == []:
		print "%s received hangup notice." %name
		ret_status = True
	else:
		print "%s not receive hangup notice" %name

	return ret_status

def gotoConferencecall(driver):
	driver.find_element_by_xpath("//android.widget.TextView[@text='Voice and video conference']").click()
	sleep(5)

def invite_conferencecall(driver, name):
	for i in range(2):
		driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_invite_join").click()
		try:
			driver.find_element_by_xpath("//android.widget.TextView[@text='%s']" %name).click()
			break
		except:
			print "not in invite view."
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_ok").click()

def answer_conferencecall(driver):
	i = 1
	ret_status = False
	
	while ret_status == False and i<=2:
		try:
			driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_add").click()
			ret_status = True
		except:
			print "not receive call, can not find answer button on screen."
			return ret_status
	
	return ret_status

def in_conference_vioicecall(driver, name):
	ret_status = False

	mylist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/img_call_avatar")
	if len(mylist) == 2:
		print "%s in conference voice call state" %name
		ret_status = True
	else:
		print "%s not in conference voice call state" %name

	return ret_status

def in_conference_videocall(driver, name):
	ret_status = False

	mylist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/item_surface_view")
	if len(mylist) == 2:
		print "%s in conference video call state" %name
		ret_status = True
	else:
		print "%s not in conference video call state" %name

	return ret_status

def conferencecall_switch(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_camera_switch").click()

def mute_conference_call(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_speaker_switch").click()

def exit_conference(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_exit").click()

def start_conference_vocie_call(driver1, driver2, userA, userB):
	ret_status = False

	gotoConferencecall(driver1)
	invite_conferencecall(driver1, userB)
	if answer_conferencecall(driver2):
		sleep(10)
		if in_conference_vioicecall(driver1, userA) and in_conference_vioicecall(driver2, userB):
			ret_status = True
		else:
			print "conference vocie call not establish successful."
		exit_conference(driver2)
		exit_conference(driver1)
	else:
		exit_conference(driver1)

	return ret_status

def start_conference_video_call(driver1, driver2, userA, userB):
	ret_status = False

	gotoConferencecall(driver1)
	invite_conferencecall(driver1, userB)
	if answer_conferencecall(driver2):
		sleep(10)
		if in_conference_vioicecall(driver1, userA) and in_conference_vioicecall(driver2, userB):
			mute_conference_call(driver1)
			mute_conference_call(driver2)
			conferencecall_switch(driver1)
			conferencecall_switch(driver2)
			sleep(5)
			if in_conference_videocall(driver1, userA) and in_conference_videocall(driver2, userB):
				ret_status = True
			else:
				print "conference video call not establish successful."
			exit_conference(driver2)
			exit_conference(driver1)
		else:
			print "conference vocie call not establish successful."
	else:
		exit_conference(driver1)

	return ret_status

	
#////////////////////////////////////////////////////////////////////
def test_video_call(driver1, driver2, userA, userB):
	print "<case start: voideo call >"
	ret_status = False

	dial_video(driver1)
	sleep(3)
	if answer_call(driver2):
		if check_in_call(driver2, userB) and check_in_call(driver1, userA):
			mute_unmute(driver2)			
			mute_unmute(driver1)
			sleep(5)		
			hangup(driver2, userB)
			sleep(5)
			if receive_hangup(driver1, userA):
				print "< case end: pass >"
				ret_status = True
			else:
				hangup(driver1, userA)
		else:
			print "not both in call state."
			hangup(driver1, userA)
			hangup(driver2, userB)
			print "< case end: fail >"
	else:
		hangup(driver1, userA)
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_voice_call(driver1, driver2, userA, userB):
	print "<case start: voice call >"
	ret_status = False

	dial_voice(driver1)
	sleep(3)
	if answer_call(driver2):
		if check_in_call(driver1, userA) and check_in_call(driver2, userB):			
			sleep(5)
			hangup(driver2, userB)
			sleep(5)
			if receive_hangup(driver1, userA):
				print "<case end: pass >"
				ret_status = True
			else:
				hangup(driver1, userA)
		else:
			print "not both in call state."
			hangup(driver1, userA)
			hangup(driver2, userB)
			print "< case end: fail >"
	else:
		hangup(driver1, userA)
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status
	return ret_status

def test_conference_voice_call(driver1, driver2, userA, userB):
	print "<case start: conference vicoe call>"
	ret_status = False

	if start_conference_vocie_call(driver1, driver2, userA, userB):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status

def test_conference_video_call(driver1, driver2, userA, userB):
	print "<case start: conference video call>"
	ret_status = False

	if start_conference_video_call(driver1, driver2, userA, userB):
		print "< case end: pass >"
		ret_status = True
	else:
		print "< case end: fail >"

	case_status[sys._getframe().f_code.co_name] = ret_status


	
def testset_call(driver1, driver2, userA = accountA, userB = accountB):
	print "********************************************---Voice/Video call and conference voice/video call---********************************************"
	case_common.gotoContact(driver1)
	case_common.click_name(driver1, userB)
	print "------------------------------------------------------------------------------------------------------------------"
	test_voice_call(driver1, driver2, userA, userB)
	print "------------------------------------------------------------------------------------------------------------------"
	test_video_call(driver1, driver2, userA, userB)
	case_common.back(driver1)
	case_common.gotoConversation(driver1)
	print "------------------------------------------------------------------------------------------------------------------"
	case_common.gotoContact(driver1)
	test_conference_voice_call(driver1, driver2, userA, userB)
	print "------------------------------------------------------------------------------------------------------------------"
	test_conference_video_call(driver1, driver2, userA, userB)
	case_common.gotoConversation(driver1)



if __name__ == "__main__":

	device_list = case_common.device_info()

	driver1 = case_common.startDemo(device_list[0], device_list[1], "4723")
	driver2 = case_common.startDemo(device_list[2], device_list[3], "4725")
	case_account.test_login(driver1,"bob011", "1")
	case_account.test_login(driver2,"bob022", "1")

	testset_call(driver1, driver2, userA=accountA, userB=accountB)

	# case_common.gotoSetting(driver1)
	# case_common.gotoSetting(driver2)
	# case_common.logout(driver1)
	# case_common.logout(driver2)
