
import numpy as np 
from scipy.stats import norm

# Define the variables

r = 0.50
S = 50
K = 42
T = 270/365
sigma = 0.50

def BlackScholes(r,S,K,T,sigma, type ='P'):
    d1 = (np.log(S/K)+ (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try :
        if type == 'C':
            price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0 ,1)
        elif type == 'P':
            price = K*np.exp(-r*T)*norm.cdf(-d2, 0 ,1) - S*norm.cdf(-d1, 0, 1)
        return price  
    except:
        print('please check all the parameters') 

print("Option prices is", round(BlackScholes(r, S, K, T, sigma, type = "P"),2))

