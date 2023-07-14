import os
import time
import socket
import subprocess
import pandas as pd
from tkinter import font
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get("https://www.spotify.com/tw/")
chrome.maximize_window()

login_button = chrome.find_element_by_xpath('//*[@id="__next"]/div[1]/header/div/nav/ul/li[6]/a') 
login_button.click()

time.sleep(1)
account = chrome.find_element_by_xpath('//*[@id="login-username"]') 
account.send_keys("wlyang1232001@yahoo.com.tw")
password = chrome.find_element_by_xpath('//*[@id="login-password"]') 
password.send_keys("23807715")
login_button = chrome.find_element_by_xpath('//*[@id="login-button"]')
login_button.click()

time.sleep(8)
search_button = chrome.find_element_by_xpath('//*[@id="main"]/div/div[2]/nav/div[1]/ul/li[2]/a')
search_button.click()

time.sleep(2)
search = chrome.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/form/input')
search.send_keys("因為你 所以我")

time.sleep(2)
target_song= chrome.find_element_by_xpath('//*[@id="searchPage"]/div/div/section[2]/div[2]/div/div/div/div[2]/div[1]/div')
target_song.click()
target_song = chrome.find_element_by_xpath('//*[@id="searchPage"]/div/div/section[2]/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/button')
target_song.click()

play = True
Key_action = webdriver.ActionChains(chrome)
action = chrome.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[3]/div/div[3]/div/div')
action.click()

while(1):
    gesture_type = input()

    if gesture_type == "0":  # 開始撥放 OK
        if not play:
            action = chrome.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button')
            action.click()
            play = not play
    if gesture_type == "1":  # 暫停撥放 5
        if play:
            action = chrome.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button')
            action.click()
            play = not play
    if gesture_type == "2":  # 音量下降 YA向下
        Key_action = webdriver.ActionChains(chrome)
        Key_action.key_down(Keys.ALT)
        Key_action.key_down(Keys.DOWN)
        Key_action.key_up(Keys.DOWN)
        Key_action.perform()
    if gesture_type == "3":  # 音量增加 YA向上
        Key_action = webdriver.ActionChains(chrome)
        Key_action.key_down(Keys.ALT)
        Key_action.key_down(Keys.UP)
        Key_action.key_up(Keys.UP)
        Key_action.perform()
    if gesture_type == "4":  # 上一首 大拇指向左
        action = chrome.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[1]/button[2]')
        action.click()
    if gesture_type == "5":  # 下一首 大拇指向右
        action = chrome.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]')
        action.click()
