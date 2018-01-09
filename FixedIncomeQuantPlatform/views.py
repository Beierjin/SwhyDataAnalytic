from django.shortcuts import render
from django.db import connection
import pandas as pd
from WindPy import *

def insertData(request):
    #建立wind连接
    w.start()
    # 建立数据库连接
    cursor = connection.cursor()

    #########利率互换数据导入############
    # 从wind获取利率互换
    windData = w.edb("M1003983, M1003984, M1004093, M1004094, M1004095, M1004096, M1004097, M1004098, "
                     "M1004099, M1004122, M1004123, M1004124, M1004125, M1004126,"
                    "M1004127, M1004128, M1004129, M1004130, M1004131, M1004132", "2000-01-01", "2018-01-09", "")

    #Wind数据整理
    timeList = [time.strftime('%Y-%m-%d') for time in windData.Times]
    print(windData)
    # 包装成DataFrame
    # df = pd.DataFrame([windData.Data], columns = windData.Codes, index = windData.Times)
    df = pd.DataFrame(index = timeList)
    for i in range(len(windData.Codes)):
        df[windData.Codes[i]] = windData.Data[i]
    print(df, len(df.index), len(df.columns))
    for i in range (0, len(df.index)):
        for j in range (0, len(df.columns)):
            print(j, i)
            print(df.iloc[i, j], df.index[i], df.columns[j])
            cursor.execute("INSERT INTO BONDINFO(BONDTYPE, BONDID, BONDDURATION, BONDYTM, TIMESTAMP) VALUES(%s, %s, %s, %s, %s)",('01', df.columns[j], '', df.iloc[j, i], df.index[i]))

    #########中债国债数据导入############
    windData = w.edb("M1004136,M1004677,M1004829,M1000155,M1000156,M1000157,M1000158,M1000159,M1000160,M1000161,"
          "M1000162,M1000163,M1000164,M1000165,M1004678,M1000166,M1000167,M1000168,M1000169,M1004711,M1000170",
        "2000-01-01", "2018-01-09", "")
    # Wind数据整理
    timeList = [time.strftime('%Y-%m-%d') for time in windData.Times]
    # 包装成DataFrame
    # df = pd.DataFrame([windData.Data], columns = windData.Codes, index = windData.Times)
    df = pd.DataFrame(index=timeList)
    for i in range(len(windData.Data)):
        df[windData.Codes[i]] = windData.Data[i]
    print(df)

    #########中债国开债数据导入############
    windData = w.edb("M1004258,M1004687,M1004259,M1004260,M1004261,M1004262,M1004263,M1004264,M1004265,M1004266,"
                     "M1004267,M1004268,M1004269,M1004270,M1004688,M1004271,M1004272,M1004273,M1004274,M1004275",
                     "2000-01-01", "2018-01-09", "")
    # Wind数据整理
    timeList = [time.strftime('%Y-%m-%d') for time in windData.Times]
    # 包装成DataFrame
    # df = pd.DataFrame([windData.Data], columns = windData.Codes, index = windData.Times)
    df = pd.DataFrame(index=timeList)
    for i in range(len(windData.Data)):
        df[windData.Codes[i]] = windData.Data[i]
    print(df)

    #########中债进出口债数据导入############
    windData = w.edb("M1004138,M1004685,M1000181,M1000182,M1000183,M1000184,M1000185,M1000186,M1000187,M1000188,"
                     "M1000189,M1000190,M1000191,M1004686,M1000192,M1000193,M1000194", "2000-01-01", "2018-01-09", "")
    # Wind数据整理
    timeList = [time.strftime('%Y-%m-%d') for time in windData.Times]
    # 包装成DataFrame
    # df = pd.DataFrame([windData.Data], columns = windData.Codes, index = windData.Times)
    df = pd.DataFrame(index=timeList)
    for i in range(len(windData.Data)):
        df[windData.Codes[i]] = windData.Data[i]
    print(df)

    #########中债农发行债数据导入############
    windData = w.edb("M1007661,M1007662,M1007663,M1007664,M1007665,M1007666,M1007667,M1007668,M1007669,M1007670,"
                     "M1007671,M1007672,M1007673,M1007674,M1007675,M1007676,M1007677", "2000-01-01", "2018-01-09", "")
    # Wind数据整理
    timeList = [time.strftime('%Y-%m-%d') for time in windData.Times]
    # 包装成DataFrame
    # df = pd.DataFrame([windData.Data], columns = windData.Codes, index = windData.Times)
    df = pd.DataFrame(index=timeList)
    for i in range(len(windData.Data)):
        df[windData.Codes[i]] = windData.Data[i]
    print(df)

    w.stop()

    #插入数据
    # cursor.execute("INSERT INTO test(num, data)VALUES(%s, %s)", (1, 'aaa'))
    print(cursor)
    return render(request, 'FixedIncome.html')

# Create your views here.
