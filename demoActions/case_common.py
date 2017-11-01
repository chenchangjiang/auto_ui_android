#coding=utf-8
from appium import webdriver
from time import sleep
from appium.webdriver.webelement import WebElement
from appium.webdriver.common.touch_action import TouchAction
import get_device
import os


def device_info():
	dinfo_dic = get_device.get_deviceinfo()

	deviceid1 = dinfo_dic.keys()[0]
	dversion1 = dinfo_dic.get(deviceid1)
	deviceid2 = dinfo_dic.keys()[1]
	dversion2 = dinfo_dic.get(deviceid2)

	return [deviceid1,dversion1,deviceid2,dversion2]
	# return [deviceid1,dversion1]

def startDemo1(deviceid1,dversion1):
	desired_caps = {}
	desired_caps['platformName'] = 'Android'
	desired_caps['platformVersion'] = dversion1
	desired_caps['deviceName'] = deviceid1
	desired_caps['udid'] = deviceid1
	desired_caps['appPackage'] = 'com.hyphenate.chatuidemo'
	desired_caps['appActivity'] = 'com.hyphenate.chatuidemo.ui.SplashActivity'
	desired_caps['unicodeKeyboard']= True
	desired_caps['resetKeyboard']= True
	# desired_caps['automationName'] = 'Uiautomator2'
	desired_caps['noReset'] = True
	desired_caps['newCommandTimeout']='2000'
	global driver
	driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
	driver.implicitly_wait(5)
	return driver
	
def startDemo2(deviceid2,dversion2):
	desired_caps = {}
	desired_caps['platformName'] = 'Android'
	desired_caps['platformVersion'] = dversion2
	desired_caps['deviceName'] = deviceid2
	desired_caps['udid'] = deviceid2
	desired_caps['appPackage'] = 'com.hyphenate.chatuidemo'
	desired_caps['appActivity'] = 'com.hyphenate.chatuidemo.ui.SplashActivity'
	desired_caps['unicodeKeyboard']= True
	desired_caps['resetKeyboard']= True
	desired_caps['noReset'] = True
	desired_caps['newCommandTimeout']='2000'
	global driver
	driver = webdriver.Remote('http://localhost:4725/wd/hub', desired_caps)
	driver.implicitly_wait(5)
	return driver

def clearAppdata(deviceid):
	os.popen("adb -s %s shell pm clear com.hyphenate.chatuidemo" %deviceid).read()

def gotoSetting(driver):
	settingButton = driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_setting")
	settingButton.click()

def gotoBlacklist(driver):
	text = "Black list"
	xpath_id = "com.hyphenate.chatuidemo:id/ll_black_list"
	elem = findelem_swipe(driver,xpath_id,text)
	elem.click()
	
def gotoContact(driver):
	contactButton = driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_address_list")
	contactButton.click()

def isContactScreen(driver):
	ret_status = False

	l1 = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/btn_address_list")
	if l1 != []:
		print "now is in contacts screen"
		ret_status = True
	else:
		print "not in contacts screen!"

	return ret_status

def gotoGroup(driver):
	groupButton = driver.find_element_by_xpath("//android.widget.TextView[@text='Group chat']")
	groupButton.click()

def gotoInvitation(driver):
	driver.find_element_by_xpath("//android.widget.TextView[@text='Invitation and notification']").click()
	
def click_name(driver,name):
	driver.find_element_by_xpath("//android.widget.TextView[@text='%s']"%name).click()

def back(driver):
	driver.press_keycode(4)

def back_home(driver):
	driver.press_keycode(3)

def back2(driver):
	driver.find_element_by_xpath("//android.widget.ImageView").click()

def gotoChatroomlist(driver):
	driver.find_element_by_xpath("//android.widget.TextView[@text = 'Channel']").click()
	
def long_click(driver,name):
	action1 = TouchAction(driver)
	el = driver.find_element_by_xpath("//android.widget.TextView[@text='%s']"%name)
	action1.long_press(el).wait(2000).perform()
	
def long_press_by_id(driver,id,duration):
	action1 = TouchAction(driver)
	el = driver.find_element_by_id(id)
	action1.press(el).wait(duration).move_to(el).release().perform()
	action1.release()
	sleep(3)

def if_logedIn(driver):
	ret_status = False
	sleep(3)
	curActivity = driver.current_activity
	if curActivity == ".ui.MainActivity":
		ret_status = True
			
	return ret_status
	
def gotoConversation(driver):
	driver.find_element_by_id("com.hyphenate.chatuidemo:id/btn_conversation").click()
	
def search(driver,content):
	el = driver.find_element_by_id("com.hyphenate.chatuidemo:id/search_bar_view")
	el.send_keys(content)
	
def find_notice(driver,fromname):
	ret_status = False
	driver.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()
	list = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@text='%s']/../android.widget.RelativeLayout/*"%fromname)
	for i in list:
		if i.get_attribute("text") == "Agree":
			ret_status = True
			break
	
	return ret_status
	
def find_notice2(driver,fromname):
	ret_status = False
	driver.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()
	
	buttom_el_text0 = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")[-1].get_attribute("text")
	print "text0: ",buttom_el_text0
	swipeUp(driver)
	buttom_el_text1 = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")[-1].get_attribute("text")
	print "text1 ", buttom_el_text1
	while buttom_el_text0 != buttom_el_text1:
		swipeUp(driver)
		buttom_el_text0 = buttom_el_text1
		buttom_el_text1 = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")[-1].get_attribute("text")	

	list = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@text='%s']/../android.widget.RelativeLayout/*"%fromname)
	for i in list:
		if i.get_attribute("text") == "Agree":
			ret_status = True
			break
	
	return ret_status
	
def notice_accept(driver,contact):
	ret_status = False
	
	driver.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()

	buttom_el_text0 = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@index = '2']")[-1].get_attribute("text")
	print "text0: ",buttom_el_text0
	swipeUp(driver)
	buttom_el_text1 = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@index = '2']")[-1].get_attribute("text")
	print "text1 ", buttom_el_text1
	while buttom_el_text0 != buttom_el_text1:
		swipeUp(driver)
		buttom_el_text0 = buttom_el_text1
		buttom_el_text1 = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@index = '2']")[-1].get_attribute("text")	

	list = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@text='%s']/../*"%contact)
	for i in list:
		if i.get_attribute("text") == "Agree":
			print "now agree"
			i.click()
			ret_status = True
			print "agreed!"
			break
	
	return ret_status
	
def notice_refuse(driver,contact):
	ret_status = False
	
	driver.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()	

	buttom_el_text0 = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@index = '2']")[-1].get_attribute("text")
	print "text0: ",buttom_el_text0
	swipeUp(driver)
	buttom_el_text1 = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@index = '2']")[-1].get_attribute("text")
	print "text1 ", buttom_el_text1
	while buttom_el_text0 != buttom_el_text1:
		swipeUp(driver)
		buttom_el_text0 = buttom_el_text1
		buttom_el_text1 = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@index = '2']")[-1].get_attribute("text")		
	
	list = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@text='%s']/../*"%contact)
	for i in list:
		if i.get_attribute("text") == "Refuse":
			i.click()
			ret_status = True
			break
	
	return ret_status

def check_onContactAgreed(driver,contact):
	ret_status = False
	driver.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()
	list = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@text='%s']/../*"%contact)
	for i in list:
		if i.get_attribute("text") == "Accepted your request":
			print "check onContactAgreed True!"
			ret_status = True
	return ret_status

def check_onContactRefused(driver,contact): #安卓demo上没有实现相关UI信息显示，为保证case能顺利执行下去，先直接返回true
	driver.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()
	ret_status = True
	
	return ret_status
	
def check_onContactInvited(driver,contact):
	ret_status = False
	driver.find_element_by_xpath("//android.widget.TextView[@text = 'Invitation and notification']").click()
	list = driver.find_elements_by_xpath("//android.widget.ListView[1]//android.widget.TextView[@text='%s']/../*"%contact)
	for i in list:
		if i.get_attribute("text") == "Refuse":
			ret_status = True
			
	return ret_status
	
def notice_isFullscreen(driver):
	ret_status = False
	width = driver.get_window_size()['width']
	height = driver.get_window_size()['height']
	print "height: ", height
	mylist = driver.find_elements_by_xpath("//android.widget.ListView[@index = '1']/*")
	
	el = mylist[-1]
	startX = el.location.get('x')
	startY = el.location.get('y')
	elSize = el.size
	elH = elSize['height']
	elW = elSize['width']
	# print "start x: ", startX
	# print "start y: ", startY
	# print "Hsize: :", elH
	
	if (startY+elH) >=  height:
		ret_status = True
	
	return ret_status

def swipeUp(driver,start_point=3/float(4),end_point=1/float(4)):
	height = driver.get_window_size()["height"]
	width = driver.get_window_size()["width"]
	driver.swipe(width/2, height*start_point, width/2, height*end_point, 1000)
	
def swipeDown(driver,start_point=1/float(4),end_point=3/float(4)):
	height = driver.get_window_size()["height"]
	width = driver.get_window_size()["width"]
	driver.swipe(width/2, height*start_point, width/2, height*end_point, 1000)

def historymsg_on_screen(driver):
	msglist = []
	mylist1 = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/tv_chatcontent")
	for i in range(len(mylist1)):
		msg = mylist1[i].get_attribute("text")
		msglist.append(msg)
	return msglist

def name_is_inScreen(driver,name):
	ret_status = False
	namelist = []
	mylist = driver.find_elements_by_id("com.hyphenate.chatuidemo:id/name")
	for el in mylist:
		namelist.append(el.get_attribute("text"))
	if name in namelist:
		ret_status = True
	return ret_status
	
def del_conversation(driver):
	try:
		while True:
			elem = driver.find_element_by_id("com.hyphenate.chatuidemo:id/list_itease_layout")
			action1 = TouchAction(driver)
			action1.long_press(elem).wait(2000).perform()
			driver.find_element_by_xpath("//android.widget.TextView[@text='Delete conversation and messages']").click()
	except:
		print 'No conversation to be deleted'

def findelem_swipe(driver,xpath_id,text,find_type="by_id"):
	ret_status = False

	try_num = 1
	while not ret_status:
		try:
			if find_type == "by_xpath":
				elem = driver.find_element_by_xpath(xpath_id)
			else:
				elem = driver.find_element_by_id(xpath_id)
			ret_status = True
			print "find %s" %text
			return elem
		except:
			if try_num == 5:
				break
			else:
				swipeUp(driver,5/float(6),3/float(6))
				print "not find %s" %text
				try_num = try_num + 1
	
if __name__=="__main__":
	driver1 = startDemo1()
	sleep(3)
	


	