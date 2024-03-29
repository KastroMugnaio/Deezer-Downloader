import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import os, time, glob

filename = "songlist.txt"


def getublock():
    s = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=en')
    dir = os.getcwd()
    prefs = {'download.default_directory': dir}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(service=s, chrome_options=options)
    driver.get(
        "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=100.0.4896.127&acceptformat=crx2,crx3&x=id%3Dcjpalhdlnbpafiamejdnhcphjbkeiagm%26uc")
    time.sleep(10)
    driver.close()


def dl_click():
    dl_button = driver.find_element(By.XPATH, "//button[text()='Download']")
    driver.implicitly_wait(1.5)
    dl_button.click()


def quality_click():
    driver.implicitly_wait(1.5)
    if quality == "1":
        ActionChains(driver).move_to_element(driver.find_element(By.ID, "mp3-128")).click().perform()
    elif quality == "2":
        ActionChains(driver).move_to_element(driver.find_element(By.ID, "mp3-320")).click().perform()
    elif quality == "3":
        ActionChains(driver).move_to_element(driver.find_element(By.ID, "flac")).click().perform()


def download():
    c = 0
    with open(filename, encoding='utf-8') as fp:
        Lines = fp.readlines()
        for line in Lines:
            c += 1
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'input').clear()
            time.sleep(1)
            search_box = driver.find_element(By.CLASS_NAME, "input")
            search_button = driver.find_element(By.ID, "snd")
            query = line.strip()
            search_box.send_keys(query)
            time.sleep(1)
            search_button.click()
            time.sleep(2)
            dl_click()
            if c == 1:
                quality_click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
                dl_click()
                c += 1
                time.sleep(5)
            else:
                quality_click()
                dl_click()
                c += 1
                time.sleep(5)
            driver.execute_script("window.history.go(-1)")
            time.sleep(1)
            print(line.strip(), "downloaded")


def start_script():
    driver.get("https://free-mp3-download.net")
    vpn_check = driver.find_element(By.XPATH, ".//*[contains(text(), 'Search using our VPN')]")
    vpn_check.click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    download()
    time.sleep(60)


if __name__ == "__main__":
    print("!!! REMEMBER: YOU NEED TO CHECK CAPTCHA EVERY 15 MINUTES !!!")
    adb = ""
    for file in glob.glob("*.crx"):
        adb = file
    time.sleep(2)
    if adb.endswith('.crx'):
        quality = input("Insert 1 for MP3 (128k), 2 MP3 (320k) or 3 for FLAC: ")
        try:
            int(quality)
        except:
            print("You haven't inserted an integer number, please re-run the tool")
            sys.exit()
        options = webdriver.ChromeOptions()
        options.add_extension(adb)
        options.add_argument('--lang=en')
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, chrome_options=options)
        start_script()
    else:
        getublock()
