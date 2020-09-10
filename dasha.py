import re
import requests
import lxml.html
import csv
import json


def get_document_urls(url, cookies):
    # url = 'http://судебныерешения.рф/extended-search?page=3'

    loaded_page = requests.request(method='GET', url=url, cookies=cookies)
    parsed_html = lxml.html.fromstring(loaded_page.text)
    a3 = parsed_html.xpath('//div[@id="list"]//a')
    hrefs = list()
    for href in a3:
        hrefs.append(href.attrib['href'])
    return hrefs


def get_article(url):
    loaded_page = requests.post(url)
    parsed_html = lxml.html.fromstring(loaded_page.text)

    court = ""
    d_no = ""
    result = ""
    s = set()

    try:
        court = parsed_html.xpath('/html/body/div/div/div[3]/div[1]/div/div[2]/div[2]/p[5]/b')[0].text
    except Exception:
        pass
    try:
        d_no = parsed_html.xpath("/html/body/div/div/div[3]/div[1]/div/div[2]/div[2]/p[1]/b")[0].text
    except Exception:
        pass
    try:
        result = parsed_html.xpath("//table")[0].xpath("//dd")[0].text
    except Exception:
        pass

    try:
        art = str(parsed_html.xpath("/html/body/div/div/div[3]/div[1]/div/div[7]/div/blockquote")[0].text_content())
        ma = re.finditer('стать?', art)
        for m in ma:
            start_pos = m.start()
            end_pos = m.start() + 20
            str_slice = art[start_pos:end_pos]
            s.add(str_slice)
    except Exception:
        pass

    return url, court, d_no, result, s


# get_article('http://судебныерешения.рф/49766212/extended')


all_hrefs = list()

# ЗАДАДИМ ПАРАМЕТРЫ ПОИСКА
search_params = {
    "extendedSearch[content]": "",  # Текст документа
    "extendedSearch[case_number]": "",  # Номер дела
    "extendedSearch[person_info][0][person]": "",  # Участник дела
    "extendedSearch[judge]": "",  # Судья
    "extendedSearch[entry_start]": "01.09.2020",  # Поступило с
    "extendedSearch[entry_end]": "02.09.2020",  # по
    "extendedSearch[result_start]": "",  # Рассмотрено с
    "extendedSearch[result_end]": "",  # по
    "extendedSearch[region][]": 3,  # id региона суда
    "extendedSearch[court][]": 4,  # id суда в регионе
}

response = requests.request(method='POST',
                            url='http://судебныерешения.рф/extended_filter',
                            data=search_params)

for i in range(1, 15):
    print("process page id={}".format(i))
    urls = get_document_urls(url='http://судебныерешения.рф/extended-search?page={}'.format(i),
                             cookies=response.history[0].cookies)

    for url in urls:
        all_hrefs.append(url)

file = open("dasa.csv", "w", newline='')
wr = csv.writer(file, delimiter=' ',
                quotechar='|', quoting=csv.QUOTE_MINIMAL)

all_count = len(all_hrefs)
k = 1
for i in all_hrefs:
    print("process url={} number {}/{}".format(i, k, all_count))
    a = get_article('http://судебныерешения.рф' + i)
    wr.writerow(a)
    file.flush()
    k += 1
    pass

# print(len(all_hrefs))

#
# не_конец = True
# page_number = 1
# while не_конец:
