## android auto
### appium测试环境部署与安装
1.  mac篇：http://www.jianshu.com/p/028dcbf51f1a
2.  widows篇：http://www.jianshu.com/p/9bb8278f7cde
3.  Linux篇：http://blog.csdn.net/gb112211/article/details/38385333

### 测试前准备
#### 　　1.连接设备：
　　准备两部测试设备，设备打开usb调试模式，然后通过USB连接到电脑，可在终端里输入：adb devices 查看，如果正确显示出设备串号，则设备连接成功：  
　　![connect devices](http://im-wiki.easemob.com/download/attachments/362722/adb_devices.png?api=v2)
#### 　　2.安装测试用app:  
#####  　　　两种方式安装app,任选一种  
　　  １. 扫码安装：直接扫描官网二维码，下载安装环信demo，环信demo扫码下载地址：http://easemob.com/download/im  
 　　　2. 提前下载好测试用的apk安装包后，通过adb命令向测试设备上安装app：adb -s <设备串号> install <安装包名>  
　　　![install apps](http://im-wiki.easemob.com/download/attachments/362722/install_apps.png?api=v2)  

#### 　　3.将测试设备的系统界面语言全都设置为英文  


### 测试执行  
Mac/ Linux:  
1. 执行 start_appium1.sh  
2. 执行 start_appium2.sh  
3. 执行 start_test.sh