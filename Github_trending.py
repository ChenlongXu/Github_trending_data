#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import requests
import asyncio
import time
from bs4 import BeautifulSoup
from lxml import etree
from pyppeteer import launch
from pathlib import Path

#需求：scraping Github daily trending page and download the data into Excel file.
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

    repo_names_03_17 = tree.xpath('//h2/a[contains(@href, "/")]/text()')
    print(repo_names_03_17)
    # ['\n      ', '\n\n      ', '\n      full-stack-fastapi-template\n', '\n      ',
    # '\n\n      ', '\n      MediaCrawler\n', '\n      ', '\n\n      ',
    # '\n      slint\n', '\n      ', '\n\n      ', '\n      gpt-pilot\n', '\n      ', '\n\n      ', '\n      MetaGPT\n', '\n      ', '\n\n      ',
    # '\n      winterjs\n', '\n      ', '\n\n      ', '\n      megacity-metro\n', '\n      ', '\n\n      ', '\n      hello-algo\n', '\n      ',
    # '\n\n      ', '\n      DARC\n', '\n      ', '\n\n      ', '\n      skyvern\n', '\n      ', '\n\n      ', '\n      developer-portfolio\n', '\n      ', '\n\n      ', '\n      googletest\n', '\n      ', '\n\n      ',
    # '\n      teable\n', '\n      ', '\n\n      ', '\n      go-redis\n', '\n      ', '\n\n      ', '\n      MyViewOfLinuxSystems\n', '\n      ', '\n\n      ', '\n      suyu\n', '\n      ', '\n\n      ', '\n      facefusion\n', '\n      ', '\n\n      ', '\n      ios-diia\n', '\n      ', '\n\n      ', '\n      aspnetcore\n', '\n      ', '\n\n      ', '\n      WingetUI\n', '\n      ', '\n\n      ', '\n      ChatGPT-Next-Web\n', '\n      ', '\n\n      ', '\n      lobe-chat\n', '\n      ', '\n\n      ', '\n      pancake-frontend\n', '\n      ', '\n\n      ', '\n      safetensors\n', '\n      ', '\n\n      ', '\n      LaVague\n']

#Pyppeteer
#async def scrape_trending_repos():
    #browser = await launch(args=['--disable-web-security'],
                           #headless=False)  # Run headless=False to see what happens in the browser
    #page = await browser.newPage()
    #await page.goto('https://github.com/trending')
    #await page.waitForSelector('article.Box-row')  # Wait for the repository container to load
    #await page.waitForTimeout(5000)  # Optional: wait for additional time to ensure content is loaded

    # Adjust the selector based on actual content
    # repo_elements = await page.querySelectorAll('h1.h3 a')
    #if not repo_elements:  # Debugging: Check if any elements were found
        #print("No elements found with the given selector")
    #for repo in repo_elements:
        #title = await page.evaluate('(element) => element.textContent', repo)
        #print(title.strip())

    #await browser.close()


#asyncio.get_event_loop().run_until_complete(scrape_trending_repos())

# Data cleaning: Remove newline characters and empty spaces, and filter out empty strings
repo_names_03_17_cleaned = [name.strip() for name in repo_names_03_17 if name.strip()]
print(repo_names_03_17_cleaned)

# Define the path to the Excel file
excel_file_path = Path('github_trending_repositories.xlsx')

# Create a DataFrame from the cleaned list of repository names
df_repo_names = pd.DataFrame(repo_names_03_17_cleaned, columns=['Repository Name'])

# Check if the Excel file already exists
if excel_file_path.is_file():
    # Read the existing Excel file
    df_existing = pd.read_excel(excel_file_path)
    # Append new data
    df_updated = pd.concat([df_existing, df_repo_names], ignore_index=True)
else:
    # If the file doesn't exist, the new data will be the entire content
    df_updated = df_repo_names

# Write the DataFrame to an Excel file, replacing the old file if it exists
df_updated.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f'Data written to {excel_file_path}')



