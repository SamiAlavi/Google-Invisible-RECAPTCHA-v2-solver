#! /usr/bin/env python

from time import sleep     # Used for to give time for a page to load from selenium import webdriver
from requests import get
from prox import get_proxies, proxy_driver
from audiorecog import recog

def getspinnertext(driver):    
    url = 'https://smodin.me/it/riorganizza-automaticamente-il-testo-in-italiano-gratuitamente'
    url = 'https://smodin.me/free-english-rewriter-and-spinner'
    driver.get(url)

    flag1 = True
    flag2 = True
    textsample=['a','b','c']

    text = driver.find_element_by_css_selector('textarea.jss167')
    text.send_keys(textsample[0])

    go = driver.find_element_by_css_selector('button.MuiButton-containedPrimary')
    driver.execute_script("window.scrollTo(0, 100)")
    sleep(2)
    go.click()
    
    sleep(1)
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
        except:
            break
        if error.text.startswith('Multiple'):
            continue
        else:
            flag1 = False
    print('Passed')
    driver.switch_to.default_content()

    inn = input('Enter y to continue:' ).lower()
    if inn=='y':
        for i in range(1,50):
            text.clear()
            text.send_keys(textsample[i%3])
            print(i)


ALL_PROXIES = get_proxies()
driver = proxy_driver(ALL_PROXIES)
getspinnertext(driver)
