import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"

}
webdriver_executable_path=r"C:\Users\greek\PycharmProjects\parsing\chromedriver.exe"

def get_source_html(url):
    driver = webdriver.Chrome(webdriver_executable_path)
    driver.maximize_window()
    try:
        driver.get(url=url)
        sleep(3)
        while True:
            find_more_element = driver.find_element_by_class_name("catalog-button-showMore")
            if driver.find_elements_by_class_name("hasmore-text"):
                with open("source.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                sleep(3)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_urls(file_path: str):

    with open(file_path, "r", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    item_divs = soup.find_all("div", class_="minicard-item__info")

    urls = []
    if len(item_divs) == 0:
        print("Empty!")
        return "[INFO] Task executed unsuccessfully!"
    else:

        for item in item_divs:
            item_url = item.find("h2", class_="minicard-item__title").find("a").get("href")
            urls.append(item_url)

    with open("urls.txt", "w") as file_urls:
        for url in urls:
            file_urls.write(f"{url}\n")

    return "[INFO] Urls collected successfully!"


def get_data(file_path):
    with open(file_path, "r") as file:
        url_list = [url.strip() for url in file.readlines()]

    for url in url_list[:1]:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        try:
            item_name = soup.find("span", {"itemprop" : "name"}).text.strip()
        except Exception as ex_:
            print(ex_)
            item_name = None

        item_phones_list = []
        try:
            item_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")
            for phone in item_phones:
                item_phone = phone.get("href").split(":")[-1].strip()
                item_phones_list.append(item_phone)
        except Exception as ex:
            item_phones_list = None

        try:
            item_address = soup.find("address", class_="iblock").text.strip()
        except Exception as ex_:
            item_address = None

        print(item_name, item_phones_list, item_address)



def main():
    url = "https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91955103369411&center%5B%5D=30.343507880992853&zoom=10"
    #get_source_html(url)
    #get_urls("source.html")
    get_data("urls.txt")

if __name__ == "__main__":
    main()
