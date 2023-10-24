'''
火锅视频 v1.3 update add 提现功能
变量 hgsp_cookie 账号和密码以@隔开 账号@密码
多账号以&隔开 账号1@密码1 & 账号2@密码2
注册链接:http://www.huoguo.video/h5/reg.html?invite_code=WYXJ5R
'''
import requests
import time
import os
import sys


class HgSp():
    VIDEO_F:int = 13 #视频次数
    def __init__(self,account,video_f=VIDEO_F):
        account=account.split('@')
        self.video_f=video_f
        self.session = requests.Session()
        self.headers={
            'os': 'android',
            'Version-Code': '1',
            'Client-Version': '1.0.0',
            'datetime': '2023-10-20 16:19:59.694',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.huoguo.video',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.12.13',
        }
        self.data = {
            'login': account[0],
            'type': '2',
            'verifiable_code': '',
            'password': account[1]
        }

    # 登录
    def login(self):
        login_response = self.session.post('http://www.huoguo.video/api/v2/auth/login', headers=self.headers, data=self.data).json()
        if "access_token" in login_response:
            token = login_response['access_token']
            del self.headers['Content-Type']
            self.headers['Authorization']=f"Bearer {token}"
            response = self.session.get('http://www.huoguo.video/api/v2/user', headers=self.headers).json()
            print(f"✅✅登录成功,当前用户:{response['name']}")
            self.main()
        else:
            print(f"{login_response['message']}")

    # 观看视频
    def watch_video(self):
        for i in range(self.video_f):
            response = self.session.get('http://www.huoguo.video/api/v2/hgb/recive', headers=self.headers).json()
            if response['message'] is not None:
                print(f'【观看视频】{response["message"]}')
            else:
                print(f'【观看视频】{response}')
            time.sleep(16)

    # 获取今日信息
    def get_today_info(self):
        response = self.session.get('http://www.huoguo.video/api/v2/hgb/detail', headers=self.headers).json()
        self.coin = response['coin']
        self.today_coin = response['today_coin']
        print(f"【观看视频】今日获得火锅币:{self.today_coin},当前总火锅币:{self.coin}")

    # 兑换储蓄金
    def exchange_saving(self):
        self.get_today_info()
        data = {'count': self.coin}
        response = self.session.post('http://www.huoguo.video/api/v2/hgb/exchange-savings', headers=self.headers, data=data).json()
        if "amount" in response:
            print(f"【兑换储蓄金】获得储蓄金{response['amount']}")
        else:
            print(f"【兑换储蓄金】{response['message']}")

    # 查询信息
    def get_info(self):
        response = self.session.get('http://www.huoguo.video/api/v2/hgb/piggy', headers=self.headers).json()
        self.balance = response['balance']
        print(f"【查询信息】当前总储蓄金:{response['saving']} 可提现余额为：{response['balance']}")

    # 提现
    def withdraw(self):
        balance_float = float(self.balance)
        amount = "{:.2f}".format(balance_float)
        data = {'amount': amount}
        response = self.session.post("http://www.huoguo.video/api/v2/wallet/withdraw", headers=self.headers,data=data).json()
        print(response)



    def main(self):
        self.watch_video()
        self.exchange_saving()
        self.get_info()
        self.withdraw()



# 主程序
def main():
    global account_list
    account_list=os.getenv("hgsp_cookie").split('&')
    if not account_list:
        print('没有获取到账号!')
        return
    print(f'⭐⭐获取到{len(account_list)}个账号')
    for index,account in enumerate(account_list):
        print(f'=================== 第{index + 1}个账号 ======================')
        HgSp(account).login()

if __name__ == '__main__':
    main()
    sys.exit()
