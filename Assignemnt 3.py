'''Having the risk factors that contains monthly observations of the 
risk-free rate and the three Fama–French risk factors
1. calculate the performance matrics:
Sharpe ratio
Sortino ratio (with risk-free rate as target)
Jensen's alpha
Three-factor alpha

'''

import pandas as pd 
import numpy as np 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from scipy.optimize import minimize

data1=pd.read_excel('Industry_Portfolios.xlsx', header=0, index_col=0)
data2=pd.read_excel('Market_portfolio.xlsx',header=0, index_col=0)
data3=pd.read_excel('Risk_Factors.xlsx',header=0, index_col=0)
excess_return=data1-np.tile(data3[['Rf']].values,len(data1.columns)) #2D array tiles，if it's 1D,need use reshape and turn to 2D
print(excess_return.head())

#sharpe ratio
mean=excess_return.mean()
std=excess_return.std()
sharpe=mean/std
sharpe=pd.DataFrame(sharpe,columns=['sharpe'])
print(sharpe)
sharpe.plot(kind='bar')
plt.title('Sharpe ratio')
plt.savefig('Sharpe ratio.jpg',dpi=300)
plt.show()

#sortino ratio
sv=((np.minimum(excess_return,0))**2).mean()#below-target semi_variance
sortino=mean/np.sqrt(sv)
sortino=pd.DataFrame(sortino,columns=['sortino'])
print(sortino)
sortino.plot(kind='bar')
plt.title('Sortino ratio')
plt.savefig('Sortino ratio.jpg',dpi=300)
plt.show()

#jensen'alpha
excess_return_m=data3[['Rm-Rf']]
mean_m=excess_return_m.mean().values
beta1=pd.DataFrame([LinearRegression().fit(excess_return_m,excess_return.iloc[:,[i]]).coef_[0,0] for i in 
range(len(excess_return.columns))],index=excess_return.columns,columns=['Beta']) 
alpha1=pd.DataFrame([LinearRegression().fit(excess_return_m,excess_return.iloc[:,[i]]).intercept_[0] for i in 
range(len(excess_return.columns))],index=excess_return.columns,columns=['Alpha'])
print(alpha1)
alpha1.plot(kind='bar')
plt.title("Jensen alpha")
plt.savefig('Jensen alpha.jpg',dpi=300)
plt.show()

#three factor alpha
three_factor=data3.iloc[:,1:]
beta2=pd.DataFrame([LinearRegression().fit(three_factor,excess_return.iloc[:,[i]]).coef_[0] for i in range(len(excess_return.columns))],index=excess_return.columns,columns=three_factor.columns)
#The regression model is y=X*Beta+e,X is a matrix, Beta is also a matrix
alpha2=pd.DataFrame([LinearRegression().fit(three_factor,excess_return.iloc[:,[i]]).intercept_[0] for i in range(len(excess_return.columns))],index=excess_return.columns,columns=['Three factor alpha'])
print(alpha2)
alpha2.plot(kind='bar')
plt.title('Three factor alpha')
plt.savefig('Three factor alpha.jpg',dpi=300)
plt.show()

#performance matric
performance=pd.concat([sharpe,sortino,alpha1,alpha2],axis=1)
print(performance)
performance.to_excel(excel_writer='Performance Matrix.xlsx')

'''2. Use the monthly returns of the ten industry portfolios to generate the
 minimum-variance frontier without short sales, using Monte Carlo simulation. 

Without short sales, portfolio weights will be limited to the range [0, 1]. 
Randomly draw each element of w, the vector of portfolio weights, from the uniform 
distribution in the range [0, 1]. Divide w by the sum of the portfolio weights, to 
ensure that the portfolio weights sum to one.

Use the normalized w to calculate the mean return and standard deviation of return.
Repeat this process until you have at least 100,000 obervations. Plot the points with 
mean return on the vertical axis and standard deviation of return on the horizontal axis 
to show the minimum-variance frontier.'''

#Minimum-Variance Frontier Revisited
#100000 Portfolios1
R=np.array(data1.mean())
V=np.array(data1.cov())
n=len(R)
R_1=[]
Sigma_1=[]
for i in range(100000):
	Wi=np.random.rand(n)
	Wi=Wi/sum(Wi)
	Ri=Wi@R
	Sigmai=np.sqrt(Wi@V@Wi)
	R_1.append(Ri)
	Sigma_1.append(Sigmai)
plt.scatter(Sigma_1,R_1,s=3)
plt.title('Minimum-Variance Frontier1')

#Minimum-Variance Frontier1
Sigma_min1=[]
R_min1=np.linspace(0.5,1.2,100)
for i in R_min1:
	fun=lambda w: np.sqrt(w@V@w)
	cons=({'type':'eq','fun':lambda w: sum(w)-1},
		{'type':'eq','fun':lambda w: w@R-i})
	bnds=(((0,1),)*n)
	res=minimize(fun,([0.1]*n),bounds=bnds, constraints=cons)
	Sigma_min1.append(res.fun)
plt.plot(Sigma_min1,R_min1)
plt.xlabel('Sigma')
plt.ylabel('Return')
plt.savefig('Minimum-Variance Frontier1.jpg',dpi=300)
plt.show()

'''3. Repeat this entire process by simulating 1/w using the standard uniform 
distribution: i.e., take the reciprocal of the random draw from the standard uniform
distribution as the portfolio weight . Plot your results to show the minimum-variance 
frontier on a separate graph.'''

#100000 Portfolios2
R_2=[]
Sigma_2=[]
for i in range(100000):
	Wi=np.random.rand(n)
	Wi=1/Wi
	Wi=Wi/sum(Wi)
	Ri=Wi@R
	Sigmai=np.sqrt(Wi@V@Wi)
	R_2.append(Ri)
	Sigma_2.append(Sigmai)
plt.scatter(Sigma_2,R_2,s=3)
plt.title('Minimum-Variance Frontier2')

#Minimum-vairance Frontier2
plt.plot(Sigma_min1,R_min1)
plt.xlabel('Sigma')
plt.ylabel('Return')
plt.savefig('Minimum-Variance Frontier2.jpg',dpi=300)
plt.show()

#Economic significance:
'''Sharpe ratio:
Sharpe ratio represents risk premium per unit of total risk:
Includes all types of systematic risk
Also includes idiosyncratic risk, which penalises individual investments and non-diversified portfolios
Implicitly assumes normal returns, so cannot distinguish between return distributions with same variance
but different skewness or kurtosis'''

'''Sortino ratio (with risk-free rate as target return):
Sortino ratio represents risk premium per unit of downside risk, so can distinguish between 
return distributions with same variance but different skewness or kurtosis'''

'''Jensen' alpha:
For passive portfolio, it represents pricing error relative to CAPM; For active portfolio, 
it represents abnormal mean return after adjusting for exposure to market risk, due to fund 
manager’s ability to identify underpriced or overpriced assets.'''

'''Three factor alpha:
For passive portfolio, it represents pricing error relative to F-F three factor model; 
For active portfolio, it represents abnormal mean return after adjusting for exposure to 
market risk, size risk and value risk, due to fund manager’s ability to identify underpriced 
or overpriced assets.'''





















