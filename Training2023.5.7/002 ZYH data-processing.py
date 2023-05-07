
# def fLoadDataMatrix(FileName):
#     f=open(FileName, encoding='utf-8')
#     reader=csv.reader(f)
#     Content=[]
#     n=0
#     m=0
#     for row in reader:
#         Content.append(row)
#         m=len(row)
#         n=n+1
    
# #    Sample Class Feature Matrix
#     Sample = []
#     for i in range(1,n):
#         Sample.append(Content[i][0])
#     print ("Samples are:",Sample,"\n")
    
#     Class = []
#     for i in range(1,n):
#         Class.append(Content[i][m-1])
#         del Content[i][m-1]
#         del Content[i][0]
#     print ("Classes are:",Class,"\n")
#     Feature = []
#     for i in range(1,m-1):
#         Feature.append(Content[0][i])
#     print ("Features are:",Feature,"\n")
    
#     del Content[0]
#     Matrix =np.mat(Content)
#     print ("Matrix is:",Matrix,"\n")
    
#     f.close()
    
#     return (Sample, Class, Feature, Matrix)

import csv
import numpy as np
import time
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
for i in range(1,n):
    days=(time.mktime(time.strptime(Content[i][0],'%Y/%m/%d'))-time.mktime(time.strptime('2018/12/31','%Y/%m/%d')))/24/60/60
    Content[i].append(days)
    Content[i].append(int(days/7))
    if objdict.get(Content[i][1], 0)==0:#如果无该键则补充
        objdict[Content[i][1]]=tot
        objredict[tot]=Content[i][1]
        objTime.append(0)
        objSum.append(0)
        objAll.append(0)
        objAppear.append(-1)
        objWeek.append(0)
        tot+=1
    objTime[objdict[Content[i][1]]]+=1
    objSum[objdict[Content[i][1]]]+=int(Content[i][2])
    objAll[objdict[Content[i][1]]]+=int(Content[i][2])*float(Content[i][3])
    if objAppear[objdict[Content[i][1]]]!=Content[i][5]:
        objAppear[objdict[Content[i][1]]]=Content[i][5]
        objWeek[objdict[Content[i][1]]]+=1

ordered_list = sorted(range(0,tot), key=lambda k:objAll[k])

f=open("dataout.csv", 'w',encoding='gbk')
f.write('物料编码,频数,数量,平均销售单价,销售总额,周频数\n')
for i in range(1,tot):
    f.write(str(objredict[ordered_list[i]]))
    f.write(",")
    f.write(str(objTime[ordered_list[i]]))
    f.write(",")
    f.write(str(objSum[ordered_list[i]]))
    f.write(",")
    f.write(str(objAll[ordered_list[i]]/objSum[ordered_list[i]]))
    f.write(",")
    f.write(str(objAll[ordered_list[i]]))
    f.write(",")
    f.write(str(objWeek[ordered_list[i]]))
    f.write("\n")
# import pandas as pd
# import numpy as np
# from scipy import stats
# import matplotlib.pyplot as plt
# f=open("ALL3.txt", encoding='utf-8')
# data=np.array((pd.Series(f.readlines()).str.split()).tolist())
# f.close()
# dataP=np.mat(data[1:,np.where(data=='POS')[1]],dtype=float)
# dataN=np.mat(data[1:,np.where(data=='NEG')[1]],dtype=float)
# dataP=dataP.T
# dataN=dataN.T
# (Tvalue,Pvalue) = stats.ttest_ind(dataP, dataN)

# data_array=np.vstack((data[1:,0],Tvalue,Pvalue)).T

# goal=[1,9,1000,10000]
# #plt.figure(figsize=(12, 10))
# for i in range(4):
#     dataAP=np.mat(data[ordered_list[goal[i]]+1,np.where(data=='POS')[1]],dtype=float)
#     dataBP=np.mat(data[ordered_list[goal[i]+1]+1,np.where(data=='POS')[1]],dtype=float)
    
#     dataAN=np.mat(data[ordered_list[goal[i]]+1,np.where(data=='NEG')[1]],dtype=float)
#     dataBN=np.mat(data[ordered_list[goal[i]+1]+1,np.where(data=='NEG')[1]],dtype=float)
    
#     #plt.subplot(int(22*10+i+1))
#     #plt.scatter(dataAP[0].tolist(), dataBP[0].tolist(),color='red')
#     #plt.scatter(dataAN[0].tolist(), dataBN[0].tolist(),color='blue')
    
# #plt.show()