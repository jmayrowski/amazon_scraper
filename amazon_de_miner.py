from lxml import html
import requests
import json
from time import sleep

def parse(url,k):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    for i in range(20):
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//span[@id="productTitle"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_COLOR = '//span[contains(@class,"selection")]/text()'
            XPATH_KEYWORD = '//meta[contains(@name,"keywords")]/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_COLOR = doc.xpath(XPATH_COLOR)
            RAW_KEYWORD = doc.xpath(XPATH_KEYWORD)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            COLOR = ' '.join(''.join(RAW_COLOR).split()) if RAW_COLOR else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            KEYWORD = ' '.join(''.join(RAW_KEYWORD).split()) if RAW_KEYWORD else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE
            #retrying in case of captcha
            if not NAME :
                raise ValueError('captcha')

            data = {
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'COLOR':COLOR,
                    'KEYWORD':KEYWORD,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    'IMG':k+".jpg",
                    'ASIN':k,
                    }

            return data
        except Exception as e:
            print (e)

def GetAsin():
    AsinList = [
    'B00SLC2FMK',
    'B005JPT5K2',
    ]
    extracted_data = []


    for i in AsinList:
        url = "http://www.amazon.de/dp/"+i
        print ("Processing: "+url)
        extracted_data.append(parse(url,i))
        sleep(5)
    f=open('data.json','w')
    json.dump(extracted_data,f,indent=4)


if __name__ == "__main__":
    GetAsin()