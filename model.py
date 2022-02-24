import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

print("demo")
# print("----------------------------------------------------------------------------------PHASE 1 VFMS--------------------------------------------------------------------")
df1 = pd.read_csv("phase_conv1.csv")
x1=df1.iloc[:,0:4]
y1=df1.iloc[:,4:6]
model1 = LinearRegression()
model1.fit(x1.values,y1)
# a=float(input("-----------------------------------------------------------------------------Nitawade------------------------------------------------------\nEnter Water Level (m) :",))
# b=float(input("Enter Water Flow (cusecs) :"))
# c=float(input("-----------------------------------------------------------------------------Balinga-------------------------------------------------------\nEnter Water Level (m) :",))
# d=float(input("Enter Water Flow (cusecs) :"))

# print(f'\n--------------------------------------------------------------------------Shingnapur--------------------------------------------------------\nPredicted Water level (m) : {y_test1[0][0]}\nPredicted Water flow (cusecs) : {y_test1[0][1]}\n')
x2=df1.iloc[:,0:6]
y2=df1.iloc[:,6:8]
model2 = LinearRegression()
model2.fit(x2.values,y2)

# print(f'-----------------------------------------------------------------------Rajaram Bandhara---------------------------------------------------\nPredicted Water level (m) : {y_test2[0][0]}\nPredicted Water flow (cusecs) : {y_test2[0][1]}\n')
x3=df1.iloc[:,0:8]
y3=df1.iloc[:,8:10]
model3 = LinearRegression()
model3.fit(x3.values,y3)

# print(f'-------------------------------------------------------------------------Ichalkaranji-----------------------------------------------------\nPredicted Water level (m) : {y_test3[0][0]}\nPredicted Water flow (cusecs) : {y_test3[0][1]}\n')


def predict_wf_wl(a, b, c, d):
    x_test1=[[a,b,c,d]]
    y_test1=model1.predict(x_test1)
    x_test2=[[a,b,c,d,y_test1[0][0],y_test1[0][1]]]
    y_test2=model2.predict(x_test2)
    x_test3=[[a,b,c,d,y_test1[0][0],y_test1[0][1],y_test2[0][0],y_test2[0][1]]]
    y_test3=model3.predict(x_test3)
    output = {
        "shingnapur_wl": "{:.2f}".format(y_test1[0][0]),
        "shingnapur_wf": "{:.2f}".format(y_test1[0][1]),
        "rajaram_bandhara_wl": "{:.2f}".format(y_test2[0][0]),
        "rajaram_bandhara_wf": "{:.2f}".format(y_test2[0][1]),
        "ichalkaranji_wl": "{:.2f}".format(y_test3[0][0]),
        "ichalkaranji_wf": "{:.2f}".format(y_test3[0][1])
    }

    return output
# print(predict_wf_wl(543.0796848, 24857, 541.3, 25696))
