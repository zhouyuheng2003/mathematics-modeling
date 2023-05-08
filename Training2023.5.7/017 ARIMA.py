import csv
import math
import numpy as np
import time
import matplotlib.pyplot as plt
f=open("data.csv", encoding='utf-8')
reader=csv.reader(f)
Content=[]
n=0
for row in reader:
    Content.append(row)
    n=n+1
start_time = '2019/12/31'
objdict={}
objredict={}
tot=1
objTime=[0]#频数
objSum=[0]#数量
objAll=[0]#总销售额
objAppear=[0]
objWeek=[0]#频数

objTot=[[]]


for i in range(1,n):
    days=(time.mktime(time.strptime(Content[i][0],'%Y/%m/%d'))-time.mktime(time.strptime('2018/12/31','%Y/%m/%d')))/24/60/60
    Content[i].append(days)
    Content[i].append(int(days/7)+1)
    if objdict.get(Content[i][1], 0)==0:#如果无该键则补充
        objdict[Content[i][1]]=tot
        objredict[tot]=Content[i][1]
        objTime.append(0)
        objSum.append(0)
        objAll.append(0)
        objAppear.append(-1)
        objWeek.append(0)
        objTot.append([])
        for j in range(0,178):
            objTot[tot].append(0)
        tot+=1
    objTime[objdict[Content[i][1]]]+=1
    objSum[objdict[Content[i][1]]]+=int(Content[i][2])
    objAll[objdict[Content[i][1]]]+=int(Content[i][2])*float(Content[i][3])
    if objAppear[objdict[Content[i][1]]]!=Content[i][5]:
        objAppear[objdict[Content[i][1]]]=Content[i][5]
        objWeek[objdict[Content[i][1]]]+=1
    objTot[objdict[Content[i][1]]][Content[i][5]]+=int(Content[i][2])#统计每个物品各周的数量

# ordered_list = sorted(range(0,tot), key=lambda k:objAll[k])
# f=open("dataout.csv", 'w',encoding='gbk')
# f.write('物料编码,频数,数量,平均销售单价,销售总额,周频数\n')
# for i in range(1,tot):
#     f.write(str(objredict[ordered_list[i]]))
#     f.write(",")
#     f.write(str(objTime[ordered_list[i]]))
#     f.write(",")
#     f.write(str(objSum[ordered_list[i]]))
#     f.write(",")
#     f.write(str(objAll[ordered_list[i]]/objSum[ordered_list[i]]))
#     f.write(",")
#     f.write(str(objAll[ordered_list[i]]))
#     f.write(",")
#     f.write(str(objWeek[ordered_list[i]]))
#     f.write("\n")


import warnings
warnings.filterwarnings("ignore")
from statsmodels.tsa.arima.model import ARIMA
chosenObject=['6004020918','6004010372','6004020900','6004021155','6004010174','6004021055','6004020768']
for kth in range(0,7):#6
    objCurrent=chosenObject[kth]
    dictCurrent=objdict[objCurrent]
    x=[0]
    y=[0]
    Y1=[0]
    Y2=[0]
    alpha=0.3
    for i in range(1,178):
        x.append(i)
        y.append(y[i-1]+objTot[dictCurrent][i])
        Y1.append(objTot[dictCurrent][i])
    S=[0,0]
    resNominator=0
    resDenominator=0
    data=[0]
    for i in range(1,178):
        data.append(Y1[i])
        model = ARIMA(data, order=(0, 0, 2))  # 替换p、d、q为合适的阶数
        model_fit = model.fit()
        
        # 进行预测
        forecast = model_fit.forecast(steps=1)  # 替换steps为您希望预测的步数
        S.append(forecast[0])
    for i in range(1,178):
        if S[i]<0:
            S[i]=0
        if i>=101-1 and i<=177-1:
            resDenominator+=1
            resNominator+=(Y1[i+1]-S[i])*(Y1[i+1]-S[i])
    resNominator=math.sqrt(resNominator/resDenominator)
    
    for i in range(0,177):
        Y2.append(S[i])
        

    # fig, ax = plt.subplots(figsize=(6, 6))
    # plt.xlabel('Information about '+objCurrent)
    # plt.ylabel('Quantity For Every Week')
    # ax.plot(x, Y1,color='blue')
    # ax.plot(x, Y2,color='red')
    # plt.show()
    print(resNominator)

