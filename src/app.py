#!/usr/bin/python3

import os, apt, sys, logging, imp, getpass
from datetime import datetime
from time import sleep
from random import uniform
from typing import List, Dict


def dynamic_importer(name, path):
    """
    Dynamically imports modules / classes
    """
    try:

        fp, pathname, description = imp.find_module(name, [path, ])
    except ImportError:
        print("unable to locate module: " + name)
        return (None, None)

    package = imp.load_module(name, fp, pathname, description)

    return package


requests = None
BeautifulSoup = None
webdriver = None
Keys = None
Options = None
By = None
EC = None
WebDriverWait = None
Image = None
pyautogui = None
wavfile = None
Controller = None
audio = None
cv2 = None


class Bot():
    def __init__(self, requestBot=False, seleniumBot=False, visualBot=False, headless=False, displayDevice=False,
                 imagePath="/images", extensions=None, openWebsite="https://www.google.com", virualDisplay=False):
        global requests, BeautifulSoup, webdriver, Keys, Options, By, EC, WebDriverWait, Image, cv2, pyautogui, wavfile, Controller, audio
        self.requestBot = False
        self.seleniumBot = False
        self.visualBot = False
        d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if imagePath == "/images":
            self.imagePath = d + imagePath
        else:
            self.imagePath = imagePath
        if requestBot:
            self.requestBot = True
            import requests
            from bs4 import BeautifulSoup
            self.tempData = None
            self.headers = {}
            self.session = requests.Session()
        if seleniumBot:
            self.seleniumBot = True
            try:
                from selenium import webdriver
                from selenium.webdriver.common.keys import Keys
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.support.ui import WebDriverWait
            except ImportError:
                os.system('.' + os.path.dirname(os.path.abspath(__file__)))
                from selenium import webdriver
                from selenium.webdriver.common.keys import Keys
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.support.ui import WebDriverWait

            options = webdriver.ChromeOptions()
            # chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            options.add_argument("--no-sandbox")
            # chromeOptions.add_argument("--disable-setuid-sandbox")

            options.add_argument("--remote-debugging-port=9222")  # this

            options.add_argument("--disable-dev-shm-using")
            # chromeOptions.add_argument("--disable-extensions")
            # chromeOptions.add_argument("--disable-gpu")
            # chromeOptions.add_argument("start-maximized")
            # chromeOptions.add_argument("disable-infobars")

            options.add_argument("user-data-dir=/home/{}/.config/google-chrome/default".format(getpass.getuser()))
            if headless:
                options.add_argument('--headless')

            self.driver = webdriver.Chrome(chrome_options=options)
            self.driver.implicitly_wait(15)

        if displayDevice:
            import pyautogui
            from scipy.io import wavfile
            from pynput.keyboard import Controller
            # audio = dynamic_importer("audio", importFolder+"/uncaptcha")
            self.keyboard = Controller()
            self.hotKey = pyautogui.hotkey

        if visualBot:
            self.visualBot = True
            from PIL import Image
            import webbrowser

            import cv2
            cache = apt.Cache()
            cache.open()
            if cache["chromium-browser"].is_installed:
                if extensions is not None:
                    os.system(f"chromium-browser --load-extension='{extensions}'")
                else:
                    webbrowser.get('chromium-browser').open_new(openWebsite)
                '''
                while True:
                    sleep(2)
                    try:
                        pos = imageSearch.imagesearch(self.imagePath + '/chromiumLogo.png')
                    except AttributeError:
                        print("Please add a an image of the chromium logo in " + self.imagePath + '/chromiumLogo.png')
                        sys.exit(1)
                    if pos[0] != -1:
                        break
                    else:
                        print("Please pin chromium to your task bar")
                        sys.exit(1)
                height, width = self.loadImageSize(self.imagePath + '/chromiumLogo.png')
                pyautogui.moveTo(pos[0] + width/2, pos[1] + height/2)
                pyautogui.click()
                
                if self.waitForImage('googleLoaded', wait=5):
                    print('Chrome Loaded ...')
                else:
                    print('Chrome not Loaded')
                    sys.exit(1)
                '''
            elif cache["google-chrome-stable"].is_installed:
                if extensions is not None:
                    print(extensions)
                    os.system(f"google-chrome '{openWebsite}' --load-extension={extensions}")
                else:
                    webbrowser.get('google-chrome').open_new(openWebsite)
                '''
                while True:
                    sleep(2)
                    try:
                        pos = imageSearch.imagesearch(self.imagePath + '/chromeLogo.png')
                    except AttributeError:
                        print("Please add a an image of the chrome logo in " + self.imagePath + '/chromeLogo.png')
                        sys.exit(1)
                    if pos[0] != -1:
                        break
                    else:
                        print("Please pin chrome to your task bar")
                        sys.exit(1)
                height, width = self.loadImageSize(self.imagePath + '/chromeLogo.png')
                pyautogui.moveTo(pos[0] + width/2, pos[1] + height/2)
                pyautogui.click()
                if self.waitForImage('googleLoaded', wait=5):
                    print('Chrome Loaded ...')
                else:
                    print('Chrome not Loaded')
                    sys.exit(1)
                '''
            else:
                print("Please install either chrome or chromium on your computer,")

    def __enter__(self):
        return self

    def __exit__(self):
        if self.visualBot:
            os.system("killall google-chrome-stable")
            os.system("killall chromium-browser")
        if self.seleniumBot:
            self.driver.quit()

    def quit(self):
        if self.visualBot:
            os.system("killall google-chrome-stable")
            os.system("killall chromium-browser")
        if self.seleniumBot:
            self.driver.quit()

    def imagesearch(image, precision=0.8):
        im = pyautogui.screenshot()
        # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return [-1, -1]
        return max_loc

    def request(self, url, data: Dict = {}, headers=None, post: bool = False, verify: bool = True):
        if headers is None:
            headers = self.headers
        if post:
            if data != {}:
                return self.session.post(url, json=data, headers=headers, verify=verify)
            else:
                return self.session.post(url, headers=headers, verify=verify)
        else:
            if data != {}:
                return self.session.get(url, json=data, headers=headers, verify=verify)
            else:
                return self.session.get(url, headers=headers, verify=verify)

    def soupSelectEle(self, tag: str, CSSSelector: Dict = {}):
        if CSSSelector == {}:
            return self.soup.find_all(tag)
        else:
            return self.soup.find_all(tag, CSSSelector)

    def makeSoup(self, html: str):
        self.soup = BeautifulSoup(html, "lxml")

    def soupScrapeData(self, elements: List, attributes: List):
        self.tempData = []
        for element in elements:
            ele = {}
            for attri in attributes:
                ele[attri] = self.soupGetData(element, attri)
            self.tempData.append(ele)

    def soupGetData(self, element, attribute):
        if attribute == "text":
            return element.text
        else:
            return element[attribute]

    def headlessWaitForElement(self, criteia, cssSelector, waitTime=20):
        if criteia == "present":
            return WebDriverWait(self.driver, waitTime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector)))
        elif criteia == "visible":
            return WebDriverWait(self.driver, waitTime).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, cssSelector)))
        elif criteia == "clickable":
            return WebDriverWait(self.driver, waitTime).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector)))

    def headlessWaitForElements(self, criteia, cssSelector, waitTime=20):
        if criteia == "present":
            return WebDriverWait(self.driver, waitTime).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, cssSelector)))
        elif criteia == "visible":
            return WebDriverWait(self.driver, waitTime).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, cssSelector)))

    def waitBetween(self, a, b):
        rand = uniform(a, b)
        sleep(rand)

    def loadImageSize(self, imgFile):
        image_file = imgFile
        img = Image.open(image_file)
        # get the image's width and height in pixels
        return img.size

    def typeText(self, s):
        for char in s:
            self.keyboard.press(char)
            self.keyboard.release(char)
            sleep(0.12)

    def waitForImage(self, filename, wait=5):
        startTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        while True:
            try:
                pos = self.imagesearch(self.imagePath + '/' + filename + '.png')
            except AttributeError:
                print("No file named " + filename + ".png in " + self.imagePath)
            if pos[0] != -1:
                return True
                pyautogui.moveTo(pos[0], pos[1])
            else:
                currentTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                tdelta = datetime.strptime(currentTime, "%d/%m/%Y %H:%M:%S") - datetime.strptime(startTime,
                                                                                                 "%d/%m/%Y %H:%M:%S")
                if tdelta.seconds > wait:
                    print("Image not found")
                    return False

    def clickImage(self, filename, wait=5):
        if self.waitForImage(filename, wait=wait):
            pos = self.imagesearch(self.imagePath + '/' + filename + '.png')
            width, height = self.loadImageSize(self.imagePath + '/' + filename + '.png')
            pyautogui.moveTo(pos[0] + width / 2, pos[1] + height / 2)
            pyautogui.click()
        else:
            sys.exit("Could not file image " + filename)

    def visualNewTab(self, address):
        pyautogui.hotkey("ctrl", "t")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "l")
        self.typeText(address)
        pyautogui.press('enter')

    def checkBoxCaptcha(self):
        if self.waitForImage('checkCaptcha', wait=0.5):
            pos = self.imagesearch(self.imagePath + '/checkCaptchaBox.png')
            width, height = self.loadImageSize(self.imagePath + '/checkCaptchaBox.png')
            pyautogui.moveTo(pos[0] + width / 2, pos[1] + height / 2)
            pyautogui.click()
            return True
        else:
            return False

    def complexCaptcha(self, wait=2):
        count = 0
        comOne = self.waitForImage('solveComplex', wait=1)
        comTwo = self.waitForImage('solveComplex2', wait=1)
        while True:
            if comOne or comTwo:
                if comOne:
                    pos = self.imagesearch(self.imagePath + '/solveComplex.png')
                    width, height = self.loadImageSize(self.imagePath + '/solveComplex.png')
                    pyautogui.moveTo(pos[0] + width * 0.8, pos[1] + height / 2)
                    pyautogui.click()
                elif comTwo:
                    pos = self.imagesearch(self.imagePath + '/solveComplex2.png')
                    width, height = self.loadImageSize(self.imagePath + '/solveComplex2.png')
                    pyautogui.moveTo(pos[0] + width * 0.8, pos[1] + height / 2)
                    pyautogui.click()
                print("Complex captcha clicked")
                count = 0
                while True:
                    comOne = self.waitForImage('solveComplex', wait=0)
                    comTwo = self.waitForImage('solveComplex2', wait=0)
                    if self.waitForImage('captchaComplete', wait=4):
                        return True
                    elif comOne or comTwo:
                        print("need to retry")
                        pos = self.imagesearch(self.imagePath + '/solveComplex2.png')
                        width, height = self.loadImageSize(self.imagePath + '/solveComplex2.png')
                        pyautogui.moveTo(pos[0] + width * 0.8, pos[1] + height / 2)
                        pyautogui.click()
                        pyautogui.moveTo(5, 5)
                        break
                    else:
                        return False
            elif count == wait:
                return False
            else:
                print("Can't find complex captcha")
                count += 1

    def attackSetup(self, task_type):
        self.TASK_PATH, self.TASK_DIR, self.TASK_NUM, self.TASK
        self.TASK_DIR = os.path.join(task_type, "task")
        self.TASK_NUM = 1

        while os.path.isdir(self.TASK_DIR + str(self.TASK_NUM)):
            self.TASK_NUM += 1
        if not os.path.isdir(self.TASK_DIR + str(self.TASK_NUM)):
            os.mkdir(self.TASK_DIR + str(self.TASK_NUM))
            logging.info("Making " + self.TASK_DIR + str(self.TASK_NUM))
        self.TASK = "task" + str(self.TASK_NUM)
        self.TASK_PATH = os.path.join(task_type, self.TASK)

    '''  
    def get_numbers(self, audio_file, parent_dir):
        self.AMP_THRESHOLD
        mp3_file = audio_file + ".mp3"
        wav_file = audio_file + ".wav"
        print("converting from " + mp3_file + " to " + wav_file)
        os.system("echo 'y' | ffmpeg -i "+mp3_file+" "+wav_file + "&> /dev/null")
        # split audio file on silence
        os.system("sox -V3 "+wav_file+" "+audio_file+"_.wav silence -l 0 1 0.5 0.1% : newfile : restart &> /dev/null")
        files = [f for f in os.listdir(parent_dir) if "_0" in f]
        audio_filenames = []
        # remove audio files that are only silence
        for f in files:
            _, snd = wavfile.read(TASK_PATH + "/" + f)
            amp = max(snd)
            print(f + ":" + str(amp))
            if amp > self.AMP_THRESHOLD: # skip this file
                audio_filenames.append(parent_dir+f)
            else:
                os.system("rm " + parent_dir+f)
        # run speech recognition on the individual numbers
        # num_str = ""
        # for f in sorted(audio_filenames):
        #     print f
        #     num_str += str(audio.getNum(f))
        # print(num_str)
        return audio.getNums(TASK_PATH, audio_filenames)
                
    def MasterBotAudio(self):
        guess_again = True

        while guess_again:
            self.attackSetup("audio")
            guess_str = self.get_numbers(TASK_PATH + "/" + TASK, TASK_PATH + "/")
            self.clickImage("CaptchaSubmitBox", wait=5)
            self.typeText(guess_str)
            # results.append(guess_str)
            self.waitBetween(0.5, 3)
            self.clickImage("VerifyCaptcha", wait=5)
            self.waitBetween(1, 2.5)
            if not self.waitForImage("checkCaptcha", wait=5):
                guess_again = False

        print("Captcha complete")
        '''
