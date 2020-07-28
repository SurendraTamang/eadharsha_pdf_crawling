#!/usr/bin/env python
'''
This is script is for scraping the pdf of eadharsha 
one of news platform in my home country

'''

import requests
from bs4 import BeautifulSoup
import random


class EadharshaPDF():

    def get_response(self, url):
        LIST_OF_USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
                               'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
                               'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
                               'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',

                               'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36', ]

        headers = {'User-Agent': random.choice(LIST_OF_USER_AGENTS)}
        response = requests.get(url=url, headers=headers)
        if response.ok:
            return response
        else:
            return None

    def get_eadharsa_pdf(self, url):
        response = self.get_response(url)

        if response:
            soup = BeautifulSoup(response.content, 'lxml')
            link_pdf_url = soup.find_all(
                class_='epaepr-archive-wrapper')[0].find('a')['href']
            print("The link is find!!", link_pdf_url)
            response2 = self.get_response(link_pdf_url)
            if response2:
                soup2 = BeautifulSoup(response2.content, 'lxml')
                pdf_url = soup2.find(id='pdf-src')['value']
                response3 = self.get_response(pdf_url)
                if response3:
                    self.download_pdf(response3)
                    print("Done!")

    def download_pdf(self, response):
        print("Started the pdf downloading!!")
        name = response.url.split('/')[-1]
        with open('pdfs/'+name, 'wb') as f:
            f.write(response.content)


if __name__ == "__main__":
    bot = EadharshaPDF()
    bot.get_eadharsa_pdf('https://www.eadarsha.com/nep/epaper')
