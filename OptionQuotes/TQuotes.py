from django.shortcuts import render

import time, re, json
from . import TYApi
# from WindPy import w

def GetTQuotesData(request, instrument):

    # 获得当前时间
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    time_zone = 'Asia/Shanghai'

    # 定价参数
    tau = 1  # 量
    r = 0.015  # 无风险利率

    # 初始化同余API
    tyApi = TYApi.TYApi()

    # 开启wind接口
    # w.start()
    #获取现价
    # forward = w.wsq(instrument, "rt_last").Data[0][0]
    forward = tyApi.TYMktQuoteGet(today, instrument, time_zone)
    # 关闭wind接口
    # w.stop()

    # 获取波动率曲线
    volSpread = tyApi.TYMdload('VOL_BLACK_ATM_' + re.sub(r'([\d]+)', '', instrument))
    # 获得波动率
    vol = tyApi.TYVolSurfaceImpliedVolGet(forward, forward, today, volSpread)

    #存储期权数据
    contractData = {}

    forwardList = getForwardList(forward)
    print(forwardList)

    for price in forwardList:
        TQuoteData = {}
        pricingCallAsk = tyApi.TYPricing(forward, price, vol - 0.03, tau, r, 'call')
        pricingCallBid = tyApi.TYPricing(forward, price, vol + 0.03, tau, r, 'call')
        pricingPutAsk = tyApi.TYPricing(forward, price, vol - 0.03, tau, r, 'put')
        pricingPutBid = tyApi.TYPricing(forward, price, vol + 0.03, tau, r, 'put')
        TQuoteData['pricingCallAsk'] = round(pricingCallAsk,2)
        TQuoteData['pricingCallBid'] = round(pricingCallBid,2)
        TQuoteData['pricingPutAsk'] = round(pricingPutAsk,2)
        TQuoteData['pricingPutBid'] = round(pricingPutBid,2)
        contractData[price] = TQuoteData

    # 压缩为JsonData
    json_data = json.dumps(contractData, ensure_ascii=False, sort_keys=True)
    print(json_data)

    return render(request, 'TQuotes.html', {'series': json_data})

'''
x<500 变动范围5, 500<x<2000 变动范围10, 2000<x<6000 变动范围50, 6000<x 变动范围100
'''
def getForwardList(forward):
    forwardList = []
    for i in range(0, 6):
        if(forward < 500):
            forwardList.append(round(forward, -1) - (i * 5))
        elif(forward < 2000 and forward >= 500):
            forwardList.append(round(forward, -1) - (i * 10))
        elif (forward < 6000 and forward >= 2000):
            forwardList.append(round(forward, -1) - (i * 50))
        elif (forward >= 6000):
            forwardList.append(round(forward, -1) - (i * 100))

    for i in range(1, 6):
        if(forward < 500):
            forwardList.append(round(forward, -1) + (i * 5))
        elif(forward < 2000 and forward >= 500):
            forwardList.append(round(forward, -1) + (i * 10))
        elif (forward < 6000 and forward >= 2000):
            forwardList.append(round(forward, -1) + (i * 50))
        elif (forward >= 6000):
            forwardList.append(round(forward, -1) + (i * 100))

    return forwardList

