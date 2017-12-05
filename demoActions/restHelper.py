#coding=utf-8
import json
import urllib2
import sys
import time
import requests
import threading
import configdata

test_env = "ebs"
appkey = "easemob-demo#chatdemoui"
test_type = "full"
test_im = "msync"
get_token = "yes"

server = configdata.server_config(test_env, test_type, test_im)
resturl = server[0]
imserver = server[1]

test_para = configdata.test_parameter(test_env, appkey, get_token, resturl)
org = test_para[0]
app = test_para[1]
token = test_para[2]

print "test env: ", test_env
print "test_type: ", test_type
print "appkey: ", appkey
print "resturl: ", resturl
print "imserver: ", imserver

myheaders={'Accept':'application/json', 'Content-Type':'application/json', 'Authorization':'Bearer '+token}

def set_admin(groupid, membername):
	myurl = "http://%s/%s/%s/chatgroups/%s/admin" %(resturl, org, app, groupid)
	mydata = {"newadmin": membername}

	try:
		resp = requests.post(url=myurl, headers=myheaders, data=json.dumps(mydata))
		resp.raise_for_status()
	except requests.RequestException as e:
		print "\t", e
		print "\t", resp.text

def get_joinroominfo():
	myurl = "http://%s/%s/%s/chatrooms?pagenum=1&pagesize=20" %(resturl, org, app)

	try:
		resp = requests.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		result = resp.json().get("data")
		roomid = result[0].get("id")
		roomname = result[0].get("name")
		room_info = [roomid, roomname]
		return room_info

def get_roomid(roomname):
	i=1
	chatroomlist = []
	count = 1 #if count = 0, it means reach the last page. So use un-0 value to initialize count.
	while count != 0:
		myurl = 'http://%s/%s/%s/chatrooms?pagenum=%d&pagesize=1000' %(resturl, org, app, i)
		resp = requests.get(url=myurl, headers=myheaders)
		diction = resp.json()
		count = diction.get('count')
		chatroom_data = diction.get('data')
		i = i + 1
		if count != 0:
			for n in range(count):
				if chatroom_data[n]['name'] == roomname:
					chatroomid = chatroom_data[n]['id']
					chatroomlist.append(chatroomid)
	return chatroomlist
			
def get_roommember(roomid):
	myurl= "http://%s/%s/%s/chatrooms/%s" % (resturl, org,app, roomid)

	try:
		resp = requests.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		resp_dic = resp.json()
		roominfo = resp_dic['data'][0]
		list1 = roominfo["affiliations"]
	
		mynum = len(list1)
		memberlist = []
		for i in range(mynum):
			membername = list1[i].values()[0]
			memberlist.append(membername)
		return memberlist
	
def del_account(name):
	myurl='http://%s/%s/%s/users/%s' %(resturl, org, app, name)

	try:
		resp = requests.delete(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	
def add_friend(name1, name2):
	myurl='http://%s/%s/%s/users/%s/contacts/users/%s' %(resturl, org, app, name1, name2)

	try:
		resp = requests.post(url=myurl, headers=myheaders)
		resp.raise_for_status()
		print "\tadd %s as %s's friend" %(name2, name1)
	except requests.RequestException as e:
		print e

def del_friend(name1, name2):
	myurl='http://%s/%s/%s/users/%s/contacts/users/%s' %(resturl, org, app, name1, name2)

	try:
		resp = requests.delete(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e

def del_friend_blacklist(name1, name2):
	myurl='http://%s/%s/%s/users/%s/blocks/users/%s' %(resturl, org, app, name1, name2)

	try:
		resp = requests.delete(url=myurl, headers=myheaders)
		resp.raise_for_status()
		print "\trest delete %s from %s friend-blacklist" %(name2, name1)
	except requests.RequestException as e:
		print e

def add_friend_blacklist(name1, name2):
	myurl='http://%s/%s/%s/users/%s/blocks/users/%s' %(resturl, org, app, name1, name2)

	try:
		resp = requests.post(url=myurl, headers=myheaders)
		resp.raise_for_status()
		print "\trest added %s to %s friend-blacklist" %(name2, name1)
	except requests.RequestException as e:
		print e

def del_group_blacklist(groupID, name):
	myurl='http://%s/%s/%s/chatgroups/%s/blocks/users/%s' %(resturl, org, app, groupID, name)

	try:
		resp = requests.delete(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e

def add_group_blacklist(groupID,name):
	myurl='http://%s/%s/%s/chatgroups/%s/blocks/users/%s' %(resturl, org, app, groupID, name)

	try:
		resp = requests.post(url=myurl, headers=myheaders)
		resp.raise_for_status()
		print "\tadd %s to group-blacklist groupid: %s" %(name, groupID)
	except requests.RequestException as e:
		print e

def add_group_member(GroupID, name):
	myurl='http://%s/%s/%s/chatgroups/%s/users/%s' %(resturl, org, app, GroupID, name)

	try:
		resp = requests.post(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e

def del_group_member(GroupID, name):
	myurl='http://%s/%s/%s/chatgroups/%s/users/%s' %(resturl, org, app, GroupID, name)

	try:
		resp = requests.delete(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e

def del_group(groupID):
	myurl='http://%s/%s/%s/chatgroups/%s' %(resturl, org, app, groupID)

	try:
		resp = request.delete(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e

def search_account(name):
	myurl = "http://%s/%s/%s/users/%s" %(resturl, org, app, name)

	try:
		resp = request.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		resp_dic = resp.json()
		print "search result: %s" %res_dic
		myresult = res_dic['error']
		return myresult
		
def sendmsg(toname, fromname='myrest', number=5, msgtype='users'):
	myurl = "http://%s/%s/%s/messages" %(resturl, org, app)

	for i in range(number):
		msgcontent = "testmsg"+str(i)
		print msgcontent
		mydata = { "target_type":msgtype, "target":[toname], "msg":{"type":"txt", "msg":msgcontent}, "from":fromname}
		try:
			resp = requests.post(url=myurl, headers=myheaders, data=json.dumps(mydata))
			resp.raise_for_status()
		except requests.RequestException as e:
			print e

		time.sleep(1)

def send10chatroommsg(roomid):
	myurl = "http://%s/%s/%s/messages" %(resturl, org, app)
	
	for i in range(10):
		data = { "target_type":"chatrooms", "target":[roomid], "msg":{"type":"txt","msg":str(i) }, "from":"test2"}
		try:
			resp = requests.post(url=myurl, headers=myheaders, data=json.dumps(data))
			resp.raise_for_status()
			print "send txt msg: %s" %i
		except requests.RequestException as e:
			print e
		time.sleep(0.8)
		
def ifpublicgroup(groupid):
	myurl = "http://%s/%s/%s/chatgroups/%s" %(resturl, org, app, groupid)

	try:
		resp = request.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		resp_dic = resp.json()
		ifpublic = res_dic['data'][0]['public']
		return ifpublic
	
def if_memberinvit(groupid):
	myurl = "http://%s/%s/%s/chatgroups/%s" %(resturl, org, app, groupid)

	try:
		resp = request.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		resp_dic = resp.json()
		ifallowinvite = res_dic['data'][0]['allowinvites']
		return ifallowinvite
	
def get_groupid(username, groupname):
	myurl = "http://%s/%s/%s/users/%s/joined_chatgroups" %(resturl, org, app, username)

	try:
		resp = requests.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		resp = requests.get(url=myurl, headers=myheaders)
		resp_dic = resp.json()
		grouplist = resp_dic['data']

		for i in range(len(grouplist)):
			if grouplist[i]['groupname'] == groupname:
				groupid = grouplist[i]['groupid']
				print "\tgroupid of %s is: %s" %(groupname, groupid)
				return groupid
			
def get_groupname(username, groupid):
	myurl = "http://%s/%s/%s/users/%s/joined_chatgroups" %(resturl, org, app, username)

	try:
		resp = request.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		resp_dic = resp.json()
		grouplist = res_dic['data']
		mylist = []
	
		for i in range(len(grouplist)):
			if grouplist[i]['groupid'] == groupid:
				groupname = grouplist[i]['groupname']
				print "groupid with %s name: %s" %(groupid, groupname)
				return groupname

def get_grouplist(username):
	myurl = "http://%s/%s/%s/users/%s/joined_chatgroups" %(resturl, org, app, username)

	try:
		resp = request.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		resp_dic = resp.json()
		grouplist = res_dic['data']
		mylist = []
	
		for i in range(len(grouplist)):
			groupname = grouplist[i]['groupname']
			mylist.append(groupname)
	
		return mylist

def get_memberlist(groupid):
	myurl = "http://%s/%s/%s/chatgroups/%s" %(resturl, org, app, groupid)

	try:
		resp = request.get(url=myurl, headers=myheaders)
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
	else:
		resp_dic = res.json()
		grouplist = es_dic['data'][0]['affiliations']
	
		mylist = []
		for d in grouplist:
			for k in d:
				mylist.append(d[k])
	
		myset = set(mylist)
		return myset
	
def get_friendList(name):
	myurl = "http://%s/%s/%s/users/%s/contacts/users" %(resturl, org, app, name)

	try:
		resp = requests.get(url=myurl, headers=myheaders)
	except requests.RequestException as e:
		print e
	else:
		resp_dic = resp.json()
		friendlist = res_dic['data']
		return friendlist

def get_groupname_with_id(groupid):
	myurl = "http://%s/%s/%s/chatgroups/%s" %(resturl, org, app, groupid)
	
	try:
		resp = requests.get(url=myurl, headers=myheaders)
		resp_dic = resp.json()
		infolist = resp_dic['data'][0]
		
		groupname = infolist['name']
		return groupname
	except KeyError,e:
		print "\tKeyError: %s" %e
		return None
	
def register_single_user(name):
	myurl = "http://%s/%s/%s/users" %(resturl, org, app)
	data = {"username":name, "password":"1"}
	print "\tdata:", data

	try:
		resp = requests.post(url=myurl, headers=myheaders, data=json.dumps(data))
		resp.raise_for_status()
		print "\trest registered new users:",name
	except requests.RequestException as e:
		print "\t", e

def del_user(name):
	myurl = "http://%s/%s/%s/users/%s" %(resturl, org, app, name)

	try:
		resp = requests.delete(url=myurl, headers=myheaders)
		resp.raise_for_status()
		print "\trest delete user: ",name
	except requests.RequestException as e:
		print "\t", e
		print "\t", resp.text

def create_group(groupname, mybool1, owner, memberlist, mybool2=False):
	myurl = "http://%s/%s/%s/chatgroups" %(resturl,org,app)

	data = {
			"groupname":groupname,
			"desc":"new rest create group",
			"public":mybool1,
			"allowinvites":mybool2,
			"maxusers":200,
			"approval":True,
			"owner":owner,
			"members":memberlist,
			# "scale":"large",
			# "mute_duration":20,
			# "debut_msg_num":20,
			# "custom":"user define self"
			}

	try:
		resp = requests.post(url=myurl, headers=myheaders, data=json.dumps(data))
		resp.raise_for_status()
		print "\trest created group: ", groupname
	except requests.RequestException as e:
		print e
		print resp.text

def chatroom_superadmin(username):
	myurl = "http://%s/%s/%s/chatrooms/super_admin" %(resturl, org, app)
	mydata = {"superadmin":username}
	try:
		resp = requests.post(url=myurl, headers=myheaders, data=json.dumps(mydata))
		resp.raise_for_status()
	except requests.RequestException as e:
		print e
		print resp.text

def del_chatroom_vianame(roomname):
	chatroomlist = get_roomid(roomname)

	if len(chatroomlist) == 0:
		print "no chatroom named %s need delete." %roomname
	else:
		for roomid in chatroomlist:
			try:
				myurl = "http://%s/%s/%s/chatrooms/%s" %(resturl, org, app, roomid)
				resp = requests.delete(url=myurl, headers=myheaders)
				resp.raise_for_status()
			except requests.RequestException as e:
				print e
				print resp.text

if __name__ == "__main__":
	del_chatroom_vianame("my_autotest_chatroom")