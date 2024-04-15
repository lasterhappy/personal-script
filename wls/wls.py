'''
屋里社 https://wulishe.cc/
捉包把Authorization的值填到变量 wls_cookie里(Bearer也要填)
目前仅支持单账号
'''
import requests
from bs4 import BeautifulSoup
import json
import os

class Wls():
    def __init__(self,cookie):
        self.session=requests.Session()
        self.session.trust_env = False
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Authorization': cookie,
        }
        self.sign_url='https://wulishe.cc/wp-json/b2/v1/userMission'
        self.sign_state_url='https://wulishe.cc/wp-json/b2/v1/getTaskData'
        self.url='https://wulishe.cc/'

    def get_sign_state(self):
        print('=================== 签到状态 ======================')
        res=self.session.get(self.url,headers=self.headers)#需要先访问页面才有任务
        response=self.session.post(self.sign_state_url,headers=self.headers)
        data=json.loads(response.text)['task']['task_mission']['finish']
        return data

    def sign(self):
        state=self.get_sign_state()
        if  state==1:
            print('已经签到过了')
            return

        print('未签到，开始执行签到！')
        response=self.session.post(self.sign_url,headers=self.headers)
        response.raise_for_status()  # 检查响应状态码
        data = response.json()  # 使用json方法直接获取字典
        print('=================== 开始签到 ======================')
        print(f'签到成功!获得{data["credit"]}积分')
        print(f'签到日期:{data["date"]}')
        print(f'连续签到:{data["mission"]["always"]}天')
        print(f'总积分:{data["mission"]["my_credit"]}')


    def main(self):
        self.sign()

if __name__=='__main__':
    cookies = os.environ.get('wls_cookie')
    Wls(cookies).main()
