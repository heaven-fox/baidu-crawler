# coding: utf-8
import wget
import os


# 接收参数说明
# song_list: 二元组(sname, durl)
# sname: 歌曲名
# durl: 下载链接
def download_all(song_list, base, cur, size):
    # 判断cur对应目录是否存在
    # 若存在, 继续判断文件是否存在
    # 否则, 创建新文件
    # 否则, 创建新目录
    c_dir = base + cur + '/'
    if not os.path.exists(c_dir):
        os.mkdir(c_dir)
    counter = 1
    for l in song_list:
        sname = l[0] + '.mp3'
        url = l[1]
        # 约定'zzz': url为空
        if url == 'zzz':
            print '歌曲%s已下架' % sname
            continue
        elif os.path.isfile(c_dir + sname):
            print u'%s已下载' % sname
            continue
        print(u'正在下载%s' % sname)
        try:
            print u'下载进度%d/%d' % (counter, size)
            print(wget.download(url, c_dir + sname))
        except IOError:
            print u'%s解析错误, 略过当前歌曲' % url
            continue
        except:
            print u'未知错误'
        print(u'%s下载完毕' % sname)
        counter += 1
    print u'下载%s的歌曲完成' % cur