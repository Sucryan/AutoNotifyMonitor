import selenium
import tkinter as tk
import time
import requests
import os.path
from os import path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json

# find the abs path of this file!
current_dir = os.path.dirname(os.path.abspath(__file__))

# load message!
Par_Path = os.path.join(current_dir, 'Par.txt')
with open(Par_Path, 'r', encoding = 'utf-8') as file:
    json_str = file.read()

user_data = json.loads(json_str)

ac = user_data['username']
pw = user_data['password']
tok = user_data['token']
req = user_data['searchItem']


# chromeDriver path
CD_Path = os.path.join(current_dir, 'chromedriver-mac-arm64', 'chromedriver')
# text path1
T_Path1 = os.path.join(current_dir, 'abc.txt')
# text path2
T_Path2 = os.path.join(current_dir, 'DEF.txt')

def crawl():
    service = Service(executable_path=CD_Path)
    timeout = 0
    try:        
        headers = {
                "Authorization": "Bearer " + tok,
                "Content-Type": "application/x-www-form-urlencoded"
            }
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless")
        
        # 禁用通知fu. 
        chrome_options.add_argument("--disable-notifications")
        
        # 禁用擴展
        chrome_options.add_argument("--disable-extensions")

        driver=webdriver.Chrome(service=service, options=chrome_options)
        
        # 防止跳出通知
        prefs = {
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # 使用ChromeDriverManager自動下載chromedriver
        '''
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=chrome_options)
        '''
        
        driver.get("https://www.facebook.com")

        #輸入帳號密碼

        elem = driver.find_element(By.NAME, 'email')
        elem.send_keys(ac)
        elem = driver.find_element(By.NAME, 'pass')
        elem.send_keys(pw)
        elem.submit()
        time.sleep(2)
        #進入二手拍
        driver.get("https://www.facebook.com/groups/817620721658179")

        # 防止跳出通知
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)

        time.sleep(2 + 10 * timeout)
        try: 
            cli = driver.find_element(By.CSS_SELECTOR,'[aria-label="搜尋"]')
            cli.click()
        except selenium.common.exceptions.NoSuchElementException:
            timeout += 1
            pass
        time.sleep(2 + 10 * timeout)
        try:
            s = driver.find_element(By.CSS_SELECTOR,'[aria-label="搜尋此社團"]')
            s.send_keys(req)
            s.send_keys(Keys.ENTER)
        except selenium.common.exceptions.NoSuchElementException:
            timeout += 1
            pass
        time.sleep(2 + 10 * timeout)
        
        try:  
            new = driver.find_element(By.CSS_SELECTOR,'[aria-label="最新"]')
            new.click()
        except selenium.common.exceptions.NoSuchElementException:
            timeout += 1
            pass
        
        
        time.sleep(5 + 10 * timeout)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        #Net = soup.find(class_= "x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        '''
        content_pivot = soup.select_one("div.x1l90r2v.x1pi30zi.x1swvt13.x1iorvi4 > div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a")
        content = content_pivot.get_text(strip=True)
        '''

        # 需要定期更改！(240903: 取每份貼文的前兩行)(反白右鍵內文，看html-div類型開頭的下一個class！)
        content1 = soup.find(class_="x1l90r2v x1pi30zi x1swvt13 x1iorvi4").find("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a")
        content2 = soup.find(class_="x1l90r2v x1pi30zi x1swvt13 x1iorvi4").find("div", class_="x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a")
        if content1 is not None and content2 is not None:
            content = content1.text + content2.text
        else:
            # Handle the case where either content1 or content2 is None
            content = (content1.text if content1 is not None else "") + (content2.text if content2 is not None else "")
        print(content)
        
        
        '''titles = soup.find_all('div', dir = 'auto')[0]
        lines = 1
        content = ""
        while(lines < 3):
            tmp = soup.find_all('div', dir = 'auto')[lines]
            txt = tmp.text
            content = content.join(txt)
            lines += 1'''
                
        #utf_content = content#.encode('utf8')

        # locally
        '''
        aContent = content
        tmp1 = aContent
        tmp2 = bContent
        if tmp1 != tmp2:
            post = "New Post!"
            params = {"message": post}
            bContent = tmp1
        else:
            post = "Nothing New.."
            params = {"message": ""}
        L_post = tk.Label(root, text = post)
        L_post.pack() 
        '''

        
        f = open(T_Path1, 'wt')
        f.write(str(content))
        f.close()

        f = open(T_Path1, 'r')
        str1 = "".join(f)
        f.close()

        F = open(T_Path2, 'r')
        str2 = "".join(F)
        F.close()

        post = ''
        if str1 != str2:
            post = 'New Post!! (' + req + ')'
            params = {"message":post}
            F = open(T_Path2, 'wt')
            F.write(str1)
            F.close
        else:
            post = 'Nothing New...'
            params = {"message":""}
        L_post = tk.Label(root, text = post)
        L_post.pack()
        
        #count = str(i)
        #L_count = tk.Label(root, text = count)
        #L_count.pack()
        #i += 1
        r = requests.post("https://notify-api.line.me/api/notify",
                            headers=headers, params=params)
    except selenium.common.exceptions.WebDriverException:
        L_net = tk.Label(root, text = 'No Internet')
        params = {"message":"No Internet"}
        L_net.pack()
    root.after(30000,crawl)     
root = tk.Tk()
root.geometry("250x170")
crawl()
root.mainloop()  