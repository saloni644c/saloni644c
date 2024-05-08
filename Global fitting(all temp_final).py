import pandas as pd
from matplotlib import pyplot as plt
from scipy import optimize
from scipy.optimize import leastsq
import numpy as np

#functions define


def sumg(wn, pars, nt, ng):
    gaus = 0
    gauss= []
    for j in range(0,nt ):
        for i in range(0, ng):
            gaus = gaus +  pars[3*j+3+i]* np.exp(-((wn -pars[0+i])**2 / (pars[3*j+54+i]**2)))
        gauss.append(gaus)
    return gauss

"""
def sum_gaus(wn, pars, nt, ng ):
    temp = sumg(wn, pars, nt,ng)
    sum = []
    for i in range(nt):
        for j in range(len(wn)):
            sum.append(temp[i][j])
    
    return sum

def sum_gaus(wn, pars, nt, ng):
    tem = 0
    for i in range(17):
        tem = tem + sumg(wn, pars, nt, ng)[i]
    return tem

def sum_gaus(wn, pars, nt, ng):
    out = []
    for i in range(0,8 ):
        temp = np.concatenate((sumg(wn, pars, nt, ng)[2*i], sumg(wn, pars, nt, ng)[2*i+1],))
        
    return temp
"""       

def sum_gauss(wn, pars, nt, ng):
    temp1 = sumg(wn, pars, nt, ng)[0][0]    
 
    for i in range(1,17):
        temp1 = np.concatenate((temp1, sumg(wn, pars, nt, ng)[i][0]))
              

    return temp1

    

def sum_gaus(wn, pars, nt, ng):
    temp = sum_gauss(wn, pars, nt, ng)
    tempf = temp.ravel()
    return tempf

def residual(pars, wn, em_c, flag1, P0, nt, ng):
    yf = em_c - sum_gaus(wn, pars, nt, ng)
    for j in range(0, (len(pars)-1)):
            if flag1[j] == 0:
                   pars[j] = P0[j]
    return yf
    

    
#data reading
file = "C:\\Users\\SALONI\\Desktop\\lineshapes_0.csv"
col_list = [ "0","15","30", "60", "90", "120", "150", "170", "190", "210", "230", "240", "250", "260", "270", "280", "290", "300"]
df = pd.read_csv(file, usecols= col_list)
wn= [df['0']]
em1= np.array(df['15'])
em2= np.array(df['30'])
em3= np.array(df['60'])
em4= np.array(df['90'])
em5= np.array(df['120'])
em6= np.array(df['150'])
em7 = np.array(df['170'])
em8= np.array(df['190'])
em9= np.array(df['210'])
em10= np.array(df['230'])
em11= np.array(df['240'])
em12= np.array(df['250'])
em13= np.array(df['260'])
em14= np.array(df['270'])
em15= np.array(df['280'])
em16= np.array(df['290'])
em17= np.array(df['300'])


  
wn_f = np.concatenate((wn, wn, wn, wn, wn, wn, wn, wn, wn, wn, wn, wn, wn, wn, wn, wn, wn))
wn_c = wn_f.ravel()
print(wn_c)
em_c = np.concatenate([em1,em2, em3, em4, em5, em6, em7, em8, em9, em10, em11, em12, em13, em14, em15, em16, em17])
print(len(em_c))

ng = 3       # number of gaussian
nt = 17      # number of temperatures for plot

pars_1 = [13500, 15000, 16000] # peak position
pars_2 =  [0.570313195, 0.646066972, 0.29301325,0.570313195, 0.646066972, 0.29301325,0.570313195, 0.646066972, 0.29301325,0.570313195, 0.646066972, 0.29301325,0.763363344,0.722850301, 0.272206975, 0.733164565 ,0.852261115,0.193091660, 0.707277732, 0.866045285 ,0.172154109, 0.80008273, 0.820704438, 0.265499239, 0.517089875 ,0.863242098,0.266470786,0.497105554 ,0.948843067,0.312502178]
#intensity of 1st , 2nd curve so on
pars_3 =[ 936.588717, 946.323134, 4032.98627,936.588717, 946.323134, 4032.98627,936.588717, 946.323134, 4032.98627,936.588717, 946.323134, 4032.98627,1025.26943, 929.854734, 1452.21669,1020.63518, 1042.06609, 740.950131, 990.205571, 918.284435, 762.068959, 785.160514, 1188.34674, 1572.40802, 691.791019, 1150.09596,1082.05519, 691.791019, 1150.09596,1082.0551]
# width of of 1st , 2nd curve so on
#from 240K
pars_22 =[ 0.527906029, 0.811470381, 0.377241631, 0.4870259, 0.863915763, 0.410576665, 0.647193850, 0.796595901, 0.498657093, 0.617536618, 0.88091848, 0.496889875, 0.582455334, 0.836246364, 0.570050792, 0.392560402, 0.841155276, 0.622406519, 0.465944185, 0.702506849, 0.6361946]
pars_33 =[744.740055, 1051.24412, 1379.71753, 649.579888, 1054.57290, 1123.43924, 864.06417, 810.851094, 998.738448, 765.872217, 840.013968, 825.099071, 712.762897, 809.000799, 978.269822, 767.763797, 832.281867, 886.609972, 531.777472, 947.097990, 1319.03045]

pars = np.concatenate([pars_1, pars_2, pars_22, pars_3, pars_33])
P0 = pars.copy()


flag1 =[]
flag2 =[]
flag3 =[]

choice = [0,1,0]
def flag(choice):
    
    for i in range(0, (len(pars)-1)):
        if i<3:
            flag1.append(1)
        
        else:
            flag1.append(0)
            
    for i in range(0, (len(pars)-1)):
        if i>=3:
            flag2.append(1)
        
        else:
            flag2.append(0)
      
    for i in range(0, (len(pars)-1)):
            flag3.append(1)
            
    total = ([flag1,flag2,flag3])
    
    for i in range(3):
        if choice[i] == 0:
            for j in range(0, (len(pars)-1)):
                total[i][j] = 0
    return total
Flg = flag(choice)

#print(sum_gaus(wn, pars, nt, ng))
#print(len(wn_c))
#plt.plot(wn_c, sum_gaus(wn, pars, nt, ng))
#plt.show()

    
#three stage optimization
popt1,pcov1, A, B, success = leastsq(residual, pars, args = (wn, em_c, Flg[0], P0, nt, ng), ftol = 1e-15, xtol=1e-15, maxfev =100000, full_output =True)

if success > 4:
   print('Message from leastsq', B)
         
Chiminopt1 = residual(popt1,wn, em_c, Flg[0], P0, nt, ng)
Chisq1 = 0
    
for i in range (len(Chiminopt1)):
    Chisq1 = Chisq1 + pow(float(Chiminopt1[i]),2)
dof1 = len(wn) - len(pars) 
redchisq1 = Chisq1/ dof1

#--------------------------------------------------------------------------------------
pars1 = np.concatenate([popt1[0:3], pars[3:16]])

popt2,pcov2, A, B, success = leastsq(residual, pars1, args = (wn, em_c, Flg[1], P0, nt, ng), ftol = 1e-15, xtol=1e-15, maxfev =100000, full_output =True)

if success > 4:
   print('Message from leastsq', B)

   
Chiminopt2 = residual(popt2,wn, em_c, Flg[1], P0, nt, ng)
Chisq2 = 0
    
for i in range (len(Chiminopt2)):
    Chisq2 = Chisq2 + pow(float(Chiminopt2[i]),2)
dof2 = len(wn) - len(pars) 
redchisq2 = Chisq2/ dof2


#3rd stage---------------------------------------------------------------------------
pars2 = np.concatenate([popt1[0:3], popt2[3:16]])

popt3,pcov3, A, B, success = leastsq(residual, pars2, args = (wn, em_c, Flg[2], P0,nt, ng), ftol = 1e-15, xtol=1e-15, maxfev =100000, full_output =True)

if success > 4:
   print('Message from leastsq', B)
   
Chiminopt3 = residual(popt3,wn, em_c, Flg[2], P0,nt, ng)
Chisq3 = 0
    
for i in range (len(Chiminopt3)):
    Chisq2 = Chisq3 + pow(float(Chiminopt3[i]),2)
dof3 = len(wn) - len(pars) 
redchisq3 = Chisq2/ dof3
#=======================================================
#creating file and entering datas

import sys
e_dataframe = pd.DataFrame({'wnm':wn, 'y1':em1, 'fitted y1':sum_gaussian(wn, popt1,nt, ng)[0], 'y2':em2, 'fittedy2':sum_gaussian(wn, popt3, gauss,nt, ng)[1] })  

sys.stdout=open("output_1.txt","w")
print (e_dataframe)
sys.stdout.close()

#output file2

sys.stdout = open("output_2.txt", "w")
print('Stage1 Optimization', 'popt1_globalP', popt1[0:3])
print('rd1', redchisq1)
print('dof1', dof1)
print('Stage2 Optimization', 'popt2_inn_30k-', popt2[4:7], 'popt2_inten_190k', popt2[7:10], 'popt2_width_30k', popt2[10:13],'popt2_width_190k', popt2[13:16])
print('rd2', redchisq2)
print('dof1', dof1)
print('Stage3 Optimization', 'popt3_globalP', popt3[0:3], 'popt3_inn_30k-', popt3[4:7], 'popt3_inten_190k', popt3[7:10], 'popt3_width_30k', popt3[10:13],'popt3_width_190k', popt3[13:16])
print('rd3', redchisq3)
print('dof1', dof1)


sys.stdout.close()


plt.plot(wn, em1)

