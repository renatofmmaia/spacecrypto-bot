import time

import PIL.Image
import pyautogui

from .image import Image
from .logger import logger
from .utils import *


def click_on_multiple_targets(target: str, not_click:str= None, filter_func = None):
    """click in a list of target. Returns number of clicks"""
    targets_positions = Image.get_target_positions(target, not_target=not_click)
    n_before = (len(targets_positions))
    logger(f"found {n_before} targets")
    if filter_func is not None:
        targets_positions = filter(filter_func, targets_positions)
    logger(f"{n_before - len(list(targets_positions))} targets filtered")
    click_count = 0
    for x, y, w, h in targets_positions:
        x, y, move_duration, click_duration, time_between  = randomize_values(x, w, y, h)
        pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeOutQuad)
        time.sleep(time_between)
        pyautogui.click(duration=click_duration)
        click_count += 1
    
    return click_count    

def click_one_target(target: str, target_global: bool = False):
    """click in a target. Returns number of clicks"""
    result = None
    try:
        x_left, y_top, w, h = Image.get_one_target_position(target, target_global=target_global)
        x, y, move_duration, click_duration, time_between  = randomize_values(x_left, w, y_top, h)
        pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeOutQuad)
        time.sleep(time_between)
        pyautogui.click(duration=click_duration)
        result = True
    except Exception as e:
        return None
        # logger(f"Error: {e}")
    
    return result

def click_in_one_of_targets(targets: list, target_global: bool = False):
    for target in targets:
        if click_one_target(target):
            return True

def click_randomly_in_position(x, y, w, h):
    x, y, move_duration, click_duration, time_between  = randomize_values(x, w, y, h)
    pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeOutQuad)
    time.sleep(time_between)
    pyautogui.click(duration=click_duration)


def click_when_target_appears(target: str, time_beteween: float = 0.5, timeout: float = 10, target_global = False):
    """ Click in a target when it appears.
        It will check for target every `time_beteween` seconds.
        After timeout seconds it will return 0 if no target was found.
        Returns 1 if target was found.
    """
    return do_with_timeout(click_one_target, args = [target, target_global])

def click_when_one_of_targets_appears(targets: list, time_beteween: float = 0.5, timeout: float = 10, target_global = False):
    return do_with_timeout(click_in_one_of_targets, args = [targets, target_global])

def randomize_values(x, w, y, h):
    x_rand = randomize_int(x, w, 0.20)
    y_rand = randomize_int(y, h, 0.20)
    move_duration = randomize(0.1, 0.5)
    click_duration = randomize(0.05, 0.2)
    time_between = randomize(0.05, 0.3)

    return x_rand, y_rand, move_duration, click_duration, time_between

def move_to(target:str):
    def move_to_logical():
        try:
            x, y, w, h = Image.get_one_target_position(target)
            x, y, move_duration, click_duration, time_between  = randomize_values(x, w, y, h)
            pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeOutQuad)
            return True
        except Exception as e:
            return None

    return do_with_timeout(move_to_logical)

def move_to_one_of_targets(targets: list, target_global: bool = False):
    for target in targets:
        if move_to(target):
            return True

def move_to_when_one_of_targets_appears(targets: list, time_beteween: float = 0.5, timeout: float = 10, target_global = False):
    return do_with_timeout(move_to_one_of_targets, args = [targets, target_global], time_beteween=time_beteween, timeout=timeout)
    
def scroll_and_click_on_targets(safe_scroll_target: str, repeat: int, distance:float, duration: float, wait:float, function_between, execute_before=True):
    res = []
    if execute_before:
        res.append(function_between())

    for i in range(repeat):
        move_to(safe_scroll_target)
        pyautogui.mouseDown(duration=0.1)
        pyautogui.moveRel(0, distance, duration)
        time.sleep(0.3)
        pyautogui.mouseUp(duration=0.1)
        time.sleep(wait)
        click_when_target_appears(safe_scroll_target)
        res.append(function_between())    
    
    return res

def scroll(safe_scroll_target, distance:float, duration: float, wait:float):

    if type(safe_scroll_target) is list:
        move_to_when_one_of_targets_appears(safe_scroll_target)
    else:
        move_to(safe_scroll_target)

    pyautogui.mouseDown(duration=0.1)
    pyautogui.moveRel(0, distance, duration)
    time.sleep(0.3)
    pyautogui.mouseUp(duration=0.1)
    time.sleep(wait)