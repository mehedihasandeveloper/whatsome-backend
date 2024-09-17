# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from urllib.parse import quote
# import time
# with open('message.txt', 'r') as file:
#     msg = file.read()
#
# msg = quote(msg)
#
# numbers = []
# with open('numbers.txt', 'r') as file:
#     for num in file.readlines():
#       numbers.append(num.rstrip())
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#
# link = 'https://web.whatsapp.com'
# driver.get(link)
# time.sleep(15)
#
# for number in numbers:
#     link2 = f'https://web.whatsapp.com/send/?phone={number}&text={msg}'
#     driver.get(link2)
#     time.sleep(5)
#     action = ActionChains(driver)
#     action.send_keys(Keys.ENTER)
#     action.perform()
#     time.sleep(10)
#
# driver.quit()



# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By  # Import By for locating elements
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from urllib.parse import quote
# import time
#
#
# with open('message.txt', 'r') as file:
#     msg = file.read()
#
# msg = quote(msg)
#
#
# numbers = []
# with open('numbers.txt', 'r') as file:
#     for num in file.readlines():
#         numbers.append(num.rstrip())
#
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#
#
# driver.get('https://web.whatsapp.com')
# time.sleep(15)
#
#
# image_path = 'C:/Users/FifoTech/Downloads/293c2108-5c10-4726-9c46-2328a89a16c1.jpg'
#
# for number in numbers:
#
#     link2 = f'https://web.whatsapp.com/send/?phone={number}&text={msg}'
#     driver.get(link2)
#     time.sleep(10)
#
#
#     attach_button = driver.find_element(By.XPATH, '//div[@title="Attach"]')
#     attach_button.click()
#     time.sleep(4)
#
#
#     image_box = driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
#     image_box.send_keys(image_path)
#
#     time.sleep(10)
#
#
#     action = ActionChains(driver)
#     action.send_keys(Keys.ENTER)
#     action.perform()
#
#     time.sleep(10)
#
# driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
import time


with open('message.txt', 'r') as file:
    msg = file.read()

msg = quote(msg)


numbers = []
with open('numbers.txt', 'r') as file:
    for num in file.readlines():
        numbers.append(num.rstrip())


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


driver.get('https://web.whatsapp.com')
time.sleep(15)


image_path = 'C:/Users/FifoTech/Downloads/123.jpg'

for number in numbers:

    link2 = f'https://web.whatsapp.com/send/?phone={number}&text={msg}'
    driver.get(link2)


    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]')))


    attach_button = driver.find_element(By.XPATH, '//div[@title="Attach"]')
    attach_button.click()


    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))


    image_box = driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    image_box.send_keys(image_path)

    time.sleep(5)


    action = ActionChains(driver)
    action.send_keys(Keys.ENTER)
    action.perform()

    time.sleep(5)


driver.quit()

