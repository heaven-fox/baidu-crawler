# coding: utf-8
import wget
import os


# 接收参数说明
# song_list: 二元组(sname, durl)
# sname: 歌曲名
# durl: 下载链接
def download_with_singer(song_list, base, singer, size):
    # 判断cur对应目录是否存在
    # 若存在, 继续判断文件是否存在
    # 否则, 创建新文件
    # 否则, 创建新目录
    c_dir = base + singer + '/'
    if not os.path.exists(c_dir):
        os.mkdir(c_dir)
    counter = 1
    for l in song_list:
        sname = l[0] + '.mp3'
        url = l[1]
        # 约定'zzz': url为空
        if url == 'zzz':
            print u'歌曲%s已下架' % sname
            continue
        elif os.path.isfile(c_dir + sname):
            print u'%s已下载' % sname
            continue
        try:
            print(u'正在下载%s' % sname)
            print u'下载进度%d/%d' % (counter, size)
            print(wget.download(url, c_dir + sname))
            print(u'%s下载完毕' % sname)
        except IOError:
            print u'%s解析错误, 略过当前歌曲' % url
        except:
            print u'未知错误'
        counter += 1
    print u'下载%s的歌曲完成' % singer


def download_with_sname(sname, data, base_dir):
    """
    根据歌曲名下载对应的歌曲
    :param sname: 歌曲名
    :param data: 二元组(author, durl)
    :param base_dir: 歌曲资源基路径
    :return:
    """
    sname += '.mp3'
    for item in data:
        author = item[0]
        t_dir = base_dir + author + '/'
        if not os.path.exists(t_dir):
            os.mkdir(t_dir)
        durl = item[1]
        if durl == 'zzz':
            print('歌曲已下架')
            continue
        elif os.path.isfile(t_dir + sname):
            print('歌曲已下载')
            continue
        try:
            print(u'正在下载%s的%s' % (author, sname))
            wget.download(durl, t_dir + sname)
            print('下载完毕')
        except Exception:
            print('下载出现错误')