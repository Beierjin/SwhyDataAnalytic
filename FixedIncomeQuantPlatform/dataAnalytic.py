from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
import json
import numpy as np

def loadPage(request):
    return render(request, 'YTMAnalytic.html')

def loadData(request):
    #抽取request中数据
    if(request.method == 'POST'):
        try:
            bondType = request.POST['bondType']
            duration = request.POST['duration']
            startTime = request.POST['startTime']
            endTime = request.POST['endTime']
        except Exception as e:
            print("get request error, ret = %s" % e.args[0])
    #获取同余数据
    quoteData = getBondYTMData(bondType, duration, startTime, endTime)
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

    #获取各种数组值
    print(arrayData)
    return

def getBondYTMData(bondType, duration, startTime, endTime):
    print(bondType, duration, startTime, endTime)
    #建立数据库连接
    cursor = connection.cursor()
    #查询数据
    try:
        cursor.execute("select bondytm.bondid, bondytm.bondduration, bondytm.bondytm, bondytm.timestamp, sys_code.codename"
                       " from bondytm, sys_code where sys_code.codetype = 'bondytmtype' "
                       "and bondytm.bondytmtype = sys_code.code and sys_code.codename = %s "
                       "and bondytm.bondduration = %s ORDER BY bondytm.timestamp DESC", (bondType, duration))
    except Exception as e:
        print("select table failed, ret = %s" % e.args[0])
        cursor.close()

    listData = cursor.fetchall()
    cursor.close()
    #类型转换
    keys = ['bondid', 'bondduration', 'bondytm', 'timestamp', 'codename']
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
        dictData[str(value[3])] = row
    return dictData