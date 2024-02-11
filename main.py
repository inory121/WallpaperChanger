import os

from ui.mainwindow import run_gui_app
if __name__ == "__main__":
    final_folder = os.getcwd() + './Konachan/'
    os.makedirs(final_folder, exist_ok=True)
    run_gui_app()
