#coding=utf-8
import json
import urllib2
import sys
import time
import requests
import threading

resturl='a1.easemob.com'
org='easemob-demo'
appkey='chatdemoui'
token='YWMtyx5ZKl-9EeeUOX-hZEvslwAAAAAAAAAAAAAAAAAAAAGP-MBq3AgR45fkRZpPlqEwAQMAAAFdB0NeiwBPGgCpIHQ1S3RGEEjA4m9uavApAPqnD5VdMOXgZQcVztxuSQ'

myheaders={'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}

def set_admin(groupid,membername):
	myurl = "http://%s/%s/%s/chatgroups/%s/admin" %(resturl,org,appkey,groupid)

	mydata = {"newadmin":membername}

	request=urllib2.Request(myurl, headers=myheaders, data=json.dumps(mydata))
	request.get_method=lambda:'POST'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print 'error code', e.code
		print 'error msg',e.read()
#注销账号
def get_joinroominfo():
	myurl = "http://%s/%s/%s/chatrooms?pagenum=1&pagesize=20" %(resturl,org,appkey)

	resp = requests.get(url=myurl,headers=myheaders)
	result = json.loads(resp.text).get("data")
	roomid = result[1].get("id")
	roomname = result[1].get("name")
	room_info = [roomid,roomname]
	return room_info


def get_roomid(roomname):
	myurl= "http://%s/%s/%s/chatrooms" % (resturl,org,appkey)
	
	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	chatroomlist = res_dic['data']

	for i in range(len(chatroomlist)):
		if chatroomlist[i]['name'] == roomname:
			chatroomid = chatroomlist[i]['id']
			print "chatroom id of %s is: %s" %(roomname,chatroomid)
			return chatroomid
			
def get_roomname(roomid):
	myurl="http://%s/%s/%s/chatrooms" % (resturl,org,appkey)
	
	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	chatroomlist = res_dic['data']

	for i in range(len(chatroomlist)):
		if chatroomlist[i]['id'] == roomid:
			chatroomname = chatroomlist[i]['name']
			print "chatroom name of %s is: %s" %(roomid,chatroomname)
			return chatroomname
			
def get_roommember(roomid):
	url_getmemberlist= "http://%s/%s/%s/chatrooms/%s" % (resturl,org,appkey,roomid)
	res = requests.get(url=url_getmemberlist,headers=myheaders)
	res_dic = json.loads(res.text)
	roominfo = res_dic['data'][0]
	list1 = roominfo["affiliations"]
	
	mynum = len(list1)
	memberlist = []
	for i in range(mynum):
		membername = list1[i].values()[0]
		memberlist.append(membername)
	return memberlist
	
def del_account(name):
	delaccount_url='http://%s/%s/%s/users/%s' %(resturl,org,appkey,name)
	
	request=urllib2.Request(delaccount_url,headers=myheaders)
	request.get_method=lambda:'DELETE'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print 'error code', e.code
		print 'error msg',e.read()
#注销账号
	
def add_friend(name1,name2):
	addcontact_url='http://%s/%s/%s/users/%s/contacts/users/%s' %(resturl,org,appkey,name1,name2)
	request=urllib2.Request(addcontact_url,headers=myheaders)
	request.get_method=lambda:'POST'
	try:
		response=urllib2.urlopen(request)
		print "\trest added friends: %s and %s" %(name1,name2)
		response.close()
	except urllib2.HTTPError,e:
		print '\terror code', e.code
		print '\terror msg',e.read()
#添加好友

def del_friend(name1,name2):
	delcontact_url='http://%s/%s/%s/users/%s/contacts/users/%s' %(resturl,org,appkey,name1,name2)
	request=urllib2.Request(delcontact_url,headers=myheaders)
	request.get_method=lambda:'DELETE'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print 'error code', e.code
		print 'error msg',e.read()
#删除好友

def del_friend_blacklist(name1,name2):
	delblack_url='http://%s/%s/%s/users/%s/blocks/users/%s' %(resturl,org,appkey,name1,name2)
	request=urllib2.Request(delblack_url,headers=myheaders)
	request.get_method=lambda:'DELETE'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print 'error code', e.code
		print 'error msg',e.read()
#好友黑名单减人

def add_friend_blacklist(name1,name2):
	addblack_url='http://%s/%s/%s/users/%s/blocks/users/%s' %(resturl,org,appkey,name1,name2)
	request=urllib2.Request(addblack_url,headers=myheaders)
	request.get_method=lambda:'POST'
	try:
		response=urllib2.urlopen(request)
		print "\trest added %s to %s friend-blacklist" %(name2,name1)
		response.close()
	except urllib2.HTTPError,e:
		print '\terror code', e.code
		print '\terror msg',e.read()
#好友黑名单加人

def del_group_blacklist(groupID,name):
	delgroupblack_url='http://%s/%s/%s/chatgroups/%s/blocks/users/%s' %(resturl,org,appkey,groupID,name)
	request=urllib2.Request(delgroupblack_url,headers=myheaders)
	request.get_method=lambda:'DELETE'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print '\terror code', e.code
		print '\terror msg',e.read()
#群黑名单减人

def add_group_blacklist(groupID,name):
	addgroupblack_url='http://%s/%s/%s/chatgroups/%s/blocks/users/%s' %(resturl,org,appkey,groupID,name)
	request=urllib2.Request(addgroupblack_url,headers=myheaders)
	request.get_method=lambda:'POST'
	try:
		response=urllib2.urlopen(request)
		print "\tadd %s to group-blacklist groupid: %s" %(name,groupID)
		response.close()
	except urllib2.HTTPError,e:
		print '\terror code', e.code
		print '\terror msg',e.read()
#群黑名单加人

# data = {"usernames":["at0","b0"]}
# request=urllib2.Request(addmember_url,headers=myheaders,data=json.dumps(data))
# request.get_method=lambda:'POST'
# try:
	# response=urllib2.urlopen(request)
	# response.close()
# except urllib2.HTTPError,e:
	# print 'error code', e.code
	# print 'error msg',e.read()
#群组加人

def add_group_member(GroupID,name):
	addmember_url2='http://%s/%s/%s/chatgroups/%s/users/%s' %(resturl,org,appkey,GroupID,name)
	request=urllib2.Request(addmember_url2,headers=myheaders)
	request.get_method=lambda:'POST'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print 'error code', e.code
		print 'error msg',e.read()
#群组加人2

def del_group_member(GroupID,name):
	delmember_url1='http://%s/%s/%s/chatgroups/%s/users/%s' %(resturl,org,appkey,GroupID,name)
	request=urllib2.Request(delmember_url1,headers=myheaders)
	request.get_method=lambda:'DELETE'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print 'error code', e.code
		print 'error msg',e.read()
#群组减人

def del_group(groupID):
	delgroup_url1='http://%s/%s/%s/chatgroups/%s' %(resturl,org,appkey,groupID)
	request=urllib2.Request(delgroup_url1,headers=myheaders)
	request.get_method=lambda:'DELETE'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print 'error code', e.code
		print 'error msg',e.read()
#删除群组'mygroup1'

def search_account(name):
	myurl = "http://a1.easemob.com/easemob-demo/chatdemoui/users/%s" %name
	
	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	print "search result: %s" %res_dic
	myresult = res_dic['error']
	return myresult
	
def ordermsg(fromname,toname,content):
	myurl = "http://a1.easemob.com/easemob-demo/chatdemoui/messages"
	msgcontent = content
	mydata = { "target_type":'users',"target":[toname],"msg":{"type":"txt","msg":msgcontent},"from":fromname}
	print "send rest order msg: %s.." %msgcontent
	
	request=urllib2.Request(url=myurl,headers=myheaders,data=json.dumps(mydata))
	request.get_method=lambda:'POST'
	try:
		response=urllib2.urlopen(request)
		response.close()
	except urllib2.HTTPError,e:
		print 'error code', e.code
		print 'error msg',e.read()
		
def sendmsg(fromname='myRest',toname='at1',number=5,msgtype='users'):
	myurl = "http://a1.easemob.com/easemob-demo/chatdemoui/messages"

	for i in range(number):
		msgcontent = "testmsg"+str(i)
		print msgcontent+"\n"
		mydata = { "target_type":msgtype,"target":[toname],"msg":{"type":"txt","msg":msgcontent},"from":fromname}
		request=urllib2.Request(url=myurl,headers=myheaders,data=json.dumps(mydata))
		request.get_method=lambda:'POST'
		try:
			response=urllib2.urlopen(request)
			response.close()
		except urllib2.HTTPError,e:
			print 'error code', e.code
			print 'error msg',e.read()
		time.sleep(0.5)

def send10chatroommsg(roomid):
	myurl = "http://a1.easemob.com/easemob-demo/chatdemoui/messages"
	
	for i in range(10):
		data = { "target_type":"chatrooms","target":[roomid],"msg":{"type":"txt","msg":str(i) },"from":"test2"}
		request=urllib2.Request(url=myurl,headers=myheaders,data=json.dumps(data))
		request.get_method=lambda:'POST'
		try:
			response=urllib2.urlopen(request)
			response.close()
		except urllib2.HTTPError,e:
			print 'error code', e.code
			print 'error msg',e.read()
		print "send txt msg: %s" %i
		sleep(1)
		
def ifpublicgroup(groupid):
	myurl = "http://a1.easemob.com/easemob-demo/chatdemoui/chatgroups/%s" %groupid

	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	datalist = res_dic['data']
	mydic = datalist[0]
	ifpublic = mydic['public']
	return ifpublic
	
def if_memberinvit(groupid):
	myurl = "http://a1.easemob.com/easemob-demo/chatdemoui/chatgroups/%s" %groupid

	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	datalist = res_dic['data']
	mydic = datalist[0]
	ifallowinvite = mydic['allowinvites']
	return ifallowinvite
	
def get_groupid(username,groupname):
	myurl = "http://a1.easemob.com/easemob-demo/chatdemoui/users/%s/joined_chatgroups" %username
	myheaders={'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}

	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	grouplist = res_dic['data']

	for i in range(len(grouplist)):
		if grouplist[i]['groupname'] == groupname:
			groupid = grouplist[i]['groupid']
			print groupid
			print "groupid of %s is: %s" %(groupname,groupid)
			return groupid
			
def get_groupname(username,groupid):
	myurl = "http://%s/%s/%s/users/%s/joined_chatgroups" %(resturl,org,appkey,username)
	myheaders={'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}

	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	grouplist = res_dic['data']
	
	mylist = []
	
	for i in range(len(grouplist)):
		if grouplist[i]['groupid'] == groupid:
			groupname = grouplist[i]['groupname']
			print "groupid with %s name: %s" %(groupid,groupname)
			return groupname

def get_grouplist(username):
	myurl = "http://%s/%s/%s/users/%s/joined_chatgroups" %(resturl,org,appkey,username)
	myheaders={'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}

	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	grouplist = res_dic['data']
	
	mylist = []
	
	for i in range(len(grouplist)):
		groupname = grouplist[i]['groupname']
		mylist.append(groupname)
	
	return mylist

def get_memberlist(groupid):
	myurl = "http://%s/%s/%s/chatgroups/%s" %(resturl,org,appkey,groupid)
	
	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	groupinfo = res_dic['data']
	grouplist = groupinfo[0]['affiliations']
	
	mylist = []
	for d in grouplist:
		for k in d:
			mylist.append(d[k])
	
	myset = set(mylist)
	return myset
	
def get_friendList(name):
	myurl = "http://%s/%s/%s/users/%s/contacts/users" %(resturl,org,appkey,name)
	
	res = requests.get(url=myurl,headers=myheaders)
	res_dic = json.loads(res.text)
	friendlist = res_dic['data']

	return friendlist

def get_groupname_with_id(groupid):
	myurl = "http://a1.easemob.com/easemob-demo/chatdemoui/chatgroups/%s" %groupid
	myheaders={'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}
	try:
		res = requests.get(url=myurl,headers=myheaders)
		res_dic = json.loads(res.text)
		groupinfo = res_dic['data']
		infolist = groupinfo[0]
		
		groupname = infolist['name']
		return groupname
	except KeyError,e:
		print "\tKeyError: %s" %e
		return None
		
# def register_users(namelist):
# 	myurl = "http://%s/%s/%s/users" %(resturl,org,appkey)
# 	myheaders = {'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}
# 	data = namelist
# 	request=urllib2.Request(myurl,headers=myheaders,data=json.dumps(data))
# 	request.get_method=lambda:'POST'

# 	try:
# 		response=urllib2.urlopen(request)
# 		print "\trest registered new users:"
# 		print "\t",namelist
# 		response.close()
# 	except urllib2.HTTPError,e:
# 		print '\terror code', e.code
# 		print '\terror msg',e.read()
	
def register_single_user(name):
	myurl = "http://%s/%s/%s/users" %(resturl,org,appkey)
	myheaders = {'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}
	data = {"username":name,"password":"1"}
	print "data:"
	print data
	request=urllib2.Request(myurl,headers=myheaders,data=json.dumps(data))
	request.get_method=lambda:'POST'

	try:
		response=urllib2.urlopen(request)
		print "\trest registered new users:"
		print "\t",name
		response.close()
	except urllib2.HTTPError,e:
		print '\terror code', e.code
		print '\terror msg',e.read()
def del_user(name):
	myurl = "http://%s/%s/%s/users/%s" %(resturl,org,appkey,name)
	myheaders = {'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}
	request=urllib2.Request(myurl,headers=myheaders)
	request.get_method=lambda:'DELETE'

	try:
		response=urllib2.urlopen(request)
		print "\trest deleted user: ",name
		response.close()
	except urllib2.HTTPError,e:
		print '\terror code', e.code
		print '\terror msg',e.read()

def create_group(groupname,mybool1,owner,memberlist,mybool2=False):
	myurl = "http://%s/%s/%s/chatgroups" %(resturl,org,appkey)
	myheaders = {'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}
	data = {
			"groupname":groupname,
			"desc":"new rest create group",
			"public":mybool1,
			"allowinvites":mybool2,
			"maxusers":200,
			"approval":True,
			"owner":owner,
			"members":memberlist,
			"scale":"large",
			"mute_duration":20,
			"debut_msg_num":20,
			"custom":"user define self"
			}
	
	request=urllib2.Request(myurl,headers=myheaders,data=json.dumps(data))
	request.get_method=lambda:'POST'

	try:
		response=urllib2.urlopen(request)
		print "\trest created group: ",groupname
		response.close()
	except urllib2.HTTPError,e:
		print '\terror code', e.code
		print '\terror msg',e.read()
		
def get_token():
	myurl = 'https://%s/management/token' %resturl
	myheaders = {'Accept':'application/json','Content-Type':'application/json'}
	data = {"grant_type":"password","username":"easemobdemoadmin","password":"thepushbox123"}
	
	request = urllib2.Request(myurl,headers=myheaders,data=json.dumps(data))
	request.get_method=lambda:'POST'
	
	try:
		response=urllib2.urlopen(request)
		resDic=json.loads(response.read())
		newToken=resDic['access_token']
		print newToken
		return newToken
		response.close()
	except urllib2.HTTPError,e:
		print '\terror code', e.code
		print '\terror msg',e.read()
		
### 常用用例
# 创建一个包含2000人的群组
def creatGroup_2000member():
	namelist = []
	for i in range(2000):
		name = 'PKUY_'+str(i)
		namelist.append(name)
		try:
			register_single_user(name,'1')
			time.sleep(0.5)
		except urllib2.HTTPError,e:
			print '\terror code', e.code
			print '\terror msg',e.read()
	print "***************************************************"
	for name in namelist:
		add_group_member('9372492169218',name)
	
def sendmsg_multi_senders():
	namelist = []
	for i in range(5):
		name = "test"+str(i)
		namelist.append(name)
	
	threads = []	
	for name in namelist:
		fromname = name
		toname = 'no8'
		msgnum = 100
		t1 = threading.Thread(target=sendmsg,args=(u'users',fromname,toname,msgnum))
		threads.append(t1)
		
	for t in threads:
		t.setDaemon(True)
		t.start()
		
	t.join()

def send10chatroommsg(roomid):
	myurl = "https://a1.easemob.com/easemob-demo/chatdemoui/messages"
	myheaders = myheaders={'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token}
	
	for i in range(10):
		data = { "target_type":"chatrooms","target":[roomid],"msg":{"type":"txt","msg":str(i) },"from":"test2"}
		request=urllib2.Request(url=myurl,headers=myheaders,data=json.dumps(data))
		request.get_method=lambda:'POST'
		try:
			response=urllib2.urlopen(request)
			response.close()
		except urllib2.HTTPError,e:
			print 'error code', e.code
			print 'error msg',e.read()
		print "send txt msg: %s" %i
		time.sleep(0.3)


if __name__ == "__main__":
	# newtoken = get_token()
	# print "new token:"
	# print newtoken
	l1 = get_roominfo()
	print l1


	
