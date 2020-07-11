import random
import numpy as np
def sum(a):
  total = 0
  for i in range(len(a)):
    total = total + a[i]
  return total
def sumofsquares(a):
  total = 0
  for i in range(len(a)):
    total = total + a[i]*a[i]
  return total
def sumofproduct(x, y):
  total = 0
  for i in range(len(x)):
    total = total + x[i]*y[i]
  return total
  
def linReg(x, y): 
  m = (len(x)*sumofproduct(x,y) - sum(x)*sum(y)) / (len(x)*sumofsquares(x)- sum(x)**2)
  b = (sum(y)-m*sum(x))/len(x)
  return [m, b]

#our algorithm 
#tested using mock data for two schools
f = open("schooldata.txt", "r")
f.readline()
#school 1:
schoolslope = int(f.readline())#change in purchases per dollar change in price
schoolzero =  int(f.readline())#demand if product is free
schoolvari = int(f.readline()) #variance in purchasing habits
schoolpop =  int(f.readline())

f.readline()
#school 2:
schooltslope = int(f.readline())
schooltzero = int(f.readline())
schooltvari = int(f.readline())
schooltpop = int(f.readline())

#wholesame prices (min quantity: price)
wholesaler = {
  1: .99, 
  10: .95, 
  50: .9, 
  200: .8, 
  1000: .65
}

def sell(price, slope = schoolslope, zero = schoolzero, vari = schoolvari):
  #returns a varied value around the mean
  avgpurchases = slope * price + zero
  sales = max(0, int(.5+np.random.normal(avgpurchases, vari, 1)))

  print("Sold: " + str(sales) + " at price: $" + str(price))
  
  return sales

def initial(maxprice):
  minprice = int(100 * maxprice*.9) / 100.0   #price range
  #generate 5 random prices within range, return
  a = []
  for i in range(0, 5):
    x = int(random.randrange(100* minprice, 100* maxprice)) / 100.0
    a.append(x)
  return a


#return optimal price for this school
def optimize(reg):
  optimalprice = 1.1
  profit = 0 
  for i in range(0, 110):
    price = i / 100.0
    psales = int(.5 + (reg[0] * price + reg[1]))
    purchase = purchaseprice(psales)
    pprofit = psales * (price - purchase)
    if pprofit > profit:
      profit = pprofit
      optimalprice = price
    
  return optimalprice

def school(pop, reg):
  print("Second school: ")
  altcoefficient = 1.0*schooltpop / schoolpop #the coefficient of alteration 
  schooltreg = reg
  schooltreg[0] *= altcoefficient
  schooltreg[1] *= altcoefficient 
  tprofits = []
  tsales = []
  tprofit = 0

  #Now we do our initial sales, but we use the predicted reg to determine our price points
  initialprice = optimize(schooltreg)
  #Generate values within (.9, 1.05) * initial price to test
  testprices =  initial( int(100 * initialprice*1.05)/100.)

  print("Test sales: ")

  for price in testprices:
    result = sell(price)
    tsales.append(result)
    p = int(100*result * (price - purchaseprice(result)))/100.
    tprofits.append(p)
    tprofit+=p
    print("For a profit of: $" + str(p))

  schooltreg = linReg(testprices, tsales)
  print("Test sales complete")

  for i in range (0, 10):
    price = optimize(schooltreg)
    result = sell(price)
    testprices.append(price)
    
    p = int(100*result * (price - purchaseprice(result)))/100.
    tprofits.append(p)
    tprofit+=p
    print("For a profit of: $" + str(p))

    tsales.append(result)
    schooltreg = linReg(testprices, tsales)

  #print(profits)
  print("Total profit: $" + str(int(100 * tprofit) /100. ))
  #print(resultsales)

def purchaseprice(qty):
  if qty < 10 :
    return wholesaler[1]
  elif qty < 50:
    return wholesaler[10]
  elif qty < 200:
    return wholesaler[50]
  elif qty < 1000:
    return wholesaler[200]
  else:
    return wholesaler[1000]

def main():
  testprices = initial(wholesaler[1])
  
  print("Test sales: ")
  sales = []
  profits = []
  profit = 0

  for price in testprices:
    result = sell(price)
    sales.append(result)

    p = int(100*result * (price - purchaseprice(result)))/100.
    profits.append(p)
    profit+=p
    print("For a profit of: $" + str(p))
    

  #reg is the linear regression line that represents our demand for the school 
  reg = linReg(testprices, sales)
  #sell 10 times
  print("Test sales complete")
  for i in range (0, 10):
    price = optimize(reg)
    result = sell(price)
    testprices.append(price)
    
    p = int(100*result * (price - purchaseprice(result)))/100.
    profits.append(p)
    profit+=p
    print("For a profit of: $" + str(p))

    sales.append(result)
    reg = linReg(testprices, sales)

  #print(profits)
  print("Total profit: $" + str(int(100 * profit) /100. ))
  #print(resultsales)

  #Repeats process for school two
  school(schooltpop, reg)




main()

