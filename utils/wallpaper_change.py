import ctypes
from .wallpaper_downloader import select_pic


def change_wallpaper():
    SPI_SETDESKWALLPAPER = 0x0014
    wallpaper_path = select_pic()
    # 更新壁纸
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)
    if not wallpaper_path:
        print('无法更改壁纸。')
    elif result:
        print('壁纸已更改成功！')
