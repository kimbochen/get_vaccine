import time
from datetime import datetime as dt

import numpy as np
import tesserocr as ts
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_vercode(img_name):
    img = np.asarray(Image.open(img_name).convert('RGB'))
    idx = np.any(img > [50, 50, 50], axis=-1)
    img[idx] = 255
    img = Image.fromarray(img).resize([360, 80], resample=Image.BILINEAR)

    ocr_result = ts.image_to_text(img, lang='snum')
    vercode = ocr_result[:-1]
    vercode = vercode.replace('B', '8')
    vercode = vercode.replace('H', '11')

    return vercode


def main():
    doctor_xp = '/html/body/div/div[2]/div/div[1]/div/div[1]/div/table/tbody/tr[4]/td[4]/a'
    captcha_img_xp = '/html/body/div/div[2]/div/form/div[3]/div[2]/img'
    nid = 'F130261848'

    driver.implicitly_wait(5)
    try:
        doctor = driver.find_element_by_xpath(doctor_xp)
        doctor.click()
    except NoSuchElementException:
        print('Cannot find the doctor link, please click it manually.')

    driver.implicitly_wait(10)
    cnoid = driver.find_element_by_id('cnoid')
    cnoid.send_keys(nid)

    captcha_img = driver.find_element_by_xpath(captcha_img_xp)
    captcha_img.screenshot('captcha.png')
    vercode = get_vercode('captcha.png')

    captcha = driver.find_element_by_id('captcha')
    captcha.send_keys(vercode)


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('https://www2.ndmctsgh.edu.tw/newwebreg/Register/Doctors?pos=B&DeptCode=11K&DeptGroup=4')

    while dt.now().strftime("%H:%M:%S") != '09:00:00':
        time.sleep(0.5)
    else:
        driver.refresh()
        main()
