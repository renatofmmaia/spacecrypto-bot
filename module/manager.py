import time

from .spaceScreen import SpaceScreen, SpaceScreenEnum, Login, Ship
from .logger import logger
from .mouse import *
from .utils import *
from .window import get_windows
from .config import Config
from enum import Enum

def create_managers():
    return [Manager(w) for w in get_windows("Space Crypto")]

class StateEnum(Enum):
    STARTING = 0,
    FIGHTING = 1,
    RECHARGE = 2,

class Manager:
    def __init__(self, window) -> None:
        self.window = window
        self.refresh_check_error = 0
        self.refresh_ships = 0
        self.refresh_print_token = 0
        self.state = StateEnum.STARTING


    def __enter__(self):
        self.window.activate()
        time.sleep(2)
        return self

    def __exit__(self, type, value, tb):
        return

    def do_what_needs_to_be_done(self, current_screen):
                
        check_error = current_screen == SpaceScreenEnum.POPUP_ERROR.value or current_screen == SpaceScreenEnum.NOT_FOUND.value
        
        refresh_check_error = Config.get('screen', 'refresh_check_error')*60
        if ((check_error) or (refresh_check_error and (now() - self.refresh_check_error > refresh_check_error))):
            Ship.do_check_error(self)

        Ship.check_lose(self)
        Ship.check_victory(self)

        refresh_ships = Config.get('refresh_ships')*60
        if (refresh_ships and (now() - self.refresh_ships > refresh_ships)):
            Ship.keep_working(self)
        
        if Config.get('telegram','token') and  Config.get('telegram','chat_id'):
            refresh_print_token = Config.get('telegram', 'refresh_print_token')*60
            if (refresh_print_token and (now() - self.refresh_print_token > refresh_print_token)):
                SpaceScreen.do_print_token(self)
        
        return True
    
    def set_refresh_timer(self, propertie_name):
        setattr(self, propertie_name, time.time())

    @property
    def is_starting(self):
        return self.state == StateEnum.STARTING
    
    def set_fighting(self):
        logger("💪 change state to fighting")
        self.state = StateEnum.FIGHTING

    @property
    def is_fighting(self):
        return self.state == StateEnum.FIGHTING
    
    def set_recharge(self):
        logger("💤 change state to recharge")
        self.state = StateEnum.RECHARGE

    @property
    def is_recharging(self):
        return self.state == StateEnum.RECHARGE
