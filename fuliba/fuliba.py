import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from colorama import Fore, Back, Style


# 从环境变量中获取Cookie
cookie_string = os.environ.get('fuliba_cookie')


# 将从环境变量中读取的Cookie字符串转换为字典格式
cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_string.split(';')}

url = "https://www.wnflb2023.com/forum.php?mod=forumdisplay&fid=2&filter=author&orderby=dateline"

# User-Agent，模拟浏览器发送请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537",
}

# 发送GET请求，获取网页内容
response = requests.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, 'html.parser')



# 从网页内容中解析出formhash的值
formhash = soup.find('input', {'name': 'formhash'})['value']


# 解析网页内容，寻找表示签到状态的元素
sign_status = soup.find('img',{'id':'fx_checkin_b'})
state_sign=sign_status.get('alt', '')


# 判断是否已经签到
ok = []
if sign_status and '已签到' in sign_status.get('alt', ''):
    print('==================================================')
    print(Fore.RED+Style.BRIGHT+"已经签到过了"+Fore.RESET+Style.RESET_ALL)
    print('==================================================')
    ok.append("已经签到过了")
else:
    # 如果没有签到，执行签到操作
    print("检测到还未签到，现在开始签到")
    time.sleep(1.5)
    print("开始签到")

    sign_in_url = f"https://www.wnflb2023.com/plugin.php?id=fx_checkin:checkin&formhash={formhash}"
    response = requests.get(sign_in_url, headers=headers, cookies=cookies)
    # 根据返回状态码判断签到是否成功
    if response.status_code == 200:
        print("签到成功")
        ok.append("签到成功")
    else:
        print("签到失败")
        ok.append("签到失败")

# 不论是否签到，都获取并显示签到信息
info_url = "https://www.wnflb2023.com/plugin.php?id=fx_checkin:list"
response = requests.get(info_url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, 'html.parser')
# 获取签到信息
day_sign_info=soup.find('div',class_='tip_c').text.split(',')[0]
outer_div = soup.find('div', class_='fx_225')
if outer_div is not None:
    user_info_ul = outer_div.find('ul', class_='fx_user-info')
    if user_info_ul is not None:
        # 获取所有的li元素
        user_info_list = user_info_ul.find_all('li')

        # 从每个li元素中获取文本
        user_info = [li.get_text(strip=True) for li in user_info_list]

        # 移除最后一个元素的最后三个字符（即 "-5"）
        user_info[-1] = user_info[-1][:-3]

        # 打印用户信息
        print("签到信息：")
        for info in user_info:
            if info==user_info[-2]:
                print(day_sign_info)
            print(info)
    else:
        print("未找到签到信息!")
    print('==================================================')
else:
    print("未找到外层div")

# 访问另一页面获取用户资产信息
assets_url = "https://www.wnflb2023.com/home.php?mod=spacecp&ac=credit&showcredit=1"
response = requests.get(assets_url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, 'html.parser')

# 获取用户资产信息
assets_ul = soup.find('ul', class_='creditl mtm bbda cl')
if assets_ul is not None:
    # 获取所有的li元素
    assets_list = assets_ul.find_all('li')

    # 从每个li元素中获取文本，并移除不需要的部分
    assets_info = []
    for li in assets_list:
        text = li.get_text(strip=True)
        if '立即充值' in text:
            text = text.split('立即充值')[0]
        assets_info.append(text)

    # 打印用户资产信息
    print("我的资产：")
    for info in assets_info:
        print(info)
    print('==================================================')
else:
    print("未找到资产信息")


# 发送邮件通知
def send_email(subject, content):
    # QQ邮箱SMTP服务器地址
    mail_host = 'smtp.qq.com'
    # QQ邮箱SMTP服务器端口
    mail_port = 465

    # 发件人邮箱
    mail_sender = os.getenv("fuliba_fa")
    # 邮箱授权码
    mail_license = os.getenv("fuliba_ma")

    # 收件人邮箱，可以是QQ邮箱
    mail_receivers = [os.getenv("fuliba_shou")]

    mm = MIMEText(content, _subtype='plain', _charset='utf-8')
    mm['Subject'] = Header(subject, 'utf-8')
    mm['From'] = mail_sender  # 发件人邮箱
    mm['To'] = ';'.join(mail_receivers)  # 收件人邮箱列表，用分号隔开

    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtp_obj.login(mail_sender, mail_license)
        smtp_obj.sendmail(mail_sender, mail_receivers, mm.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("邮件发送失败", e)


# 在签到成功或失败后，调用这个函数发送邮件
# 在签到成功或失败后，调用这个函数发送邮件
if response.status_code == 200:
    user_info_str = "\n".join(user_info)
    assets_info_str = "\n".join(assets_info)
    email_content = f"{ok[0]}\n\n用户信息:\n{user_info_str}\n\n资产信息:\n{assets_info_str}"
    send_email('签到通知', email_content)
else:
    print(f'今天已签到')
    send_email('签到通知', '签到失败')
