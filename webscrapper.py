import requests
from bs4 import BeautifulSoup
import csv

site_url ="https://pricebaba.com/laptop/pricelist/dell-laptops?page={}"
datas_url= []
for i in range(1,13):
    site_html = requests.get(site_url.format(i)).text
    html_content = BeautifulSoup(site_html,'lxml')
    if not html_content.find_all('div',attrs={'class':'pg-error'}):
        html_section = html_content.find_all('div',attrs={'id':'productsCnt'})[0]
        html_section_part = html_section.find_all('span',attrs={'class':'target_link','class':'seePrices'})
        datas_url.extend([section['data-href'] for section in html_section_part])
    else:
        print(i,'not found')
        

all_product = []
header = []
for url in datas_url:
    print(url)
    product_content = requests.get(url).text
    product_soup = BeautifulSoup(product_content,'lxml')
    tables = product_soup.find_all('div',attrs={'id':'specificationsTab'})[0].find_all('table')
    product_info ={}
    for table in tables:
        tbody = table.find('tbody')
        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            product_info.setdefault(tds[0].text,tds[1].text)
            header.append(tds[0].text)
    all_product.append(product_info)    

header = list(set(header))
for product in all_product:
    for head in header:
        product.setdefault(head,'')

with open('laptop.csv','w',newline='',encoding='utf-8') as csvwriter:
    writer =csv.DictWriter(csvwriter,fieldnames=header)
    writer.writeheader()
    writer.writerows(all_product)
