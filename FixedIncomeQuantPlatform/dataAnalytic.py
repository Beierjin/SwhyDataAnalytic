from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
import json
import numpy as np

def loadPage(request):
    return render(request, 'YTMAnalytic.html')

def loadData(request):
    quoteData = {}
    #抽取request中数据
    if(request.method == 'POST'):
        try:
            bondType = request.POST['bondType']
            duration = request.POST['duration']
            startTime = request.POST['startTime']
            endTime = request.POST['endTime']
            containerName = request.POST['containerName']
        except Exception as e:
            print("get request error, ret = %s" % e.args[0])
    #获取YTM数据
    quoteData['quoteData'] = getBondYTMData(bondType, duration, startTime, endTime)
    #存储债券名称
    quoteData['bondType'] = bondType
    #存储container的名字
    quoteData['containerName'] = containerName
    print(quoteData)
    return JsonResponse(json.dumps(quoteData, ensure_ascii=False, sort_keys=True), safe=False)

def getBondYTMAnalyicData(request):
    #抽取request中数据
    if (request.method == 'POST'):
        try:
            arrayData = request.POST.getlist('arrayData[]')
        except Exception as e:
            print("get request error, ret = %s" % e.args[0])

    #存储类型转换
    arrayData = np.array(arrayData)
    arrayData = arrayData.astype(np.float)
    arrayData = [data for data in arrayData if str(data) != 'nan']

    #获取各种数据指标

    #获取各种数组值
    print(arrayData)
    return

def getBondYTMDiffCacl(request):
    quoteData = {}
    #抽取request中数据
    if (request.method == 'POST'):
        try:
            bondType = request.POST.getlist('bondType[]')
            duration = request.POST.getlist('duration[]')
            startTime = request.POST['startTime']
            endTime = request.POST['endTime']
            containerName = request.POST['containerName']
        except Exception as e:
            print("get request error, ret = %s" % e.args[0])

    #获取价差数据，价差可以换为除法。--------此处如果有多条数据可以用循环
    YTMData1 = getBondYTMData(bondType[0], duration[0], startTime, endTime)
    YTMData2 = getBondYTMData(bondType[1], duration[1], startTime, endTime)
    diffData = dictMinus(YTMData1, YTMData2)
    # 获取YTM数据
    quoteData['quoteData'] = diffData
    # 存储债券名称
    quoteData['bondType'] = '价差--'+ bondType[0] + '和' + bondType[1]
    # 存储container的名字
    quoteData['containerName'] = containerName
    print(quoteData)
    return JsonResponse(json.dumps(quoteData, ensure_ascii=False, sort_keys=True), safe=False)

def getBondYTMData(bondType, duration, startTime, endTime):
    print(bondType, duration, startTime, endTime)
    #建立数据库连接
    cursor = connection.cursor()
    #查询数据
    try:
        cursor.execute("select bondytm.bondytm, bondytm.timestamp"
                       " from bondytm, sys_code where sys_code.codetype = 'bondytmtype' "
                       "and bondytm.bondytmtype = sys_code.code and sys_code.codename = %s "
                       "and bondytm.bondduration = %s ORDER BY bondytm.timestamp DESC", (bondType, duration))
    except Exception as e:
        print("select table failed, ret = %s" % e.args[0])
        cursor.close()

    listData = cursor.fetchall()
    cursor.close()
    #类型转换
    keys = ['bondytm', 'timestamp']
    dictData = list2dict(keys, listData)
    # dictData = [(k, dictData[k]) for k in sorted(dictData.keys())]
    return dictData

def list2dict(keys, values):
    dictData = {}
    for value in values:
        row = {}
        value = list(value)
        for i in range(0, len(keys)):
            row[keys[i]] = str(value[i])
        #时间戳作为keys
        dictData[str(value[1])] = row
    return dictData

def dictMinus(dict1, dict2):
    diffDict = {}
    for k, v in dict2.items():
        if k in dict1.keys():
            data = {}
            data['bondytm'] = (float(dict1[k]['bondytm']) - float(v['bondytm']))
            data['timestamp'] = k
            diffDict[k] = data

    return diffDict