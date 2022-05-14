# encoding: utf-8
# author: walker
# date: 2018-06-11
# summary: 使用 requests 下载大文件

import time
import requests

# 下载一个大文件
def DownOneFile(srcUrl, localFile):
    print('%s\n --->>>\n  %s' % (srcUrl, localFile))
    
    startTime = time.time()
    with requests.get(srcUrl, stream=True) as r:
        contentLength = int(r.headers['content-length'])
        line = 'content-length: %dB/ %.2fKB/ %.2fMB'
        line = line % (contentLength, contentLength/1024, contentLength/1024/1024)
        print(line)
        downSize = 0
        with open(localFile, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                downSize += len(chunk)
                line = '%d KB/s - %.2f MB， 共 %.2f MB'
                line = line % (downSize/1024/(time.time()-startTime), downSize/1024/1024, contentLength/1024/1024)
                print(line, end='\r')
                if downSize >= contentLength:
                    break
        timeCost = time.time() - startTime
        line = '共耗时: %.2f s, 平均速度: %.2f KB/s'
        line = line % (timeCost, downSize/1024/timeCost)
        print(line)

if __name__ == '__main__':
    f=open('Challenge 2011 Training Set A.txt',"r")
    for line in f.readlines():
        srcUrl= line.split('>')[0][:-1]
        files=srcUrl.split('/')[-1]
        localFile ='F:/PhysioBank_Databases/pc2011/'+ files
        DownOneFile(srcUrl, localFile)
    f.close()