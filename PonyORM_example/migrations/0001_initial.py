# -*- coding: utf-8 -*-
# Generated by Pony ORM 0.8-dev on 2018-06-08 15:44
from __future__ import unicode_literals

from pony import orm

dependencies = []

def define_entities(db):
    class StoredItem(db.Entity):
        url = orm.Required(str)
        description = orm.Optional(str)