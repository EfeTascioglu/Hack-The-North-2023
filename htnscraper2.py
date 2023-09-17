from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

driver = None  # global variable to store the driver


login_url = """https://auth.hackthenorth.com/?redirect=my.hackthenorth.com%2F&method=cookie"""
default_user_url = """https://my.hackthenorth.com/qr/2023/fiery-horse-link-town"""

# very secure login credentials
# please don't look at this
email = "andy.gong@mail.utoronto.ca"
password = "CompleteSecurityRisk1"

def setup_browser():
    global driver
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2, # Disable images
        "profile.default_content_setting_values.stylesheets": 2 # Disable CSS
    })
    driver = webdriver.Chrome(options=options)


def scrape_htn_profile_optimized(user_url=default_user_url) -> (str, str):
    global driver
    if not driver:
        setup_browser()
    
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
    
    # Use WebDriverWait instead of sleep or implicit wait
    wait = WebDriverWait(driver, 10) # 10 seconds timeout
    wait.until(EC.url_changes(login_url))
    
    driver.get(user_url)
    
    try:
        user_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.sc-dIsUp.jEEywD.sc-LvPXS.dZmfky"))).text
    except NoSuchElementException:
        user_name = "Unknown"
        
    try:
        bio_info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.sc-dujIKe.gKBZFy"))).text
    except NoSuchElementException:
        bio_info = ""
    
    return str(user_name) + "\n" + str(bio_info)


if __name__ == "__main__":
    user_name, bioinfo = scrape_htn_profile()
    print(user_name)
    print(bioinfo)
    teardown_browser()