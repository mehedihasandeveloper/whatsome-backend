# from flask import Flask, request, jsonify
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from urllib.parse import quote
# import time
#
# app = Flask(__name__)
#
# def initialize_driver():
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get('https://web.whatsapp.com')
#     time.sleep(15)
#     return driver
#
#
# """
# # working fine. Send only message api
# """
#
# @app.route('/send_message', methods=['POST'])
# def send_message():
#     data = request.json
#
#     msg = data.get('message')
#     numbers = data.get('numbers', [])
#
#     if not msg or not numbers:
#         return jsonify({'error': 'Message and numbers are required'}), 400
#
#     msg = quote(msg)
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#
#     try:
#         link = 'https://web.whatsapp.com'
#         driver.get(link)
#         time.sleep(20)
#
#         for number in numbers:
#             link2 = f'https://web.whatsapp.com/send/?phone={number}&text={msg}'
#             driver.get(link2)
#             time.sleep(10)
#             action = ActionChains(driver)
#             action.send_keys(Keys.ENTER)
#             action.perform()
#             time.sleep(10)
#
#         return jsonify({'status': 'Messages sent successfully'})
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#     finally:
#         driver.quit()
#
# # working fine
# def send_picture(driver, numbers, image_path):
#     for number in numbers:
#         link = f'https://web.whatsapp.com/send/?phone={number}'
#         driver.get(link)
#         time.sleep(20)
#
#         attach_button = WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]'))
#         )
#         attach_button.click()
#
#         image_box = WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
#         )
#         image_box.send_keys(image_path)
#
#         time.sleep(10)
#         ActionChains(driver).send_keys(Keys.ENTER).perform()
#         time.sleep(10)
#
# # working fine
# @app.route('/send-picture', methods=['POST'])
# def api_send_picture():
#     data = request.json
#     numbers = data.get('numbers', [])
#     image_path = data.get('image_path', '')
#
#     driver = initialize_driver()
#     send_picture(driver, numbers, image_path)
#     driver.quit()
#
#     return jsonify({"status": "success", "message": "Pictures sent successfully!"})
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

import os
import pickle
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
import time
import threading

app = Flask(__name__)

COOKIE_FILE_PATH = 'whatsapp_cookies.pkl'
driver = None  # Global driver to keep the session alive

def initialize_driver():
    global driver
    if driver is None:
        # Start a new WebDriver session if it's not already running
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get('https://web.whatsapp.com')

        # Check if we have stored cookies and load them
        if os.path.exists(COOKIE_FILE_PATH):
            with open(COOKIE_FILE_PATH, 'rb') as cookie_file:
                cookies = pickle.load(cookie_file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(10)  # Give some time to refresh with the cookies
        else:
            time.sleep(15)  # Allow time for initial manual login
            # Save cookies after first login
            cookies = driver.get_cookies()
            with open(COOKIE_FILE_PATH, 'wb') as cookie_file:
                pickle.dump(cookies, cookie_file)

    return driver

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json

    msg = data.get('message')
    numbers = data.get('numbers', [])

    if not msg or not numbers:
        return jsonify({'error': 'Message and numbers are required'}), 400

    msg = quote(msg)
    driver = initialize_driver()

    try:
        for number in numbers:
            link = f'https://web.whatsapp.com/send/?phone={number}&text={msg}'
            driver.get(link)
            time.sleep(10)
            action = ActionChains(driver)
            action.send_keys(Keys.ENTER)
            action.perform()
            time.sleep(10)

        return jsonify({'status': 'Messages sent successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def send_picture(driver, numbers, image_path):
    for number in numbers:
        link = f'https://web.whatsapp.com/send/?phone={number}'
        driver.get(link)
        time.sleep(20)

        attach_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]'))
        )
        attach_button.click()

        image_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
        )
        image_box.send_keys(image_path)

        time.sleep(10)
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(10)

@app.route('/send-picture', methods=['POST'])
def api_send_picture():
    data = request.json
    numbers = data.get('numbers', [])
    image_path = data.get('image_path', '')

    driver = initialize_driver()
    send_picture(driver, numbers, image_path)
    # driver.quit() # Removed quitting the driver to keep the session active

    return jsonify({"status": "success", "message": "Pictures sent successfully!"})

if __name__ == "__main__":
    threading.Thread(target=initialize_driver).start()  # Initialize driver when the app starts
    app.run(debug=True)

