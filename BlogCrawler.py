# -*- coding: utf-8 -*-

import urllib2 #打开url相关
import re #正则表达式

class BDTB:
    baseUrl = 'http://royburns.cn/'
    num1 = 1
    num2 = 1

    # 统计artical出现的次数
    def countArtical(self):
        html = self.getPage()
        reg = re.compile(r'article')
        items = reg.findall(html)
        countNumber = items.count("article")

        return countNumber

    #获取源代码
    def getPage(self):
        try:
            url = self.baseUrl
            request = urllib2.Request(url)
            response = urllib2.urlopen(request).read()
            return response
        except Exception,e:
            print e

    #截取字符串article之间的代码
    def getString(self):
        html = self.getPage()
        BDTB.num1 = html.index('<article',BDTB.num1)
        BDTB.num2 = html.index('</article>',BDTB.num2)
        BDTB.num1 = BDTB.num1+1
        BDTB.num2 = BDTB.num2+1
        return html[BDTB.num1:BDTB.num2]

    #匹配内容
    def getContent(self):
        articleNum = self.countArtical()
        f = open('text1.txt','w')
        f.write('[')

        for i in range(1,articleNum+1,2):
            article = self.getString()

            #获取h1之间的内容
            num1 = article.find('<h1')
            num2 = article.find('</h1>')
            s = article[num1:num2]
            re_h = re.compile('</?\w+[^>]*>') # HTML标签
            title = re_h.sub('', s) # 去掉HTML 标签

            #获取href后之间的内容
            num3 = s.index('href=')+6
            num4 = s.find('/">')
            href = s[num3:num4]

            #获取tag的内容
            num5 = article.find('tags')+6
            num6 = article.find('</footer>')
            getFooterCode1 = article[num5:num6] #获取s与</footer>之间的内容，将其新建为getFooterCode2

            reg = re.compile(r'tag/')
            tagsNumCode = reg.findall(getFooterCode1)
            tagsNum = tagsNumCode.count('tag/')
            #获取tag需要
            num7 = 0
            num8 = 0
            atag = []
            for m in range(tagsNum):
                num7 = getFooterCode1.index('<a',num7)
                num8 = getFooterCode1.index('</a>',num8)
                getTagCode = getFooterCode1[num7:num8]
                atag.append(re_h.sub('',getTagCode))#去掉html标签
                num7 = num7 + 1
                num8 = num8 + 1

            #标号
            j = (i+1)/2
            n = "%d"%j #将int类型数据转换成String

            #将内容写入文本
            f.write('{\n')
            f.write('"id": "'+n+'"\n')
            f.write('"title": "'+title+'"\n')
            f.write('"permalink": "'+href+'"\n')
            while tagsNum != 0:
                f.write('"tags": "'+atag[tagsNum-1]+'"\n')
                tagsNum = tagsNum - 1
            if (i+1) == articleNum:
                f.write('}\n')
            else:
                f.write('},')

        f.write(']\n')
        f.close()

bdtb = BDTB()
print 'start。。。。'
try:
    ss = bdtb.getContent()

except Exception,e:
    print e

print 'finish。。。。'