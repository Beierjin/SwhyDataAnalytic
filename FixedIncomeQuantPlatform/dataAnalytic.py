from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
import json

def loadPage(request):
    return render(request, 'YTMAnalytic.html')

def loadData(request):
    #获取同余数据
    quoteData = getBondYTMData()
    print(quoteData)
    return JsonResponse(json.dumps(quoteData, ensure_ascii=False, sort_keys=True), safe=False)

def getBondYTMData():
    #建立数据库连接
    cursor = connection.cursor()
    #查询数据
    try:
        cursor.execute("select bondytm.bondid, bondytm.bondduration, bondytm.bondytm, bondytm.timestamp, sys_code.codename"
                       " from bondytm, sys_code where sys_code.codetype = 'bondytmtype' "
                       "and bondytm.bondytmtype = sys_code.code and sys_code.codename = '中债农发行债' "
                       "and bondytm.bondduration = '1Y' ORDER BY bondytm.timestamp DESC")
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