import requests
import json
import re
import time
import pickle
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from urllib.parse import urljoin
import cv2
import numpy as np
import base64

from personal_info import login_data
from slide import SlideCrack


headers = {
    "Cookie": "",
}


def cookies2str(cookies):
    cookie = [item["name"] + "=" + item["value"] for item in cookies]
    cookiestr = ';'.join(item for item in cookie)
    return cookiestr

class Reportor():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = "https://idas.uestc.edu.cn/authserver/login"
        self.sess = requests.Session()
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 100)
        self.login()
        self.update_cookies()

    def login(self):
        # self.driver.get(self.daily_report_url)
        # TODO selenium输入密码登录,并且实现滑块验证码破解
        self.driver.get(self.login_url)
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="casLoginForm"]/p[4]/button').click()

        self.get_captcha1()
        self.get_captcha2()
        # 滑块图片
        image1 = "./front.png"
        # 背景图片
        image2 = "./bg.png"
        # 处理结果图片,用红线标注
        image3 = "/.3.png"
        sc = SlideCrack(image1, image2, image3)
        distance = sc.discern()
        slider = self.get_slider()
        track = self.get_track(distance)
        self.move_to_gap(slider, track)

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()         # 利用动作链，获取slider，perform是

        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()       # xoffset横坐标，yoffset纵坐标。使得鼠标向前推进
        time.sleep(0.5)                                     # 推动到合适位置之后，暂停一会
        ActionChains(self.driver).release().perform()      # 抬起鼠标左键

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'slider')))
        return slider

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:                   # 所以 track是不会大于总长度的
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 移动距离x = v0t + 1/2 * a * t^2，现做了加速运动
            move = v0 * t + 1 / 2 * a * t * t
            # 当前速度v = v0 + at  速度已经达到v，该速度作为下次的初速度
            v = v0 + a * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))                   # track 就是最终鼠标在 X 轴移动的轨迹
        return track

    def get_captcha1(self):
        JS = 'return document.getElementsByTagName("canvas")[0].toDataURL("image/png");'
        # 执行 JS 代码并拿到图片 base64 数据
        im_info = self.driver.execute_script(JS)  #执行js文件得到带图片信息的图片数据
        im_base64 = im_info.split(',')[1]  #拿到base64编码的图片信息
        im_bytes = base64.b64decode(im_base64)  #转为bytes类型
        with open('bg.png','wb') as f:  #保存图片到本地
            f.write(im_bytes)

    def get_captcha2(self):
        JS = 'return document.getElementsByTagName("canvas")[1].toDataURL("image/png");'
        # 执行 JS 代码并拿到图片 base64 数据
        im_info = self.driver.execute_script(JS)  #执行js文件得到带图片信息的图片数据
        im_base64 = im_info.split(',')[1]  #拿到base64编码的图片信息
        im_bytes = base64.b64decode(im_base64)  #转为bytes类型
        with open('front.png','wb') as f:  #保存图片到本地
            f.write(im_bytes)


if __name__ == "__main__":
    reportor = Reportor(login_data['username'], login_data['password'])
    