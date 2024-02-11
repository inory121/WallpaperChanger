import os
import json
import time
import random
import requests
from PyQt5.QtCore import QObject, pyqtSignal
from bs4 import BeautifulSoup
from .log_util import logger
from .request_util import make_request
from . import config_util as config


def select_pic(image_folder=os.getcwd() + '/Konachan'):
    last_shown_image = None
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    if image_files:
        while True:
            random_image = random.choice(image_files)
            if random_image != last_shown_image:
                full_image_path = os.path.join(image_folder, random_image)
                last_shown_image = random_image
                logger.info(f'{full_image_path}')
                return full_image_path
            else:
                continue
    else:
        print("该文件夹下没有找到任何图片文件.")


class ImageDownloader(QObject):
    finished = pyqtSignal()
    BASE_URL = f"https://konachan.{config.konachan_domain}"

    def __init__(self):
        super().__init__()

    @staticmethod
    def _get_random_page_number(previous_page):
        while True:
            user_input = input('Input:请输入您爬取的页数，默认为随机页:')
            if not user_input.strip():
                return random.randint(1, int(previous_page))
            try:
                return int(user_input)
            except ValueError:
                print("无效的输入，请输入一个整数。")

    @staticmethod
    def _create_folder(tags):
        final_folder = os.path.join(os.getcwd(), 'Konachan', tags) if tags else os.path.join(os.getcwd(), 'Konachan')
        os.makedirs(final_folder, exist_ok=True)
        return final_folder

    @staticmethod
    def _download_images(final_folder, jsonlist):
        for item in jsonlist:
            id_number = item['id']
            parent_id = item['parent_id']
            rating = item['rating']
            file_url = item['file_url']
            if parent_id is not None or rating != 's':
                continue
            file_suffix = os.path.splitext(file_url)[1]
            final_file_path = os.path.join(final_folder, str(id_number) + file_suffix)
            os.makedirs(os.path.dirname(final_file_path), exist_ok=True)
            if os.access(final_file_path, os.F_OK):
                logger.info(f'图片{id_number}存在，跳过')
            else:
                try:
                    res = make_request(file_url)
                    res.raise_for_status()
                    with open(final_file_path, 'wb') as f:
                        f.write(res.content)
                    logger.info(f'下载id为{id_number}的图片,url链接为{file_url}')
                except (requests.exceptions.RequestException, FileNotFoundError, PermissionError) as e:
                    logger.error(f"下载id为{id_number}的图片出错: {str(e)}")

    def start_download(self):
        pages_num = None
        try:
            tags = input('Input:请输入您的tags:')
            limit = input('Input:请输入您的limit(想要获取多少张图片，每次上限100):')
            res = make_request(self.BASE_URL + '/post').content
            soup = BeautifulSoup(res, 'html.parser')
            next_page_element = soup.find('a', class_='next_page')
            previous_page = next_page_element.find_previous_sibling('a').text if next_page_element else 1
            logger.info(f'检测到总页数为{previous_page},回车开始随机选择一页下载，或者手动输入要下载的页数')
            pages_num = self._get_random_page_number(previous_page)
            logger.info(f'开始下载第{pages_num}页')
            final_folder = self._create_folder(tags)
            url_net = f'{self.BASE_URL}/post.json?page={pages_num}&tags={tags}&limit={limit}'
            res = make_request(url_net).content
            jsonlist = json.loads(res)
            if not jsonlist:
                os.rmdir(final_folder)
                logger.error('请检查输入的参数是否有误！！')
                self.start_download()
            self._download_images(final_folder, jsonlist)
            print('进入休眠3s')
            time.sleep(3)
        except (requests.exceptions.RequestException, ValueError, json.JSONDecodeError) as e:
            logger.error(f"获取第{pages_num}页数据时出错: {str(e)}")
        self.finished.emit()
        return
