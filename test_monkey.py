# coding=utf-8
from locust import HttpLocust, TaskSet, task
import json
import yaml
import threading
from common_classes import OpenApi
from faker import Faker


# 定义用户行为
class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    @task
    def login(self):
        f1 = open("test2.yaml", "r", encoding='utf-8')  # 打开test2.yaml 文件
        cases = yaml.load(f1.read(), Loader=yaml.FullLoader)  # 读取test2.yaml文件
        data = cases["test5"]["data"]
        for i in range(len(data["params"])):
            f=Faker()
            if isinstance(data["params"][0], dict):  # 判断i 类型是不是dict
                if "onlineOrderNo" in data["params"][0]:  # 是dict的话。循环查找onlineOrderNo在 i
                    data["params"][0]["onlineOrderNo"]=f.ean13()  # 给onlineOrderNo 赋值
                else:
                    print('onlineOrderNo not in data["params"][' + str(i) + ']')  # 否则打印onlieOrderNo不在i 里
            else:
                print('data["params"][' + str(i) + '] is not dict, value ' + str(data["params"][i]))
        # o=OpenApi()
        # self.client.headers=o.get_headers(data)
        headers={'appkey': '86fcbcf1389f442d8fa834310a1c01cc',
                 'Content-Type': 'application/json',
                 'Authorization': 'GPX-HMAC256 APIKEY=86fcbcf1389f442d8fa834310a1c01cc,TIMESTAMP=1552568277517,NONCE=321213123,SIGN=7V4yatZhBue2OMNi8AJxs1LC0mE4AKjFUAq8jBjr1hITTkEzXIcqeF5YYc4qpWqVyBBoroJyHdjQ3fOErsiq4X2E4dBN4gkDaRUgrWUzMBbBdR05NkoqBW1n5Z0ALQr5',
                 'lang': 'zh_CH'}
        r=self.client.post(cases["test5"]["url"],
                           data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers=headers)
        if r.content:
            print(threading.current_thread().name + " status code: " + str(r.status_code) + ". res content" + str(
                r.content))
        else:
            print(threading.current_thread().name + " status code: " + str(r.status_code) + ". without content")
        if r.status_code != 200:
            r.failure('Wrong.Response')


# class second(TaskSet):
#     def on_start(self):
#         self.delivery()
#
#     @task
#     def delivery(self):
#         f1=open("test2.yaml", "r", encoding='utf-8')  # 打开test2.yaml 文件
#         cases=yaml.load(f1.read(), Loader=yaml.FullLoader)  # 读取test2.yaml文件
#         data=cases["test3"]["data"]
#         o=OpenApi()
#         self.client.headers=o.get_headers(data)
#         r1=self.client.post(cases["test3"]["url"],
#                             data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
#         if r1.content:
#             print("status code: " + str(r1.status_code) + ". res content" + str(r1.content))
#         else:
#             print("status code: " + str(r1.status_code) + ". without content")


class MobileUserLocust(HttpLocust):
    weight=1
    task_set=UserBehavior
    min_wait=1000
    max_wait=1000
    host="http://192.168.2.143"

# class sencond1(HttpLocust):
#     weight=1
#     task_set=second
#     min_wait=1000
#     max_wait=1000
#     host="https://test-api.int.parcelfuture.com"
