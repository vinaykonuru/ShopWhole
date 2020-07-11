import random
import numpy as np
from matplotlib import pyplot as plt
import pylab

#Linear regression functions
def check(a):
  flag = False
  for i in range(0, len(a)-1):
    if a[i]!=a[i+1]:
      flag = True
  return flag
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
#tested using mock purchasing patterns for two schools
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

#wholesale prices for product being sold (min quantity: price)
#w = open("wholesaler.txt")
wholesaler = {}

wp = open("wholesaleprices.txt", "r")
for line in wp:
  a = line.split(" ")
  wholesaler.update( {int(a[0]) : float(a[1])} )

def sell(price, slope = schoolslope, zero = schoolzero, vari = schoolvari):
  avgpurchases = slope * price + zero
  sales = max(0, int(.5+np.random.normal(avgpurchases, vari, 1)))

  print("Sold: " + str(sales) + " at price: $" + str(price))
  
  return sales

#generate 5 random prices within range, return
def initial(maxprice):
  minprice = int(100 * maxprice*.9) / 100.0   #price range
  a = []
  for i in range(0, 5):
    x = int(random.randrange(100* minprice, 100* maxprice)) / 100.0
    a.append(x)
  return a


#return optimal price based on current purchasing habits
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

#Repeats process for additional schools
def school(pop, reg):
  print("Second school: ")
  altcoefficient = 1.0*schooltpop / schoolpop #the coefficient of alteration 
  schooltreg = []
  schooltreg.append(reg[0])
  schooltreg.append(reg[1])
  #Scale regression values based on new school size
  schooltreg[0] *= altcoefficient
  schooltreg[1] *= altcoefficient 
  
  tprofits = []
  tsales = []
  tprofit = 0

  #Now we do our initial sales, but we use the predicted reg to determine our price range
  initialprice = optimize(schooltreg)
  #Generate values within (.9, 1.05) * initial optimal price to test
  testprices =  initial( int(100 * initialprice*1.05)/100.)

  print("Test sales: ")
  for price in testprices:
    result = sell(price)
    tsales.append(result)
    p = int(100*result * (price - purchaseprice(result)))/100.
    tprofits.append(p)
    tprofit+=p
    print("For a profit of: $" + str(p))
    

  #Updates school's regression using data from first sales
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

  print("Total profit: $" + str(int(100 * tprofit) /100. ))
  return schooltreg

#Outputs the wholesale price per unit for an order of given size
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

def visual(regs):
  trueline = [schoolslope, schoolzero]

  for i in range(len(regs)):
    x = np.linspace(.6, 1, 30)
    y = x * trueline[0] + trueline[1]
    error = np.random.normal(10, .01, size=y.shape)
    fig = plt.figure()
    fig.subplots_adjust(top=0.8)
    ax1 = fig.add_subplot(211)
    ax1.set_ylabel('Purchases')
    ax1.set_title('Regression predicted vs. actual')
    ax1.set_xlabel('Price ($)')
    plt.ylim(0, 1000)
    plt.plot(x, y, 'k-')
    plt.fill_between(x, y-error, y+error)
    x1 = np.linspace(.5, 1, 30)
    y1 = x * regs[i][0] + regs[i][1]
    plt.plot(x1, y1, "k--")
    plt.savefig('Graphs/' + str(i) + '.png', bbox_inches='tight')
    plt.close()

def profitvisual(profits):
  fig = plt.figure()
  fig.subplots_adjust(top=2)
  ax1 = fig.add_subplot(211)
  ax1.set_ylabel('Profit ($)')
  ax1.set_xlabel('Sale iteration number')
  ax1.set_title('Profit optimization over time')
  x = np.linspace(0, 53, 54)
  y = []
  for i in range(0, 54):
    y.append(profits[i])
  plt.scatter(x, y, s=25, c='black')
  reg = linReg(x, y)
  #print(reg)
  y1 = x * reg[0] + reg[1]
  plt.plot(x , y1, 'r--')
  plt.savefig('Graphs/profit.png', bbox_inches='tight')
  plt.close()

def main():
  #First school
  pricestest = initial(wholesaler[1])
  
  storereg = []
  print("Test sales: ")
  sales = []
  profits = []
  profit = 0
  testprices = []
  reg = []
  regtest = False
  for price in pricestest:
    result = sell(price)
    sales.append(result)
    testprices.append(price)
    p = int(100*result * (price - purchaseprice(result)))/100
    profits.append(p)
    profit+=p
    print("For a profit of: $" + str(p))
    regtest = check(testprices)
    if regtest:
      reg = linReg(testprices, sales)
      storereg.append(reg)
  
  #reg is the linear regression line that represents our demand for the school 
  reg = linReg(testprices, sales)
  #sell 10 times
  print("Test sales complete")
  for i in range (0, 50):
    price = optimize(reg)
    result = sell(price)
    testprices.append(price)
    
    p = int(100*result * (price - purchaseprice(result)))/100.
    profits.append(p)
    profit+=p
    print("For a profit of: $" + str(p))

    sales.append(result)
    reg = linReg(testprices, sales)
    print(str(i))
    #print(reg)
    storereg.append(reg)
  #print(storereg)

  #print(profits)
  print("Total profit: $" + str(int(100 * profit) /100. ))
  #print(resultsales)

  #Repeats process for school two
  #treg = school(schooltpop, reg)

  #Updates base prediction as an average of the two schools

  #reg[0] = (reg[0] + treg[0]) / 2.
  #reg[1] = (reg[1] + treg[1]) / 2.

  #For additional schools:
  #Update school info
  #schooltslope = int(f.readline())
  #schooltzero = int(f.readline())
  #schooltvari = int(f.readline())
  #schooltpop = int(f.readline())
  #Run school simulation
  #treg = school(schooltpop, reg)
  #Update regression (n = the number school this is)
  #reg[0] = (n-1) * reg[0] / n + treg[0] / n
  #reg[1] = (n-1) * reg[1] / n + treg[1] / n
  #print(storereg[53])
  #visual(storereg)
  #profitvisual(profits)
  return 0

main()
