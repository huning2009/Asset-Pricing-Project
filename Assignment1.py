'''Having the return for industry portfolios
1. calculate R and V, define e
2. using R, V and e to calculate alpha, zeta and delta
3. generate Rp, use alpha ,zeta and delta to calculate Sigma
4. put Sigma and Rp in one DataFrame, plot the minimum variance frontier
'''
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#Calculate mean, cov, std
data=pd.read_excel('Industry_Portfolios.xlsx',header=0,index_col=0)
mean=data.mean()
cov=data.cov()
std=data.std()

#Put mean and std in one DataFrame and export to excel
mean_std=pd.DataFrame(mean,columns=['mean'])
mean_std['std']=std
mean_std.to_excel(excel_writer='mean_std.xlsx')
cov.to_excel(excel_writer='cov.xlsx')

#define R, V and e
R=np.array(mean)
RT=R
V=np.array(cov)
VI=np.linalg.inv(V)
e=np.ones(len(R))
eT=e

#calculte alpha,zeta and delta
alpha=RT@VI@e 
zeta=RT@VI@R
delta=eT@VI@e#These three are all scalar

#plot minimum-variance frontier(without Riskless asset)
Rp1=np.linspace(0,2,100)
Varp1=(1/delta)+(delta/(zeta*delta-alpha**2))*((Rp1-alpha/delta)**2)
Sigma1=np.sqrt(Varp1)
front1=pd.DataFrame(zip(Rp1,Sigma1),columns=['Rp1','Sigma1'])
fig1,ax1=plt.subplots()
front1.plot(x='Sigma1',y='Rp1',ax=ax1,label='fontier without riskless asset')

#plot efficient frontier(with Riskless asset)
rf=0.13
Rp2=np.linspace(0.13,2,100)
Varp2=((Rp2-rf)**2)/(zeta-2*alpha*rf+delta*rf**2)
Sigma2=np.sqrt(Varp2)
front2=pd.DataFrame(zip(Rp2,Sigma2),columns=['Rp2','Sigma2'])
front2.plot(x='Sigma2',y='Rp2',ax=ax1,label='frontier with riskless asset')

#plot tangency portfolio
Rtg=(alpha*rf-zeta)/(delta*rf-alpha)
Vartg=((Rtg-rf)**2)/(zeta-2*alpha*rf+delta*rf**2)
Sigmatg=np.sqrt(Vartg)
print('Rtg',Rtg,'Sigmatg',Sigmatg)
Ptg=pd.DataFrame([[Rtg,Sigmatg]],columns=['Rtg','Sigmatg']) #Both Rtg and Sigmatg are scalar
Ptg.plot(x='Sigmatg',y='Rtg',ax=ax1,label='tangency portfolio',kind='scatter')

#put label and title, save fig
plt.xlabel('Sigma(%)')
plt.ylabel('Mean Return(%)')
plt.title('Minimum-Variance and Efficient Frontiers')
plt.savefig('Minimum-Variance and Efficient Frontiers.jpg',dpi=300)
plt.show()

#calculate weights of tangency portfolio
a=(zeta*VI@e-alpha*VI@R)/(zeta*delta-alpha**2)
b=(delta*VI@R-alpha*VI@e)/(zeta*delta-alpha**2)
Wo=a+b*Rtg
Wo=pd.DataFrame(Wo,index=data.columns,columns=['weights'])
print(Wo)
Wo.to_excel(excel_writer='weights.xlsx')

#calculate risk premium for tangency portfolio
premium=Rtg-rf
print('premium',premium)

#calculate sharpe ratio for tangency portfolio
Sharpe=premium/Sigmatg
print('Sharpe',Sharpe)

#Economic Significance
'''Minimum_variance frontier
Minimum-variance frontier consists of portfolios with least risk for specified mean return, so no portfolios exist to the left of this frontier.'''

'''Efficient frontier
Efficient frontier consists of portfolios with highest mean return for specified level of risk, so risk-averse investor must invest in portfolio on this frontier in order to maximise expected utility (of wealth).'''

'''Tangency portfolio
Tangency portfolio has the highest Sharpe ratio out of all portfolios.'''













