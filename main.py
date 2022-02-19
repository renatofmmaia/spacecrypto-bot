import sys
import traceback
from time import sleep
import numpy as np
import PIL

import requests
from packaging import version

from module.spaceScreen import SpaceScreen, SpaceScreenEnum
from module.config import Config
from module.image import Image
from module.logger import logger, reset_log_file
from module.manager import create_managers
from module.telegram import TelegramBot
from module.window import get_resolution, WindowsResolutionEnum

__version__ = "0.0.3"


def main(config_file):
    try:
        # monitor_resolution = get_resolution()
        # if(monitor_resolution == WindowsResolutionEnum.NOT_SUPPORTED):
        #     logger("Oh no, your resolution is not supported, this bot only support 1920x1080", color="red", force_log_file=True)
        #     quit()
        
        # Load configs
        Config.load_config(config_file)
        TelegramBot.load_config()
        Image.load_targets_global()
        Image.load_targets_default()
        user_interface_percent = Image.set_images_resolution()
        Image.load_targets_user(user_interface_percent)
        
        
        # if Config.get("generals", "reset_log_file"):
        #     reset_log_file()

        # r = requests.get(
        #     "https://api.github.com/gists/715eabaa3bca5ca70709a6397b806e86"
        # )
        # if r.ok:
        #     data = r.json()

        #     start_message = data["files"]["start_message"]["content"]
        #     logger(start_message, color="cyan", datetime=False)

        #     last_version = data["files"]["version"]["content"].strip()
        #     version_installed = version.parse(__version__)
        #     logger(f"-> Current version: {version_installed}", color="cyan", datetime=False)

        #     if version.parse(last_version) > version.parse(__version__):
        #         logger("-----------------------------------------------", color="green", datetime=False)
        #         logger(f"New version available: {last_version}.", color="green", datetime=False)
        #         update_message = data["files"]["update_message"]["content"]
        #         logger(update_message, color="green", datetime=False)
        #         logger("-----------------------------------------------", color="green", datetime=False)
        # else:
        #     logger("Unable to check for updates.")

        managers = create_managers()
        logger(f"{len(managers)} Spacecrypto window (s) found")
        browser_count = 1
        show_initial_screen_message = True
        while True:
            try:
                for manager in managers:
                    current_screen = SpaceScreen.get_current_screen()
                    
                    if show_initial_screen_message:
                        logger(f"💫 Spacecrypto window[{browser_count}] inicializado em: {SpaceScreenEnum(current_screen).name}")
                    
                    with manager:
                        manager.do_what_needs_to_be_done(current_screen)
                    
                    if browser_count == len(managers):
                        browser_count = 1
                        show_initial_screen_message = False
                    else:
                        browser_count += 1
            except Exception as e:
                logger(
                    traceback.format_exc(),
                    color="red",
                    force_log_file=True,
                    terminal=False,
                )
                logger(
                    f"😬 Ohh no! A error has occurred in the last action.\n{e}\n Check the log  file for more details.",
                    color="yellow",
                )
            sleep(5)
    except Exception as e:
        logger(traceback.format_exc(), color="red", force_log_file=True, terminal=False)
        logger("😬 Ohh no! We couldn't start the bot.", color="red")


if __name__ == "__main__":
    config_path = "config.yaml"

    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        config_path = f"config_profiles/{config_file}.yaml"

    main(config_path)
