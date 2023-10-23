'''
4414站长论坛 v1.0
捉包把域名www.4414.cn请求里面的cookie的值填到环境变量 zzlt_cookie 里
目前仅支持单账号
'''
import requests
from bs4 import BeautifulSoup
import sys
import os

class Demo():
    def __init__(self,cookie):
        self.session=requests.Session()
        self.headers={
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Host': 'www.4414.cn',
            'Cookie':cookie
        }
        self.info_url='https://www.4414.cn/plugin.php?id=k_misign:sign'
        response=self.session.get(self.info_url,headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.formhash=soup.find('input',{'name':'formhash'})['value']

    # 签到状态
    def sign(self):
        print('=================== 签到状态 ======================')
        url='https://www.4414.cn/plugin.php'
        params={
            'id':'k_misign:sign',
            'operation':'qiandao',
            'formhash':self.formhash
        }
        response=self.session.get(url,headers=self.headers,params=params)
        if '今日已签' in response.text:
            print('您已签到完毕，今日已无需再次签到！')
        else:
            print('签到成功!')


    # 获取签到信息
    def get_info(self):
        print('=================== 签到信息 ======================')
        response=self.session.get(self.info_url,headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        infos=soup.select('ul.countqian li')
        if infos is not None:
            for info in infos:
                print(f'{info.select_one("h4").text}:{info.select_one("input")["value"]}{info.select_one("b:nth-last-child(1)").text.strip()}')

    def main(self):
        self.sign()
        self.get_info()

# 主程序
def main():
    cookie= os.environ.get('zzlt_cookie')
    Demo(cookie).main()

if __name__ == '__main__':
    main()
    sys.exit()