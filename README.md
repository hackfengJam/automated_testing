## 基于 flask 和 grequests 的自动化测试

---

### 写在前面
因为自己也是弄着玩的，说是黑盒测试其实还是需要用到你项目代码里的app（因为我需要获取url_map，当然这一步完全没必要，因为你的测试用例是可以指定所有参数的，包括url_map，但是我就是这么做了=。=。。。若果你觉得我写的还可以的话，你可以自己clone下来，修改成你想要的^_^）

说是白盒测试也不对，因为我是基于测试用例，通过route层去进行测试的。

可以说是灰盒测试了。。。。。。。（你可以我说是强行灰盒，无所谓啦，就是随便撸的代码，能用起来是最好的嘛。。）
目前正在完善，希望有小伙伴一起讨论自动化测试，作为一个搞后端开发，自动化测试我觉得很有趣（后续我可能也会去用selenium去写一个测试脚本玩一玩。。。）

---

### 注：
> - <strong>If you want to know the source code, you should look at *test_master/app_by_requests_test.py*</strong>

> - <strong>You can create such a file --> *config/config.yaml*,  like this --> *config/config.yaml.example*, or add all the configuration to the source code as follows.</strong>


### 你需要的输入

<pre>
domain = 'http://xxxx/xx'  # 项目部署的服务器地址

# 你的所有蓝图路由应当有一个，注册蓝图的方法/函数
_routes_init_file_path = '/Users/xxxxx/Workspaces/xxxx/xxxxx/web.py'
_routes_init_method_name = 'register_blueprints'


# 前面也提到过，需要你的项目app
_app_file_path = '/Users/xxxxx/Workspaces/xxxx/xxxxx/web.py'
_app_name = 'app'


"""
# json file a structure is a list/array of the following dictionaries
obj = dict(
    path_kwargs=dict(),  # example: if you have a route, is app.routes("/aa/bb/<\id>"), the path_kwargs= {"id": 1}
    method="",  # method = "GET"/"POST"/"DELETE"/"PUT"/"PATCH", and case-sensitive free. "OPTIONS" and "HEAD" no support, you can overwrite self._init_rs() to support.
    url="",  # example: if you have a route, is app.routes("/aa/bb/<\id>"), the url= "/aa/bb/<\id>"
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
input_data_path = "/Users/xxxxx/Data/xxx.json"  # 测试用例，需要一个json文件，数据结构在上面注释已说明

</pre>

------
### 当然，上面的路径最好写相对路径
