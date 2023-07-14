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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service

enabled = True


def center_window(root, width, height):  # 視窗置中
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = "%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2,)
    root.geometry(size)


def onOK():
    website_type = radioValue.get()  # 取得網站類型
    video_name = entry.get()  # 取得輸入文字

    global enabled
    if enabled == False:
        tkinter.messagebox.showinfo(title="Warning", message="影片或音樂播放中")
        return

    if video_name == "" or video_name == "請輸入影片或音樂名稱":
        tkinter.messagebox.showinfo(title="Warning", message="請輸入影片或音樂名稱")
        return

    enabled = False

    options = Options()
    options.add_argument("--disable-notifications") # 關閉通知視窗
    #chrome = webdriver.Chrome("./chromedriver", chrome_options=options)  # 使用 Chrome 的 WebDriver
    service = Service()    
    chrome = webdriver.Chrome(service=service, options=options)

    if website_type == 1:  # Youtube video
        
        action = webdriver.ActionChains(chrome)
        chrome.get("https://www.youtube.com")
        # chrome.maximize_window()
        
        # 傳入搜尋字串
        search = chrome.find_element(By.XPATH, "//input[@id='search']")
        search.send_keys(video_name)

        # 點擊搜尋
        time.sleep(1)
        action.key_down(Keys.ENTER)
        action.key_up(Keys.ENTER)
        action.perform()

        # 點選第一個影片
        time.sleep(1)
        video_to_play = chrome.find_element(By.XPATH,'//*[@id="video-title"]/yt-formatted-string')
        video_to_play.click()

        # 劇院模式
        time.sleep(0.5)
        action.key_down("t")
        action.key_up("t")
        action.perform()

        # 跳過廣告
        for _ in range(2):
            try:
                time.sleep(6)
                #skip_ad = chrome.find_element_by_xpath('//*[@id="skip-button:5"]/span')
                #skip_ad.click()
                chrome.find_element(By.XPATH, '//*[@id="skip-button:5"]/span').click()

            except:
                continue
        
        gesture_type = ""
        gesture_totaltype = ["播放", "暫停", "音量降低", "音量提升", "快進", "倒退"]
        count = 0
        threahold = 10
        play = True

        while 1:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 與手勢辨識程式取得連線
            host = socket.gethostname()
            port = 9999
            client.connect((host, port))
            
            msg = client.recv(1024)
            receive_msg = str(msg.decode("utf-8"))

            client.send(("ACK").encode('utf-8'))
            client.close()

            try: 
                chrome.find_element(By.XPATH, '//*[@id="container"]/h1/yt-formatted-string')
            except:
                break
                
            print("收到", receive_msg)
            if receive_msg == "Nothing":
                continue

            if gesture_type != receive_msg:  # 確保辨識成功五次才做對應的控制動作
                gesture_type = receive_msg
                count = 0
            elif gesture_type == receive_msg and count < threahold:
                count += 1
            elif count == threahold:
                print("現在狀態：", gesture_type)
                print("收到指令: ", gesture_totaltype[int(gesture_type)])
                if gesture_type == "0":
                  # 開始撥放 OK
                    if not play:
                        action.key_down("k")
                        action.key_up("k")
                        action.perform()
                        play = not play
                if gesture_type == "1":  # 暫停撥放 5
                    if play:
                        action.key_down("k")
                        action.key_up("k")
                        action.perform()
                        play = not play
                if gesture_type == "2":  # 音量下降 YA向下
                    action.key_down(Keys.DOWN)
                    action.key_up(Keys.DOWN)
                    action.perform()
                if gesture_type == "3":  # 音量增加 YA向上
                    action.key_down(Keys.UP)
                    action.key_up(Keys.UP)
                    action.perform()
                if gesture_type == "4":  # 倒退 大拇指向左
                    action.key_down("j")
                    action.key_up("j")
                    action.perform()
                if gesture_type == "5":  # 快進 大拇指向右
                    action.key_down("l")
                    action.key_up("l")
                    action.perform()

                count = 0
                
    if website_type == 2: # Spotify
        action = webdriver.ActionChains(chrome)

        chrome.get("https://www.spotify.com/tw/")
        chrome.maximize_window()

        login_button = chrome.find_element(By.XPATH, '//*[@id="__next"]/div[1]/header/div/nav/ul/li[6]/a') 
        login_button.click()

        time.sleep(1)
        account = chrome.find_element(By.XPATH, '//*[@id="login-username"]') 
        account.send_keys("jiayihsu0518@gmail.com") # 輸入帳號
        password = chrome.find_element(By.XPATH, '//*[@id="login-password"]') 
        password.send_keys("davcas378") # 輸入密碼
        login_button = chrome.find_element(By.XPATH, '//*[@id="login-button"]')
        login_button.click()

        time.sleep(4)
        search_button = chrome.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/nav/div[1]/ul/li[2]/a')
        search_button.click()

        time.sleep(2)
        search = chrome.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/form/input')
        search.send_keys(video_name)

        time.sleep(2)
        target_song= chrome.find_element(By.XPATH, '//*[@id="searchPage"]/div/div/section[2]/div[2]/div/div/div/div[2]/div[1]/div')
        target_song.click()
        target_song = chrome.find_element(By.XPATH, '//*[@id="searchPage"]/div/div/section[2]/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/button')
        target_song.click()

        Key_action = webdriver.ActionChains(chrome)
        action = chrome.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[3]/div/div[3]/div/div')
        action.click()

        gesture_type = ""
        gesture_totaltype = ["播放", "暫停", "音量降低", "音量提升", "下一首", "上一首"]
        count = 0
        threahold = 10
        play = True

        while(1):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 與手勢辨識程式取得連線
            host = socket.gethostname()
            port = 9999
            client.connect((host, port))
            
            msg = client.recv(1024)
            receive_msg = str(msg.decode("utf-8"))

            client.send(("ACK").encode('utf-8'))
            client.close()

            try: 
                test_element = chrome.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button')
            except:
                print("網頁關閉")
                break
                
            print("收到", receive_msg)
            if receive_msg == "Nothing":
                continue

            if gesture_type != receive_msg:  # 確保辨識成功五次才做對應的控制動作
                gesture_type = receive_msg
                count = 0
            elif gesture_type == receive_msg and count < threahold:
                count += 1
            elif count == threahold:
                if gesture_type == "0":  # 開始撥放 OK
                    if not play:
                        action = chrome.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button')
                        action.click()
                        play = not play
                if gesture_type == "1":  # 暫停撥放 5
                    if play:
                        action = chrome.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button')
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
                    action = chrome.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[1]/button[2]')
                    action.click()
                if gesture_type == "5":  # 下一首 大拇指向右
                    action = chrome.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]')
                    action.click()

                count = 0
    enabled = True

def onExit():
    root.destroy() # 關閉視窗

root = tk.Tk()
root.title("影片控制小幫手")
center_window(root, 400, 300)

# 標題文字
label = tk.Label(root, text="請選擇網站~~~~", font=10)
label.place(x=130, y=30)

# 單選按鍵
radioValue = tk.IntVar()
radioValue.set(1)
rdioOne = tk.Radiobutton(root, text="Youtube", variable=radioValue, value=1, font=10)
rdioTwo = tk.Radiobutton(root, text="Spotify", variable=radioValue, value=2, font=10)
rdioOne.place(x=100, y=80)
rdioTwo.place(x=100, y=130)

# 輸入欄位
entry = tk.Entry(root, width=20, font=10)
entry.insert(0, "請輸入影片名稱")
entry.configure(state=tk.DISABLED)


def on_click(event):
    entry.configure(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.unbind("<Button-1>", on_click_id)


on_click_id = entry.bind("<Button-1>", on_click)
entry.place(x=100, y=190)

# 按鈕
button1 = tk.Button(root, text="查詢", font=10, command=onOK)
button1.place(x=130, y=240)
button2 = tk.Button(root, text="關閉", font=10, command=onExit)
button2.place(x=210, y=240)

root.mainloop() # 重複執行，直到關閉視窗

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 與手勢辨識程式取得連線
host = socket.gethostname()
port = 9999
client.connect((host, port))

msg = client.recv(1024)
receive_msg = str(msg.decode("utf-8"))
client.send(("EXIT").encode('utf-8')) # 傳送關閉訊息
client.close()

print("播放器程式結束")
exit()
