# noip-renewer
Send pushbullet notifications if No-IP hosts need renewal

### Installation

```
$ mkdir drivers
$ cd drivers
$ wget http://security.debian.org/debian-security/pool/updates/main/c/chromium/chromium-driver_79.0.3945.130-1~deb10u1_armhf.deb
$ mkdir extract
$ dpkg-deb -R chromium-driver_79.0.3945.130-1~deb10u1_armhf.deb extract
$ mv extract/usr/local/bin/chromedriver chromium-driver_79.0.3945.130-1
$ chmod u+x chromium-driver_79.0.3945.130-1
$ mv chromium-driver_79.0.3945.130-1 ../chromium-driver
$ sudo apt-get install libminizip1 libwebpmux3 libgtk-3-0 libxss1 libre2-5 chromium-browser
$ wget http://security-cdn.debian.org/debian-security/pool/updates/main/c/chromium/chromium_79.0.3945.130-1~deb10u1_armhf.deb
$ sudo dpkg -i chromium_79.0.3945.130-1~deb10u1_armhf.deb
$ sudo apt-get install -f
```

#### Vhost

```
$ virtualenv -p python3 ./env
$ source env/bin/activate
$ pip install --upgrade pip
$ pip install --upgrade setuptools
$ pip3 install -U -r requirements.txt
```

### Usage

```
$ python3 noip.py 
``` 
   
#### Software
- Python 3
- [Selenium](https://github.com/SeleniumHQ/Selenium)
- Chromium Driver

#### Requirements

```bash
$ pip3 install -U -r requirements.txt
``` 
