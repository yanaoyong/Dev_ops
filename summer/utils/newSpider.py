import re
import hashlib
import smtplib
from email.mime.text import MIMEText

from email.header import Header
import traceback
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from config import dbconfig

Url = "http://221.233.24.23/eams/login.action"
InfoUrl = "http://221.233.24.23/eams/stdDetail.action"
GradeUrl = "http://221.233.24.23/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR"

def getInfos(user_id,password,email):
    driver = webdriver.PhantomJS()
    driver.get(Url)
    username = driver.find_element_by_id("username")
    passwd = driver.find_element_by_id("password")
    submit = driver.find_element_by_name("submitBtn")
    username.send_keys(user_id)
    passwd.send_keys(password)
    tm.sleep(1)
    submit.click()
    driver.get(InfoUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    infos = {}
    keys = []
    vals = []
    trs = soup.find_all("tr")
    for tr in trs[1:-1]:
        tds = tr.find_all("td")
        if len(tds) == 0:
            continue
        key1 = tds[0].getText()[:-1]
        val1 = tds[1].getText()
        key2 = tds[2].getText()[:-1]
        val2 = tds[3].getText()
        keys.append(key1)
        keys.append(key2)
        vals.append(val1)
        vals.append(val2)
    for i in range(len(vals)-1):
        infos[keys[i]] = vals[i]
    print(infos)
    
    driver.get(GradeUrl)
    html = driver.page_source
    soup = BeautifulSoup(html,"lxml")
    tables = soup.find_all("table")
    point_trs = tables[0].find_all("tr")
    grades_trs = tables[1].find_all("tr")
    
    print(point_trs)
    print(grades_trs)
    
    
    time = "2"+point_trs[-1].getText().split("2")[-1]
    all_point_tds = point_trs[-2].find_all("th")
    all_point = {}
    all_point_keys = ["种类","必修门数","必修总学分","必修平均绩点"]
    point_keys = []
    grade_keys = []
    points = []
    grades = []
    for idx, all_point_td in enumerate(all_point_tds):
        all_point[all_point_keys[idx]] = all_point_td.getText()
    for point_th in point_trs[0].find_all("th"):
        point_keys.append(point_th.getText())
    for grade_th in grades_trs[0].find_all("th"):
        grade_keys.append(grade_th.getText())
    print("-----"*20)
    print(all_point)
    for point_tr in point_trs[1:-2]:
        point = {}
        point_tds = point_tr.find_all("td")
        for idx, point_td in enumerate(point_tds):
            point[point_keys[idx]] = point_td.getText()
        points.append(point)
    print(points)
    print("-----"*20)
    for grades_tr in grades_trs[1:]:
        grade = {}
        grades_tds = grades_tr.find_all("td")
        for idx, grade_td in enumerate(grades_tds):
            grade[grade_keys[idx]] = grade_td.getText().strip()
        grades.append(grade)
    print(grades)
    infos["统计时间"] = time
    infos["绩点"] = points
    infos["总绩点"] = all_point
    infos["成绩"] = grades
    infos["user_id"] = user_id
    infos["passwd"] = password
    return infos


def get_detectiom(user_id,pwd,email):
    '''
    先从数据库获取信息，判断是否过期，不过期则返回，否则重新抓取并更新数据库并且发送更新邮件给用户
    '''  
    user_id=str(user_id)
    client = MongoClient(dbconfig["mongodb"],dbconfig["mondgodb_port"])
    table=client[dbconfig["db"]][dbconfig["table"]]
    info=table.find({"学号":user_id})
    if info.count():
        if time.time()-info[0]["时间戳"] < 3600*24:
            return info[0]
        else:
            info = getInfos(user_id,password,email)
            if info["状态"]=="正常":
                table.update_one({"学籍信息.学号":user_id},info)
            return info
            send_mail(email)
    else:
        # 数据库中没有该用户信息
        info=getInfos(user_id,password,email)
        table.insert(info)
        return info


def send_mail(email, mail_host='smtp.163.com', port=25):
  msg = MIMEText("请到http://192.168.1.137 中查看你的更新后的成绩")  # 邮件内容
  message['Subject'] = Header("成绩更新提醒", 'utf-8') # 邮件主题
  msg['From'] = 15908609620@163.com   # 发送者账号
  message['To'] = Header(email, 'utf-8') # 收件人
  smtp = smtplib.SMTP(mail_host, port=port)   # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
  smtp.login("15908609620@163.com", "密码")          # 登录发送者的邮箱账号，密码
  # 参数分别是 发送者，接收者
  smtp.sendmail("1508609620@163.com", email, msg.as_string())
  print('email send success.')