import requests
import json
import os
import random
import time

class pixiv_downloader:

    def __init__(self):
        """初始化部分变量以及参数"""

        self.cookies = {
            'first_visit_datetime_pc': '2025-04-26%2000%3A51%3A30',
            'p_ab_id': '3',
            'p_ab_id_2': '5',
            'p_ab_d_id': '2120287316',
            'yuid_b': 'QnZEcUg',
            '_ga': 'GA1.1.486650107.1745596292',
            'PHPSESSID': '51673615_qSCAtnP8aLzcLWCpVDnxKUZ8cDygx4Xw',
            'device_token': '3b2b5a0560499c549a0404e054dbe5f0',
            'privacy_policy_agreement': '7',
            'c_type': '25',
            'privacy_policy_notification': '0',
            'a_type': '0',
            'b_type': '1',
            '_ga_MZ1NL4PHH0': 'GS1.1.1745728699.2.1.1745729041.0.0.0',
            '__cf_bm': 'tnTfNYOME3t675rkc.89V6I7MqHacgNvlnaBpuhTngg-1745754106-1.0.1.1-VdUGxzwl2.RtOatmhXAzUJObLOanOBQbNR5DRwf11wrgkv7ORSY8idAj387P.xm1dND0cE_C.oQ8rd0E3TnNSiQTW6Q_5ipZhrWU4fVVTZ2iRjdd1g2usrojIALVHz.O',
            '_ga_75BBYNYN9J': 'GS1.1.1745754202.8.0.1745754202.0.0.0',
            'cf_clearance': 'FaFpzDXrhtaNcLhhCfNjKkrLR1XJc.g5nbHVlkzK.z0-1745754205-1.2.1.1-hrgjgI9ZLJxvUNBFkoxA1XX9TfhW0UO5Kx49W8gNgbscQfg6PT1mo14ihdzf3..r03yeTWDkHMerJwXm4q.jpv1AakB23HDqTeMYt9Y0uX63PKQsbHt9o3hZK93rpR0z9bzxgvVpTkNmoXW90s33Vb5VJSDH9b6ldog6zvfNW8CCMWhP2ih7VJZqtr8ZXd6YWI5wwuJTUmeirU43HIw7jd0523lCbv6LlEYDIUg.ScnhDNH0AnBoiUccVif25P1By16JaNF6y5ED1SSV_6t5bZZCGXrpvU74W6WpKxmaHUOAjUOmqcMTLVOJph.ykNctNYWWpFvwBR7oG.kj4XosF0BygsYhJp1qD0jkOGawoKs',
        }

        self.headers = {
            'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'baggage': 'sentry-environment=production,sentry-release=6fd5102e49345241a6127965c0bd65bd4f7efc35,sentry-public_key=ef1dbbb613954e15a50df0190ec0f023,sentry-trace_id=1cc46bc52a12021f464004e126aa5295,sentry-sampled=false',
            'priority': 'u=1, i',
            'referer': 'https://www.pixiv.net/',
            'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sentry-trace': '1cc46bc52a12021f464004e126aa5295-870254c1b1679fd4-0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
            'x-user-id': '51673615',
        }

    def download(self):
        """下载文本文件中所有的用户的作品"""

        with open(rf'./user_ids.txt', mode='r', encoding='utf8') as user_ids_file:

            user_id = user_ids_file.readline().strip()

            """遍历文件user_ids中的所有用户的id"""
            while user_id:

                self.user_id = user_id

                self.download_one_user(user_id=user_id)

                print(f'----已成功下载用户id为{user_id}的用户的全部作品----')

                user_id = user_ids_file.readline().strip()

        print('----已成功下载文件user_isd.txt中所有用户的作品----')

    def download_one_user(self, user_id):
        """根据参数user_id下载一个用户的所有作品"""

        # 创建一个用于保存当前user_id的作品的文件夹
        self.create_dir(dir_path=rf'./contents/{user_id}')

        # 获取当前指定用户的所有作品的id,包括illust_ids 和 manga_ids
        self.get_artwork_ids(user_id=user_id)

        # 遍历illust_ids，下载所有的插图
        self.download_illusts()

        # 下载当前用户的所有漫画
        self.download_mangas()

        print(rf'----用户{self.user_id}的所有作品均已下载完毕----')

    def get_artwork_ids(self, user_id):
        """根据参数user_id获取当前目标用户的所有作品的作品id"""

        prrams = {'lang' : 'zh', 'sensitiveFilterMode' : 'userSetting'}

        url         = rf'https://www.pixiv.net/ajax/user/{user_id}/profile/all?sensitiveFilterMode=userSetting&lang=zh'

        params = {
            'sensitiveFilterMode': 'userSetting',
            'lang': 'zh',
        }

        responce = requests.get(url=url, headers=self.headers, cookies=self.cookies,params=params)

        responce = responce.content.decode(responce.apparent_encoding)

        json_responce = json.loads(responce)

        try:

            self.illust_ids = json_responce['body']['illusts']

        except:

            self.illust_ids = {}

        self.manga_ids = json_responce['body']['manga']

        if (type(self.manga_ids) == type([])):

            self.manga_ids = {}

        # print(f'{self.illust_ids} \n {self.manga_ids}')

    def download_illusts(self):
        """下载所有的插画"""

        print(self.illust_ids)

        for illust_id in self.illust_ids.keys():  # 遍历illust_ids

            # # 创建一个拥有保存当前user_id的用户的插画的文件夹
            # self.create_dir(rf'./contents/{self.user_id}/插画')

            # 获取当前插画作品的所有原图下载链接
            original_urls = self.get_illust_original_urls(illust_id=illust_id)

            # 下载当前id指定的所有插画
            self.download_illust(original_urls=original_urls, illust_id=illust_id)

        print(rf'----用户{self.user_id}的所有插画均已下载完毕----')

    def get_illust_original_urls(self, illust_id):
        """获取当前作品的原图下载链接"""

        url = rf'https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang=zh'

        responce = requests.get(url=url, headers=self.headers, params={'lang': 'zh'}, cookies=self.cookies)

        responce = responce.content.decode(responce.apparent_encoding)

        print(responce)

        json_responce = json.loads(responce)

        original_urls = []

        for element in json_responce['body']:

            original_url = element['urls']['original']

            original_urls.append(original_url)

        # print(original_urls)

        return original_urls

    def download_illust(self, original_urls, illust_id):
        """根据参数中的图片原图链接，下载图片"""

        illust_number = 0

        for original_url in original_urls:

            # 分支结构，选择图片的后缀名格式
            if 'jpg' in original_url:

                content_type = '.jpg'

            elif 'png' in original_url:

                content_type = '.png'

            elif 'jpeg' in original_url:

                content_type = 'jpeg'

            elif 'gif' in original_url:

                content_type = 'gif'

            else:

                print(rf'原图链接为{original_url}的图片未成功下载')

                exit()

            content_path = rf'./contents/{self.user_id}/{illust_id}_{illust_number}{content_type}'

            # 判断当前媒体内容是否已经在磁盘中存在，如果存在就跳过，不存在就将其下载下来
            if os.path.exists(content_path):

                continue

            responce = requests.get(url=original_url, headers=self.headers, cookies=self.cookies).content

            # 将已经获取到的媒体数据写入到本地磁盘中
            with open(content_path, mode='wb') as file:

                file.write(responce)

            illust_number += 1

            self.delay(min_ms=200, max_ms=300)

    def create_dir(self, dir_path):
        """创建一个根据参数dif_path指定的文件夹"""

        if not os.path.exists(dir_path):

            os.mkdir(dir_path)

        else:

            pass

    def delay(self, min_ms, max_ms):
        """延时一段时间"""

        time.sleep(random.randint(min_ms, max_ms)/1000)

    def download_mangas(self):
        """下载当前指定用户的所有漫画作品"""

        self.illust_ids = self.manga_ids

        self.download_illusts()


downloader = pixiv_downloader()
downloader.download()