# coding=utf-8
import datetime
import os
from logging import log

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from ele.itemScan import getItemList

FILE_DIR = r'USER/'
ORDER_DIR = r'ORDER/'

def sayHello(request):
    s = 'Hello World!'
    current_time = datetime.datetime.now()
    html = '<html><head></head><body><h1> %s </h1><p> %s </p></body></html>' % (s, current_time)
    return HttpResponse(html)


def showGoods(request):
    params = {}
    ip = get_client_ip(request)
    if os.path.exists(FILE_DIR + ip + '.txt'):
        f = open(FILE_DIR + ip + '.txt', "r")
        nickname = f.readline()
        f.close()
        params['nickname'] = nickname
    else:
        return render_to_response('register.html')


    try:
        id = request.GET['id']
        params['foods'] = getItemList(id)
    except:
        params['foods'] = getItemList()
    return render_to_response('info.html', params)

def get_client_ip(request):
    try:
      real_ip = request.META['HTTP_X_FORWARDED_FOR']
      regip = real_ip.split(",")[0]
    except:
      try:
        regip = request.META['REMOTE_ADDR']
      except:
        regip = ""
    return regip

def add(request):
    ip = get_client_ip(request)
    name = request.GET['name'].replace(' ', '')
    f = open(FILE_DIR + ip + '.txt', 'w')
    f.write(name.encode('utf-8'))
    f.close()
    params = {}
    params['foods'] = getItemList()
    return render_to_response('info.html', params)

def order(request):
    ip = get_client_ip(request)
    id = request.GET['id']
    name = request.GET['name']
    # read nickname

    f = open(FILE_DIR + ip + '.txt', "r")
    nickname = f.readline()
    f.close()

    f = open(ORDER_DIR + ip + '.txt', 'w')
    f.write(nickname + ' ' + str(id) + ' ' + name.encode('utf-8'))
    f.close()
    params = {}
    params['foods'] = getItemList()
    return HttpResponseRedirect('/orderList')

def orderList(request):
    # itemList = getItemList()
    calMap = {}
    params = []
    for parent,dirnames,filenames in os.walk(ORDER_DIR):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:                        #输出文件信息
            if filename.find('99.48.58') >= 0:
                continue
            else:
                f = open(ORDER_DIR + filename, 'r')
                content = f.readline()
                f.close()
                orders = {}
                orders['name'] = content.split(' ')[0]
                orders['id'] = content.split(' ')[1]
                orders['food'] = content.split(' ')[2]
                # foodId = content.split(' ')[1]
                # orders['food'] = foodId
                # for item in itemList:
                #     # orders['food'] = item['category_id']
                #     if str(foodId) == str(item['category_id']):
                #         orders['food'] = item['name']

                # if orders['name'] in calList:
                #     calList[orders['name']] += 1
                # else:
                #     calList.append(orders['name'])

                # f = open('result.txt', 'a')
                # f.write(orders['name'] + ' ' + orders['food'] + '\n')
                params.append(orders)

    ip = get_client_ip(request)
    f = open(FILE_DIR + ip + '.txt', 'r')
    name =f.readline()

    return render_to_response('list.html', {'orderList' : params, 'name' : name} )