import os
import pathlib
from pathlib import Path
# 获取当前模块的绝对路径
module_path = os.path.abspath(__file__)

# 提取项目根目录路径
project_root = str(pathlib.Path(module_path).parent.parent)

# 打印项目根目录路径
print(project_root)

# if getattr(sys, 'frozen', False):
#     # 如果是PyInstaller打包的环境
#     base_path = Path(sys._MEIPASS)
#     print(base_path)
# else:
# 开发环境或直接运行脚本时
base_path = Path(__file__).parent
print(base_path)

config_path = base_path / 'config.yaml'
