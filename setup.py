import sys
from cx_Freeze import setup, Executable

# 声明包含的模块及依赖项
includes = []
excludes = []
packages = ["utils", "ui"]

# 设置主程序入口
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="changeWallpaper",
    version="1.0.0",
    description="换壁纸",
    executables=[
        Executable("main.py", base="Console")
    ],
    options={
        "build_exe": {
            "include_files": ["config.yaml"],  # 如果有需要包含的数据文件
            "includes": includes,
            "excludes": excludes,
            "packages": packages,
        }
    },
)