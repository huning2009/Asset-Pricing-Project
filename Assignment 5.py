

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import bisect

'''Consider a Barberis, Huang and Santos (2001) economy with the following parameter choices for the investor's utility function:
δ=0.99,γ=1,λ=2
Consumption growth has a lognormal distribution:
lng̃ =0.02+0.02ϵ̃ 
where epsilon is a standard normal random variable. With these parameter choices, the risk-free rate is constant at 1.0303 per year. 
Simulate the distribution for consumption growth with at least 10,000 random draws for epsilon. 
'''
#construct g
g=[]
for i in range(10000):
	epsilon=np.random.randn()
	a=np.random.rand()
	if a>0.01:
		nu=0
	else:
		nu=np.log(0.5)
	gi=np.exp(0.02+0.02*epsilon+nu)
	g.append(gi)
g=np.array(g)

'''Define x as one plus the dividend-price ratio for the market portfolio:
x=(1+P/D)D/P=1+D/P
and define the error term:
e(x)=0.99b0E[ν̂ (xg̃ )]+0.99x−1
where utility from financial gain or loss is given by:
ν̂ (R)=R−1.0303 for R≥1.0303
ν̂ (R)=2(R−1.0303)forR<1.0303
Calculate the equilibrium values of x for b0 in the range [0, 10] using bisect method
'''
#define nuhat
rf=1.0303
def nuhat(R):
	if R>rf:
		return R-rf
	if R<rf:
		return 2*(R-rf)

#define error 
'''error can not be defined as error=0.99*b0*nuhat((x*g).mean())+0.99*x-1,can only put .mean outside of nuhat
but if do that way, x*g is an array，can not compare with rf'''
def error(x,g,b0):
	nu=0
	for i in g:
		nui=nuhat(i*x)
		nu+=nui
	nu=nu/len(g)
	return 0.99*b0*nu+0.99*x-1

#compute x, for one b0, get one xi 
b0=np.linspace(0,10,101)
x=[]
for i in b0:
	xi=bisect(lambda x: error(x,g,i),1,1.1)
	x.append(xi)
x=np.array(x)
print('x',x)

'''Use x to calculate the price-dividend ratio for the market portfolio:
PD=1/(x−1)
Plot the price-dividend ratio (on the vertical axis) vs b0 (on the horizontal axis). '''
#compute and plot PDratio
PDratio=1/(x-1)
plt.plot(b0,PDratio)
plt.xlabel('b0')
plt.ylabel('PDratio')
plt.title('PDratio VS b0')
plt.show()

'''calculate the expected market return:
E[Rm]=E[xg̃ ]
Plot the equity premium (on the vertical axis) vs b0 (on the horizontal axis). '''
#calculate expected market return
rm=x*(g.mean())
premium=rm-rf
plt.plot(b0,premium)
plt.xlabel('b0')
plt.ylabel('Equity premium')
plt.title('Equity premium VS b0')
plt.show()

#self-defined bisect
'''def mybisect(f,xlow,xhigh):
	if f(xlow)<0 and f(xhigh)>0:
		for i in range(100000):
			x=0.5*(xlow+xhigh)
			if abs(f(x))<10**(-8):
				return x
				break 
			else:
				if f(x)<0:
					xlow=x
				else:
					xhigh=x
	else:
		print('f(xlow) and f(xhigh) must have different sign')'''

'''Economic significance:
Investor's utility function for financial gain or loss [i.e., nuhat(R)]:
Adding the investor’s utility function for financial gain or loss to investors’ preference allows us to incorporate the prospect theory, where financial gain or loss is measured relative to reference level based on risk-free rate

Parameter lambda.
Investor is more sensitive to financial loss than financial gain, and lambda determines degree of loss aversion, so lambda must be bigger than 1. The more sensitive the investors are to financial losses, the bigger the lambda. 

Parameter b0
b0 determines amount of emphasis that investor puts on utility from financial gain or loss, compared to utility of consumption. Equity premium will increase with b0, as investors puts more emphasis in utility from financial gain or loss.'''



