import logging

# 创建一个logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志级别，可选DEBUG, INFO, WARNING, ERROR, CRITICAL

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('./app.log')
fh.setLevel(logging.DEBUG)  # 文件处理器也可以设置不同的日志级别

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

# 记录一条日志
# logger.info("This is an info message")
# logger.debug("Debugging information")
# logger.warning("Warning exists")
# logger.error("An error occurred")
# logger.critical("Critical error")

# 当不再需要日志功能时，可以移除所有handler
# logger.handlers.clear()
