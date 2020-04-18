'''Having the Market portfolio monthly return and the 10 industry portofolio monthly return
1. calculate excess reutrn for market and 10 industry portfolios
2. use montly excess return of all portfolios to regress on market portfolio monthly excess return, get 10 beta and 10 alpha
3. put 10 beta and 10 alpha in one DataFrame and export to excel
4. calculate mean monthly return for 10 portfolios and get 10 mean，concat market mean
5. use 11 mean monthly return to regress on 11 beta to get the slope and intercept for SML
6. generate beta from 0-2 and use the intercept and beta to calculate r
7. put beta and r into one DataFrame and plot the SML
8. put 11 beta and 11 mean into one DataFrame and plot the positions of these 11 portfolios '''

import pandas as pd 
import numpy as np 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data1=pd.read_excel('Industry_Portfolios.xlsx', header=0, index_col=0)
data2=pd.read_excel('Market_portfolio.xlsx',header=0, index_col=0)

'''LinearRegression().fit() the first parameter must be a DataFrame，or numpy 2darray, can't be Seriesor 1darray，the second parameter can be 1d or 2d
if the second parameter is 2D，return coef is 2D，intercept is 1D；if the second parameter is 1D，return coef is 1D，intercept is scalar'''
#calculate excess reutrn for market and 10 industry portfolios
rf=0.13
excess_return=data1-rf
excess_return_m=data2-rf

#use montly excess return of all portfolios to regress on market portfolio monthly excess return,
#get 10 beta and 10 alpha,put 10 beta and 10 alpha in one DataFrame and export to excel
Beta=pd.DataFrame([LinearRegression().fit(excess_return_m,excess_return.iloc[:,[i]]).coef_[0,0] for i in 
range(len(excess_return.columns))],index=excess_return.columns,columns=['Beta'])
Alpha=pd.DataFrame([LinearRegression().fit(excess_return_m,excess_return.iloc[:,[i]]).intercept_[0] for i in 
range(len(excess_return.columns))],index=excess_return.columns,columns=['Alpha'])
table=pd.concat([Beta,Alpha],axis=1)
print(table)
table.to_excel(excel_writer='Beta_Alpha.xlsx')

#calculate mean monthly return for 10 portfolios and get 10 mean, concat market mean
#use 11 mean monthly return to regress on 11 beta to get the slope and intercept for SML
Mean=pd.DataFrame(data1.mean(),columns=['Mean'])
Mean_m=pd.DataFrame(data2.mean(),columns=['Mean'])
Mean=pd.concat([Mean,Mean_m],axis=0) #add market Mean
Beta_m=pd.DataFrame([[1]],columns=['Beta'],index=['Market'])
Beta=pd.concat([Beta,Beta_m],axis=0) #add matket Beta
slope=LinearRegression().fit(Beta,Mean).coef_[0][0]
intercept=LinearRegression().fit(Beta,Mean).intercept_[0]
print('slope',slope,'intercept',intercept)

#generate beta from 0-2 and use the intercept and beta to calculate R
#put beta and r into one DataFrame and plot the SML
Beta_all=np.linspace(0,2,100)
R=intercept+slope*Beta_all
SML=pd.DataFrame(zip(Beta_all, R),columns=['Beta_all','R'])
fig1,ax1=plt.subplots()
SML.plot(x='Beta_all',y='R',ax=ax1,label='SML',style=['k-'])

#put 11 beta and 11 mean into one DataFrame and plot the positions of these 11 portfolios
Port=pd.concat((Beta,Mean),axis=1)
Port.plot(x='Beta',y='Mean',ax=ax1, label='Portfolios',style=['bo'])
plt.title('Security Market Line')
plt.xlabel('Beta')
plt.ylabel('R(%)')
plt.savefig('Security Market Line.jpg',dpi=300)
plt.show()

#Econoimic significance
'''Intercept:
For individual assets or passive managed portfolios, Alpha represents pricing error relative to CAPM. 
When the alpha is positive,the mean return of the respective portfolio lies above the SML and is underpriced and conversely,
when alpha is negative, it basically means that the mean return of the portfolio lies below the SML 
and is overpriced. In an efficient market, alpha will disappear quickly because all the investors will
long the portfolio with positive alpha and short the portfolio with negative alpha, 
driving the price of the portfolio back to SML. For actively managed portfolios, it represents 
abnormal mean return after adjusting for exposure to market risk, due to fund manager’s ability to 
identify underpriced or overpriced assets.'''

'''Slope:
Beta refers to the degree of the portfolios’ exposure to the market risk. A positive beta implies a 
positive correlation where the portfolio moves in the same direction as the market portfolio. 
A negative beta implies a negative correlation where portfolio moves in opposite direction as 
the market portfolio. The bigger the beta, the bigger the portfolio’s exposure to the market risk.
For example, If a portfolio’s beta is 1.5, it means that for 1% movement of the market portfolio, 
that particular portfolio’s movement is 1.5%. '''

'''SML:
SML is a graphical representation of the capital asset pricing model (CAPM), which shows different 
levels of systematic or market risk plotted against the expected return of the entire market at a 
given point in time. All the appropriate priced portfolios should fall on the SML. Security that 
lies above SML is underpriced and security that lies below SML is overpriced. Thus SML can be used 
by investors to evaluate a security or portfolio in terms of whether it offers a favorable expected 
return against its level of risk. Investors should long the security that lies above the SML and short 
the secuities that lies below the SML, which will drive the price of securities back to the SML.'''







