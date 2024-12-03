from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time 
import os

def get_driver(driver_num = 1):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-notifications')
    chrome_service = Service(f'D:/TYNGOC/CNTT/A_Code/facebook_scraping/driver/chromedriver-win64_{str(driver_num)}/chromedriver.exe')

    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    driver.implicitly_wait(5)
    return driver  
 
def is_logged_in(driver):
    try:
        # Tìm phần tử xuất hiện trên trang chủ sau khi đăng nhập 
        driver.find_element(By.XPATH, '//*[@id="mount_0_0_FB"]/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div/div/label/input')
        return True
    except:
        return False
      
def save_cookies(driver, username, password):
    # 1. Open faceboook
    while not is_logged_in(driver):
        driver.get("http://facebook.com")

        # Đợi trang tải và tìm kiếm phần tử đầu vào email
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password_input = driver.find_element(By.NAME, "pass")

            email_input.send_keys(username)
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            
        except Exception as e:
            print("Lỗi khi tìm phần tử", e)
            return

        # Chờ đăng nhập thành công
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_FB"]/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div/div/label/input'))
            )
        except:
            print("Đăng nhập không thành công! Thử lại")
            continue
    
    print("Đăng nhập thành cồng!")
    pickle.dump(driver.get_cookies(), open(f"my_cookie_{str(username)}.pkl","wb"))

    driver.close()

def login(scrap_url, driver, username, password):
    # Nếu tệp cookies.pkl đã tồn tại, tải cookies từ tệps
    if os.path.exists(f"my_cookie_{str(username)}.pkl"):
        print("Tệp cookies.pkl tồn tại. Đang tải cookies...")
        
        driver.get("https://www.facebook.com")  # Truy cập trang để thêm cookies
        cookies = pickle.load(open(f"my_cookie_{str(username)}.pkl", "rb"))
        
        for cookie in cookies:
            driver.add_cookie(cookie)

        # Làm mới trình duyệt sau khi thêm cookies
        driver.refresh()
        driver.get(scrap_url)
        time.sleep(5)
        
    else:
        save_cookies(driver, username, password)
    
if __name__ == "__main__":
    driver = get_driver(1)
    '''
    username = "hoangvinhcolab1@gmail.com"
    password = "Songchetmacbay0"
    '''
    username = "batuoccui@gmail.com"
    password = "Nguyenty1912@%#"
    scrap_url = "https://www.facebook.com/groups/364372744044518"
    login(scrap_url, driver, username, password)