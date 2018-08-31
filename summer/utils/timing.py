import newSpider
def test():
    print("123")
schedule.every().day.at("05:00").do(get_detectiom(user_id,pwd,email):)
schedule.every().day.at("17:00").do(get_detectiom(user_id,pwd,email):)
while 1:
    schedule.run_pending()
# 这个脚本会再每天的05:00和17:00调用test()函数，方法不能传入参数
# test不需用加()，只需传入函数名称