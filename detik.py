from bs4 import BeautifulSoup
import pandas as pd
import json, random, re, requests


class Detik():
    def __init__(self, topic):
        self.topic = topic


    def get_urls(self):
        news_links = []
        # get news URL from page 1 to 5
        for page in range(1,6):
            url = "https://www.detik.com/search/searchall?query=" + self.topic + "&siteid=2&sortby=time&page=" + str(page)
            html_page = requests.get(url).content
            soup = BeautifulSoup(html_page, 'lxml')
            articles = soup.find_all('article')

            for article in articles:
                urls = article.find_all('a')
                for url in urls:
                    news_links.append(url.get('href'))

        return news_links


    def extract_news(self):
        # get news article details from scraped urls
        scraped_info = []
        for news in self.get_urls():
            source = news
            html_page = requests.get(news).content
            soup = BeautifulSoup(html_page, 'lxml')
            # check if title, author, date, news div, is not None type
            title = soup.find('h1', class_='detail__title')
            if title is not None:
                title = title.text
                title = title.replace('\n', '')
                title = title.strip()

            
            author = soup.find('div', class_='detail__author')
            if author is not None:
                author = author.text

            date = soup.find('div', class_='detail__date')
            if date is not None:
                date = date.text

            news_div = soup.find_all('div', class_='detail__body-text itp_bodycontent')
            if news_div is not None:
                for i in news_div:
                    news_content = i.find('p').text
                    # convert scraped data into dictionary
                    news_data = {
                        "url": source,
                        "judul": title,
                        "penulis": author,
                        "tanggal": date,
                        "isi": news_content
                    }
                    # add dicts into a list
                    scraped_info.append(news_data)

        df = pd.DataFrame.from_dict(scraped_info)
        df.to_csv('{}.csv'.format(self.topic),index=False)

topic = input("Masukan topik berita yang ingin diambil: ")
shop = Detik(topic)
shop.extract_news()
