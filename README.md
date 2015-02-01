# baidu-crawler
###环境配置:
#####1.python环境: 
######python -V == 2.7.9
######python modules, 详见requirements.txt定义
#####2.数据库配置:
######conf目录下的cm.py文件记录着redis及mysql数据库的相关配置信息, 歌曲下载后的存储路径，当然, 你也可自定义
###使用说明:
######直接运行main.py, 获取歌手对应的歌曲url, 部署一层redis做缓冲, 最终将其存入mysql; 读取mysql的记录,下载url对应的歌曲。
###不足之处:
######单线程, 阻塞态, 容易受网络条件影响, 程序被阻塞, 无法进行后续的下载任务