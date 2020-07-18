#! /usr/bin/env python

from time import sleep     # Used for to give time for a page to load from selenium import webdriver
from requests import get
from pandas_ods_reader import read_ods
from prox import get_proxies, proxy_driver
from audiorecog import recog

def writeConvFile(text):
    with open('convtext.txt','a') as f:
        f.write(text)

def writeProgress(count):    
    with open('start.txt','w') as f:
        f.write(count)

def captchasolver(driver):
    flag1 = True    
    iframe = driver.find_element_by_xpath("//iframe[@title='recaptcha challenge']") # captcha frame
    driver.switch_to.frame(iframe)
  
    sleep(1)
    btnsolve = driver.find_element_by_id('solver-button')
    btnverify = driver.find_element_by_id('recaptcha-verify-button')
    while flag1:
        btnsolve.click() # SOLVER btn
        sleep(6)
        dwnld = driver.find_element_by_css_selector('a.rc-audiochallenge-tdownload-link').get_attribute('href')
        aud = get(dwnld)
        with open('captcha.mp3', 'wb') as f:
            f.write(aud.content)
        txt = recog()
        print(txt)
        driver.find_element_by_id('audio-response').send_keys(txt)
        sleep(1)
        btnverify.click()
        try:
            error = driver.find_element_by_css_selector('div.rc-audiochallenge-error-message')
            if error.text.startswith('Multiple'):
                continue
            else:
                flag1 = False
        except:
            continue
        driver.switch_to.default_content()
    return True

def getspinnertext(driver,start,texts):    
    url = 'https://smodin.me/it/riorganizza-automaticamente-il-testo-in-italiano-gratuitamente'
    #url = 'https://smodin.me/free-english-rewriter-and-spinner'
    driver.get(url)

    text = driver.find_element_by_css_selector('textarea.jss167')
    go = driver.find_element_by_css_selector('button.MuiButton-containedPrimary')
    convtext = driver.find_element_by_css_selector('div.jss168')
    driver.execute_script("window.scrollTo(0, 100)")

    for i in range(start,len(texts)):    
        text.send_keys(texts[i][0]) # input text
        sleep(2)
        go.click()    # click on REWRITE
        sleep(1)

        if captchasolver(driver):
            writeConvFile(f'{i}) {convtext.text}')
            writeProgress(str(i))
            text.clear()
    

texts = read_ods('./60 text portions.ods', 1, headers=False).dropna().values
with open('start.txt','r') as f:
    start = int(f.read())
    
ALL_PROXIES = get_proxies()
driver = proxy_driver(ALL_PROXIES)
getspinnertext(driver,start,texts)
