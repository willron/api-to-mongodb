# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jsontest', '0002_auto_20150708_0545'),
    ]

    operations = [
        migrations.DeleteModel(
            name='jsontestdb',
        ),
    ]
