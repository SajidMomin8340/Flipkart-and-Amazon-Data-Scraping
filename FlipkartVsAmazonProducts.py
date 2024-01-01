from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

product = input("Enter Product Name: ")
flipkart = product.replace(" ", "%20")
amazon = product.replace(" ", "+")
source=f"https://www.amazon.in/s?k={amazon}&crid=3GXUQMUGDV8WT"
source1 = f"https://www.flipkart.com/search?q={flipkart}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
edge_path = 'D:\\Sajid\\Scraping\\msedgedriver.exe'
driver = webdriver.Edge(edge_path)

print("*************************************************************************** \n")
print("                     Starting Program, Please wait ..... \n")
print("Connecting to Flipkart")
driver.get(source1)
flip="Flipkart"
driver.maximize_window()
time.sleep(3)
# pagination
pagination = driver.find_element_by_class_name('yFHi8N')
pages = pagination.find_elements_by_class_name('ge-49M')
last_page = 3
title = []
price = []
rating = []
current_page = 1

while current_page <= last_page:
    try:
        page = driver.find_element_by_class_name('_36fx1h')
        try:
            products = page.find_elements_by_class_name('_3pLy-c')
            for product in products:
                title.append(product.find_element_by_class_name('_4rR01T').text)
                price.append(product.find_element_by_class_name('_1_WHN1').text)
                rating.append(product.find_element_by_class_name('_1lRcqv').text)
        except NoSuchElementException:
            pass

        try:
            # Try to find elements with class '_4ddWXP'
            products = page.find_elements_by_class_name('_4ddWXP')
            for product in products:
                title.append(product.find_element_by_class_name('s1Q9rs').text)
                price.append(product.find_element_by_xpath('.//div[contains(@class,"_30jeq3")]').text)
                try:
                    rating.append(product.find_element_by_class_name('_3LWZlK').text)
                except NoSuchElementException:
                    rating.append('N/A')
        except NoSuchElementException:
            pass

        current_page += 1
        try:
            next_page = driver.find_element_by_xpath('//span[text()="Next"]')
            next_page.click()
            # Add a small delay to wait for the next page to load
            time.sleep(2)
        except (NoSuchElementException, StaleElementReferenceException):
            pass

    except Exception as e:
        print(f"An error occurred: {e}")

print("""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")

amaz="Amazon"
print("*************************************************************************** \n")
print("                     Starting Program, Please wait ..... \n")
print("Connecting to Amazon")
driver.get(source)
driver.maximize_window()
time.sleep(3)
paginations = driver.find_element_by_class_name('s-pagination-strip')
pagess = paginations.find_elements_by_class_name('s-pagination-item')
last_page1 = 3
title1 = []
price1 = []
current_page1=1
while current_page1 <= last_page1:
    try:
        pages = driver.find_element_by_class_name('s-main-slot')
        try:
            productss = pages.find_elements_by_class_name('puisg-col-12-of-24')
            for productsss in productss:
                    title1.append(productsss.find_element_by_xpath('.//h2//a//span').text)
                    price1.append(productsss.find_element_by_class_name('a-price-whole').text)
        except NoSuchElementException:
            pass
        current_page1 += 1
        try:
            next_page1 = driver.find_element_by_class_name('s-pagination-next')
            next_page1.click()
            # Add a small delay to wait for the next page to load
            time.sleep(2)
        except (NoSuchElementException, StaleElementReferenceException):
            pass
    except Exception as e:
       print(f"An error occurred: {e}")

driver.quit()
print("""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")

df1 = pd.DataFrame({'Amazon':amaz,'Title': title1,'Price':price1})
df = pd.DataFrame({'Flipkart':flip,'Title': title, 'Price': price, 'Rating': rating})
df.to_csv("FlipKart Data.csv", index=False)
df1.to_csv("Amazon Data.csv", index=False)






