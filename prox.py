from selenium.webdriver.common.proxy import Proxy, ProxyType
from fake_useragent import UserAgent
from selenium import webdriver

def get_proxies():
    print('----GETTING PROXIES----')
    options = webdriver.ChromeOptions()
    options.add_argument("log-level=3")
    options.add_argument("--headless")
    driver = webdriver.Chrome('chromedriver.exe',options=options)
    driver.get("https://free-proxy-list.net/")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0]+":"+result[1])

    driver.close()
    if len(PROXIES)>0:
        print(f'{len(PROXIES)} proxies found')
    else:
        print('No proxies found')        
        
    return PROXIES

def proxy_driver(PROXIES):
    print('\n----CONNECTING TO PROXY----')
    options = webdriver.ChromeOptions()
    prox = Proxy()

    if len(PROXIES) < 1:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()
        
    pxy = PROXIES[-1]
    print(f'Current Proxy ({pxy})')

    prox.proxy_type = ProxyType.MANUAL
    prox.autodetect = False
    prox.http_proxy = pxy
    prox.socks_proxy = pxy
    prox.ssl_proxy = pxy
    options.Proxy = prox
    
    print('\n----GETTING USER AGENTS----')
    ua = UserAgent()
    userAgent = ua.random
    print(f'Current UserAgent\n{userAgent}')
    
    options.add_argument("--start-maximized")
    options.add_argument("--proxy-server=%s" % pxy)
    options.add_argument("user-agent={userAgent}")
    options.add_argument("ignore-certificate-errors")
    options.add_argument("--disable-bundled-ppapi-flash")   # Disable internal Flash player
    options.add_argument("--disable-plugins-discovery")     # Disable external Flash player (by not allowing it to load)
    options.add_extension('mpbjkejclgfgadiemmefgebjfooflfhl.crx')    
    driver = webdriver.Chrome('chromedriver.exe',options=options)
    return driver
