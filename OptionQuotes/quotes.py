from django.shortcuts import render

import re, time, os, json
import pandas as pd
from WindPy import w

from . import TYApi

#读取期货合约
baseDir = os.path.dirname(os.path.abspath(__name__))
contractListFileDir = baseDir + '\\files\\BasicInfo\\contractList.xlsx'
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
    w.start()

    #获取报价
    for contract in contractList.keys():

        contractData = {}

        #获取期货现价
        # forward = tyApi.TYMktQuoteGet(today, contract, time_zone)
        forward = w.wsq(contract, "rt_last").Data[0][0]

        #获取波动率曲线
        volSpread = tyApi.TYMdload('VOL_BLACK_ATM_' + re.sub(r'([\d]+)', '', contract))
        #获得波动率
        vol = tyApi.TYVolSurfaceImpliedVolGet(forward, forward, today, volSpread)

        pricingAsk = tyApi.TYPricing(forward, forward, vol - 0.03, tau, r, 'call')
        pricingBid = tyApi.TYPricing(forward, forward, vol + 0.03, tau, r, 'put')

        contractData['forward'] = forward
        contractData['pricingAsk'] = round(pricingAsk,2)
        contractData['pricingBid'] = round(pricingBid, 2)
        contractData['name'] = contractList[contract]

        #组成dict
        quoteData[contract] = contractData

    #关闭wind接口
    w.stop()

    # 压缩为JsonData
    json_data = json.dumps(quoteData, ensure_ascii=False)
    print(json_data)

    return render(request, 'quotes.html', {'series': json_data})