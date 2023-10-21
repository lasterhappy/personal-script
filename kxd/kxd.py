'''
科学刀 v1.0
捉包把域名www.kxdao.net请求里面的cookie的值填到变量 kxd_cookie 里
目前仅支持单账号
'''


import requests
from bs4 import BeautifulSoup
import os

cookies= os.environ.get('kxd_cookie')

kxd_url="https://www.kxdao.net/"
kxd_sign_url="https://www.kxdao.net/plugin.php?id=dsu_amupper&formhash=64872b19"
kxd_info_url="https://www.kxdao.net/home.php?mod=spacecp&ac=credit&showcredit=1"
session = requests.Session()
headers = {
        'Host':'www.kxdao.net',
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Cookie':cookies,
        }


# 签到
def kxd_sign():
    response = session.get(kxd_sign_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    login_status=soup.select_one('div#messagetext p').text.split('。')
    print('=================== 签到状态 ======================\n')
    if login_status is not None:
        if len(login_status)>1:
            print('签到成功!')
        for item in login_status:
            print(item)
    get_user_sign_info(soup)
    answer()

# 签到信息
def get_user_sign_info(html):
    print('\n=================== 签到信息 ======================')
    sign_info=html.select('div#pperwb_menu strong')
    if sign_info is not None:
        for item in sign_info:
            print(item.text)

# 答题
def answer():
    print('=================== 答题状态 ======================\n')
    answer_url='https://www.kxdao.net/plugin.php?id=ahome_dayquestion:pop'
    data={
        'formhash':'64872b19',
        'answer':'1',
        'submit':'true'
    }
    response=session.post(answer_url,headers=headers,data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    message_text=soup.select_one('div#messagetext p').text
    print(message_text)


# 获取用户信息
def get_user_info():
    response = session.get(kxd_info_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    info_ul=soup.find('ul',class_='creditl mtm bbda cl')
    print('\n=================== 用户信息 ======================')
    if info_ul is not None:
        info_li_list=info_ul.find_all('li')
        for item in info_li_list:
            print(item.text.replace(' ','').replace(':',': '))
    else:
        print("未找到用户信息！")

if __name__ == '__main__':
    kxd_sign()
    get_user_info()

