#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"
__Date__ = "2018/3/15 下午2:27"
import re
import grequests
import json
from grequests import AsyncRequest
from functools import partial
from werkzeug.routing import Rule
from . import constant
import imp
import requests
import exceptions
from requests import Session, Request
import os


# class MyAsyncRequest(AsyncRequest):
#     def __init__(self, method, url, rule, **kwargs):
#         super(MyAsyncRequest, self).__init__(method, url, **kwargs)
#         self.rule = rule
#
#     def __eq__(self, other):
#         return self.__class__ is other.__class__ and \
#                self.rule == other.rule

class MyAsyncRequest(AsyncRequest):
    def __init__(self, method, url, rule, **kwargs):
        super(MyAsyncRequest, self).__init__(method, url, **kwargs)
        self.rule = rule

    def __eq__(self, other):
        return self.__class__ is other.__class__ and \
               self.rule == other.rule


class MyAppTestCase(object):
    """
    # TODO
    for automated testing

    """

    def __init__(self, domain, routes_init_file_path, routes_init_method_name, app_file_path, app_name, **kwargs):

        # The relative path can also be used
        self.routes_init_file_path = routes_init_file_path
        self.routes_init_method_name = routes_init_method_name

        # The relative path can also be used
        self.app_file_path = app_file_path
        self.app_name = app_name

        self.app = None

        self.headers = dict()

        # web.register_blueprints()
        # self.url_map = app.url_map
        # self.domain = 'http://localhost:5000'
        # self.domain = 'http://120.27.129.215:8087/api'
        self.domain = domain
        # self.domain = 'http://testing.ecams.cloudcare.cn:8100'
        self.validate_dict = dict()  # TODO

        self.url_dict = None
        # Init url_dict

        """ need to input """
        self.params_dict = None
        # Init params_dict

        """
        dict(
            # method=self.method,
            # url=self.url,
            headers=self.headers,
            files=None,
            data=None,
            json=None,
            params=None,
            auth=None,
            cookies=None,
            hooks=None,
        )
        """

        self.rs = None  # rs init in test_app

        self.output_data = None

        if "input_data_path" in kwargs:
            self.input_data_path = kwargs["input_data_path"]
        else:
            self.input_data_path = None

    def _do_some_init(self):
        self._init_app()
        self._do_something_for_authentication()
        self._set_url_dict()
        self._set_params_dict()
        self._init_rs()

    def _do_something_for_authentication(self):  # 下面是token验证, 如果你需要其他Authentication, 你可以继承这个方法
        token = {
            'x-cc-cuid': 'mN5MGPPFMC49y3HEXieB2H',
            'x-cc-uuid': 'tjJoHJPx4PeM78DfyN3yAJ',
        }
        self.headers.update(token)

    def construct_url(self, end_point):
        link_ch = '/'
        if end_point.startswith('/'):
            link_ch = ''
        return link_ch.join([self.domain, end_point])

    def exception_handler(self, request, exception):
        # TODO
        print request.url, 'is raise ', exception

    def _init_app(self):
        web = imp.load_source('web', self.routes_init_file_path)
        if hasattr(web, self.routes_init_method_name):
            getattr(web, self.routes_init_method_name)()
        else:
            raise AttributeError("'%s' does not have '%s'" % (self.routes_init_file_path, self.routes_init_method_name))
        app = imp.load_source('app', self.app_file_path)
        if hasattr(app, self.app_name):
            self.app = getattr(web, self.app_name)
        else:
            raise AttributeError("'%s' does not have '%s'" % (self.app_file_path, self.app_name))

    def _init_rs(self):

        rs_get = []
        rs_post = []
        rs_put = []
        rs_patch = []
        rs_delete = []
        rs_options = []
        rs_head = []

        self.rs = {
            'GET': rs_get,
            'POST': rs_post,
            'PUT': rs_put,
            'PATCH': rs_patch,
            'DELETE': rs_delete,
            # 'OPTIONS': rs_options,
            # 'HEAD': rs_head,
        }

    def _set_url_dict(self):
        self.url_dict = dict()
        url_map = self.app.url_map
        for i in url_map.iter_rules():
            # print i.rule, i.methods - set(['OPTIONS', 'HEAD'])
            key = i.endpoint.split('.')[0]
            if key in self.url_dict:
                self.url_dict[key].add(i)
            else:
                self.url_dict[key] = set([i])
        """
        keys = url_dict.keys()
        print keys
        ['serverapi0', u'cost', 'static', 'cdnapi0', 'sync_instances', 'sync_system_image', 
        'databaseapi0', 'security_groupapi0', u'script', 'sync_cdn_instances', u'token', 
        'sync_slb_instances', 'snapshotapi0', 'sync_oss_instances', 'floatingipapi0', 
        u'inventory', 'objectstorageapi0', 'imageapi0', u'auth', 'natapi0', u'user', 
        'diskapi0', 'loadbalancerapi0', 'vswitchapi0', 'sync_rds_instances', 'vpcapi0']
        """

    def get_input_data(self):
        # quote from requests.Session().request()
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, bytes, or file-like object to send
            in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) whether the SSL cert will be verified.
            A CA_BUNDLE path can also be provided. Defaults to ``True``.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :rtype: requests.Response
        """
        """
        # json file a structure is a list/array of the following dictionaries
        obj = dict(
            path_kwargs=dict(),
            method="",
            url="",
            headers=dict(),
            files=None,
            data=dict(),
            json=dict(),
            params=dict(),
            auth=None,
            cookies=None,
            hooks=None,
        )
        """

        if self.input_data_path is None or self.input_data_path == "":
            return []
        else:
            if os.path.exists(self.input_data_path) and os.path.isfile(self.input_data_path):
                if self.input_data_path.endswith(".json"):
                    with open(self.input_data_path, 'r') as f:
                        input_data = json.load(f)
                        return input_data
                else:
                    raise Exception("FileType Error: '%s' must be json file" % self.input_data_path)
            else:
                raise Exception("Type Error: '%s' not a file" % self.input_data_path)

    def _set_params_dict(self):
        input_data = self.get_input_data()

        self.params_dict = dict()
        for item in input_data:
            if item['url'] in self.params_dict:
                self.params_dict[item['url']][item['method']] = item
            else:
                self.params_dict[item['url']] = dict()
                self.params_dict[item['url']][item['method']] = item

    def _get_request_args_dict(self, method, url):
        args = self.params_dict.get(url, {}).get(method, {})  # TODO
        path_kwargs = args.pop('path_kwargs', {})
        args.pop('method', None)
        args.pop('url', None)
        return path_kwargs, args

    # # quit
    # def _get_forgery_arguments(self, arg, rule):  # unfinished
    #     return arg
    #
    # # quit
    # def get_forgery_arguments_dict(self, arguments, rule):
    #     tempalte = {key: self._get_forgery_arguments(key, rule) for key in arguments}
    #     return tempalte

    def _logger_successful(self, item, **kwargs):
        # TODO 'print' needs to be replaced with 'logger'
        resp = item.response
        if resp is not None:
            content = resp.content
        else:
            content = ""
        print "%s: %s" % (item.rule.rule, item.method), " ---->\n", content

    def _logger_pending(self, item, **kwargs):
        # TODO 'print' needs to be replaced with 'logger'
        resp = item.response
        if resp is not None:
            content = resp.content
        else:
            content = ""
        print "%s: %s" % (item.rule.rule, item.method), " ---->\n", content
        # print content

    def _logger_exceptional(self, item, **kwargs):
        # TODO 'print' needs to be replaced with 'logger'
        resp = item.response
        if resp is not None:
            content = resp.content
        else:
            content = ""
        print "%s: %s" % (item.rule.rule, item.method), " ---->\n", content

    def logger(self, item, i_type, **kwargs):
        func_dict = dict(
            successful=self._logger_successful,
            pending=self._logger_pending,
            exceptional=self._logger_exceptional,
        )
        if i_type in func_dict:
            func_dict[i_type](item, **kwargs)
        else:
            # TODO 'raise Exception' needs to be replaced with 'logger'
            raise Exception("I_TypeError: '%s' unexpected i_type, maybe you should input '%s'" % (
                i_type, "', '".join(func_dict.keys())))

    def get_response(self, rs):
        """
        # You can overwrite this method in the subclass, set your own strategy
        :param rs: List,  A list of MyAsyncRequest
        :return: successful, pending, exceptional
        """

        grequests.map(rs, stream=False, size=5, exception_handler=None, gtimeout=None)

    def output_result(self, successful, pending, exceptional, **kwargs):
        # TODO 'print' needs to be replaced with 'output'
        print 'successful: '
        for item in successful:
            self.logger(item, "successful")

        print 'pending: '
        for item in pending:
            self.logger(item, "pending")

        print 'exceptional: '
        for item in exceptional:
            self.logger(item, "exceptional")

    def create_request(self, method, rule):
        method = method.upper()
        if method in rule.methods:
            path_kwargs, kwargs = self._get_request_args_dict(method, rule.rule)
            path_kwargs_keys = path_kwargs.keys()
            if len(set(rule.arguments) - set(path_kwargs_keys)) != len(set(path_kwargs_keys) - set(rule.arguments)):
                if len(rule.arguments) < len(path_kwargs_keys):
                    # TODO 'print' needs to be replaced with 'logger'
                    print "url: %s -> %s, too many path_kwargs" % (rule.rule, method)
                else:
                    # TODO 'print' needs to be replaced with 'logger'
                    print "url: %s -> %s, missing '%s' path_kwargs " % (
                        rule.rule, method, "', '".join(set(rule.arguments) - set(path_kwargs_keys)))
                return

            if len(rule.arguments) == 0:
                # rs_get.append(grequests.get(self.construct_url(rule.rule), headers=self.headers))
                async_request_method = partial(MyAsyncRequest, method)
                self.rs[method].append(
                    async_request_method(self.construct_url(rule.rule), rule, headers=self.headers,
                                         **kwargs))
            else:
                # forgery_arguments_dict = self.get_forgery_arguments_dict(rule.arguments, rule)
                async_request_method = partial(MyAsyncRequest, method)
                url = rule.rule
                arguments = re.findall('(<.*?>)', url)

                # TODO need to be optimization
                # url = /aa/bb/<string:cc>
                for arg in arguments:  # arg = <string:cc>
                    key = arg[1:-1].split(':')[-1]  # key = cc
                    # url = re.sub(arg, forgery_arguments_dict[key], url)
                    url = re.sub(arg, path_kwargs[key], url)

                self.rs[method].append(async_request_method(self.construct_url(url), rule, headers=self.headers,
                                                            **kwargs))

    def send_request(self):
        for method in self.rs.keys():
            if len(self.rs[method]) == 0:
                continue
            self.get_response(self.rs[method])

    def output_preprocessor(self):
        """
        # You can overwrite this method in the subclass, set your own strategy
        """
        self.output_data = dict()

        for method in self.rs.keys():
            successful, pending, exceptional = [], [], []
            items = self.rs[method]
            for item in items:
                _item = item.response
                if _item is None:
                    exceptional.append(item)
                    continue
                if _item.status_code == 200:
                    content = _item.content
                    if content is None or content == '':
                        content = '{}'
                    content = json.loads(content)
                    code = content.get('code', -1)
                    if code == constant.SUCCESS:
                        successful.append(item)
                    elif code == constant.ParamsError:
                        pending.append(item)
                    else:
                        exceptional.append(item)
            self.output_result(successful, pending, exceptional)
            self.output_data[method] = (successful, pending, exceptional)

    def get_output_data(self):
        """
        # You can overwrite this method in the subclass, set your own strategy
        :return output_data, output_data is assigned in self.output_preprocessor()
        """
        return self.output_data

    def test_app(self):
        self._do_some_init()
        for key, urls in self.url_dict.iteritems():  # iteritems() in python3 is items()
            for rule in urls:
                for method in self.rs.keys():
                    if method in rule.methods:
                        self.create_request(method, rule)

        # print grequests.map(rs, exception_handler=self.exception_handler)
        self.send_request()
        self.output_preprocessor()


if __name__ == '__main__':
    domain = 'http://xxxx/xx'

    _routes_init_file_path = '/Users/xxxxx/Workspaces/xxxx/xxxxx/web.py'
    _routes_init_method_name = 'register_blueprints'

    _app_file_path = '/Users/xxxxx/Workspaces/xxxx/xxxxx/web.py'
    _app_name = 'app'

    input_data_path = "/Users/xxxxx/Data/xxx.json"  # 测试用例

    app_test = MyAppTestCase(domain, _routes_init_file_path, _routes_init_method_name, _app_file_path, _app_name)
    app_test.test_app()

    output_data = app_test.get_output_data()
    """
    # You can overwrite self.get_output_data() in the subclass, set your own strategy
        output_data is assigned in self.output_preprocessor()
    """
    print output_data
