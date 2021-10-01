import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

webdriver_executable_path=r"C:\Users\User\PycharmProjects\parsing2\chromedriver.exe"


def get_source_html(url):
    driver = webdriver.Chrome(webdriver_executable_path)
    driver.maximize_window()
    try:
        driver.get(url=url)
        sleep(5)
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

def get_items_urls(file_path: str):

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
        print(url_list)


def main():
    url = "https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91955103369411&center%5B%5D=30.343507880992853&zoom=10"
    get_source_html(url)
    print(get_items_urls("source.html"))
    get_data("urls.txt")

if __name__ == "__main__":
    main()
