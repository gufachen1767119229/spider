import requests
from bs4 import BeautifulSoup
def parse_page(url):
    url = 'http://www.weather.com.cn/textFC/hn.shtml'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    response = requests.get(url, headers=headers)
    # print(response.content.decode('utf-8'))
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text, 'html5lib')
    # print(soup)
    conMidtab = soup.find('div', class_="conMidtab")
    tables = conMidtab.find_all('table')
    # print(tables)
    for table in tables:
        trs = table.find_all('tr')[2:]
        #print(trs)
        for index, tr in enumerate(trs):
            # for tr in trs:
            tds = tr.find_all('td')
            city_td = tds[0]
            #print(city_td)
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]

            weather_td = tds[1]
            if index == 0:
                weather_td = tds[2]
            weather_td = list(weather_td.stripped_strings)[0]
            print({ "city" : city, "weather" : weather_td })



def main():
    urls = {'http://www.weather.com.cn/textFC/hb.shtml',
            'http://www.weather.com.cn/textFC/hn.shtml',
            'http://www.weather.com.cn/textFC/db.shtml',
            'http://www.weather.com.cn/textFC/hd.shtml',
            'http://www.weather.com.cn/textFC/hz.shtml',
            'http://www.weather.com.cn/textFC/xb.shtml',
            'http://www.weather.com.cn/textFC/xn.shtml',
            'http://www.weather.com.cn/textFC/gat.shtml'}
    for url in urls:
        parse_page(url)

if __name__ == '__main__':
    main()