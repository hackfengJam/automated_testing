#!/usr/bin/env python
# -*- coding:utf-8 -*-
from test_master.app_by_requests_test import MyAppTestCase

__Author__ = "HackFun"
__Date__ = "2018/6/21 下午3:32"


def main():
    app_test = MyAppTestCase()

    app_test.test_app()

    output_data = app_test.output_data
    """
    # You can overwrite self.output_data() in the subclass, set your own strategy
        output_data is assigned in self.output_preprocessor()
    """

    print output_data


if __name__ == '__main__':
    # domain = 'http://xxxx/xx'
    #
    # _routes_init_file_path = '/Users/xxxxx/Workspaces/xxxx/xxxxx/web.py'
    # _routes_init_method_name = 'register_blueprints'
    #
    # _app_file_path = '/Users/xxxxx/Workspaces/xxxx/xxxxx/web.py'
    # _app_name = 'app'
    #
    # input_data_path = "/Users/xxxxx/Data/xxx.json"  # 测试用例
    #
    # app_test = MyAppTestCase(domain, _routes_init_file_path, _routes_init_method_name, _app_file_path, _app_name)
    main()
