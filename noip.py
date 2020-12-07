#!/home/user/projects/noip-renewer/env/bin/python
from selenium import webdriver
from time import sleep
from sys import argv
#from fake_useragent import UserAgent
import re
import subprocess

def method2():
    div = browser.find_element_by_id("host-panel")
    table = div.find_element_by_tag_name("table")
    body = table.find_element_by_tag_name("tbody")
    return body.find_elements_by_tag_name("tr")

def pushbullet(text, accountEmail):
    text = text.replace('\n', ' | ').replace('\r', '')
    text = ' '.join(text.split())
    text = text.replace(' Modify', ' ')
    text += ' for account ' + accountEmail
    print('Text sent : %s' % text)
    myCmd = '/usr/local/bin/pushbullet'
    out = subprocess.Popen([myCmd, 'push', 'My Phone', 'note', text],
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    print(stdout)
    print("\n")
    print(stderr)
    print("\n")

#USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
LOGIN_URL = "https://www.noip.com/login"
HOST_URL = "https://my.noip.com/#!/dynamic-dns"
LOGOUT_URL = "https://my.noip.com/logout"

# ASK CREDENTIALS
if len(argv) == 3:
    email = argv[1]
    password = argv[2]
else:
    config = open('./config.txt', 'rt')
    x = []
    for line in config:
        splitString = line.split()
        if len(splitString) == 2:
            email = splitString[0]
            password = splitString[1]
            print("Account: %s" % email)

            # OPEN BROWSER
            print('Opening browser')
            #browserOptions = webdriver.FirefoxOptions()
            browserOptions = webdriver.ChromeOptions()
            browserOptions.add_argument("--headless")
            browserOptions.add_argument("--disable-gpu")
            browserOptions.add_argument("--disable-translate");
            browserOptions.add_argument("--disable-infobars")
            #added for Raspbian Buster 4.0+ versions. Check https://www.raspberrypi.org/forums/viewtopic.php?t=258019 for reference.
            browserOptions.add_argument("disable-features=VizDisplayCompositor")
            browserOptions.add_argument("window-size=1200x800")

            # random user agent
            #ua = UserAgent()
            #userAgent = ua.random
            #print(userAgent)
            #browserOptions.add_argument(f'user-agent={userAgent}')
            print(USER_AGENT)
            browserOptions.add_argument("user-agent=%s" % USER_AGENT)

            #browser = webdriver.Firefox(options=browserOptions, executable_path=r"./geckodriver")
            browser = webdriver.Chrome("./chromium-driver", options=browserOptions)
            browser.set_page_load_timeout(120)

            # LOGIN
            print('Login page')
            browser.get(LOGIN_URL)
            browser.find_element_by_name("username").send_keys(email)
            browser.find_element_by_name("password").send_keys(password)
            browser.find_element_by_name("Login").click()

            # RENEW HOSTS
            try:
                browser.get(HOST_URL)
                hosts = method2()

                for host in hosts:
                    print('Host: ' + host.text)
                    regex = r"(?:Expired|Expires in (\d*))"
                    m = re.findall(regex, host.text)
                    if m:
                        if m[0] == '':
                            print('Host expired')
                            pushbullet(host.text, email)
                        else:
                            remainingDays = int(m[0])
                            if remainingDays < 5:
                                pushbullet(host.text, email)

                        sleep(0.25)

            except Exception as e:
                print("Error: ", e)

            finally:
                browser.get(LOGOUT_URL)
                browser.quit()
