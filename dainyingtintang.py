import requests
from lxml import etree
header = {"User-Agent" :
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
          "Referer" : "https://www.dytt8.net/"}


BASE_DOMAIN = 'https://www.dytt8.net/html/gndy/dyzz/list_23_1.html'
response = requests.get(BASE_DOMAIN, headers=header)

text = response.text
html = etree.HTML(text)

all_a = html.xpath("//div[@class='co_content8']//a")
for a in all_a:
    b = "https://www.dytt8.net"
    href = a.xpath("@href")[0]
    if href.startswith('/'):
        a_href = b + href
        # print(a_href)
        url = a_href
        # print(url)


        response = requests.get(url, headers=header)
        text = response.content.decode('gbk')
        html = etree.HTML(text)

        movie = {}
        time = html.xpath("//div[@class='co_content8']/ul//text()")[0].strip()  # strip用来清除空格
        movie['time'] = time
        image = html.xpath("//div[@id='Zoom']//img/@src")[0]
        movie['image'] = image
        #print(movie)

        Zooms = html.xpath("//text()")
        for index, info in enumerate(Zooms):
            if info.startswith("◎年　　代"):
                info = info.replace("◎年　　代", "").strip()
                movie['info'] = info

            elif info.startswith("◎译　　名"):
                info = info.replace("◎译　　名", "").strip()
                movie['name'] = info
            elif info.startswith("◎主　　演"):
                actors = []
                for x in range(index + 1, len(Zooms)):
                    actor = Zooms[x].strip()
                    # print(actor)
                    if actor.startswith("◎"):
                        break
                    actors.append(actor)
                movie['actor'] = actors
                print(movie)






