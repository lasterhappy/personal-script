'''
科学刀 v2.0
捉包把域名www.kxdao.net请求里面的cookie的值填到变量 kxd_cookie 里
目前仅支持单账号
'''

import requests
from bs4 import BeautifulSoup
import os


class Kxd():
    def __init__(self, cookies):
        self.cookies = cookies
        self.formhash = ""
        self.kxd_url = "https://www.kxdao.net/"
        self.kxd_sign_url = "https://www.kxdao.net/plugin.php?id=dsu_amupper&formhash="
        self.kxd_info_url = "https://www.kxdao.net/home.php?mod=spacecp&ac=credit&showcredit=1"
        self.answer_url = 'https://www.kxdao.net/plugin.php?id=ahome_dayquestion:pop'
        self.session = requests.Session()
        self.headers = {
            'Host': 'www.kxdao.net',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Cookie': self.cookies,
        }

    # 签到
    def kxd_sign(self):
        login_res = self.session.get(self.kxd_info_url, headers=self.headers)
        soup_login = BeautifulSoup(login_res.text, 'html.parser')
        self.formhash = soup_login.select_one(
            "form#scbar_form input[name='formhash']")['value']
        response = self.session.get(
            self.kxd_sign_url+self.formhash, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        login_status = soup.select_one('div#messagetext p').text.split('。')
        print('=================== 签到状态 ======================\n')
        if login_status is not None:
            if len(login_status) > 1:
                print('签到成功!')
            for item in login_status:
                print(item)
        self.get_user_sign_info(soup)
        self.answer()

    # 获取用户签到信息
    def get_user_sign_info(self, html):
        print('\n=================== 签到信息 ======================')
        sign_info = html.select('div#pperwb_menu strong')
        if sign_info is not None:
            for item in sign_info:
                print(item.text)

    # 每日答题
    def answer(self):
        print('=================== 答题状态 ======================\n')
        data = {
            'formhash': self.formhash,
            'answer': '1',
            'submit': 'true'
        }
        response = self.session.post(
            self.answer_url, headers=self.headers, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        message_text = soup.select_one('div#messagetext p').text
        print(message_text)

    # 获取用户信息
    def get_user_info(self):
        response = self.session.get(self.kxd_info_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        info_ul = soup.find('ul', class_='creditl mtm bbda cl')
        print('\n=================== 用户信息 ======================')
        if info_ul is not None:
            info_li_list = info_ul.find_all('li')
            for item in info_li_list:
                print(item.text.replace(' ', '').replace(':', ': '))
        else:
            print("未找到用户信息！")

    def main(self):
        self.kxd_sign()
        self.get_user_info()


if __name__ == '__main__':
    cookies = os.environ.get('kxd_cookie')
    Kxd(cookies).main()
