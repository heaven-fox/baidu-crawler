#!/bin/bash

# wget cookie
wget --post-data='user=_向他人学习&pass=pengxiyang1991&submit=Login' --save-cookies=cookies.txt --keep-session-cookies http://pan.baidu.com
wget --referer=http://pan.baidu.com --cookie=on --load-cookies=cookies.txt --keep-session-cookies --save-cookies=cookies.txt http://file.qianqian.com//data2/music/122871878/122871878.mp3?xcode=b84c8925557de57388a08f215e9bd3c5a51358eed5180bdeu0026src=u0022http%3A%2F%2Fpan.baidu.com%2Fshare%2Flink%3Fshareid%3D904310480%26uk%3D4232889411u0022
