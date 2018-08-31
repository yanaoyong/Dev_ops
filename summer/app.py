from flask import Flask,render_template,request
from a6 import get
from pymongo import MongoClient

app=Flask(__name__)

client = MongoClient("192.168.1.129",27017)
db = client["mydb4"]
col = db["students"]

def Get(user_id,password):
    info = col.find({"user_id":user_id})
    if info.count() == 1:
        if info[0]["passwd"]==password:
            return info[0]
        else:
            return {}
    elif info.count()==0:
        info = get(user_id,password)
        col.insert(info)
        return info


@app.route("/",methods=["POST","GET"])
def index():
    return render_template("index.html")


@app.route("/info",methods=["POST","GET"])
def showinfo():
    if request.method=="GET":
        return "没有好好填学号与密码吧"
    elif request.method=="POST":
        user_id=request.form["username"]
        password=request.form["password"]
        infos=Get(user_id,password)
        return render_template("info.html",content=infos)
    return render_template("index.html")

@app.errorhandler(405)
def error(e):
    content = "405你协议弄错了吧"
    return render_template("error.html",content = content)
@app.errorhandler(404)
def error(e):
    content = "404你地址弄错了吧"
    return render_template("error.html",content = content)

if __name__=='__main__':
    app.run(host="192.168.1.129",port=8080)
