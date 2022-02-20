from os import listdir, path, mkdir
from turtle import width

import mss
import numpy as np
import PIL.Image
from cv2 import cv2

from .config import Config
from .logger import logger
from .utils import *


class Image:
    TARGETS = []
    TARGETS_GLOBAL = []
    MONITOR_LEFT = None
    MONITOR_TOP = None
    
    def load_targets_global():
        path = "assets/images/targets_global/"
        file_names = listdir(path)

        targets = {}
        for file in file_names:
            targets[replace(file, ".png")] = cv2.imread(path + file)

        Image.TARGETS_GLOBAL = targets

    def load_targets_default():
        path = "assets/images/targets/"
        file_names = listdir(path)

        targets = {}
        for file in file_names:
            targets[replace(file, ".png")] = cv2.imread(path + file)

        Image.TARGETS = targets
    
    def load_targets_user():
        Image.set_images_resolution()
        path = f"assets/images/targets_user/"
        file_names = listdir(path)

        Image.TARGETS = []
        targets = {}
        for file in file_names:
            targets[replace(file, ".png")] = cv2.imread(path + file)

        Image.TARGETS = targets

    def screen():
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = np.array(sct.grab(monitor))
            Image.MONITOR_LEFT = monitor["left"]
            Image.MONITOR_TOP = monitor["top"]
            return sct_img[:, :, :3]
    
    def get_monitor_with_target(target):
        position_bomb = Image.get_one_target_position(target, 0)
        with mss.mss() as sct:
            monitors = sct.monitors
        
        for monitor in monitors:
            if len(monitors) == 1:
                return monitor.values()
            if Image.position_inside_position(position_bomb, monitor.values()):
                return monitor.values()

        return monitors[0]
    
    def get_compare_result(img1, img2):
        return cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)

    
    def position_inside_position(position_in, position_out):
        x_in,y_in,w_in,h_in = position_in
        x_out,y_out,w_out,h_out = position_out

        start_inside_x = x_out <= x_in <= (x_out+w_out)
        finish_inside_x = x_out <= x_in + w_in <= (x_out + w_out)
        start_inside_y = y_out <= y_in <= (y_out+h_out)
        finish_inside_y = y_out <= y_in + h_in <= (y_out + h_out)
        
        return start_inside_x and finish_inside_x and start_inside_y and finish_inside_y


    def print_full_screen(image_name: str):
        image_name = f'{image_name}.png'
        image = pyautogui.screenshot()
        image.save(image_name)
        return image_name
        
    def print_partial_screen(image_name: str, target: str):
        image_name = f'{image_name}.png'
        x,y,w,h = Image.get_one_target_position(target, 0)
        image = pyautogui.screenshot(region=(x,y,w,h))
        image.save(image_name)
        return image_name

    def get_target_positions(target:str, screen_image = None, threshold:float=0.8, not_target:str=None):
        threshold_config = Config.PROPERTIES["threshold"]["to_work"]
        if(threshold_config):
            threshold = threshold_config
            
        target_img = Image.TARGETS[target]
        height, width = target_img.shape[:2]

        screen_img = Image.screen() if screen_image is None else screen_image
        result = cv2.matchTemplate(screen_img, target_img, cv2.TM_CCOEFF_NORMED)

        if not_target is not None:
            not_target_img = Image.TARGETS[not_target]
            not_target_result = cv2.matchTemplate(screen_img, not_target_img, cv2.TM_CCOEFF_NORMED)
            result[result < not_target_result] = 0

        y_result, x_result = np.where( result >= threshold)
        
        results_len = len(x_result)
        del_index = []
        for i in range(1, results_len):
            x = x_result[i]
            y = y_result[i]
            x_range = x_result[i-1], x_result[i-1]+width
            y_range = y_result[i-1], y_result[i-1]+height

            if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
                del_index.append(i)

        y_result = np.delete(y_result, del_index)
        x_result = np.delete(x_result, del_index)

        
        targets_positions = []
        for (x,y) in zip(x_result, y_result):
            x += Image.MONITOR_LEFT
            y += Image.MONITOR_TOP
            targets_positions.append([x,y,width,height])
            
        return targets_positions

    def get_first_target_position(target:str, screen_image = None, threshold:float=0.8, not_target:str=None):
        positions = Image.get_target_positions(target, screen_image, threshold, not_target)
        if len(positions) == 0:
            return None
        return positions[0]
    
    def get_one_target_position(target:str, threshold:float=0.8, target_global = False, screen_image = None):
        threshold_config = Config.get("threshold", "default")
        if(threshold_config):
            threshold = threshold_config
            
        target_img = Image.TARGETS_GLOBAL[target] if target_global else Image.TARGETS[target]
        screen_img = Image.screen() if screen_image is None else screen_image
        result = cv2.matchTemplate(screen_img, target_img, cv2.TM_CCOEFF_NORMED)

        if result.max() < threshold:
            raise Exception(f"{target} not found")
            
        yloc, xloc = np.where(result == result.max())
        xloc += Image.MONITOR_LEFT
        yloc += Image.MONITOR_TOP
        height, width = target_img.shape[:2]
        
        return xloc[0], yloc[0], width, height

    def get_max_result_between(targets:list, y_limits=None, x_limits=None, threshold:float=0, screen_img=None):
        index = 0
        max_result = 0
        for i, target in enumerate(targets):
            screen = Image.screen() if screen_img is None else screen_img
            if y_limits is not None:
                screen= screen[y_limits[0]:y_limits[1], :]
            if x_limits is not None:
                x,w = x_limits
                screen= screen[:, x:x+w]
            result = cv2.matchTemplate(screen, Image.TARGETS[target], cv2.TM_CCOEFF_NORMED)
            if result.max() > max_result:
                max_result = result.max()
                index = i
        
        return index


    def filter_by_green_bar(item):
        x,y,w,h = item
        y_increment = round(h*0.1)
        screen_img = Image.screen()[y:y+h+y_increment,:]
        result = Image.get_target_positions("hero_bar_green", screen_image=screen_img)
        return len(result) > 0
    
    def set_images_resolution():
        im_fh = np.array(Image.TARGETS_GLOBAL['screen_full_hd'])
        diag_fh = (im_fh.shape[0]**2 + im_fh.shape[1]**2)**0.5
        
        im_user = np.array(Image.TARGETS_GLOBAL['screen_user'])
        diag_user = (im_user.shape[0]**2 + im_user.shape[1]**2)**0.5
            
        user_interface_percent = (diag_user / diag_fh)
        
        path_user_by_resolution = f'./assets/images/targets_user'
        
        if not path.exists(path_user_by_resolution):
            mkdir(path_user_by_resolution)
            
        for image_name in Image.TARGETS:            
            image = PIL.Image.open(f'./assets/images/targets/{image_name}.png')
            h = round(np.array(image).shape[0] * user_interface_percent)
            w = round(np.array(image).shape[1] * user_interface_percent)
            image = image.resize((w,h), PIL.Image.ANTIALIAS)
            image.save(f'{path_user_by_resolution}/{image_name}.png')

      