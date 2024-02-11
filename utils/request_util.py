import requests
from . import config_util as config
from .log_util import logger


def extract_cookies(cookie):
    """
    从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies
    """
    cookies = dict([part.split("=", 1) for part in cookie.split("; ")])
    return cookies


def make_request(url, proxy_enabled=None, timeout=10):
    """
    发起网络请求到指定的 URL，可选包含 headers 和 proxies 参数。

    参数:
        url (str): 请求的 URL。
        headers (dict, 可选): 请求中包含的头部信息。
        proxies (dict, 可选): 请求中使用的代理。
        proxy_enabled (bool): 是否启用代理，默认为 False。

    返回值:
        bytes: 请求返回的内容。
    """
    if proxy_enabled is None:
        proxy_enabled = config.proxy_enabled
    try:
        if proxy_enabled:
            req = requests.get(url, headers=config.headers,
                               proxies=config.proxies_v2ray if config.proxies_v2ray_enabled else config.proxies_ssr,
                               timeout=timeout)
        else:
            req = requests.get(url, headers=config.headers, timeout=timeout)
        return req
    except requests.RequestException as e:
        logger.error(f'\n----请检查代理设置(检查config.yaml的代理配置)----\n{e}')
