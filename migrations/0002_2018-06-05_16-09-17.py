# -*- coding: utf-8 -*-
# Generated by Pony ORM 0.8-dev on 2018-06-05 16:09
from __future__ import unicode_literals

from pony import orm
from pony.migrate import diagram_ops as op

dependencies = ['0001_initial']

operations = [
    op.AddAttr('StoredItem', 'test', orm.Optional(str, sql_default="''"))]
