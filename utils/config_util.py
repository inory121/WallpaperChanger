import yaml
from .log_util import logger
# 读取YAML配置文件
try:
    with open('./config.yaml', "r") as yaml_file:
        config_data = yaml.safe_load(yaml_file)
except FileNotFoundError:
    logger.error("配置文件不存在，请检查路径。")
except yaml.YAMLError as e:
    logger.error("YAML 文件格式错误:", e)


# 访问配置数据
proxy_enabled = config_data.get("proxy", {}).get("enabled", False)
headers = config_data.get("headers", {})
proxies_v2ray_enabled = config_data.get("proxies_v2ray", {}).get("enabled", False)
proxies_v2ray = config_data.get("proxies_v2ray", {})
proxies_ssr_enabled = config_data.get("proxies_ssr", {}).get("enabled", False)
proxies_ssr = config_data.get("proxies_ssr", {})
konachan_rating = config_data.get("konachan", {}).get("rating", "")
konachan_domain = config_data.get("konachan", {}).get("domain", "")
