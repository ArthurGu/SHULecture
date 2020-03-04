'''
计院学术报告爬虫
FYear 年份
Month 报告月份
Day 日期
报告题目: artTitle.text
发布时间: artTime.text
报告人: outPerson.split('：')[1]
报告时间: ATime.text.split("：")[1]
报告地点: Apalce.text.split("：")[1]
内容:artInfo.text
'''
import requests
import re
from bs4 import BeautifulSoup
import traceback
# import pymysql
from table import Lecture
import datetime


def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        traceback.print_exc()
        return ""


def getArtlist(lst, artlisturl):
    html = getHTMLText(artlisturl)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a', attrs={'class': 'Normal'})
    for i in a:
        try:
            href = i.get('href')
            lst.append(href)
        except:
            traceback.print_exc()
            continue


def getArtlist2(lst, artlisturl):
    html = getHTMLText(artlisturl)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a', attrs={'class': 'linkfont1'})
    for i in a[:7]:
        try:
            href = i.get('href')
            lst.append(href)
        except:
            traceback.print_exc()
            continue


def getArtlist3(lst, artlisturl):
    html = getHTMLText(artlisturl)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a', attrs={'class': 'myTitle'})
    for i in a[:8]:
        try:
            href = i.get('href')[2:]
            lst.append(href)
        except:
            traceback.print_exc()
            continue


def getArticle(lst, autourl):
    for art in lst:
        url = autourl + art  # 每篇学术报告的link
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            content = ''
            soup = BeautifulSoup(html, 'html.parser')
            artInfo = soup.find('span', attrs={'id': 'dnn_ctr1319_ArticleDetails_ctl00_lblArticle'})  # content
            artTitle = soup.find('span', attrs={'class': 'shuHead'})  # 标题
            artTime = soup.find('span', attrs={'id': 'dnn_ctr1319_ArticleDetails_ctl00_lblDatePosted'})  # 发布时间
            Person = soup.find('p', string=re.compile('报 告 人'))  # 报告人
            ATime = soup.find('p', string=re.compile("报告时间"))  # 报告时间
            a = artInfo.find_all('p')
            for i in range(len(a)):
                # print(a[i].text)
                if re.search(r'报 告 人|报告时间|报告地点', a[i].text) == None:
                    if a[i].text != '\xa0':
                        content = content + a[i].text + '\n'
            # print(content)
            FYear = int(artTime.text[0:4])  # 年
            aMonth = re.split(r"月", ATime.text.split("：")[1])[0]  # 月份
            Month = aMonth[-2:]
            if '年' in Month:
                Month = Month.replace('年', '')
            elif Month[0] == '0':
                Month = Month.replace(Month[0], '')
            Month = int(Month)
            aDay = re.split(r"日", ATime.text.split("：")[1])[0]
            Day = aDay[-2:]
            if '月' in Day:
                Day = Day.replace('月', '')
            elif Day[0] == '0':
                Day = Day.replace(Day[0], '')
            Day = int(Day)
            # print(type(FYear), type(Day))
            Apalce = soup.find('p', string=re.compile("报告地点"))
            outPerson = " ".join(Person.text.split())
            # artInfo.text.replace('\\n', '\n')
            # print(artInfo.text)
            # infoDict.update({"报告题目": artTitle.text, "发布时间": artTime.text, "报告人": outPerson.split('：')[1],
            # "报告时间": ATime.text.split("：")[1], "报告地点": Apalce.text.split("：")[1]})
            date = str(FYear) + '-' + str(Month) + '-' + str(Day)
            n_date = datetime.datetime.now().date()
            a_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if n_date.__le__(a_date):
                lecture = Lecture(1, artTitle.text, outPerson.split('：')[1], ATime.text.split("：", 1)[1], FYear,
                                  Month, Day, Apalce.text.split("：")[1], content, 0)
                title = Lecture.query.filter_by(Title=artTitle.text, Lecturer=lecture.Lecturer).first()
                if title == None:
                    lecture.save()
            # with open(fpath, 'a', encoding='utf-8') as f: #将数据保存为txt格式
            # f.write(str(infoDict)+'\n')
            # print(infoDict)
        except:
            traceback.print_exc()
            continue


def getArticle2(lst, autourl):
    for art in lst:
        url = autourl + art  # 每篇学术报告的link
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, 'html.parser')
            infoDict = {}
            content = ''
            artInfo = soup.find('span', attrs={'class': 'ArticleContent'})
            artTitle = soup.find('span', attrs={'id': 'dnn_ctr51190_ArtDetail_lblTitle'}).text
            artTime = soup.find('span', attrs={'id': 'dnn_ctr51190_ArtDetail_lblDatePosted'}).text
            a = artInfo.find_all(attrs={'class': 'MsoNormal'})
            for i in range(len(a)):
                # print(a[i].text)
                if re.search(r'题    目|演 讲 人|时    间|地    点', a[i].text) == None:
                    if a[i].text != '\xa0':
                        content = content + a[i].text + '\n'
            # print(content)
            # for i in len(a):
            # if
            Atime = a[4].text.split('：', 1)[1]
            Aplace = a[5].text.split('：')[1]
            Person = a[2].text.split('：')[1]
            Year = int(Atime[:4])
            aMonth = re.split(r"月", Atime)[0]  # 月份
            Month = aMonth[-2:]
            if '年' in Month:
                Month = Month.replace('年', '')
            elif Month[0] == '0':
                Month = Month.replace(Month[0], '')
            Month = int(Month)
            aDay = re.split(r"日", Atime)[0]
            Day = aDay[-2:]
            if '月' in Day:
                Day = Day.replace('月', '')
            elif Day[0] == '0':
                Day = Day.replace(Day[0], '')
            Day = int(Day)
            # print(Year, Month, Day)
            date = str(Year) + '-' + str(Month) + '-' + str(Day)
            n_date = datetime.datetime.now().date()
            a_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if n_date.__le__(a_date):
                lecture = Lecture(2, artTitle, Person, Atime, Year, Month, Day, Aplace,
                                  content, 0)
                title = Lecture.query.filter_by(Title=artTitle, Lecturer=lecture.Lecturer).first()
                if title == None:
                    lecture.save()
                # print(a_date,'chaoshi')
            # else:
            # print(a_date,"weichaoshi")
            # print(type(date))
            # infoDict.update({"报告题目": artTitle, "发布时间": artTime, "报告人": Person,
            # "报告时间": Atime, "报告地点": Aplace})
            # print(infoDict)
            # print(artTitle)
        except:
            traceback.print_exc()
            continue


def getArticle3(lst, autourl):
    for art in lst:
        url = autourl + art  # 每篇学术报告的link
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, 'html.parser')
            infoDict = {}
            content = ''
            artInfo = soup.find('span', attrs={'class': 'ArticleContent'})
            artTitle = soup.find('span', attrs={'id': 'dnn_ctr66336_ArtDetail_lblTitle'}).text
            artTime = soup.find('span', attrs={'id': 'dnn_ctr66336_ArtDetail_lblDatePosted'}).text
            a = artInfo.find_all('div')
            for i in range(len(a)):
                # print(a[i])
                if re.search(r'时间|时    间|主讲人|演讲人|题目|地点|地    点', a[i].text) == None:
                    if a[i].text != '\xa0':
                        content = content + a[i].text + '\n'
            # print(content)
            match = re.search(r'[演讲|主讲]人', a[4].text)
            i = 4
            if match == None:
                i = i + 2
            Person = a[i].text.split('：')[1]
            Atime = a[i + 1].text.split('：', 1)[1]
            Aplace = a[i + 2].text.split('：')[1]
            Year = int(Atime[:4])
            aMonth = re.split(r"月", Atime)[0]  # 月份
            Month = aMonth[-2:]
            if '年' in Month:
                Month = Month.replace('年', '')
            elif Month[0] == '0':
                Month = Month.replace(Month[0], '')
            Month = int(Month)
            aDay = re.split(r"日", Atime)[0]
            Day = aDay[-2:]
            if '月' in Day:
                Day = Day.replace('月', '')
            elif Day[0] == '0':
                Day = Day.replace(Day[0], '')
            Day = int(Day)
            # print(Year, Month, Day)
            date = str(Year) + '-' + str(Month) + '-' + str(Day)
            n_date = datetime.datetime.now().date()
            a_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if n_date.__le__(a_date):
                lecture = Lecture(4, artTitle, Person, Atime, Year, Month, Day, Aplace,
                                  content, 0)
                title = Lecture.query.filter_by(Title=artTitle, Lecturer=lecture.Lecturer).first()
                if title == None:
                    lecture.save()
            # print(Aplace)
            # infoDict.update({"报告题目": artTitle, "发布时间": artTime, "报告人": Person,
            # "报告时间": Atime, "报告地点": Aplace})
            # print(infoDict)
        except:
            traceback.print_exc()
            continue


def getArticle4(lst, autourl):
    for art in lst:
        url = autourl + art  # 每篇学术报告的link
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, 'html.parser')
            infoDict = {}
            content = ''
            artInfo = soup.find('div', attrs={'class': 'c188358_content'})
            artTitle = soup.find('span', attrs={'class': 'c188358_title'}).text
            artTime = soup.find('span', attrs={'class': 'c188358_date'}).text
            a = soup.find('div', attrs={'class': 'c188358_content'})
            b = artInfo.find_all('p')
            for i in range(len(b)):
                # print(b[i].text)
                if re.search(r'时间|报告题目|演讲人|题目|地点|报告人', b[i].text) == None:
                    if b[i].text != '\xa0':
                        content = content + b[i].text + '\n'
            # print(content)
            Person = a.find_all('p')[1].text
            if re.search('人', Person) == None:
                Person = a.find_all('p')[3].text
                if re.search('人', Person) == None:
                    Person = a.find_all('p')[6].text
            Person = re.split('[：:]', Person)[1]
            Atime = a.find_all('p')[2].text
            if re.search('时间', Atime) == None:
                Atime = a.find_all('p')[1].text
                if re.search('时间', Atime) == None:
                    Atime = a.find_all('p')[3].text
            Atime = Atime.split('：', 1)[1]
            Year = int(Atime[:4])
            aMonth = re.split(r"月", Atime)[0]  # 月份
            Month = aMonth[-2:]
            if '年' in Month:
                Month = Month.replace('年', '')
            elif Month[0] == '0':
                Month = Month.replace(Month[0], '')
            Month = int(Month)
            aDay = re.split(r"日", Atime)[0]
            Day = aDay[-2:]
            if '月' in Day:
                Day = Day.replace('月', '')
            elif Day[0] == '0':
                Day = Day.replace(Day[0], '')
            Day = int(Day)
            # print(Year, Month, Day)
            Aplace = a.find_all('p')[3].text
            if re.search('地点', Aplace) == None:
                Aplace = a.find_all('p')[2].text
                if re.search('地点', Aplace) == None:
                    Aplace = a.find_all('p')[4].text
            Aplace = Aplace.split('：')[1]
            date = str(Year) + '-' + str(Month) + '-' + str(Day)
            n_date = datetime.datetime.now().date()
            a_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if n_date.__le__(a_date):
                lecture = Lecture(8, artTitle, Person, Atime, Year, Month, Day, Aplace,
                                  content, 0)
                title = Lecture.query.filter_by(Title=artTitle, Lecturer=lecture.Lecturer).first()
                if title == None:
                    lecture.save()
            # infoDict.update({"报告题目": artTitle, "发布时间": artTime, "报告人": Person,
            # "报告时间": Atime, "报告地点": Aplace})
            # print(infoDict)
        except:
            traceback.print_exc()
            continue


def getArticle5(lst, autourl):
    for art in lst:
        url = autourl + art  # 每篇学术报告的link
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, 'html.parser')
            infoDict = {}
            content = ''
            artInfo = soup.find('span', attrs={'class': 'ArticleContent'})
            artTitle = soup.find('span', attrs={'id': 'dnn_ctr60055_ArtDetail_lblTitle'}).text
            artTime = soup.find('span', attrs={'id': 'dnn_ctr60055_ArtDetail_lblDatePosted'}).text
            a = artInfo.find_all('p')
            for i in range(len(a)):
                # print(b[i].text)
                if re.search(r'时间|报告题目|演讲人|题目|地点|报告人[：:]', a[i].text) == None:
                    if a[i].text != '\xa0':
                        content = content + a[i].text + '\n'
            # print(content)
            Atime = a[0].text
            Aplace = a[1].text
            Person = a[2].text
            if re.search(r'时间', Atime) == None:
                if re.search(r'题目', Atime) == None:
                    Atime = a[1].text
                    Person = a[0].text
                    Aplace = a[2].text
                else:
                    Atime = a[2].text
                    Person = a[1].text
                    Aplace = a[3].text
                for i in range(3):
                    if re.search(r'时间', Atime) == None:
                        Atime = a[2 + i].text
            Atime = "".join(re.split(r'[：:]', Atime, 1)[1].split())
            Person = re.split(r'[：:]', Person, 1)[1]
            Aplace = re.split(r'[：:]', Aplace, 1)[1]
            Year = int(Atime[:4])
            aMonth = re.split(r"月", Atime)[0]  # 月份
            Month = aMonth[-2:]
            if '年' in Month:
                Month = Month.replace('年', '')
            elif Month[0] == '0':
                Month = Month.replace(Month[0], '')
            Month = int(Month)
            aDay = re.split(r"日", Atime)[0]
            Day = aDay[-2:]
            if '月' in Day:
                Day = Day.replace('月', '')
            elif Day[0] == '0':
                Day = Day.replace(Day[0], '')
            Day = int(Day)
            date = str(Year) + '-' + str(Month) + '-' + str(Day)
            n_date = datetime.datetime.now().date()
            a_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if n_date.__le__(a_date):
                lecture = Lecture(16, artTitle, Person, Atime, Year, Month, Day, Aplace,
                                  content, 0)
                title = Lecture.query.filter_by(Title=artTitle, Lecturer=lecture.Lecturer).first()
                if title == None:
                    lecture.save()
            # infoDict.update({"报告题目": artTitle, "发布时间": artTime, "报告人": Person,
            #  "报告时间": Atime, "报告地点": Aplace})
            # print(infoDict)
        except:
            traceback.print_exc()
            continue


def sp():
    Url = 'http://cs.shu.edu.cn/Default.aspx?tabid=556'  # 学术报告栏
    Aurl = 'http://cs.shu.edu.cn/'  # 计院url
    Murl = 'http://www.ms.shu.edu.cn/Default.aspx?tabid=27399'  # 管院报告栏
    MaUrl = 'http://www.ms.shu.edu.cn'  # 管院url
    Jurl = 'http://www.soe.shu.edu.cn/Default.aspx?tabid=35742'  # 经院报告栏
    JaUrl = 'http://www.soe.shu.edu.cn'  # 经院url
    Turl = 'http://www.ce.shu.edu.cn/index/xsbg.htm'  # 土木报告栏
    TaUrl = 'http://www.ce.shu.edu.cn'
    Burl = 'http://www.bio.shu.edu.cn/Default.aspx?tabid=31648&mid=60055&ShowAll=true'  # 生科报告栏
    BaUrl = 'http://www.bio.shu.edu.cn'
    slist = []
    glist = []
    jlist = []
    tlist = []
    blist = []
    getArtlist2(blist, Burl)
    getArticle5(blist, BaUrl)
    getArtlist3(tlist, Turl)  # 土木
    # print(tlist)
    getArticle4(tlist, TaUrl)
    getArtlist(slist, Url)  # 计院
    getArticle(slist, Aurl)
    getArtlist2(glist, Murl)  # 管院
    getArticle2(glist, MaUrl)
    getArtlist2(jlist, Jurl)  # 经院
    getArticle3(jlist, JaUrl)


def update():
    lectures = Lecture.query.order_by(Lecture.Year, Lecture.Month, Lecture.Day).all()
    n_date = datetime.datetime.now().date()
    print(n_date)
    for lecture in lectures:
        Year = lecture.Year
        Month = lecture.Month
        Day = lecture.Day
        date = str(Year) + '-' + str(Month) + '-' + str(Day)
        a_date = datetime.date(Year,Month,Day)
        # a_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        # print(type(a_date),type(n_date))
        if n_date.__le__(a_date):
            print(lecture.Year, lecture.Month, lecture.Day)
            break
        else:
            lecture.remove()
            print("delete", lecture.Year, lecture.Month, lecture.Day)
    print(lectures)


if __name__ == '__main__':
    # sp()
    update()
