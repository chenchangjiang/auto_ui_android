#coding=utf-8
from collections import OrderedDict

dic_Name = {}

dic_Name["accountA"] = "bob011"
dic_Name["accountB"] = "bob022"
dic_Name["accountC"] = "bob033"

accountA = dic_Name["accountA"]
accountB = dic_Name["accountB"]
accountC = dic_Name["accountC"]

dic_Group = {}
dic_Group["main_group"] = 'GK1'
dic_Group["add_agree"] = "add_agree"
dic_Group["add_refuse"] = "add_refuse"
dic_Group["del_member"] = "del_member"
dic_Group["block_member"] = "block_member"
dic_Group["unblock_member"] = "unblock_member"
dic_Group["trans_owner"] = "trans_owner"
dic_Group["B_exit"] = "B_exit"
dic_Group["B_join"] = "B_join"
dic_Group["member_invite"] = "member_invite"

case_status = OrderedDict()

