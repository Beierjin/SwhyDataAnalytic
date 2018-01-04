from django.shortcuts import render

import re, time, os, json, math
import pandas as pd
from django.http import JsonResponse
# from WindPy import w

from . import TYApi

#读取期货合约
baseDir = os.path.dirname(os.path.abspath(__name__))
contractListFileDir = baseDir + '/files/BasicInfo/contractList.xlsx'
print(baseDir)
contractList = list(pd.read_excel(contractListFileDir)['contract'])
contractName = list(pd.read_excel(contractListFileDir)['name'])
contractList = dict(zip(contractList, contractName))

def GetQuotesDataFromTY(request):

    quoteData = {}

    #获得当前时间
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    time_zone = 'Asia/Shanghai'

    #定价参数
    tau = 1   #量
    r = 0.015     #无风险利率

    #初始化同余API
    tyApi = TYApi.TYApi()

    #开启wind接口
    # w.start()

    #获取报价
    for contract in contractList.keys():

        contractData = {}

        #获取期货现价
        forward = tyApi.TYMktQuoteGet(today, contract, time_zone)
        # forward = w.wsq(contract, "rt_last").Data[0][0]

        #获取波动率曲线
        volSpread = tyApi.TYMdload('VOL_BLACK_ATM_' + re.sub(r'([\d]+)', '', contract))
        #获得波动率
        vol = tyApi.TYVolSurfaceImpliedVolGet(forward, forward, today, volSpread)

        pricingAsk = float(tyApi.TYPricing(forward, forward, vol - 0.03, tau, r, 'call'))
        # print(pricingAsk)
        #出错处理
        if(math.isnan(pricingAsk)):
            pricingAsk = float(0)
        pricingBid = float(tyApi.TYPricing(forward, forward, vol + 0.03, tau, r, 'call'))
        # 出错处理
        if (math.isnan(pricingBid)):
            pricingBid = float(0)

        contractData['forward'] = round(forward, 2)
        contractData['pricingAsk'] = round(pricingAsk, 2)
        contractData['pricingBid'] = round(pricingBid, 2)
        contractData['name'] = contractList[contract]

        #组成dict
        quoteData[contract] = contractData

    #关闭wind接口
    # w.stop()

    # 压缩为JsonData
    json_data = json.dumps(quoteData, ensure_ascii=False, sort_keys=True)
    print(json_data)

    return render(request, 'quotes.html', {'series': json_data})

def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)