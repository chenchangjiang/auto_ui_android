#coding=utf-8
import requests
import json

def server_config(test_env,test_type,test_im):
	config = {"ebs":{"rest":"a1.easemob.com","ejabberd_gray":"182.92.239.119:5222","msync_gray":"60.205.128.208:443",\
				"ejabberd":"im1.easemob.com","msync":"msync-im1.easemob.com"},\
		"k8s_sdb":{"rest":"118.193.28.212:31080","ejabberd":"118.193.28.212:31092","msync":"118.193.28.212:31097"},\
		"vip1":{"rest":"a1-vip1.easemob.com","ejabberd":"im1-vip1.easemob.com","msync":"msync-im1-vip1.easemob.com:443"},\
		"vip5":{"rest":"a1-vip5.easemob.com","ejabberd":"im1-vip5.easemob.com","msync":"101.37.226.88:443"},\
		"vip6":{"rest":"a1-vip6.easemob.com","ejabberd":"im1-vip6.easemob.com","msync":"60.205.85.241:6717"},\
		"vip7":{"rest":"a1-vip7.easemob.com","ejabberd":"im1-vip7.easemob.com:5222","msync":"msync-vip7.easemob.com:6717"},\
		"aws":{"rest":"a1-pro4.easemob.com","ejabberd":"im1-pro4.easemob.com:5222","msync":"msync-pro4.easemob.com:6717"},\
		}
	if test_type == "gray":
		im = test_im + "_" + test_type
	else:
		im = test_im
	try:
		rest_server = config[test_env]["rest"]
		im_server = config[test_env][im]
		server = [rest_server, im_server]
		return server
	except KeyError:
		raise Exception("some config not find, check again.")

def test_parameter(test_env,appkey,get_token,resturl):
    orgapp = appkey.split("#")
    org = orgapp[0]
    app = orgapp[1]
    token_env = env_token(test_env,get_token,resturl)
    token = token_env[0]
    im_token = token_env[1]
    headers = {'Content-Type':'application/json','Authorization':'Bearer '+token}
    imheaders = {'Content-Type':'application/json','Authorization':'Bearer '+im_token}
    return [org, app, token, headers]

def org_token(test_env,resturl):
	parameter = {"ebs":{"orgname":"easemobdemoadmin","orgpwd":"thepushbox123"},\
				"k8s_sdb":{"orgname":"easemob","orgpwd":"easemob"},\
				"vip1":{"orgname":"easemobdemovip1admin","orgpwd":"thepushbox"},\
				"vip5":{"orgname":"vip5demoadmin","orgpwd":"thepushbox"},\
				"vip6":{"orgname":"admin","orgpwd":"123456"},\
				"vip7":{"orgname":"","orgpwd":""},\
				"aws":{"orgname":"admin","orgpwd":"1234567"}				
				}
	orgname = parameter[test_env]["orgname"]
	orgpwd = parameter[test_env]["orgpwd"]
	token = rest_getorgtoken(resturl,orgname,orgpwd)
	return token

def env_token(test_env,get_token,resturl):
	parameter = {"ebs":{"token":"YWMtImJ7VKzAEeeBehvyqCjuuAAAAAAAAAAAAAAAAAAAAAGP-MBq3AgR45fkRZpPlqEwAQMAAAFe__NGEgBPGgB7ws_kUZrWmXNdQhY95AhP_3ODyzQDrf2zAyvAb7AaPA"},\
                "k8s_sdb":{"token":"YWMtv82_qp0xEeeqiHXfi5VoRAAAAV_O_eCaUvYTSJDoP7zgUveIjnlRoDj-n2Y"},\
                "vip1":{"token":"YWMtKjipeoL-EeekNuv9745IpgAAAV8jRw2H42rOKOMUSBYTXF2mxiIwfooVey8"},\
                "vip5":{"token":"YWMtMq0PSq4-EeejI62A2cz8sgAAAAAAAAAAAAAAAAAAAAEQ9tSAuFkR5aTJWWIOBU6WAQMAAAFfCbsqfQBPGgCmAr-IUTMDHy56VYsGTMuGsqMJaVQgvsGRZsMJxCmSag"},\
                "vip6":{"token":"YWMtaOrLOK4-EeeaM92Bz9Xk2gAAAWA-uh33z6v-WGf7IBzvWe1jLauP09msU90"},\
                "vip7":{"token":"YWMtcinYcL7mEeeJziMwCB3S9gAAAWCr4ud3osO2KZE0yAYFYdDHuBMC6Tov82o"},\
                "aws":{"token":"YWMtcAacrq49Eee_xJeRGpdneAAAAWA-s77UqUd0Gvk_3Kvy5OmNxLMBKUSFun0"},\
                "im_token":"YWMt39RfMMOqEeKYE_GW7tu81ABCDT71lGijyjG4VUIC2AwZGzUjVbPp_4qRD5k"
                }  
	if get_token == "yes":
		token = org_token(test_env,resturl)
	else:
	    token = parameter[test_env]["token"]
	im_token = parameter["im_token"]
	return [token, im_token]

def rest_getorgtoken(resturl,orgname,orgpwd):
	myurl = 'http://%s/management/token' %resturl
	token_headers = {'Accept':'application/json','Content-Type':'application/json'}
	data = {"grant_type":"password","username":orgname,"password":orgpwd}
	
	resp = requests.post(url=myurl,headers=token_headers,data=json.dumps(data))
	token = json.loads(resp.text).get("access_token")
	return token

if __name__ == '__main__':
	token = org_token("ebs","a1.easemob.com")
	print token
