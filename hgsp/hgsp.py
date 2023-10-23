'''
火锅视频 v1.0
捉包把域名www.huoguo.video请求里面的Authorization的值(包括Bearer)填到变量 hgsp_cookie 里
多账号以@隔开 账号1@账号2
注册链接:http://www.huoguo.video/h5/reg.html?invite_code=WYXJ5R
'''
import requests
import time
import os
import sys




class HgSp():
    VIDEO_F:int = 12 #视频次数
    def __init__(self,auth,index,video_f=VIDEO_F):
        self.video_f=video_f
        self.auth=auth
        self.index=index
        self.pre=f'[账号{index+1}]'
        self.session = requests.Session()
        self.headers={
            'os': 'android',
            'Version-Code': '1',
            'Client-Version': '1.0.0',
            'datetime': '2023-10-20 16:19:59.694',
            'Accept': 'application/json',
            'Authorization': auth,
            'Host': 'www.huoguo.video',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.12.13',
        }

    # 观看视频
    def watch_video(self):
        for i in range(self.video_f):
            response = self.session.get('http://www.huoguo.video/api/v2/hgb/recive', headers=self.headers).json()
            if response['message'] is not None:
                print(f'{self.pre}【看视频】{response["message"]}')
            else:
                print(f'{self.pre}【看视频】{response}')
            time.sleep(16)

    # 兑换储蓄金
    def exchange_saving(self):
        coin = self.session.get('http://www.huoguo.video/api/v2/hgb/coin', headers=self.headers).json()['coin']
        data = {
            'count': coin,
        }
        response = self.session.post('http://www.huoguo.video/api/v2/hgb/exchange-savings', headers=self.headers, data=data)
        if response.json()['message'] is not None:
            print(f'{self.pre}【兑换储蓄金】{response.json()["message"]}')
        else:
            print(f'{self.pre}【兑换储蓄金】{response.json()}')

    # 查询信息
    def get_info(self):
        response = self.session.get('http://www.huoguo.video/api/v2/hgb/open', headers=self.headers).json()
        if response["message"] is not None:
            print(f'{self.pre}【查询信息】{response["message"]}')
        else:
            print(f'{self.pre}【查询信息】获得 {response["amount"]}， 余额 {["balance"]}, 储蓄金 {["saving"]}')

    def main(self):
        self.watch_video()
        self.exchange_saving()
        self.get_info()



# 主程序
def main():
    global auth_list
    auth_list=os.getenv("hgsp_cookie").split('@')
    if not auth_list:
        print('没有获取到账号!')
        return
    print(f'⭐⭐获取到{len(auth_list)}个账号')
    for index,auth in enumerate(auth_list):
        print(f'=================== 第{index + 1}个账号 ======================')
        HgSp(auth,index).main()

if __name__ == '__main__':
    main()
    sys.exit()
