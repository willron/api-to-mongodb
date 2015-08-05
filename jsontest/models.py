from django.db import models
from mongoengine import *
# from testjson.settings import ZhengXuPengTest


class jsontestdb(Document):
    # test_key = StringField(req)
    test_key = StringField(required=True)
    test_value = StringField()

# class jsontestdb(models.Model):
#     # test_key = StringField(req)
#     test_key = CharField()
#     test_value = CharField()