#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import requests
import asyncio
import time
import os
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

#需求：scraping Github daily trending page and download the data into an Excel file.
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

    repo_names_03_22 = tree.xpath('//h2/a[contains(@href, "/")]/text()')
    repo_names_03_22_cleaned = [name.strip() for name in repo_names_03_22 if name.strip()]
    print(repo_names_03_22_cleaned)

    authors_names_03_22 = tree.xpath('/html/body//article/h2/a/span/text()')
    authors_names_03_22_cleaned = [name.strip().replace("/", "") for name in authors_names_03_22 if name.strip()]
    print(authors_names_03_22_cleaned)

    repo_descriptions_03_22 = tree.xpath('/html/body//article/p/text()') or ["None"]
    repo_descriptions_03_22_cleaned = [name.strip() for name in repo_descriptions_03_22 if name.strip()]
    print(repo_descriptions_03_22_cleaned)

    languages_03_22 = tree.xpath('/html/body//article/div[@class="f6 color-fg-muted mt-2"]/span/span[2]/text()') or ["None"]
    languages_03_22_cleaned = [name.strip() for name in languages_03_22 if name.strip()]
    print(languages_03_22_cleaned)

    total_stars_03_22 = tree.xpath('/html/body//article/div[@class="f6 color-fg-muted mt-2"]/a[1]/text()')
    total_stars_03_22_cleaned = [name.strip() for name in total_stars_03_22 if name.strip()]
    print(total_stars_03_22_cleaned)

    total_forks_03_22 = tree.xpath('/html/body//article/div[@class="f6 color-fg-muted mt-2"]/a[2]/text()')
    total_forks_03_22_cleaned = [name.strip() for name in total_forks_03_22 if name.strip()]
    print(total_forks_03_22_cleaned)

    built_by_03_22 = tree.xpath('/html/body//article/div[@class="f6 color-fg-muted mt-2"]/span[2]//a/img/@src')
    built_by_03_22_cleaned = [name.strip() for name in built_by_03_22 if name.strip()]
    print(built_by_03_22_cleaned)

def save_data_to_excel(*args, file_name='Github_Trending_Data_03_22.xlsx'):
    # Check if the file exists
    if os.path.exists(file_name):
        wb = load_workbook(file_name)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        # If creating a new file, add the headers
        headers = ["Repository Names", "Repository Authors", "Repository Descriptions", "Languages", "Total Stars", "Total Forks", "Built By",
                   "Date"]
        ws.append(headers)

    # args[0] through args[6] correspond to the collected data lists
    # Zip them together so each "row" in the zipped list contains all items that should go in the same row of the Excel file
    for data_row in zip(*args, ['2024_03_22' for _ in range(len(args[0]))]):
        ws.append(data_row)

    # Adjust column widths with respect to the longest piece of data in that column
    column_widths = []
    for row in ws.iter_rows():
        for i, cell in enumerate(row):
            try:
                column_widths[i] = max(column_widths[i], len(str(cell.value)))
            except IndexError:
                column_widths.append(len(str(cell.value)))

    for i, column_width in enumerate(column_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = column_width + 2  # Adding 2 for a little extra width

    # Save the workbook
    wb.save(file_name)

if __name__ == "__main__":
    save_data_to_excel(repo_names_03_22_cleaned, authors_names_03_22_cleaned, repo_descriptions_03_22_cleaned, languages_03_22_cleaned, total_stars_03_22_cleaned, total_forks_03_22_cleaned, built_by_03_22_cleaned)


