import time
import requests
import json
import subprocess
import urllib3
import board
from digitalio import DigitalInOut
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

up_left = [0b01110, 0b01011, 0b01101, 0b01001, 0b00111, 0b00001, 0b00110, 0b01100]
up_right = [0b00000, 0b00000, 0b00110, 0b01010, 0b01100, 0b10000, 0b01100, 0b00110]
down_left = [0b01011, 0b10000, 0b10110, 0b10100, 0b01001, 0b01000, 0b00100, 0b00011]
down_right = [0b10010, 0b00101, 0b01101, 0b00001, 0b11010, 0b00010, 0b00100, 0b11000]

lcd_columns = 16
lcd_rows = 2

lcd_rs = DigitalInOut(board.D25)
lcd_en = DigitalInOut(board.D24)
lcd_d4 = DigitalInOut(board.D23)
lcd_d5 = DigitalInOut(board.D17)
lcd_d6 = DigitalInOut(board.D18)
lcd_d7 = DigitalInOut(board.D22)

lcd = Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

lcd.create_char(0, up_left)
lcd.create_char(1, up_right)
lcd.create_char(2, down_left)
lcd.create_char(3, down_right)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pwd = 'PASSWORD' # replace with your password
auth_payload = {"password": pwd}
url_auth = 'https://pi.hole/api/auth'
url_sys = 'https://pi.hole/api/info/system'
url_block = 'https://pi.hole/api/stats/summary'

response = json.loads(requests.request("POST", url_auth, json=auth_payload, verify=False).text)
sid, csrf = response['session']['sid'], response['session']['csrf']

payload = {}
headers = {"X-FTL-SID": sid, "X-FTL-CSRF": csrf}

status = json.loads(requests.request("GET", url_sys, headers=headers, data=payload, verify=False).text)
ram_use = f'{int(status["system"]["memory"]["ram"]["%used"])}%'

summary = json.loads(requests.request("GET", url_block, headers=headers, data=payload, verify=False).text)
blocked = summary["queries"]["blocked"]

temp_output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
temp = f"{int(int(temp_output.replace('temp=', '')[:-5])*(9/5)+32)}\xDF"

top_string = "TEMP RAM BLKD  "
bottom_string = f'{temp:{4}} {ram_use:{3}} {blocked:{5}}'

lcd.clear()
lcd.cursor_position(2, 0)
lcd.message = top_string
lcd.cursor_position(2, 1)
lcd.message = bottom_string

lcd.cursor_position(0, 0)
lcd.message = '\x00'
lcd.cursor_position(1, 0)
lcd.message = '\x01'
lcd.cursor_position(0, 1)
lcd.message = '\x02'
lcd.cursor_position(1, 1)
lcd.message = '\x03'

delete = requests.request("DELETE", url_auth, headers=headers, data=payload, verify=False)
