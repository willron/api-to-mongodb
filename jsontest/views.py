#coding:utf-8
import json, pymongo, md5, time, re
from django.shortcuts import HttpResponse

#连接数据库
con = pymongo.MongoClient('192.168.0.228', 27017)
zxpdb = con.zxpdb

def insert(request):
    #数据插入
    if request.method == 'POST':    #POST提交
        try:
            received_json_data = json.loads(request.body)   #获取POST请求主体
        except StandardError, e:
            return HttpResponse('just json')
        if 'table' in received_json_data:
        #判断表名是否有效
            checktablename = str(received_json_data['table'])
            ret = re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', checktablename)
            if not ret:
               return HttpResponse('invalid table name')
        else:
            return HttpResponse('Need table')

        table = str(received_json_data['table'])    #获取table字符串
        string = "zxpdb.%s" % table  #生成表字符串

        nowtime = time.time()  #获取时间戳
        unmd5str = str(received_json_data) + str(nowtime)  #将POST请求主体转为字符串再与时间戳合并
        md5str = md5.new(unmd5str)  #用合并字符生成MD5值当id字段
        dataid = md5str.hexdigest()
        received_json_data['id'] = dataid   #将id字段加入到请求主体

        try:
            muser = eval(string)    #字符串导入为变量,使表生效
            muser.save(received_json_data)  #将请求主体写入数据库
            return HttpResponse(dataid)
        except StandardError, e:
            return HttpResponse('StandardError:%s' % e)

    return HttpResponse('it was GET request')

def select(request):
    if request.method == 'POST':
        try:
            received_json_data = json.loads(request.body)   #获取POST请求主体
        except StandardError, e:
            return HttpResponse('just json')

        if 'table' in received_json_data:
        #判断表名是否有效
            checktablename = str(received_json_data['table'])
            ret = re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', checktablename)
            if not ret:
               return HttpResponse('invalid table name')
        else:
            return HttpResponse('Need table')

        try:
            #引入表名并搜索
            table = str(received_json_data['table'])
            string = "zxpdb.%s" % table
            muser = eval(string)

            #搜索关键字,默认ID不显示.因为显示出来会面的json格式化函数
            all1 = muser.find(received_json_data, projection={'_id': False})

            #搜索结果以列表形式展示
            list1 = []
            for i in all1:
                list1.append(i)

            #判断搜索结果是否为空
            if list1:
                jsonstr = json.dumps(list1, ensure_ascii=False)
                return HttpResponse(jsonstr)
            else:
                return HttpResponse('None')

        except StandardError, e:
            return HttpResponse('StandardError:%s' % e)

    return HttpResponse('it was GET request')


def update(request):
    if request.method == 'POST':
        try:
            received_json_data = json.loads(request.body)   #获取POST请求主体
        except StandardError, e:
            return HttpResponse('just json')

        if not (('id' in received_json_data) and ('table' in received_json_data)):
        #判断是否存在table名和id项
            return HttpResponse('Need table and id')

        #判断表名是否存在
        if not received_json_data['table'] in zxpdb.collection_names():
            return HttpResponse('no table %s in DataBase' % received_json_data['table'])

        #获取表名,id值和打算修改的数据项
        table = str(received_json_data['table'])
        searchid = str(received_json_data['id'])
        readyupdate = received_json_data['readyupdate']

        #判断id值是否存在于修改数据项内,如果存在则提示不能修改id
        if 'id' in readyupdate:
            return HttpResponse('Do not change id')

        #引入表名,搜索与修改数据
        try:
            string = "zxpdb.%s" % table
            muser = eval(string)
            ret = muser.find_one_and_update({"id": searchid}, {"$set": readyupdate})

            if ret:
            #如修改成功,会返回修改的数据.不成功则返回None
                return HttpResponse('OK')
            else:
                return HttpResponse('update false')

        except StandardError, e:
            return HttpResponse('StandardError:%s' % e)

    return HttpResponse('it was GET request')
