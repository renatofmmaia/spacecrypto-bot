from distutils.command.config import config
from enum import Enum


from cv2 import cv2

from .config import Config
from .image import Image
from .logger import LoggerEnum, logger, logger_translated
from .mouse import *
from .utils import *
from .telegram import TelegramBot
class SpaceScreenEnum(Enum):
    POPUP_ERROR = -2
    NOT_FOUND = -1
    LOGIN = 0
    HOME = 1
    SHIP = 2
    HUNTING = 3
    BASE = 4
    LOSE = 5
    

class SpaceScreen:
    def wait_for_screen(
        spaceScreenEnum, time_beteween: float = 0.5, timeout: float = 60
    ):
        def check_screen():
            screen = SpaceScreen.get_current_screen()
            if screen == spaceScreenEnum:
                return True
            else:
                return None
        res = do_with_timeout(
            check_screen, time_beteween=time_beteween, timeout=timeout
        )
        
        if res is None:
            raise Exception(f'Timeout waiting for screen {spaceScreenEnum(spaceScreenEnum).name}.')
        
        return res
    
    def wait_for_leave_screen(
        spaceScreenEnum, time_beteween: float = 0.5, timeout: float = 60
    ):
        def check_screen():
            screen = SpaceScreen.get_current_screen()
            if screen == spaceScreenEnum:
                return None
            else:
                return True

        return do_with_timeout(
            check_screen, time_beteween=time_beteween, timeout=timeout
        )


    def get_current_screen(time_beteween: float = 0.5, timeout: float = 20):
        targets = {
            SpaceScreenEnum.HOME.value: Image.TARGETS["identify_home"],
            SpaceScreenEnum.LOGIN.value: Image.TARGETS["identify_login"],
            SpaceScreenEnum.BASE.value: Image.TARGETS["identify_base"],
            SpaceScreenEnum.HUNTING.value: Image.TARGETS["identify_hunting"],
            SpaceScreenEnum.LOSE.value: Image.TARGETS["identify_lose"],
            SpaceScreenEnum.POPUP_ERROR.value: Image.TARGETS["popup_erro"],
        }
        max_value = 0
        img = Image.screen()
        screen_name = -1

        for name, target_img in targets.items():
            result = cv2.matchTemplate(img, target_img, cv2.TM_CCOEFF_NORMED)
            max_value_local = result.max()
            if max_value_local > max_value:
                max_value = max_value_local
                screen_name = name

        return screen_name if max_value > Config.get("threshold", "default") else -1
    
    def go_to_home(manager):
        current_screen = SpaceScreen.get_current_screen()
        if current_screen == SpaceScreenEnum.HOME.value:
            return
        elif current_screen == SpaceScreenEnum.LOSE.value:
            click_when_target_appears("button_confirm_without_time")
            if not click_when_target_appears("button_hunt_ships"):
                Login.do_login(manager)
        elif current_screen == SpaceScreenEnum.HUNTING.value:
            logger_translated("Space Ships", LoggerEnum.BUTTON_CLICK)
            if not click_when_target_appears("button_hunt_ships"):
                Login.do_login(manager)
        else:
            Login.do_login(manager)
            return

        SpaceScreen.wait_for_screen(SpaceScreenEnum.HOME.value)
        
    def do_print_token(manager):
        logger_translated("print token", LoggerEnum.ACTION)
        image = None      
        
        try:
            image = Image.print_full_screen("print")
            TelegramBot.send_message_with_image(image, "Family JOW, não deixe de contribuir com a evolução do bot :D")
        except Exception as e:
            logger(str(e))
            logger("😬 Ohh no! We couldn't send your farm report to Telegram.", color="yellow", force_log_file=True)
        
        manager.set_refresh_timer("refresh_print_token")
    
class Login:
    def do_login(manager):
        current_screen = SpaceScreen.get_current_screen()
        logged = False
        
        if current_screen != SpaceScreenEnum.LOGIN.value and current_screen != SpaceScreenEnum.NOT_FOUND.value and current_screen != SpaceScreenEnum.POPUP_ERROR.value:
            logged = True

        if not logged:
            logger_translated("login", LoggerEnum.ACTION)

            login_attepmts = Config.PROPERTIES["screen"]["number_login_attempts"]
        
            for i in range(login_attepmts):
                
                if SpaceScreen.get_current_screen() != SpaceScreenEnum.LOGIN.value:
                    refresh_page()
                    SpaceScreen.wait_for_screen(SpaceScreenEnum.LOGIN.value)

                logger_translated("Login", LoggerEnum.PAGE_FOUND)

                logger_translated("wallet", LoggerEnum.BUTTON_CLICK)
                if not click_when_target_appears("button_connect_wallet"):
                    refresh_page()
                    continue

                logger_translated("sigin wallet", LoggerEnum.BUTTON_CLICK)
                if not click_when_target_appears("button_connect_wallet_sign"):
                    refresh_page()
                    continue
                
                logger_translated("play", LoggerEnum.BUTTON_CLICK)
                if not click_when_target_appears("button_connect_wallet_play"):
                    refresh_page()
                    continue

                if (SpaceScreen.wait_for_screen(SpaceScreenEnum.HOME.value) != SpaceScreenEnum.HOME.value):
                    logger("🚫 Failed to login, restart proccess...")
                    continue
                else:
                    logger("🎉 Login successfully!")
                    logged = True
                    break

        manager.set_refresh_timer("refresh_login")
        return logged
    
class Ship:
    def do_check_error(manager):        
        current_screen = SpaceScreen.get_current_screen()
        
        if current_screen == SpaceScreenEnum.POPUP_ERROR.value or current_screen == SpaceScreenEnum.NOT_FOUND.value:
            logger_translated("Check screen error found, restarting...", LoggerEnum.ERROR)
            Login.do_login(manager)

        manager.set_refresh_timer("refresh_check_error")
        
    def keep_working(manager):
        logger_translated(f"Ships keeping work", LoggerEnum.ACTION)
        
        current_screen = SpaceScreen.get_current_screen()
        
        if current_screen != SpaceScreenEnum.HOME.value:
            SpaceScreen.go_to_home(manager)
        
        scale_factor = 25
        ship_bar = [
            "ship_bar_50", "ship_bar_75", "ship_bar_100"
        ]
        
        if current_screen == SpaceScreenEnum.HUNTING.value:
            return True
        
        scroll_times=0
        n_ships = 0

        def click_first(btns_pos):
            for button_position in btns_pos:
                x,y,w,h = button_position
                initial_y = y + h - height_search_area
                final_y = initial_y + height_search_area
                
                search_img = screen_img[initial_y:final_y, :, :]

                life_max_values = [Image.get_compare_result(search_img, Image.TARGETS[bar]).max() for bar in ship_bar]
                life_index, life_max_value= 0, 0
                for i, value in enumerate(life_max_values):
                    life_index, life_max_value = (i, value) if value >= life_max_value else (life_index, life_max_value)

                ship_life = 50 + (life_index * scale_factor)

                logger(f"{ship_life}%", end=" ", datetime=False)
                if ship_life >= ship_work_percent:
                    click_randomly_in_position(x,y,w,h)
                    logger("💪;", datetime=False)
                    return True
                else:
                    logger("💤;", datetime=False)
                
                return False

        logger(f"Sending ships to fight:")
        
        while scroll_times <= (Config.get('screen','scroll', 'repeat')):
            if n_ships >= Config.get('screen','n_ships_to_fight'):
                break
            
            screen_img = Image.screen()
            
            buttons_position = Image.get_target_positions("button_fight_on", not_target="button_fight_off", screen_image=screen_img)
            
            if not buttons_position:
                Ship.scroll_screen()
                scroll_times += 1
                continue 

            x_buttons, _, w_buttons, _ = buttons_position[0]
            height_search_area, width_search_area = Image.TARGETS["ship_search_area"].shape[:2]
            inital_x = x_buttons + w_buttons - width_search_area
            final_x = inital_x + width_search_area
            
            screen_img = screen_img[:,inital_x:final_x, :]
            logger("↳", end=" ", datetime=False)
            
            ship_work_percent = Config.get('ship_work_percent')
            
            if click_first(buttons_position):
                n_ships +=1
                continue
        
        click_when_target_appears('btn_fight_boss')
        click_when_target_appears('button_confirm_without_time', 10)    

        logger(f"🚀 {n_ships} new ships sent to explode the boss 💣💣💣.")
        manager.set_refresh_timer("refresh_ships")
        return True

    def scroll_screen():
        scroll( 
                    safe_scroll_target="ship_bar_vertical",
                    distance=Config.get('screen','scroll', 'distance'),
                    duration=Config.get('screen','scroll', 'duration'),
                    wait=Config.get('screen','scroll', 'wait'),
                )