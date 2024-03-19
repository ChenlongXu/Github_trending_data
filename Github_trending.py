import time
from bs4 import BeautifulSoup
from lxml import etree
from pyppeteer import launch
from pathlib import Path

#需求：scraping Github daily trending page and downloading the data into an Excel file.
if __name__ == "__main__":
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    #爬取到页面源码数据
    url = 'https://github.com/trending'
    page_text = requests.get(url=url,headers=headers).text

    #数据解析
    tree = etree.HTML(page_text)
    #repo_name = tree.xpath('/html/body/div[1]/div[6]/main/div[3]/div/div[2]/article[1]/h2/a')

    repo_names_03_19 = tree.xpath('//h2/a[contains(@href, "/")]/text()')
    # print(repo_names_03_19)

    authors_names_03_19 = tree.xpath('/html/body//article/h2/a/span/text()')
    # print(authors_names_03_19)

    repo_descriptions_03_19 = tree.xpath('/html/body//article/p/text()')
    # print(repo_descriptions_03_19)

    languages_03_19 = tree.xpath('/html/body//article/div[@class="f6 color-fg-muted mt-2"]/span/span[2]/text()')
    # print(languages_03_19)

    total_stars_03_19 = tree.xpath('/html/body//article/div[@class="f6 color-fg-muted mt-2"]/a[1]/text()')
    # print(total_stars_03_19)

    total_forks_03_19 = tree.xpath('/html/body//article/div[@class="f6 color-fg-muted mt-2"]/a[2]/text()')
    # print(total_forks_03_19)

    built_by_03_19 = tree.xpath('/html/body//article/div[@class="f6 color-fg-muted mt-2"]/span[2]//a/img/@src')
    print(built_by_03_19)
# Data cleaning: Remove newline characters and empty spaces, and filter out empty strings
# repo_names_03_19_cleaned = [name.strip() for name in repo_names_03_19 if name.strip()]
# print(repo_names_03_19_cleaned)


