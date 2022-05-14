from bs4 import BeautifulSoup
import urllib.request
import requests
import re

#获取网页源代码
def getHtml(url):
    req = urllib.request.Request(url)
    webpage = urllib.request.urlopen(req)
    html = webpage.read()
    return html

#下载文件
def downloadPDF(url, title):
    #get请求
    file = requests.get(url)
    title = title + ".png"
    with open(title, "wb") as code:
        code.write(file.content)


if __name__ == '__main__':
  urlMed = "小破站资源/技术文献/教你如何制作温鑫PE的系统U盘/"
  #链接中含有汉字需要转换一下格式，如果有特殊符号，比如':'，直接转换则会导致无法识别，所以先转换再拼接
  urlMed_conv = urllib.parse.quote(urlMed)
  #获取网页源代码
  htmlRoot = getHtml('http://pan.win10sys.com/' + urlMed_conv)
  #解析
  soup = BeautifulSoup(htmlRoot, 'html.parser')  
  
  # 逐层查找<a>标签  
  for k in soup.find_all('a',target="_blank"):
      #剔除不含class属性的标签
      if (k.string is not '不想要') or (k.string is not '也不想要'): 
          # 通过标签进一步筛选链接，比如要求class属性是['classfix']
#          if k['class'] == ['clearfix']:
              # 拼接链接并读取
              HtmlNew = 'http://pan.win10sys.com/' + urlMed_conv + k['href']
              html = getHtml(HtmlNew)
               # 找个标签作为文件名，比如title
              title = k['id']
              # 解析PDF下载页面  
              soup2 = BeautifulSoup(html, 'html.parser')
               # 找第二层<a>标签
#              for k2 in soup2.find_all('a',href=True):
              for k2 in soup2.find_all('a',href=re.compile("png")):
#                  此处可再加判断，比如只读取class属性是['download-menu']的<a>：
#                  if k2['class'] == ['download-menu']:
                    HtmlNew2 = 'http://pan.win10sys.com/' + urlMed_conv + k2['href']
                    downloadPDF(HtmlNew2, title)
                    print("success:" + " " + title)
#          else:
#              print("剔除:" + ' ' + k)
      else:
          print("剔除:" + ' ' + k)


