import requests
from . import config_util as config
from .log_util import logger


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
    proxy_dict = {
        'http': config.proxy_url,
        'https': config.proxy_url,
    }
    if proxy_enabled is None:
        proxy_enabled = config.proxy_enabled
    try:
        if proxy_enabled:
            req = requests.get(url, headers=config.headers, proxies=proxy_dict, timeout=timeout)
        else:
            req = requests.get(url, headers=config.headers, timeout=timeout)
        # logger.info(f'请求结果{req}')
        return req
    except requests.RequestException as e:
        logger.error(f'\n----请检查代理设置(检查config.yaml的代理配置),非代理下载不稳定，建议开启代理----\n{e}')
