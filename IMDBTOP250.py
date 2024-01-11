import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式，如果你不需要浏览器GUI可以启用
driver = webdriver.Chrome(options=options)

# 函数来处理列表中的第一个元素，如果列表为空则返回空字符串
def get_first_text(lst):
    return lst[0].strip() if lst else ''

# 根URL和头信息
try:
    # 访问IMDb的Top 250页面
    driver.get('https://www.imdb.com/chart/top/')

    # 使用requests获取页面内容
    base_url = 'https://www.imdb.com/chart/top/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    }
    response = requests.get(url=base_url, headers=headers)

    if response.status_code == 200:
        html = etree.HTML(response.text)
        # 注意这里的XPath可能需要根据实际页面结构调整
        lis = html.xpath('//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul')


        with open('IMDB_top250.txt', 'w', encoding='utf-8') as f:
            for li in lis:
                # 提取电影信息
                title = get_first_text(li.xpath('./li[1]/div[2]/div/div/div[1]/a/h3/text()'))
                link = get_first_text(li.xpath('./li[1]/div[2]/div/div/div[1]/a/@href'))
                full_link = 'https://www.imdb.com' + link
                score = get_first_text(li.xpath('./li[1]/div[2]/div/div/span/div/span/text()'))

                for index, li in enumerate(lis, start=1):
                    # Use Selenium to locate the li element on the actual page
                    try:
                        # Construct an XPath that finds the nth li element on the page
                        li_xpath = f"(//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-between sc-71ed9118-0 kvsUNk compact-list-view ipc-metadata-list--base']/li[@class='ipc-metadata-list-summary-item sc-3f724978-0 enKyEL cli-parent'])[{index}]"
                        li_element = driver.find_element(By.XPATH, li_xpath)
                        
                        # Now find the button within this li element
                        button = li_element.find_element(By.XPATH, ".//svg[@class='ipc-icon ipc-icon--info']")
                        button.click()

                        # Wait for the popup content to load and extract
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'ipc-promptable-base__content'))
                        )
                        popup_content = driver.find_element(By.CLASS_NAME, 'ipc-promptable-base__content').text

                    except NoSuchElementException:
                        f.write(f'{title}\t{full_link}\t{score}\t"Button not found"\n')

    else:
        print('Failed to retrieve data from:', base_url)

finally:
    driver.quit()


