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

chosenObject=['6004020918','6004020900','6004020905','6004021055','6004020921','6004010256']
for kth in range(0,6):#6
    objCurrent=chosenObject[kth]
    dictCurrent=objdict[objCurrent]
    x=[0]
    y=[0]
    Y1=[0]
    Y2=[0]
    Y3=[0]
    alpha=0.3
    for i in range(1,178):
        x.append(i)
        y.append(y[i-1]+objTot[dictCurrent][i])
        Y1.append(float(objTot[dictCurrent][i]))
    S1=[Y1[1]]
    resNominator=0
    resDenominator=0
    for i in range(1,178):
        S1.append(float(alpha*Y1[i]+(1-alpha)*S1[i-1]))
    S2=[S1[1]]
    for i in range(1,178):
        S2.append(float(alpha*S1[i]+(1-alpha)*S2[i-1]))
    S3=[S2[1]]
    for i in range(1,178):
        S3.append(float(alpha*S2[i]+(1-alpha)*S3[i-1]))
    S=[Y1[1]]
    
    que=[]
    have=0.0
    serviceLevel=0
    serviceTot=0
    serviceNominator=0
    serviceDenominator=0
    SS=0#服务水平0.85   sqrt(1) 标准差
    for i in range(1,178):
        A=3.0*S1[i]-3.0*S2[i]+S3[i]
        B=alpha/(2.0*(1.0-alpha)*(1.0-alpha))*((6.0-5.0*alpha)*S1[i]-2.0*(5.0-4.0*alpha)*S2[i]+(4.0-3.0*alpha)*S3[i])
        C=alpha*alpha/(2.0*(1.0-alpha)*(1.0-alpha))*(S1[i]-2.0*S2[i]+S3[i])
        
        S.append(float(A+B+C))
        if S[i]<0:
            S[i]=0
        if i>=101-1 and i<=177-1:
            resDenominator+=1
            resNominator+=(Y1[i+1]-S[i])*(Y1[i+1]-S[i])
            que.append((Y1[i+1]-S[i])*(Y1[i+1]-S[i]))
            avg=0
            for j in range(1,i):
                avg+=Y1[j]
            avg/=(i-1)
            SS=0
            for j in range(1,i):
                SS+=(avg-Y1[i])*(avg-Y1[i])
            SS/=(i-1)
            SS=math.sqrt(SS)*0.85
            #SS=0
            if have<S[i]+SS:
                have=math.ceil(S[i])+SS
            
            if Y1[i+1]==0:
                a=1
                serviceLevel+=1
                serviceTot+=1
            elif have>Y1[i+1]:
                serviceLevel+=1
                
                have-=Y1[i+1]
                serviceTot+=1
            else:
                serviceLevel+=1.0*have/Y1[i+1]
                have=0
                serviceTot+=1
            Y3.append(have)
        else:
            Y3.append(0)
    resNominator=math.sqrt(resNominator/resDenominator)
    
    for i in range(0,177):
        Y2.append(S[i])
        
        
    # fig, ax = plt.subplots(figsize=(6, 6))
    # plt.xlabel('Information about '+objCurrent)
    # plt.ylabel('Accumulated quantity')
    # ax.plot(x, y)
    # plt.show()

    # fig, ax = plt.subplots(figsize=(6, 6))
    # plt.xlabel('Information about '+objCurrent)
    # plt.ylabel('Quantity For Every Week')
    # ax.plot(x, Y1,color='blue')
    # ax.plot(x, Y3,color='red')
    # plt.show()
    # print(resNominator)
    print(serviceLevel/serviceTot)
