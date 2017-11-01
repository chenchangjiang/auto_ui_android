#coding=utf-8
from case_common import *
from restHelper import *
from case_account import *
from case_contact import *
from case_chat import *
from case_group import *
from case_chatroom import *
from case_call import *
from testdata import *
import init
import os
import traceback


if __name__ == "__main__":
	try:
		t1 = time.time()

		device_list = device_info()
		case_common.clearAppdata(device_list[0])
		case_common.clearAppdata(device_list[2])

		init.init_all()

		driver1 = startDemo1(device_list[0],device_list[1])
		driver2 = startDemo2(device_list[2],device_list[3])

		testset_account(driver1)

		test_login(driver1, username = accountA, password = "1")
		test_login(driver2, username = accountB, password = "1")
		case_common.del_conversation(driver1)
		case_common.del_conversation(driver2)

		testset_single_chat(driver1,driver2, fromname = accountA, toname = accountB)
		testset_group_chat(driver1,driver2, fromname = accountA, groupname = dic_Group["group0"])

		testset_call(driver1, driver2, userA = accountA, userB = accountB)

		testset_friend(driver1, driver2, userA = accountA, userB = accountB, userC = accountC)
		
		testset_chatroom(driver1, accountA)

		case_common.gotoSetting(driver2)
		case_group.close_AutoAcceptGroupInvitation(driver2)
		sleep(2)
		case_common.gotoConversation(driver2)

		testset_group(driver1, driver2, dic_Group, isadmincase = 0)
		init.group_Broles2()
		case_account.switch_user(driver1,accountC)
		case_common.del_conversation(driver1)
		testset_group(driver1, driver2, dic_Group, isadmincase = 1)
	
	except Exception, e:
		print traceback.print_exc()

	#计算下整个测试完成所花费的时间
	t2 = time.time()  
	t = (t2-t1)
	str_min = str(int(t/60))
	str_sec = str(int(t%60))
	test_duration = str_min+":"+str_sec  

	print "#####################################################################################################"
	print "test done. test time: %s" %test_duration

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


	cur_path = os.getcwd()
	print "cur_path: "+cur_path
	
	caselist = []
	f = open(r"./demoActions/caseList.txt","r")
	lines = f.readlines()

	for line in lines:
		str1 = line[:-1]
		caselist.append(str1)


	norunlist = []
	for case in caselist:
		if (case not in passlist) & (case not in faillist):
			norunlist.append(case)
	if norunlist == []:
		print "no-run list: None."
	else:
		print "no-run list:"
		for case in norunlist:
			print "\t"+case
