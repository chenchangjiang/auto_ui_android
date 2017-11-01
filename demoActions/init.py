#coding=utf-8
from restHelper import *
from testdata import *


# 注销所有测试账号(如果有)
def del_users():
	print "----------------------------------------------------------------------------------"
	namelist = dic_Name.values()
	for name in namelist:
		del_user(name)

# 重新创建测试账号
def new_users():
	print "----------------------------------------------------------------------------------"
	namelist = dic_Name.values()
	print "Generate Testing Accounts:"
	for name in namelist:
		register_single_user(name)

# 建立测试用好友关系
def friends():
	print "----------------------------------------------------------------------------------"
	print "Generate Friendship For Testing Accounts:"
	add_friend(accountA,accountB)
	add_friend(accountC,accountB)

# 测试用好友黑名单
# print "----------------------------------------------------------------------------------"
# print "Generate Friend-blacklist:"
# add_friend_blacklist("myat1","myb1")

# 创建测试用群并同时拉accountC进群组
def groups():
	print "----------------------------------------------------------------------------------"
	print "Generate Testing Groups:"
	memberlist1 = [accountC]
	for groupname in dic_Group.values(): 
		if groupname != dic_Group["member_invite"]:
			create_group(groupname,True,accountA,memberlist1)

	create_group(dic_Group["member_invite"], False, accountC, [accountA], True)



# 设置accountC为所有测试群的群管理员
def admin():
	print "----------------------------------------------------------------------------------"
	print "set group admin:"
	groupnamelist = dic_Group.values()
	groupidlist = []
	for groupname in groupnamelist:
		groupid = get_groupid(accountA, groupname)
		groupidlist.append(groupid)

	for groupid in groupidlist:
		set_admin(groupid,accountC)

# 拉accountB进群，并设置accountB在群组中的角色
def group_Broles():
	groupid = get_groupid(accountA,dic_Group["group0"])
	add_group_member(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["del_member"])
	add_group_member(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["block_member"])
	add_group_member(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["unblock_member"])
	add_group_member(groupid, accountB)
	add_group_blacklist(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["B_exit"])
	add_group_member(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["trans_owner"])
	add_group_member(groupid, accountB)
	set_admin(groupid, accountB)


def group_Broles2():
	groupid = get_groupid(accountA,dic_Group["group0"])
	del_group_member(groupid, accountB)
	add_group_member(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["add_agree"])
	del_group_member(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["del_member"])
	add_group_member(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["block_member"])
	add_group_member(groupid, accountB)

	groupid = get_groupid(accountA, dic_Group["unblock_member"])
	add_group_member(groupid, accountB)
	add_group_blacklist(groupid, accountB)

def init_all():
	print "*****************************************************************************************"
	print "start init:"
	del_users()
	new_users()
	friends()
	groups()
	admin()
	group_Broles()
	print "******************************************************************************************"
	print "init Done. now wait for test..."

	
if __name__ == "__main__":
	init_all()
