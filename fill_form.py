import re

import numpy as np
import tesserocr as ts
from PIL import Image
from selenium import webdriver


def main():
    CAPTCHA_IMG_XP = '/html/body/div/div[2]/div/form/div[3]/div[2]/img'
    NID = 'F130261848'

    driver = webdriver.Firefox()
    driver.get('https://www2.ndmctsgh.edu.tw/newwebreg/Register/Doctors?pos=B&DeptCode=11K&DeptGroup=4')

    driver.implicitly_wait(600)
    cnoid = driver.find_element_by_id('cnoid')
    cnoid.send_keys(NID)

    captcha_img = driver.find_element_by_xpath(CAPTCHA_IMG_XP)
    captcha_img.screenshot('captcha.png')

    img = np.asarray(Image.open('captcha.png').convert('RGB'))
    img[np.any(img > [50, 50, 50], axis=-1)] = 255
    img = Image.fromarray(img).resize([360, 80], resample=Image.BILINEAR)

    ocr_result = ts.image_to_text(img, lang='snum')
    vercode = re.sub(r'[ ,\n,A-Z,a-z]', '', ocr_result)

    captcha = driver.find_element_by_id('captcha')
    captcha.send_keys(vercode)


if __name__ == '__main__':
    main()
