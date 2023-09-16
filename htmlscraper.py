from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


import time

login_url = """https://auth.hackthenorth.com/?redirect=my.hackthenorth.com%2F&method=cookie"""
default_user_url = """https://my.hackthenorth.com/qr/2023/fiery-horse-link-town"""

# very secure login credentials
# please don't look at this
email = "andy.gong@mail.utoronto.ca"
password = "CompleteSecurityRisk1"

def scrape_htn_profile(user_url = default_user_url) -> (str, str):
    # Set up the headless browser
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    # Load the login page in the headless browser
    driver.get(login_url)

    # Find the email and password fields and fill them in
    email_field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    email_field.send_keys(email)
    password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    password_field.send_keys(password)

    # Submit the login form
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait for login to complete
    while driver.current_url == login_url:
        time.sleep(0.2)

    # Load the website in the headless browser
    driver.get(user_url)

    # Wait for the content to load
    driver.implicitly_wait(10)

    # Find the content between the specified tags
    user_name = driver.find_element(By.CSS_SELECTOR, "p.sc-dIsUp.jEEywD.sc-LvPXS.dZmfky").text

    bio_info = driver.find_element(By.CSS_SELECTOR, "p.sc-dujIKe.gKBZFy").text

    # We can also grab interests in a similar way, but the tag is shared with bio_info so it's slightly more involved.

    # Output the extracted information
    # print(user_name)
    # print(bio_info)

    driver.quit()

    return user_name, bio_info

if __name__ == "__main__":
    user_name, bioinfo = scrape_htn_profile()
    print(user_name)
    print(bioinfo)