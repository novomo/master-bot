#!/usr/bin/python3

import os
import apt
import sys
import logging
import imp
from subprocess import Popen, PIPE
import getpass
from datetime import datetime
from time import sleep
from random import uniform
import random
from typing import List, Dict
from stem import Signal
from stem.control import Controller as Tor
import numpy as np


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
Display = None
XlibDisplay = None
LEFT = None
MIDDLE = None
RIGHT = None
X = None
fake_input = None
XlibXK = None


d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Bot():
    def __init__(self, requestBot: bool=False, seleniumBot: bool=False, visualBot: bool=False, 
        headless: bool=False, imagePath: str=f"{d}/images", virtualDisplay: bool=False, showVirtualDisplay: int=1, implicitWait: int=15, proxy: str="", torPass: str=""):
        global requests, BeautifulSoup, webdriver, Keys, Options, By, EC, WebDriverWait, Image, \
            cv2, pyautogui, wavfile, Controller, audio, XlibDisplay, Display, MIDDLE, LEFT, RIGHT, \
            X, fake_input, XlibXK
        if showVirtualDisplay > 1:
            print("showVirtualDisplay can only be 0 or 1")
            sys.exit(1)

        self.imagePath = imagePath
        self.visualBot = visualBot
        self.seleniumBot = seleniumBot
        self.requestBot = requestBot
        self.virtualDisplay = virtualDisplay
        self.browserProcesses = []
        self.showVirtualDisplay = showVirtualDisplay
        self.proxy = proxy
        self.headless = headless
        self.torPass=torPass
        if requestBot:
            import requests
            from bs4 import BeautifulSoup
            self.requestBot = True
            self.tempData = None
            self.headers = {}
            self.session = requests.Session()
            if proxy != "":
                self.session.proxies = {'http':  proxy,
                                        'https': proxy}
                
        if visualBot:
            from scipy.io import wavfile
            from pynput.keyboard import Controller
            self.keyboard = Controller()
            import pyautogui
            self.hotKey = pyautogui.hotkey
            


        if virtualDisplay:
            from pyvirtualdisplay import Display
            self.vDisplay = Display(visible=showVirtualDisplay, size=(1600,900))
            self.vDisplay.start()
        

        if virtualDisplay and visualBot:
            import Xlib.display as XlibDisplay
            from pyautogui import LEFT, MIDDLE, RIGHT
            from Xlib import X
            from Xlib.ext.xtest import fake_input
            import Xlib.XK as XlibXK
            pyautogui._pyautogui_x11._display = XlibDisplay.Display(
                            os.environ['DISPLAY']
                        )
            sleep(2)



            

        if seleniumBot:
            from selenium import webdriver
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            self.seleniumBot = True
            self.By = By
            self.implicitWait = implicitWait

            self.loadChromedriver()
     
        
            
        if visualBot:
            self.visualBot = True
            from PIL import Image
            import webbrowser
            import cv2
            

    def __enter__(self):
        return self

    def __exit__(self):
        if self.visualBot:
            os.system('killall chromedriver')
            os.system("killall google-chrome-stable")
            os.system("killall chromium-browser")
            os.system('killall chrome')
            os.system('killall google-chrome')
        if self.seleniumBot:
            self.driver.quit()
        if self.virtualDisplay:
            self.vDisplay.stop()
            os.system('killall Xvfb')

    def quit(self):
        if self.visualBot:
            os.system('killall chromedriver')
            os.system("killall google-chrome-stable")
            os.system("killall chromium-browser")
            os.system('killall chrome')
            os.system('killall google-chrome')
        if self.seleniumBot:
            self.driver.quit()
        if self.virtualDisplay:
            self.vDisplay.stop()
            os.system('killall Xvfb')

    '''
    Searchs for an image on the screen

    input :

    image : path to the image file (see opencv imread for supported types)
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    im : a PIL image, usefull if you intend to search the same unchanging region for several elements

    returns :
    the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not

    '''

    def imagesearch(image: str, precision: float = 0.8):
        im = pyautogui.screenshot()
        # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        return [-1, -1] if max_val < precision else max_loc
    '''

    Calls request from stored session

    input : 

    url : URL to send request to
    data : JSON data to be sent with request
    headers : If request headers need to be different from stored headers

    output:

    response object

    '''
    
    def loadChromedriver(self):
        options = webdriver.ChromeOptions()
        # chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_argument("--no-sandbox")
        # chromeOptions.add_argument("--disable-setuid-sandbox")

        options.add_argument("--remote-debugging-port=9222") 

        options.add_argument("--disable-dev-shm-using")
        # chromeOptions.add_argument("--disable-extensions")
        # chromeOptions.add_argument("--disable-gpu")
        # chromeOptions.add_argument("start-maximized")
        # chromeOptions.add_argument("disable-infobars")

        options.add_argument("user-data-dir=/home/{}/.config/google-chrome/default".format(getpass.getuser()))
        if self.headless:
            options.add_argument('--headless')
        if self.proxy != "":
            options.add_argument('--proxy-server=%s' % self.proxy)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(self.implicitWait)
        

    def request(self, url: str, data: Dict = {}, headers: Dict = {}, 
            post: bool = False, verify: bool = True):
        if headers == {}:
            headers = self.headers
        if post:
            return self.session.post(url, json=data, headers=headers, verify=verify) if data != {} else self.session.post(url, headers=headers, verify=verify)
        else:
            return self.session.get(url, json=data, headers=headers, verify=verify) if data != {} else self.session.get(url, headers=headers, verify=verify)
                
    '''

    Obtains requested bs4 soup elements from html

    input : 

    tag : html element tag
    CSSSelector : Dict containing filters {'class': 'needed-class'}

    output:

    array soup elements

    '''   

    def soupSelectEle(self, tag: str, CSSSelector: Dict = {}):
        return self.soup.find_all(tag) if CSSSelector == {} else self.soup.find_all(tag, CSSSelector)

    '''

    Turns HTML in BeautifulSoup object

    input : 

    html : html string

    output:

    Beautiful Soup

    ''' 

    def makeSoup(self, html: str):
        self.soup = BeautifulSoup(html, "lxml")

    '''

    Recieves the array of objects contains determined html elements with only needed attributes

    input : 

    elements : List of html elements
    attributes : List of needed elements

    output:

    List of Dicts containing all the elemnts attributes that was asked for

    ''' 

    def soupScrapeData(self, elements: List, attributes: List[str]):
        self.tempData = [dict( [ (ele[attri],self.soupGetData(element, attri)) for attri in attributes ] ) for element in elements]

    '''

    Gets data from single HTML element

    input : 

    element : html element tag
    attribute : html attribute

    output:

    requested attribute value

    ''' 

    def soupGetData(self, element, attribute: str):
        return element.text if attribute == "text" else element[attribute]
            
    '''

    Waits for selenium element to be the required state

    input : 

    criteia : type of state "present", "visible", "clickable"
    selector : selection string
    by : selenium elemnt slector."e.g. By.ID"
    waitTime : amount of seconds to wait
    output:

    slenium element

    ''' 

    def headlessWaitForElement(self, criteia: str, selector: str, by, waitTime: int = 20):
        if criteia == "present":
            return WebDriverWait(self.driver, waitTime).until(
                EC.presence_of_element_located((by, selector)))
        elif criteia == "visible":
            return WebDriverWait(self.driver, waitTime).until(
                EC.visibility_of_element_located((by, selector)))
        elif criteia == "clickable":
            return WebDriverWait(self.driver, waitTime).until(
                EC.element_to_be_clickable((by, selector)))

    '''

    Waits for selenium elements to be the required state

    input : 

    criteia : type of state "present", "visible", "clickable"
    selector : selection string
    by : selenium elemnt slector."e.g. By.ID"
    waitTime : amount of seconds to wait
    output:

    list of slenium elements
    ''' 

    def headlessWaitForElements(self, criteia: str, selector: str, by, waitTime: int=20):
        if criteia == "present":
            return WebDriverWait(self.driver, waitTime).until(
                EC.presence_of_all_elements_located((by, selector)))
        elif criteia == "visible":
            return WebDriverWait(self.driver, waitTime).until(
                EC.visibility_of_all_elements_located((by, selector)))

    '''

    switches to iframe in selenium

    input : 

    selector : selection string
    by : selenium elemnt slector."e.g. By.

    output:


    ''' 

    def headlessSwitchToIFrame(self, by, selector: str, waitTime: int=20):
        WebDriverWait(self.driver, waitTime).until(EC.frame_to_be_available_and_switch_to_it((by, selector)))

    '''

    waits for a random amount of time to help prevent anti-bot detedction

    input : 

    a : start integer
    b : end integer

    output:

    array soup elements

    ''' 

    def waitBetween(self, a: int, b: int):
        rand = uniform(a, b)
        sleep(rand)

    '''

    gets the size of a image

    input : 

    imgFile : path to file

    output:

    tuple of width and height

    ''' 

    def loadImageSize(self, imgFile: str):
        image_file = imgFile
        img = Image.open(image_file)
        # get the image's width and height in pixels
        return img.size

    '''

    Types char of string like a person

    input : 

    s : string to be typed

    output:

    ''' 

    def typeText(self, s: str):
        for char in s:
            self.keyboard.press(char)
            self.keyboard.release(char)
            sleep(0.12)

    '''

    grabs a region (topx, topy, bottomx, bottomy)
    to the tuple (topx, topy, width, height)

    input : a tuple containing the 4 coordinates of the region to capture

    output : a PIL image of the area selected.

    '''
    def region_grabber(self, region: tuple):
        x1 = region[0]
        y1 = region[1]
        width = region[2]-x1
        height = region[3]-y1

        return pyautogui.screenshot(region=(x1,y1,width,height))

    '''

    Searchs for an image within an area

    input :

    image : path to the image file (see opencv imread for supported types)
    x1 : top left x value
    y1 : top left y value
    x2 : bottom right x value
    y2 : bottom right y value
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
    im : a PIL image, usefull if you intend to search the same unchanging region for several elements

    returns :
    the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not

    '''
    def imagesearcharea(self, image: str, x1: int,y1: int,x2: int,y2: int, precision: float=0.8, im=None) :
        if im is None :
            im = self.region_grabber(region=(x1, y1, x2, y2))
            #im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"

        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return [-1, -1]
        return max_loc

    def startBrowserVisible(self, browser: str, extensions: str="", openWebsite: str="https://www.google.com"):
        if len(extensions) != "":
            os.system(f"{browser} '{openWebsite}' --no-sandbox --load-extension='{extensions}'")
        else: 
            os.system(f"{browser} '{openWebsite}' --no-sandbox")

    def startBrowserNotVisible(self, browser: str, extensions: str="", openWebsite: str="https://www.google.com"):
        if len(extensions) != "":
            os.system(f"xvfb-run -a {browser} '{openWebsite}' --no-sandbox --load-extension='{extensions}'")
        else: 
            os.system(f"xvfb-run -a {browser} '{openWebsite}' --no-sandbox")


    def startBrowser(self, extensions: str="", openWebsite: str="https://www.google.com"):
        cache = apt.Cache()
        cache.open()
        if cache["chromium-browser"].is_installed:
            if self.virtualDisplay and not self.showVirtualDisplay:
                self.startBrowserNotVisible('chromium-browser', extensions=extensions, openWebsite=openWebsite)
            elif self.virtualDisplay and self.showVirtualDisplay:
                self.startBrowserVisible('chromium-browser', extensions=extensions, openWebsite=openWebsite)
            elif not self.virtualDisplay:
                self.startBrowserVisible('chromium-browser', extensions=extensions, openWebsite=openWebsite)
        elif cache["google-chrome-stable"].is_installed:
            if self.virtualDisplay and not self.showVirtualDisplay:
                self.startBrowserNotVisible('google-chrome', extensions=extensions, openWebsite=openWebsite)
            elif self.virtualDisplay and self.showVirtualDisplay:
                self.startBrowserVisible('google-chrome', extensions=extensions, openWebsite=openWebsite)
            elif not self.virtualDisplay:
                self.startBrowserVisible('google-chrome', extensions=extensions, openWebsite=openWebsite)
        else:
            print("Please install either chrome or chromium on your computer.")
            sys.exit(1)


    def stopBrowsers(self, browsers : List[str] = []):
        for browser in browsers:
            print(f"kill -9 {browser}")
            os.system(f"kill -9 {browser}")
        if self.virtualDisplay:
            os.system('killall Xvfb')



    '''

    waits for image to by available for set amount of time


    input :

    filename : path to the image file (see opencv imread for supported types)
    wait : top left x value
    

    returns :
    
    True if image found and False if image not found with time frame

    '''
    def waitForImage(self, filename: str, wait: int=5):
        startTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        while True:
            try:
                pos = self.imagesearch(self.imagePath + '/' + filename + '.png')
            except AttributeError:
                print("No file named " + filename + ".png in " + self.imagePath)
            if pos[0] != -1:
                return True
            else:
                currentTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                tdelta = datetime.strptime(currentTime, "%d/%m/%Y %H:%M:%S") - datetime.strptime(startTime,
                                                                                                 "%d/%m/%Y %H:%M:%S")
                if tdelta.seconds > wait:
                    print("Image not found")
                    return False

    '''

    click on the center of an image with a bit of random.
    eg, if an image is 100*100 with an offset of 5 it may click at 52,50 the first time and then 55,53 etc
    Usefull to avoid anti-bot monitoring while staying precise.

    this function doesn't search for the image, it's only ment for easy clicking on the images.

    input :

    image : path to the image file (see opencv imread for supported types)
    pos : array containing the position of the top left corner of the image [x,y]
    action : button of the mouse to activate : "left" "right" "middle", see pyautogui.click documentation for more info
    time : time taken for the mouse to move from where it was to the new position
    '''

    def click_image(self, image: str, pos: List[int], action: str, timestamp: int,offset: int=5):
        img = cv2.imread(image)
        height, width, channels = img.shape
        pyautogui.moveTo(pos[0] + (width / 2 + offset), pos[1] + (height / 2 + offset),
                         timestamp)
        pyautogui.click(button=action)


    


    '''
    Searchs for an image on screen continuously until it's found.

    input :
    image : path to the image file (see opencv imread for supported types)
    time : Waiting time after failing to find the image 
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

    returns :
    the top left corner coordinates of the element if found as an array [x,y] 

    '''
    def imagesearch_loop(self, image: str, timesample: int, precision: float=0.8):
        pos = self.imagesearch(image, precision)
        while pos[0] == -1:
            print(image+" not found, waiting")
            sleep(timesample)
            pos = self.imagesearch(image, precision)
        return pos

    '''
    Searchs for an image on screen continuously until it's found or max number of samples reached.

    input :
    image : path to the image file (see opencv imread for supported types)
    time : Waiting time after failing to find the image
    maxSamples: maximum number of samples before function times out.
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

    returns :
    the top left corner coordinates of the element if found as an array [x,y] 

    '''
    def imagesearch_numLoop(self, image: str, timesample: int, maxSamples: int, precision: int=0.8):
        pos = self.imagesearch(image, precision)
        count = 0
        while pos[0] == -1:
            print(image+" not found, waiting")
            sleep(timesample)
            pos = self.imagesearch(image, precision)
            count = count + 1
            if count>maxSamples:
                break
        return pos

    '''
    Searchs for an image on a region of the screen continuously until it's found.

    input :
    image : path to the image file (see opencv imread for supported types)
    time : Waiting time after failing to find the image 
    x1 : top left x value
    y1 : top left y value
    x2 : bottom right x value
    y2 : bottom right y value
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

    returns :
    the top left corner coordinates of the element as an array [x,y] 

    '''
    def imagesearch_region_loop(self, image: str, timesample: int, x1: int, 
                y1: int, x2: int, y2: int, precision: float=0.8):
        pos = self.imagesearcharea(image, x1,y1,x2,y2, precision)

        while pos[0] == -1:
            sleep(timesample)
            pos = self.imagesearcharea(image, x1, y1, x2, y2, precision)
        return pos

    '''
    Searches for an image on the screen and counts the number of occurrences.

    input :
    image : path to the target image file (see opencv imread for supported types)
    precision : the higher, the lesser tolerant and fewer false positives are found default is 0.9

    returns :
    the number of times a given image appears on the screen.
    optionally an output image with all the occurances boxed with a red outline.

    '''
    def imagesearch_count(self, image: str, precision: float=0.9):
        img_rgb = pyautogui.screenshot()
        img_rgb = np.array(img_rgb)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        count = 0
        for pt in zip(*loc[::-1]):  # Swap columns and rows
            #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2) // Uncomment to draw boxes around found occurances
            count = count + 1
        #cv2.imwrite('result.png', img_rgb) // Uncomment to write output image with boxes drawn around occurances
        return count


    def r(self, num: int, rand: int):
        return num + rand*random.random()

    '''

    Creates a new tab in browser if using cv2 bot

    input : 

    address : url to navigate to

    output:


    ''' 

    def visualNewTab(self, address: str):
        pyautogui.hotkey("ctrl", "t")
        sleep(0.5)
        pyautogui.hotkey("ctrl", "l")
        self.typeText(address)
        pyautogui.press('enter')

    
    def changeIP(self):
        if self.seleniumBot:
            self.driver.quit()
            
        with Tor.from_port(port = 9051) as controller:
            controller.authenticate(password=self.torPass)
            controller.signal(Signal.NEWNYM)
            
        if self.seleniumBot:
            self.loadChromedriver()
        
        if self.proxy and self.requestBot:
            self.session = None
            self.session = requests.Session()
            if self.proxy != "":
                self.session.proxies = {'http':  self.proxy,
                                        'https': self.proxy}
