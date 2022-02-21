from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, os, json
import wget
import config

Wpath = '' # put the path to chrome driver 
searchQuery = '' # inform here your search keyword 

output_tojson = []

browser_options = webdriver.ChromeOptions()
options = [
'--disable-blink-features', 
'--no-sandbox', 
'--disable-extensions',
'--ignore-certificate-errors', 
'--incognito'
]
for option in options:
    browser_options.add_argument(option)
browser = webdriver.Chrome(executable_path=Wpath, options=browser_options)
wait = WebDriverWait(browser, 30)

#this function after generating the path for the future directory return the path in a string format to be used later 
def make_path():
    directory_name = searchQuery # the search keyword will be used to create a directory with the same name 
    path_dir = '' # inform here the full path to the Ali srapper script 
    path = os.path.join(path_dir, directory_name)
    return str(path)

 #create a directory with the search keyword this dir will recieve the images downloaded later 
def make_dir():
    try:
        make_dir = os.mkdir(make_path())
    except Exception as e:
        print(f'{e}')
        pass

#return a json file once the script break or at the end of the iteration  
def get_json():
    path = make_path()
    return json.dump(output_tojson, open(path+'.json', 'w'), indent=2)

def scrowldown():
       return browser.execute_script('window.scrollBy(0,280)', '')

def get_bottom_page():
    page_down = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")

def get_top_page():
    page_up = browser.execute_script("window.scrollTo(document.body.scrollHeight ,0);var scrollup=document.body.scrollHeight;return scrollup;")

def change_page_result():
    dBase_xpath = "//a[@class='seb-pagination__pages-link pages-next']"
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, dBase_xpath))).click()
        time.sleep(5)
        find_product()
    except Exception as e:
        print(f"\ncouldn't acces the next button initializing scrolldown: {e}")
    try:
        browser.execute_script('window.scrollBy(0,40)', '')
        wait.until(EC.element_to_be_clickable((By.XPATH, dBase_xpath))).click()
        time.sleep(15)
        find_product()
    except Exception as e:
        print(f"\ncouldn't find the next button check if pages are all parsed: {e}")
        get_json()

def get_results():
    results = browser.find_elements(By.XPATH, "//div[@data-aplus-auto-normal-offer='true']")
    return results

def get_connexion():
    alibaba_login = 'https://passport.alibaba.com/'
    browser.get(alibaba_login)
    
    time.sleep(5)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@title='sign in with linkedin']"))).click()
    time.sleep(5)
    window_before = browser.window_handles[0]
    window_after = browser.window_handles[1]
    browser.switch_to.window(window_after)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))).send_keys(config.LINKEDIN_USERNAME)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys(config.LINKEDIN_PASSWORD)
    time.sleep(4)
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    browser.switch_to.window(window_before)
    time.sleep(3)
    browser.maximize_window()
    time.sleep(5)
    browser.find_element(By.XPATH,"//div[@class='gdpr-btn gdpr-agree-btn']").click()

def initialize_search():
    search = browser.find_element(By.XPATH,"//input[@class='ui-searchbar-keyword']")
    search.clear()
    query = searchQuery
    search.send_keys(query)
    search.send_keys(Keys.ENTER)
    make_dir()
    print(f" {searchQuery} dir done")

def find_product():

    path = make_path()
    get_bottom_page()
    time.sleep(10)
    get_top_page()
    results = get_results()
    print(len(results))
    
    
    count = 0
    
    
    for i in results:
        
        time.sleep(2)
        
        product_name = i.find_element(By.XPATH,".//h2[@data-e2e-name='title']").text
        
        url = i.find_element(By.TAG_NAME, "a")
        product_url = url.get_attribute("href")
        

        try:
            normal_price = i.find_element(By.XPATH, ".//span[@class='elements-offer-price-normal__price']").text
        except:
            print(f'normal price not found switching to promotion:')
            normal_price = None
        try :
            promotion_price = i.find_element(By.XPATH, ".//span[@class='elements-offer-price-normal__promotion']").text
        except Exception as e:
            print(f'promotion not found keeping normal price')
            promotion_price = None
        
        min_quantity = i.find_element(By.CSS_SELECTOR, ".element-offer-minorder-normal__value").text
        
        img_div = i.find_element(By.CSS_SELECTOR, ".seb-img-switcher__imgs")
        img_url = img_div.get_attribute("data-image")
        img_url = 'https:'+img_url
        img_url = img_url.replace('_300x300.jpg','')
        
        destination = path +'/'+ img_url.split('/')[-1]
        wget.download(img_url, destination)
        
        count +=1
        scrowldown()
        
        output_item = {
            "Product_name": product_name,
            "Product_normal_price": normal_price,
            "Product_Promotion_price": promotion_price,
            "Product_min_quantity": min_quantity,
            "Product_image" : img_url,
            "product_page": product_url
            }
        output.append(output_item)
        if count == len(results):
            
            change_page_result()

if __main__=='__name__':
    get_connexion()
    time.sleep(10)
    initialize_search()
    find_product()