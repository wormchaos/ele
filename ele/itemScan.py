import re
import requests


def getFoods(html):
    reg = r'<div class="np clearfix"(.*\n*).*\n*.*\n*.*\n*.*\n*.*\n*</div>'
    textRe = re.compile(reg)
    return re.findall(textRe,html)


def getItemList(shopId = '256263'):
    r = requests.get('https://mainsite-restapi.ele.me/shopping/v1/menu?restaurant_id=' + shopId)
    result = r.json()

    list = []

    for item in result:
        #print item['description']
        for food in item['foods']:
            map = {}
            map["name"] = food['name']
            map["description"] = food['description']
            map["category_id"] = food['category_id']
            url = food['image_path']
            if url and len(url) > 2:
                map["img"] = 'http://fuss10.elemecdn.com/' + url[0:1] + '/' + url[1:3] + '/' + url[3:] + '.jpeg?imageMogr2/thumbnail/100x100/format/webp/quality/85'
            else:
                map["img"] = ''
            list.append(map)
    return list