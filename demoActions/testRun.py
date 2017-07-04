#coding=utf-8
from case_common import *
from restHelper import *
from case_account import *
from case_contact import *
from case_chat import *
from case_group import *
from case_chatroom import *
from testdata import *
import init
import os
import traceback


if __name__ == "__main__":
	try:
		init.init_all()

		driver1 = startDemo1()
		driver2 = startDemo2()

		testset_account(driver1)

		test_login(driver1, username = accountA, password = "1")
		test_login(driver2, username = accountB, password = "1")
		testset_single_chat(driver1,driver2, fromname = accountA, toname = accountB)
		testset_group_chat(driver1,driver2, fromname = accountA, groupname = dic_Group["group0"])

		testset_friend(driver1, driver2, userA = accountA, userB = accountB, userC = accountC)

		# testset_chatroom(driver1, accountA, roomname)
		case_common.gotoSetting(driver2)
		case_common.swipeUp(driver2)
		sleep(2)
		case_common.swipeUp(driver2)
		case_group.close_AutoAcceptGroupInvitation(driver2)
		sleep(2)
		case_common.gotoConversation(driver2)

		testset_group(driver1, driver2, dic_Group, isadmincase = 0)
		init.group_Broles2()
		testset_group(driver1, driver2, dic_Group, isadmincase = 1)
	
	except Exception, e:
		print traceback.print_exc()
	
	print "#####################################################################################################"
	print "test done."	
	passlist = []
	faillist = []
	norunlist = []
	for k in case_status:
		if case_status[k] == True:
			passlist.append(k)
		elif case_status[k] == False:
			faillist.append(k)

	print "fail %d:" %len(faillist)
	for i in faillist:
		print "	"+i
	print "pass %d: " %len(passlist)
	for i in passlist:
		print "	"+i
	



	






