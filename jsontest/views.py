#coding:utf-8
import json, pymongo, md5, time
from django.shortcuts import HttpResponse

#连接数据库
con = pymongo.MongoClient('192.168.0.228', 27017)
zxpdb = con.zxpdb

def insert(request):
    #数据插入
    if request.method == 'POST':    #POST提交
        received_json_data = json.loads(request.body)   #获取POST请求主体

        if not 'table' in received_json_data:   #判断是否存在table键
            return HttpResponse('Need table')

        table = str(received_json_data['table'])    #获取table字符串
        string = "zxpdb.%s" %table  #生成表字符串

        muser = eval(string)    #字符串导入为变量,使表生效
        TIME = time.time()  #获取时间戳
        unMD5str = str(received_json_data) + str(TIME)  #将POST请求主体转为字符串再与时间戳合并
        MD5str = md5.new(unMD5str)  #用合并字符生成MD5值当id字段
        ID = MD5str.hexdigest()

        received_json_data['id'] = ID   #将id字段加入到请求主体

        muser.save(received_json_data)  #将请求主体写入数据库
        return HttpResponse(ID)
    return HttpResponse('it was GET request')

def select(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)

        if not 'table' in received_json_data:   #判断是否存在table键
            return HttpResponse('Need table')

        table = str(received_json_data['table'])
        string = "zxpdb.%s" %table
        muser = eval(string)

        all1 = muser.find(received_json_data, projection={'_id': False})

        list1 = []
        for i in all1:
            list1.append(i)
        jsonstr = json.dumps(list1, ensure_ascii=False)
        return HttpResponse(jsonstr)
    return HttpResponse('it was GET request')


def update(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)

        if not (('id' in received_json_data) and ('table' in received_json_data)):
             return HttpResponse('Need table and id')
        table = str(received_json_data['table'])
        searchid = str(received_json_data['id'])
        readyupdate = received_json_data['readyupdate']

        if 'id' in readyupdate:
            return HttpResponse('Do not change id')

        string = "zxpdb.%s" %table
        muser = eval(string)
        muser.find_one_and_update({"id":searchid},{"$set":readyupdate})

        return HttpResponse('OK')
    return HttpResponse('it was GET request')
