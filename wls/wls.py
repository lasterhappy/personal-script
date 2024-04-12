'''
屋里社
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

    def get_sign_state(self):
        print('=================== 签到状态 ======================')
        response=self.session.post(self.sign_state_url,headers=self.headers)
        data=json.loads(response.text)['task']['task_mission']['finish']
        return data

    def sign(self):
        state=self.get_sign_state()
        if  state==1:
            print('已经签到过了')
        else:
            print('=================== 开始签到 ======================')
            response=self.session.post(self.sign_url,headers=self.headers)
            text=response.text.replace('"', '').replace('\n', '')
            print(f'签到成功!获得{text}积分')


    def main(self):
        self.sign()

if __name__=='__main__':
    cookies = os.environ.get('wls_cookie')
    Wls(cookies).main()
