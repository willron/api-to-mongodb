import json
from django.shortcuts import HttpResponse
from .models import *
import pymongo
con = pymongo.MongoClient('192.168.0.228', 27017)
zxpdb = con.zxpdb

def insert(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        table = str(received_json_data['table'])
        string = "zxpdb.%s" %table
        muser = eval(string)
        print string
        #TABLE = aaa
        #muser = zxpdb.user1 # table
        # testkey = received_json_data['test_key']
        # testvalue = received_json_data['test_value']
        # jsonstr = json.dumps(received_json_data)
        # print received_json_data
        # print jsonstr
        # jsontestdb.objects.create( test_key = testkey.encode('utf-8'), test_value = received_json_data)
        muser.save(received_json_data)
        return HttpResponse('OK')
    return HttpResponse('it was GET request')

def select(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        # table = str(received_json_data['table'])
        string = "zxpdb.%s" %table
        muser = eval(string)

        all1 = muser.find(received_json_data)
        list1 = []
        for i in all1:
            list1.append(i)
        print list1
    return HttpResponse('it was GET request')

def update(request):
    pass
