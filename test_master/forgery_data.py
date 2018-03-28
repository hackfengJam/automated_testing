#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"
__Date__ = "2018/3/16 下午3:05"

import random
from sqlalchemy.sql.expression import func
from flask import request


# TODO
# for building app_by_request_test.MyAppTestCase.get_forgery_arguments_dict
def wapper(_func):
    def fun(*args, **kwargs):
        # print request.endpoint
        # print request.url_rule
        # print request.url
        # print _v["cost_summary_month"]
        _func(*args, **kwargs)

    return fun


def random_mobile():
    """
    :return: random valid mobile()
    """
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153",
               "155",
               "156", "157", "158", "159", "186", "187", "188"]
    while True:
        mobile = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
        # with session_scope() as db_session:
        #     if not db_session.query(User).filter(User.mobile == mobile).first():
        #         break
        break
    return mobile


def random_email():
    """
    :return: random email_address
    """
    character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    email = ""
    email_head_num = random.randint(6, 10)
    for one_round in range(email_head_num):
        random_num = random.randint(0, len(character) - 1)
        email = email + character[random_num]
    email = email + "@test.com"
    return email


def get_random_unique_id_from_mysql(type_class):
    """
    :param type: []
    :return: random unique_id from mysql or None
    """
    # list_class = []
    # if type_class in list_class:
    #     with session_scope() as db_session:
    #         unique_id = db_session.query(type_class.unique_id).order_by(func.random()).first()
    #         return unique_id[0]
    # else:
    #     return None
    with session_scope() as db_session:
        unique_id = db_session.query(type_class.unique_id).order_by(func.random()).first()
        return unique_id[0]


def get_random_cuid_and_uuid_from_usermaster():
    pass


def _column_value_is_invalid(column_value):
    return column_value is None or column_value is '' or column_value < 0


def get_random_one_column_form_mysql(type_class, column_name=''):
    """
    :param type_class: <class> from ecams.models.entities.*
    :param column_name: <string> from class field(column) name
    :return:column_value or None
    """

    if column_name == '' or column_name is None:
        with session_scope() as db_session:
            while True:
                obj = db_session.query(type_class).order_by(func.random()).first()
                return obj.to_dict()
    if hasattr(type_class, column_name):
        with session_scope() as db_session:
            while True:
                column_values = db_session.query(getattr(type_class, column_name)).order_by(func.random()).first()
                column_value = column_values[0]
                if _column_value_is_invalid(column_value):
                    continue
                return column_value
    else:
        return None

#
# if __name__ == '__main__':
#     from ecams.app import app
#
#     print app.url_map
#
#     import web
#
#     web.register_blueprints()
#     print app.url_map
