#import all necessary modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

#Opeaning browser and maximize 
driver=webdriver.Chrome()    #Chrome driver should be present in Python script folder
driver.get("https://www.bt.com/")
driver.implicitly_wait(0.10)
driver.maximize_window()

# Close accept Cookie pop-up if it appears
try:
    wait = WebDriverWait(driver, 30)
    driver.switch_to.frame("trustarc_cm")
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//a[text()='Accept all cookies']"))).click()
except:
    pass
finally:
    driver.switch_to.default_content()

# Hover to Mobile menu and select Mobile phones
Mobile=driver.find_element(By.XPATH,"(//a[contains(@href,'mobile')]//span[text()='Mobile'])[1]")
Mobile.click()
driver.find_element(By.XPATH,"//a[text()='Mobile phones']").click()

#Verify the numbers of banners present below “See Handset details” should not be less than 3
banners=driver.find_elements(By.XPATH,"//*[@class='flexpay-card_card_wrapper__Antym']")
assert len(banners)>=3

#Scroll down and click View SIM only deals
sim_details = driver.find_element(By.XPATH,"//a[text()='View SIM only deals']")
driver.execute_script("arguments[0].scrollIntoView(true)",sim_details)
sim_details.click()

#Validate the title for new page.
assert driver.title == "SIM Only Deals | Compare SIMO Plans & Contracts | BT Mobile"

#Validate “30% off and double data” was 125GB 250GB Essential Plan, was £27 £18.90 per month
expected_plan = '"30% off and double data" was 125GB 250GB Essential Plan, was £27 £18.90 Per month'
product_card = "//*[contains(@class,'simo-card-ee_product_card')]"
plans = driver.find_elements(By.XPATH,product_card)
for i in range(len(plans)):
    actula_plan_text=""
    plan="(//div[contains(@class,'social_norm')])[{}]".format(i+1)
    actula_plan_text=driver.find_element(By.XPATH,plan).text
    data="(//div[contains(@class,'plan_details_wrapper')][1])[{}]".format(i+1)
    data_text=driver.find_element(By.XPATH, data).text
    price="(//div[contains(@class,'plan_details_wrapper')][2])[{}]".format(i+1)
    price_text=driver.find_element(By.XPATH, price).text
    actula_plan_text= '"'+actula_plan_text+'"'+" "+' '.join(data_text.split("\n"))+", "+' '.join(price_text.split("\n"))
    if expected_plan in actula_plan_text:
        break
assert expected_plan in actula_plan_text
print("Siddharoodha practice")
#Close browser
driver.close()
