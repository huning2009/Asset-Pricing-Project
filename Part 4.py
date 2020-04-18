import numpy as np
import matplotlib.pyplot as plt

'''lng̃ =0.02+0.02ϵ̃ +ν̃ 
Here epsilon is a standard normal random variable, while nu is an independent random variable 
that has value of either zero (with probability of 98.3%) or ln(0.65) (with probability of 1.7%). 
Simulate epsilon with 10,000 random draws from a standard normal distribution, and simulate nu with 
10,000 random draws from a standard uniform distribution. '''
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

'''Use the simulated distribution of consumption growth to calculate the pricing kernel for power utility:
M̃ =0.99g̃**(−γ)
for gamma in the range [1,4]. Calculate the mean and standard deviation of the pricing kernel for all 
values of gamma. Plot the ratio SD(M)/E(M) (on the vertical axis) vs gamma (on the horizontal axis). 
Take note of the smallest value of gamma for which SD(M)/E(M) > 0.4 (i.e., for which the Hansen–Jagannathan bound is satisfied). '''
#Part 1: Hansen–Jagannathan Bound
gamma=np.linspace(1,4,100)
M_mean=np.array([(0.99*g**(-i)).mean() for i in gamma]) #for one gamma, got one mean and one std for M
M_std=np.array([(0.99*g**(-i)).std() for i in gamma])
M_ratio=M_std/M_mean
print('M_ratio',M_ratio)
plt.plot(gamma,M_ratio)
plt.xlabel('gamma')
plt.ylabel('Volatility of M')
plt.title('Volatility of M VS gamma')
plt.savefig('Mvol VS gamma.jpg',dpi=300)
plt.show()

'''Use the simulated distribution of consumption growth to find the expected market return,
for gamma in the range [1, 7]:E[R̃m]=(D1/P)E[g̃], Plot P1/D (on the vertical axis) vs gamma (on the horizontal axis). '''
#Part 2: Price-Dividend Ratio
gamma2=np.linspace(1,7,100)
PD_ratio=np.array([(0.99*g**(1-i)).mean() for i in gamma2]) #for one gamma, got one PD ratio
plt.plot(gamma2,PD_ratio)
plt.xlabel('gamma')
plt.ylabel('PD_ratio')
plt.title('Price dividend ratio VS gamma')
plt.savefig('Price dividend ratio VS gamma.jpg',dpi=300)
plt.show()

'''Use the simulated distribution of consumption growth to find the expected market return, 
for gamma in the range [1, 7]:E[R̃m]=D1/PE[g̃]
Use the simulated distribution of consumption growth to find the risk-free rate, 
for gamma in the range [1,7]:Rf=1/0.99E[g̃**(−γ)]
Plot the equity premium (on the vertical axis) vs gamma (on the horizontal axis).'''
#Part 3: Equity Premium
Rm=(1/PD_ratio)*(g.mean())
M_mean2=np.array([(0.99*g**(-i)).mean() for i in gamma2])
Rf=1/M_mean2
print('Rm',Rm)
print('Rf',Rf)
premium= Rm-Rf
plt.plot(gamma2,premium)
plt.xlabel('gamma')
plt.ylabel('equity premium')
plt.title('equity premium VS gamma')
plt.savefig('equity premium VS gamma.jpg',dpi=300)
plt.show()

'''Economic Significance for part 1:
For investor with power utility, volatility of pricing kernel is increasing in gamma, which is investor's (constant) coefficient of relative aversion.

H–J bound sets lower bound on volatility of pricing kernel, which becomes lower bound on investor's coefficient of relative risk aversion.

H–J bound is satisfied for reasonably low levels of relative risk aversion, so less (or no) equity premium puzzle.

Intuition is that rare disasters make consumption growth more risky (by introducing substantial amount of downside risk), so investor demands larger risk premium for given level of relative risk aversion.
'''








