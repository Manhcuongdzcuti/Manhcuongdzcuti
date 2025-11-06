
import requests
import base64
import json
import os
from datetime import datetime, timedelta
from time import sleep
import requests
import json
import uuid
import base64
import re
from datetime import datetime
import requests
import requests
import json
from colorama import Fore, Style, init









class TraoDoiSub_Api(object):

    def __init__(self, username, password, ) -> None:
        self.username = username
        self.password = password
        
        self.session = requests.Session()
        self.headers = {'authority': 'traodoisub.com', 'accept': 'application/json, text/javascript, */*; q=0.01', 'cache-control': 'max-age=0',
                        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'origin': 'https://traodoisub.com', 'referer': 'https://traodoisub.com/', 'x-requested-with': 'XMLHttpRequest'}

    def info(self):
        response = self.session.post('https://traodoisub.com/scr/login.php', headers=self.headers, data={
                                     'username': self.username, 'password': self.password}, )
        if 'success' in response.text:
            self.cookie = response.headers['Set-cookie']
            headers = {'authority': 'traodoisub.com', 'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-language': 'en-US,en;q=0.9', 'cookie': self.cookie, 'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
                       'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49', 'x-requested-with': 'XMLHttpRequest'}
            response = self.session.get(
                'https://traodoisub.com/view/setting/load.php', headers=headers).json()
            self.token = response['tokentds']
            self.xu = response['xu']
            self.name = response['user']
            return (True, self.name, self.xu, self.token)
        else:
            return (False, None)

    def facebook_configuration(self, id):
        try:
            response = self.session.post('https://traodoisub.com/scr/datnick.php',
                                         headers=self.headers, data={'iddat': id}, ).text
            return True if '1' in response else False
        except:
            return False

    def add_uid(self, id, g_recaptcha_response):
        headers = {'authority': 'traodoisub.com', 'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-language': 'en-US,en;q=0.9', 'cookie': self.cookie, 'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
                   'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49', 'x-requested-with': 'XMLHttpRequest'}
        response = self.session.post('https://traodoisub.com/scr/add_uid.php', headers=headers, data={
                                     'idfb': id, 'g-recaptcha-response': g_recaptcha_response}, ).text
        if 'success' in response:
            return (True, None)
        elif 'error' in response:
            return (False, response)
        else:
            return response

    def get_g_recaptcha_response(self, apikey):
        try:
            response = requests.get(
                'https://traodoisub.com/view/cauhinh/', headers=self.headers, )
            if response.status_code != 200:
                print('Lỗi khi lấy sitekey!')
                return (False, None)
            sitekey = response.text.split('data-sitekey="')[1].split('"')[0]
            captcha_solver = NextCaptcha(apikey)
            success, task_id = captcha_solver.recaptchav2(
                sitekey, 'https://traodoisub.com/view/cauhinh/')
            if success:
                success, g_recaptcha_response = captcha_solver.get_result(
                    task_id)
                if success:
                    return (True, g_recaptcha_response)
        except:
            return (False, 'Lỗi khi lấy reCAPTCHA')

    def get_nv_vip(self, fields, type):
        try:
            list_nv = self.session.get(
                f'https://traodoisub.com/api/?fields={fields}&access_token={self.token}&type={type}', ).json()
            return list_nv
        except:
            return False

    def get_nv_thuong(self, fields):
        try:
            list_nv = self.session.get(
                f'https://traodoisub.com/api/?fields={fields}&access_token={self.token}', ).json()
            return list_nv
        except:
            return False

    def get_xu_vip(self, type, id):
        try:
            get_xu = self.session.get(
                f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}', ).json()
            return get_xu
        except:
            return False

    def get_xu_thuong(self, type, id):
        try:
            get_xu = self.session.get(
                f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}', ).json()
            return get_xu
        except:
            return False

    def cache(self, type, id):
        try:
            cache = self.session.get(
                f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}', ).json()
            return cache
        except:
            return False

class NextCaptcha:

    def __init__(self, apikey):
        self.apikey = apikey
        self.create_task_url = 'https://api.3xcaptcha.com/createTask'
        self.get_result_url = 'https://api.3xcaptcha.com/getTaskResult'


    def get_result(self, task_id, max_retries=10, delay=0):
        data = {'clientKey': self.apikey, 'taskId': task_id}
        for x in range(max_retries):
            try:
                response = requests.post(
                    self.get_result_url, json=data, timeout=10).json()
                if response.get('errorId', 0) != 0:
                    print(f'Lỗi lấy kết quả: {response}')
                    return (False, None)
                if response.get('status') == 'ready':
                    return (True, response['solution']['gRecaptchaResponse'])
                sleep(delay)
            except requests.RequestException as e:
                print(f'Lỗi khi lấy kết quả Captcha: {e}')
                return (False, None)
        print('Hết số lần thử, không có kết quả.')
        return (False, None)
def encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string


def Delay(value):
    while not value <= 1:
        value -= 0.123
        print(
            f'\x1b[1;39m[\x1b[1;36mTIENDEV\x1b[1;39m][ \x1b[1;36mDELAY \x1b[1;39m][\x1b[1;36m{str(value)[0:5]}\x1b[1;39m][\x1b[1;33mX  \x1b[1;39m ]', '               ', end='\r')
        sleep(0.025)
        print(
            f'\x1b[1;39m[\x1b[1;36mTIENDEV\x1b[1;39m][ \x1b[1;36mDELAY \x1b[1;39m][\x1b[1;36m{str(value)[0:5]}\x1b[1;39m[\x1b[1;33m X   \x1b[1;39m]', '               ', end='\r')
        sleep(0.025)
        print(
            f'\x1b[1;39m[\x1b[1;36mTIENDEV\x1b[1;39m][ \x1b[1;36mDELAY \x1b[1;39m][\x1b[1;36m{str(value)[0:5]}\x1b[1;39m[\x1b[1;33m  X  \x1b[1;39m]', '               ', end='\r')
        sleep(0.025)
        print(
            f'\x1b[1;39m[\x1b[1;36mTIENDEV\x1b[1;39m][ \x1b[1;36mDELAY \x1b[1;39m][\x1b[1;36m{str(value)[0:5]}\x1b[1;39m[\x1b[1;33m   X \x1b[1;39m]', '               ', end='\r')
        sleep(0.025)
        print(
            f'\x1b[1;39m[\x1b[1;36mTIENDEV\x1b[1;39m][ \x1b[1;36mDELAY \x1b[1;39m][\x1b[1;36m{str(value)[0:5]}\x1b[1;39m[\x1b[1;33m    X\x1b[1;39m]', '               ', end='\r')
        sleep(0.025)

def Nhap_Cookie():
    listck = []
    demck = 0
    while True:
        demck += 1
        ck = input(f'{thanh} Nhập Cookie Facebook Thứ {demck}: ')
        if ck == '' and demck > 1:
            break
        fb = Facebook_Api(ck)
        info = fb.info()
        if 'success' in info:
            name = info['name']
            uid = info['id']
            thanhngang(50)
            print(f'{thanh} Id Facebook: {uid} | Tên Tài Khoản: {name}')
            listck.append(ck)
            thanhngang(50)
        else:
            thanhngang(50)
            print(
                f'{thanh} Trạng Thái Acc: [DIE]\n{thanh} Tin Nhắn: Đăng Nhập Thất Bại')
            demck -= 1
            thanhngang(50)
    return listck


import json
def Nhap_Setting():
    apikey = input(
        f'{thanh} Nhập Apikey 3xcaptcha Để Auto Add Cấu Hình (Enter để bỏ qua): ')
    min = int(input(f'{thanh} Nhập Delay Min: '))
    max = int(input(f'{thanh} Nhập Delay Max: '))
    nvblock = int(input(f'{thanh} Sau Bao Nhiêu Nhiệm Vụ Thì Chống Block: '))
    delaybl = int(input(f'{thanh} Sau {nvblock} Nhiệm Vụ Thì Nghỉ Ngơi: '))
    doinick = int(input(f'{thanh} Sau Bao Nhiêu Nhiệm Vụ Thì Đổi Nick: '))
    nhiemvuloi = int(input(f'{thanh} Lỗi Bao Nhiêu Nhiệm Vụ Thì Xóa Cookie: '))
    config = {'apikey': apikey, 'min': min, 'max': max, 'nvblock': nvblock,
              'delaybl': delaybl, 'doinick': doinick, 'nhiemvuloi': nhiemvuloi}
    with open('settingch.json', 'w') as f:
        json.dump(config, f)
    return config
def thanhngang(soluong=70):
    print("-" * soluong)

thanh = "[🌀] "


init(autoreset=True)

def banner():
    print(
        f"{Fore.CYAN}╔══════════════════════════════════════════════════════╗\n"
        f"{Fore.CYAN}║                                                      ║\n"
        f"{Fore.CYAN}║  {Fore.WHITE}████████╗██╗███████╗███╗  ██╗██████╗ ███████╗██╗   ██╗ {Fore.CYAN}║\n"
        f"{Fore.CYAN}║  {Fore.WHITE}╚══██╔══╝██║██╔════╝████╗ ██║██╔══██╗██╔════╝██║   ██║ {Fore.CYAN}║\n"
        f"{Fore.CYAN}║     {Fore.WHITE}██║   ██║█████╗  ██╔██╗██║██║  ██║█████╗  ██║   ██║ {Fore.CYAN}║\n"
        f"{Fore.CYAN}║     {Fore.WHITE}██║   ██║██╔══╝  ██║╚████║██║  ██║██╔══╝  ╚██╗ ██╔╝ {Fore.CYAN}║\n"
        f"{Fore.CYAN}║     {Fore.WHITE}██║   ██║███████╗██║ ╚███║██████╔╝███████╗ ╚████╔╝  {Fore.CYAN}║\n"
        f"{Fore.CYAN}║     {Fore.WHITE}╚═╝   ╚═╝╚══════╝╚═╝  ╚══╝╚═════╝ ╚══════╝  ╚═══╝   {Fore.CYAN}║\n"
        f"{Fore.CYAN}║                                                      ║\n"
        f"{Fore.CYAN}║        {Fore.YELLOW}Admin: TienDev | Website: nguyennamtien.shop    {Fore.CYAN}║\n"
        f"{Fore.CYAN}║              {Fore.GREEN}Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}               {Fore.CYAN}║\n"
        f"{Fore.CYAN}╚══════════════════════════════════════════════════════╝\n"
    )
    thanhngang(55)
    
def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_to_base64(string):
    return base64.b64encode(string.encode()).decode()
class Facebook_Api(object):

    def __init__(self, cookie):
        try:
            self.lsd = ''
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.actor_id = self.cookie.split('c_user=')[1].split(';')[0]
            
            self.headers = {'authority': 'www.facebook.com', 'accept': '*/*', 'cookie': self.cookie, 'origin': 'https://www.facebook.com',
                            'referer': 'https://www.facebook.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin'}
            
                    
            url = requests.get(
                f'https://www.facebook.com/{self.actor_id}', headers=self.headers, ).url
            response = requests.get(
                url, headers=self.headers, ).text
            matches = re.findall(
                '\\["DTSGInitialData",\\[\\],\\{"token":"(.*?)"\\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall('jazoest=(.*?)\\"', response)[0]
                self.lsd += re.findall(
                    '\\["LSD",\\[\\],\\{"token":"(.*?)"\\}', response)[0]
        except:
            pass

    def info(self):
        get = requests.get('https://www.facebook.com/me',
                           headers=self.headers, ).text
        try:
            name = get.split('<title>')[1].split('</title>')[0]
            return {'success': 200, 'id': self.actor_id, 'name': name}
        except:
            return {'error': 200}

    def Checkspam(self):
        data = {'av': self.actor_id, '__user': self.actor_id, '__a': '1', '__req': '8', '__hs': '20038.HYP:comet_pkg.2.1..2.1', 'dpr': '1', '__ccg': 'EXCELLENT', '__rev': '1018089718', '__s': 'mtrukx:3ui1ys:yphvdu', '__hsi': '7435940161710523784', '__dyn': '7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D8vwRwlE-U2zxe2GewbS361qw8Xwn82Lx-0lK3qazo720Bo2ZwrU6C0hq1Iwqo35wvodo7u2-2K0UE',
                '__csr': 'gzl5849ahWFaeU-rK4Uyii9VAmWl6zpUCUgK3K2mi2q2Ki687W08Pyo1yp9Esw14e0OE1u80now05XXw0Dhw0eNi', '__comet_req': '15', 'fb_dtsg': self.fb_dtsg, 'jazoest': self.jazoest, 'lsd': self.lsd, '__spin_r': '1018089718', '__spin_b': 'trunk', '__spin_t': '1731314734', 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'FBScrapingWarningMutation', 'variables': '{}', 'server_timestamps': 'true', 'doc_id': '6339492849481770'}
        response = requests.post('https://www.facebook.com/api/graphql/',
                                 headers=self.headers, data=data, )
        return response.text

    def reaction(self, id, type):
        reac = {'LIKE': '1635855486666999', 'LOVE': '1678524932434102', 'CARE': '613557422527858',
                'HAHA': '115940658764963', 'WOW': '478547315650144', 'SAD': '908563459236466', 'ANGRY': '444813342392137'}
        idreac = reac.get(type)
        data = {'av': self.actor_id, '__usid': '6-Tsfgotwhb2nus:Psfgosvgerpwk:0-Asfgotw11gc1if-RV=6:F=', '__aaid': '0', '__user': self.actor_id, '__a': '1', '__req': '2c', '__hs': '19896.HYP:comet_pkg.2.1..2.1', 'dpr': '1', '__ccg': 'EXCELLENT', '__rev': '1014402108', '__s': '5vdtpn:wbz2hc:8r67q5', '__hsi': '7383159623287270781', '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C17xt3odE98K361twYwJyE24wJwpUe8hwaG1sw9u0LVEtwMw65xO2OU7m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwqo31wiE567Udo5qfK0zEkxe2GewyDwkUe9obrwKxm5oe8464-5pUfEdK261eBx_wHwdG7FoarCwLyES0Io88cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13whEeE4WVU-4EdrxG1fy8bUaU', '__csr': 'gug_2A4A8gkqTf2Ih6RFnbk9mBqaBaTs8_tntineDdSyWqiGRYCiPi_SJuLCGcHBaiQXtLpXsyjIymm8oFJswG8CSGGLzAq8AiWZ6VGDgyQiiTBKU-8GczE9USmi4A9DBABHgWEK3K9y9prxaEa9KqQV8qUlxW22u4EnznDxSewLxq3W2K16BxiE5VqwbW1dz8qwCwjoeEvwaKVU6q0yo5a2i58aE7W0CE5O0fdw1jim0dNw7ewPBG0688025ew0bki0cow3c8C05Vo0aNF40BU0rmU3LDwaO06hU06RG6U1g82Bw0Gxw6Gw', '__comet_req': '15', 'fb_dtsg': self.fb_dtsg, 'jazoest': self.jazoest, 'lsd': self.lsd, '__spin_r': '1014402108', '__spin_b': 'trunk', '__spin_t': '1719025807', 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
                'variables': f'''{{"input":{{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,1719027162723,322693,4748854339,,","feedback_id":"{encode_to_base64('feedback:' + str(id))}","feedback_reaction_id":"{idreac}","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"tracking":["AZWUDdylhKB7Q-Esd2HQq9i7j4CmKRfjJP03XBxVNfpztKO0WSnXmh5gtIcplhFxZdk33kQBTHSXLNH-zJaEXFlMxQOu_JG98LVXCvCqk1XLyQqGKuL_dCYK7qSwJmt89TDw1KPpL-BPxB9qLIil1D_4Thuoa4XMgovMVLAXncnXCsoQvAnchMg6ksQOIEX3CqRCqIIKd47O7F7PYR1TkMNbeeSccW83SEUmtuyO5Jc_wiY0ZrrPejfiJeLgtk3snxyTd-JXW1nvjBRjfbLySxmh69u-N_cuDwvqp7A1QwK5pgV49vJlHP63g4do1q6D6kQmTWtBY7iA-beU44knFS7aCLNiq1aGN9Hhg0QTIYJ9rXXEeHbUuAPSK419ieoaj4rb_4lA-Wdaz3oWiWwH0EIzGs0Zj3srHRqfR94oe4PbJ6gz5f64k0kQ2QRWReCO5kpQeiAd1f25oP9yiH_MbpTcfxMr-z83luvUWMF6K0-A-NXEuF5AiCLkWDapNyRwpuGMs8FIdUJmPXF9TGe3wslF5sZRVTKAWRdFMVAsUn-lFT8tVAZVvd4UtScTnmxc1YOArpHD-_Lzt7NDdbuPQWQohqkGVlQVLMoJNZnF_oRLL8je6-ra17lJ8inQPICnw7GP-ne_3A03eT4zA6YsxCC3eIhQK-xyodjfm1j0cMvydXhB89fjTcuz0Uoy0oPyfstl7Sm-AUoGugNch3Mz2jQAXo0E_FX4mbkMYX2WUBW2XSNxssYZYaRXC4FUIrQoVhAJbxU6lomRQIPY8aCS0Ge9iUk8nHq4YZzJgmB7VnFRUd8Oe1sSSiIUWpMNVBONuCIT9Wjipt1lxWEs4KjlHk-SRaEZc_eX4mLwS0RcycI8eXg6kzw2WOlPvGDWalTaMryy6QdJLjoqwidHO21JSbAWPqrBzQAEcoSau_UHC6soSO9UgcBQqdAKBfJbdMhBkmxSwVoxJR_puqsTfuCT6Aa_gFixolGrbgxx5h2-XAARx4SbGplK5kWMw27FpMvgpctU248HpEQ7zGJRTJylE84EWcVHMlVm0pGZb8tlrZSQQme6zxPWbzoQv3xY8CsH4UDu1gBhmWe_wL6KwZJxj3wRrlle54cqhzStoGL5JQwMGaxdwITRusdKgmwwEQJxxH63GvPwqL9oRMvIaHyGfKegOVyG2HMyxmiQmtb5EtaFd6n3JjMCBF74Kcn33TJhQ1yjHoltdO_tKqnj0nPVgRGfN-kdJA7G6HZFvz6j82WfKmzi1lgpUcoZ5T8Fwpx-yyBHV0J4sGF0qR4uBYNcTGkFtbD0tZnUxfy_POfmf8E3phVJrS__XIvnlB5c6yvyGGdYvafQkszlRrTAzDu9pH6TZo1K3Jc1a-wfPWZJ3uBJ_cku-YeTj8piEmR-cMeyWTJR7InVB2IFZx2AoyElAFbMuPVZVp64RgC3ugiyC1nY7HycH2T3POGARB6wP4RFXybScGN4OGwM8e3W2p-Za1BTR09lHRlzeukops0DSBUkhr9GrgMZaw7eAsztGlIXZ_4"],"session_id":"{uuid.uuid4()}","actor_id":"{self.actor_id}","client_mutation_id":"3"}},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}}''', 'server_timestamps': 'true', 'doc_id': '7047198228715224'}
        response = requests.post('https://www.facebook.com/api/graphql/',
                                 headers=self.headers, data=data, )
        if '{"data":{"feedback_react":{"feedback":{"id":' in response.text:
            return True
        else:
            return False

    def reactioncmt(self, id, type):
        reac = {'LIKE': '1635855486666999', 'LOVE': '1678524932434102', 'CARE': '613557422527858',
                'HAHA': '115940658764963', 'WOW': '478547315650144', 'SAD': '908563459236466', 'ANGRY': '444813342392137'}
        g_now = datetime.now()
        d = g_now.strftime('%Y-%m-%d %H:%M:%S.%f')
        datetime_object = datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')
        timestamp = str(datetime_object.timestamp())
        starttime = timestamp.replace('.', '')
        id_reac = reac.get(type)
        data = {'av': self.actor_id, '__aaid': '0', '__user': self.actor_id, '__a': '1', '__req': '1a', '__hs': '19906.HYP:comet_pkg.2.1..2.1', 'dpr': '1', '__ccg': 'GOOD', '__rev': '1014619389', '__s': 'z5ciff:vre7af:23swxc', '__hsi': '7387045920424178191', '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C1vgS3q2ibwyzE2qwJyE24wJwkEkwUx60GE5O0BU2_CxS320om78-221Rwwwqo462mcwfG12wOx62G5Usw9m1YwBgK7o6C2O0B84G1hx-3m1mzXw8W58jwGzEaE5e3ym2SUbElxm3y11xfxmu3W3rwxwjFovUaU3VBwFKq2-azo2NwwwOg2cwMwhEkxebwHwNxe6Uak0zU8oC1hxB0qo4e16wWwjHDzUiwRK6E4-8wLwHw', '__csr': 'gJ0AH5n4n4PhcQW4Oh4JFsIH4f5ji9iWuzqSltFlETn_trnbH_YIJX9iWiAiQBpeht9uYyhrvOOaiSV9CKmriyF4EzjBGh4XRqy8O4Z4HGypAaDAG8DzE-iKii5bUGaiXyocA22iayUOUG9BKUkxe2vBBxe5898S5k48fogxqQU9oO1bwiU9FpEowOBwYwLCw86u2y0Eo885-1uwFwOwpU1jo7-0IU108iw8i0kq0bVw6gBxa4E1g83tw0_yBw2hE012EoG0uG0gh068w23Q0dlw0wKw68Aw0huU0a7VU0jkw0E-w8W0cPK6U', '__comet_req': '15', 'fb_dtsg': self.fb_dtsg, 'jazoest': self.jazoest, 'lsd': self.lsd,
                '__spin_r': '1014619389', '__spin_b': 'trunk', '__spin_t': '1719930656', 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation', 'variables': '{"input":{"attribution_id_v2":"CometVideoHomeNewPermalinkRoot.react,comet.watch.injection,via_cold_start,1719930662698,975645,2392950137,,","feedback_id":"' + encode_to_base64('feedback:' + str(id)) + '","feedback_reaction_id":"' + id_reac + '","feedback_source":"TAHOE","is_tracking_encrypted":true,"tracking":[],"session_id":"' + str(uuid.uuid4()) + '","downstream_share_session_id":"' + str(uuid.uuid4()) + '","downstream_share_session_origin_uri":"https://fb.watch/t3OatrTuqv/?mibextid=Nif5oz","downstream_share_session_start_time":"' + starttime + '","actor_id":"' + self.actor_id + '","client_mutation_id":"1"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}', 'server_timestamps': 'true', 'doc_id': '7616998081714004'}
        response = requests.post('https://www.facebook.com/api/graphql/',
                                 headers=self.headers, data=data, )
        if '{"data":{"feedback_react":{"feedback":{"id":' in response.text:
            return True
        else:
            return False
import requests, os, json, datetime
from time import sleep
from datetime import datetime
from random import randint
import random 
def Main():
    ptool = 0
    dem = 0
    count = 0
    banner()
    print('-' * 70)
    
    banner()
    while True:
        if os.path.exists('acc_tds_log.txt'):
            with open('acc_tds_log.txt', 'r') as f:
                username, password = f.read().split('_')
            tds = TraoDoiSub_Api(username, password, )
            profile = tds.info()
            try:
                print(f'{thanh} Nhập [1] Để Chạy Acc Tài Khoản {profile[1]}')
                print(f'{thanh} Nhập [2] Nhập Tài Khoản Trao Đổi Sub Mới')
                thanhngang(50)
                chon = input(f'{thanh} Nhập: ')
                thanhngang(50)
                if chon == '2':
                    os.remove('acc_tds_log.txt')
                elif chon == '1':
                    pass
                else:
                    print(f'{thanh} Vui Lòng Chọn Đúng')
                    thanhngang(50)
                    continue
            except:
                print(
                    f'{thanh} Trạng Thái Acc: [DIE]\n{thanh} Tin Nhắn: Đăng Nhập Thất Bại')
                os.remove('acc_tds_log.txt')
        if not os.path.exists('acc_tds_log.txt'):
            username, password = (input(f'{thanh} Nhập Tài Khoản TDS: '), input(
                f'{thanh} Nhập Mật Khẩu TDS: '))
            thanhngang(50)
            with open('acc_tds_log.txt', 'w') as f:
                f.write(f'{username}_{password}')
        with open('acc_tds_log.txt', 'r') as f:
            username, password = f.read().split('_')
        tds = TraoDoiSub_Api(username, password, )
        profile = tds.info()
        try:
            user = profile[1]
            xu = profile[2]
            print(
                f'{thanh} Trạng Thái Acc: [LIVE]\n{thanh} Tin Nhắn: Đăng Nhập Thành Công')
            break
        except:
            print(
                f'{thanh} Trạng Thái Acc: [DIE]\n{thanh} Tin Nhắn: Đăng Nhập Thất Bại')
            thanhngang(50)
            os.remove('acc_tds_log.txt')
    thanhngang(50)
    while True:
        if os.path.exists('Cookie_FB.txt'):
            print(f'{thanh} Nhập [1] Sử Dụng Cookie Facebook Đã Lưu')
            print(f'{thanh} Nhập [2] Nhập Cookie Facebook Mới')
            thanhngang(50)
            chon = input(f'{thanh} Nhập: ')
            thanhngang(50)
            if chon == '1':
                print(f'Đang Lấy Dữ Liệu Đã Lưu')
                sleep(1)
                with open('Cookie_FB.txt', 'r') as f:
                    listck = json.loads(f.read())
                    break
            elif chon == '2':
                os.remove('Cookie_FB.txt')
            else:
                print(f'{thanh} Vui Lòng Chọn Đúng')
                thanhngang(50)
                continue
        if not os.path.exists('Cookie_FB.txt'):
            listck = Nhap_Cookie()
            with open('Cookie_FB.txt', 'w') as f:
                json.dump(listck, f)
            break
    banner()
    print(f'{thanh} Tên Tài khoản: {user}')
    print(f"{thanh} Xu Hiện Tại: {str(format(int(xu), ','))}")
    print(f'{thanh} Số Facebook: {len(listck)}')
    thanhngang(50)
    print(f'{thanh} Nhập [1] Để Chạy Nhiệm Vụ Cảm Xúc Vip')
    print(f'{thanh} Nhập [2] Để Chạy Nhiệm Vụ Cảm Xúc Cmt Vip')
    print(f'{thanh} Nhập [9] Để Chạy Nhiệm Vụ Like Thường')
    print(f'{thanh} Nhập [0] Để Chạy Nhiệm Vụ Cảm Xúc Thường')
    print(f'{thanh} Có Thể Chọn Nhiều Nhiệm Vụ (Ví Dụ: 123...)')
    thanhngang(50)
    listnv = []
    nhap = input(f'{thanh}  Nhập Số Để Chọn Nhiệm Vụ: ')
    listnv.append(nhap)
    thanhngang(50)
    if os.path.exists("setting.json"):
        with open("setting.json", "r") as f:
            content = f.read().strip()
            try:
                config = json.loads(content) if content else {}
            except:
                config = {}
                
        if config:
            apikey = config['apikey']
            min = config['min']
            max = config['max']
            nvblock = config['nvblock']
            delaybl = config['delaybl']
            doinick = config['doinick']
            nhiemvuloi = config['nhiemvuloi']
            print(f'{thanh} Đã Thấy Cấu Hình Cũ')
            print(f'{thanh} Api Key 3xCapcha: {apikey}')
            print(f'{thanh} Delay Min: {min}')
            print(f'{thanh} Delay Max: {max}')
            print(f'{thanh} Sau {nvblock} Nhiệm Vụ Thì Chống Block')
            print(f'{thanh} Sau {nvblock} Nhiệm Vụ Thì Nghỉ Ngơi {delaybl}')
            print(f'{thanh} Sau {doinick} Nhiệm Vụ Thì Đổi Nick')
            print(f'{thanh} Lỗi {nhiemvuloi} Nhiệm Vụ Thì Đổi Nhiệm Vụ')
        chon = input(f'{thanh} Bạn Có Muốn Sử Dụng Cấu Hình Cũ Không? (y/n): ')
        if chon == 'y':
            apikey = config['apikey']
            min = config['min']
            max = config['max']
            nvblock = config['nvblock']
            delaybl = config['delaybl']
            doinick = config['doinick']
            nhiemvuloi = config['nhiemvuloi']
        else:
            print(f'{thanh} Đã Xóa Cấu Hình Cũ')
            thanhngang(50)
            os.remove('settingch.json')
            config = Nhap_Setting()
            apikey = config['apikey']
            min = config['min']
            max = config['max']
            nvblock = config['nvblock']
            delaybl = config['delaybl']
            doinick = config['doinick']
            nhiemvuloi = config['nhiemvuloi']
    else:
        config = Nhap_Setting()
        apikey = config['apikey']
        min = config['min']
        max = config['max']
        nvblock = config['nvblock']
        delaybl = config['delaybl']
        doinick = config['doinick']
        nhiemvuloi = config['nhiemvuloi']
    chonan = input(f'{thanh} Bạn Có Muốn Ẩn Id Facebook Không (y/n): ')
    thanhngang(50)
    while True:
        if len(listck) == 0:
            print(f'Đã Xoá Tất Cả Cookie, Vui Lòng Nhập Lại')
            listck = Nhap_Cookie()
            with open('Cookie_FB.txt', 'w') as f:
                json.dump(listck, f)
        for ck in listck:
            nhiemvu = listnv[0]
            loireaction, loicxcmt, loishare, loifollow, loipage, loigr, loilike, loiliket, loisharet, loiliket = (
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            
            
            fb = Facebook_Api(ck, )
            info = fb.info()
            if 'success' in info:
                name = info['name']
                uid = info['id']
            else:
                uid = ck.split('c_user=')[1].split(';')[0]
                print(f'Cookie Tài Khoản {uid} Die', end='\r')
                sleep(1)
                print('                                     ', end='\r')
                listck.remove(ck)
                continue
            if chonan == 'y':
                uid2 = uid[:3] + '#' * (len(uid) - 6) + uid[-3:]
            else:
                uid2 = uid
            cauhinh = tds.facebook_configuration(uid)
            if cauhinh == True:
                print(f'Id Facebook: {uid2} | Tên Tài khoản: {name}')
            elif apikey:
                print(f'Đang Thêm Id Facebook: {uid} | Tên Tài khoản: {name}')
                get_g_recaptcha_response = tds.get_g_recaptcha_response(apikey)
                if get_g_recaptcha_response[0] == True:
                    add_uid = tds.add_uid(uid, get_g_recaptcha_response[1])
                    if add_uid[0] == True:
                        cauhinh = tds.facebook_configuration(uid)
                        if cauhinh == True:
                            print(
                                f'Id Facebook: {uid2} | Tên Tài khoản: {name}')
                        else:
                            print(
                                f'Cấu Hình Thất Bại Id Facebook: {uid} | Tên Tài khoản: {name}')
                            listck.remove(ck)
                            continue
                    else:
                        print(
                            f'Thêm Cấu Hình Thất Bại Id Facebook: {uid} | Tên Tài khoản: {name}')
                        listck.remove(ck)
                        continue
                else:
                    print(
                        f'Thêm Cấu Hình Thất Bại Id Facebook: {uid} | Tên Tài khoản: {name}')
                    listck.remove(ck)
                    continue
            else:
                print(
                    f'Cấu Hình Thất Bại Id Facebook: {uid} | Tên Tài khoản: {name}')
                listck.remove(ck)
                continue
            ptool = 0
            while True:
                if ptool == 1:
                    break
                if nhiemvu == '':
                    print(f'Tài Khoản {name} Đã Bị Block Tất Cả Tương Tác ')
                    listck.remove(ck)
                    ptool = 1
                    break
                if '1' in nhiemvu:
                    listcx = tds.get_nv_vip('facebook_reaction', 'ALL')
                    if listcx == False:
                        print(
                            f'Không Đào Được Quặng                            ', end='\r')
                        sleep(2)
                        print(
                            '                                                        ', end='\r')
                    elif 'error' in listcx:
                        if listcx['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
                            count = listcx['countdown']
                            print(
                                f'Đang Đào Được Quặng, COUNTDOWN: {str(round(count, 3))}              ', end='\r')
                            sleep(1)
                            print(
                                '                                                       ', end='\r')
                            Delay(count)
                        else:
                            print(listcx['error'], end='\r')
                            sleep(1)
                            print(
                                '                                                       ', end='\r')
                    else:
                        list_nv = listcx['data']
                        if len(list_nv) == 0:
                            print(
                                f'Đã Hết Quặng Sắt Ở Vùng Này Vui Lòng Đến Chỗ Khác                           ', end='\r')
                            sleep(1)
                            print(
                                '                                                        ', end='\r')
                        else:
                            print(
                                f'Tìm Thấy {len(list_nv)} Nhiệm Vụ Cảm Xúc                      ', end='\r')
                            for x in list_nv:
                                idpost = x['id']
                                id = idpost.split(
                                    '_')[1] if '_' in idpost else idpost
                                id2 = id[:3] + '#' * (len(id) - 6) + id[-3:]
                                code = x['code']
                                type = x['type']
                                like = fb.reaction(id, type)
                                if like == False:
                                    print(
                                        f'FAIL {type}: {id}            ', end='\r')
                                    sleep(2)
                                    print(
                                        '                                                       ', end='\r')
                                    Delay(3)
                                    loireaction += 1
                                else:
                                    nhan = tds.get_xu_vip(
                                        'facebook_reaction', code)
                                    if 'success' in nhan:
                                        xu = nhan['data']['xu']
                                        msg = nhan['data']['msg']
                                        loireaction = 0
                                        dem += 1
                                        time = datetime.now().strftime('%H:%M:%S')
                                        print(
                                            f"[{dem}][{time}][{type}][{id2}][{msg}][{str(format(int(xu), ','))}]")
                                        if dem % doinick == 0:
                                            ptool = 1
                                            break
                                        if dem % nvblock == 0:
                                            Delay(delaybl)
                                        else:
                                            Delay(randint(min, max))
                                if loireaction >= nhiemvuloi:
                                    fb2 = Facebook_Api(ck)
                                    checktt = fb2.info()
                                    if 'error' in checktt:
                                        print(
                                            f'Cookie Tài Khoản {name} Đã Bị Out or Checkpoint !!!                ')
                                        listck.remove(ck)
                                        ptool = 1
                                        break
                                    else:
                                        print(
                                            f'Tài Khoản {name} Đã Bị Block Cảm Xúc                            ', end='\r')
                                        sleep(1)
                                        print(
                                            '                                                        ', end='\r')
                                        nhiemvu = nhiemvu.replace('1', '')
                                        break
                if ptool == 1:
                    break
                if '2' in nhiemvu:
                    listcxcmt = tds.get_nv_vip('facebook_reactioncmt', 'ALL')
                    if listcxcmt == False:
                        print(
                            f'Không Get Được Nhiệm Vụ Cảm Xúc Cmt                           ', end='\r')
                        sleep(1)
                        print(
                            '                                                        ', end='\r')
                    elif 'error' in listcxcmt:
                        if listcxcmt['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
                            count = listcxcmt['countdown']
                            print(
                                f'Đang Get Nhiệm Vụ Follow, COUNTDOWN: {str(round(count, 3))}              ', end='\r')
                            sleep(1)
                            print(
                                '                                                       ', end='\r')
                            Delay(count)
                        else:
                            print(listcxcmt['error'], end='\r')
                            sleep(1)
                            print(
                                '                                                       ', end='\r')
                    else:
                        list_nv = listcxcmt['data']
                        if len(list_nv) == 0:
                            print(
                                f'Hết Nhiệm Vụ Cảm Xúc Cmt                           ', end='\r')
                            sleep(1)
                            print(
                                '                                                        ', end='\r')
                        else:
                            print(
                                f'Tìm Thấy {len(list_nv)} Nhiệm Vụ Cảm Xúc Cmt                     ', end='\r')
                            for x in list_nv:
                                idpost = x['id']
                                id = idpost.split(
                                    '_')[1] if '_' in idpost else idpost
                                id2 = id[:3] + '#' * (len(id) - 6) + id[-3:]
                                code = x['code']
                                type = x['type']
                                like = fb.reactioncmt(id, type)
                                if like == False:
                                    print(
                                        f'FAIL {type}CMT: {id}            ', end='\r')
                                    sleep(2)
                                    print(
                                        '                                                       ', end='\r')
                                    Delay(3)
                                    loicxcmt += 1
                                else:
                                    nhan = tds.get_xu_vip(
                                        'facebook_reactioncmt', code)
                                    if 'success' in nhan:
                                        xu = nhan['data']['xu']
                                        msg = nhan['data']['msg']
                                        loicxcmt = 0
                                        dem += 1
                                        time = datetime.now().strftime('%H:%M:%S')
                                        print(
                                            f"[{dem}][{time}][{type}CMT][{id2}][{msg}][{str(format(int(xu), ','))}]")
                                        if dem % doinick == 0:
                                            ptool = 1
                                            break
                                        if dem % nvblock == 0:
                                            Delay(delaybl)
                                        else:
                                            Delay(randint(min, max))
                                if loicxcmt >= nhiemvuloi:
                                    fb2 = Facebook_Api(ck)
                                    checktt = fb2.info()
                                    if 'error' in checktt:
                                        print(
                                            f'Cookie Tài Khoản {name} Đã Bị Out or Checkpoint !!!                ')
                                        listck.remove(ck)
                                        ptool = 1
                                        break
                                    else:
                                        print(
                                            f'Tài Khoản {name} Đã Bị Block Cảm Xúc Cmt                            ', end='\r')
                                        sleep(1)
                                        print(
                                            '                                                        ', end='\r')
                                        nhiemvu = nhiemvu.replace('2', '')
                                        break
                if ptool == 1:
                    break
                if '9' in nhiemvu:
                    listlike = tds.get_nv_thuong('like')
                    if listlike == False:
                        print(
                            f'Không Get Được Nhiệm Vụ Like Thường                          ', end='\r')
                        sleep(1)
                        print(
                            '                                                        ', end='\r')
                    elif 'error' in listlike:
                        if listlike['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
                            count = listlike['countdown']
                            print(
                                f'Đang Get Nhiệm Vụ Like Thường, COUNTDOWN: {str(round(count, 3))}              ', end='\r')
                            sleep(1)
                            print(
                                '                                                       ', end='\r')
                            Delay(count)
                        else:
                            print(listlike['error'], end='\r')
                            sleep(1)
                            print(
                                '                                                       ', end='\r')
                    else:
                        list_nv = listlike
                        if len(list_nv) == 0:
                            print(
                                f'Hết Nhiệm Vụ Like Thường                          ', end='\r')
                            sleep(1)
                            print(
                                '                                                        ', end='\r')
                        else:
                            print(
                                f'Tìm Thấy {len(list_nv)} Nhiệm Vụ Like Thường                    ', end='\r')
                            for x in list_nv:
                                idpost = x['id']
                                id = idpost.split(
                                    '_')[1] if '_' in idpost else idpost
                                id2 = id[:3] + '*' * (len(id) - 6) + id[-3:]
                                like = fb.reaction(id, 'LIKE')
                                if like == False:
                                    print(
                                        f'FAIL LIKETHUONG: {id}            ', end='\r')
                                    sleep(2)
                                    print(
                                        '                                                       ', end='\r')
                                    Delay(3)
                                    loiliket += 1
                                else:
                                    nhan = tds.get_xu_thuong('LIKE', idpost)
                                    if 'success' in nhan:
                                        xu = nhan['data']['xu']
                                        msg = nhan['data']['msg']
                                        loiliket = 0
                                        dem += 1
                                        time = datetime.now().strftime('%H:%M:%S')
                                        print(
                                            f"[{dem}][{time}][LIKETHUONG][{id2}][{msg}][{str(format(int(xu), ','))}]")
                                        if dem % doinick == 0:
                                            ptool = 1
                                            break
                                        if dem % nvblock == 0:
                                            Delay(delaybl)
                                        else:
                                            Delay(randint(min, max))
                                if loiliket >= nhiemvuloi:
                                    fb2 = Facebook_Api(ck)
                                    checktt = fb2.info()
                                    if 'error' in checktt:
                                        print(
                                            f'Cookie Tài Khoản {name} Đã Bị Out or Checkpoint !!!                ')
                                        listck.remove(ck)
                                        ptool = 1
                                        break
                                    else:
                                        print(
                                            f'Tài Khoản {name} Đã Bị Block Like                            ', end='\r')
                                        sleep(1)
                                        print(
                                            '                                                        ', end='\r')
                                        nhiemvu = nhiemvu.replace('9', '')
                                        break
                if ptool == 1:
                    break
                if '0' in nhiemvu:
                    listlike = tds.get_nv_thuong('reaction')
                    if listlike == False:
                        print(
                            f'Không Get Được Nhiệm Vụ Cảm Xúc Thường                          ', end='\r')
                        sleep(1)
                        print(
                            '                                                        ', end='\r')
                    elif 'error' in listlike:
                        if listlike['error'] == 'Thao tác quá nhanh vui lòng chậm lại':
                            count = listlike['countdown']
                            print(
                                f'Đang Get Nhiệm Vụ Cảm Xúc Thường, COUNTDOWN: {str(round(count, 3))}              ', end='\r')
                            sleep(1)
                            print(
                                '                                                       ', end='\r')
                            Delay(count)
                        else:
                            print(listlike['error'], end='\r')
                            sleep(1)
                            print(
                                '                                                       ', end='\r')
                    else:
                        list_nv = listlike
                        if len(list_nv) == 0:
                            print(
                                f'Hết Nhiệm Vụ Cảm Xúc Thường                          ', end='\r')
                            sleep(1)
                            print(
                                '                                                        ', end='\r')
                        else:
                            print(
                                f'Tìm Thấy {len(list_nv)} Nhiệm Vụ Cảm Xúc Thường                    ', end='\r')
                            for x in list_nv:
                                idpost = x['id']
                                type = x['type']
                                id = idpost.split(
                                    '_')[1] if '_' in idpost else idpost
                                id2 = id[:3] + '*' * (len(id) - 6) + id[-3:]
                                like = fb.reaction(id, type)
                                if like == False:
                                    print(
                                        f'FAIL {type}: {id}            ', end='\r')
                                    sleep(2)
                                    print(
                                        '                                                       ', end='\r')
                                    Delay(3)
                                    loiliket += 1
                                else:
                                    nhan = tds.get_xu_thuong(type, idpost)
                                    if 'success' in nhan:
                                        xu = nhan['data']['xu']
                                        msg = nhan['data']['msg']
                                        loiliket = 0
                                        dem += 1
                                        time = datetime.now().strftime('%H:%M:%S')
                                        print(
                                            f"[{dem}][{time}][{type}THUONG][{id2}][{msg}][{str(format(int(xu), ','))}]")
                                        if dem % doinick == 0:
                                            ptool = 1
                                            break
                                        if dem % nvblock == 0:
                                            Delay(delaybl)
                                        else:
                                            Delay(randint(min, max))
                                if loiliket >= nhiemvuloi:
                                    fb2 = Facebook_Api(ck)
                                    checktt = fb2.info()
                                    if 'error' in checktt:
                                        print(
                                            f'Cookie Tài Khoản {name} Đã Bị Out or Checkpoint !!!                ')
                                        listck.remove(ck)
                                        ptool = 1
                                        break
                                    else:
                                        print(
                                            f'Tài Khoản {name} Đã Bị Block Cảm Xúc                            ', end='\r')
                                        sleep(1)
                                        print(
                                            '                                                        ', end='\r')
                                        nhiemvu = nhiemvu.replace('0', '')
                                        break

if __name__ == "__main__":
    
    Main()
