import matplotlib.pyplot as plt

data = []
with open('data.csv','r') as data_file:
    data_file.readline()
    for line in data_file.readlines():
        data.append(float(line.split(',')[1].strip()))

def calculate_ema(data, period):
    smoothing_factor = 2 / (period + 1)
    multiplaier = 1 - smoothing_factor
    numerator = 0
    denominator = 0
    for i in range(period):
        numerator += data[i] * (multiplaier ** i)
        denominator += (multiplaier ** i)
    return numerator/denominator

def calculate_macd(data):
    macd = []
    for i in range(len(data)-26):
        macd.append(calculate_ema(data[i:],12) - calculate_ema(data[i:],26))
    return macd

def calculate_signal(macd):
    signal = []
    for i in range(len(macd)-9):
        signal.append(calculate_ema(macd[i:],9))
    return signal

def get_sells_buys(macd, signal, prices):
    sells = [[],[],[]]
    buys = [[],[],[]]
    for i in range(1, len(macd)):
        if macd[i-1] < signal[i-1] and macd[i] >= signal[i]:
            sells[0].append(i)
            sells[1].append(prices[i])
            sells[2].append(macd[i])
        if macd[i-1] > signal[i-1] and macd[i] <= signal[i]:
            buys[0].append(i)
            buys[1].append(prices[i])
            buys[2].append(macd[i])
    return sells, buys

def plot(prices, macd, signal, total, sells, buys):
    x = list(range(0,len(macd)))
    #wykresy macd i signal
    plt.subplot(3, 1, 1)
    plt.plot(x,macd, label="MACD")
    plt.plot(x,signal, linestyle="--", label="Signal", zorder=0)
    plt.scatter(buys[0], buys[2], color="green", marker="^", zorder=1, s=15, label="Buy")
    plt.scatter(sells[0], sells[2], color="red", marker="v", zorder=1, s=15, label="Sell")
    plt.ylabel("Signal \ MACD")
    plt.xlabel("Day")
    #wykres notowań oraz sygnałów kupna i sprzedaży
    plt.subplot(3, 1, 2)
    plt.plot(x, prices[:len(macd)], zorder=0)
    plt.scatter(buys[0], buys[1], color="green", marker="^", zorder=1, s=15, label="Buy")
    plt.scatter(sells[0], sells[1], color="red", marker="v", zorder=1, s=15, label="Sell")
    """for i, (xi, yi) in enumerate(zip(buys[0], buys[1])):
        plt.annotate(f'({xi}, {yi})', (xi, yi), textcoords="offset points", xytext=(0, 10), ha='center')
    for i, (xi, yi) in enumerate(zip(sells[0], sells[1])):
        plt.annotate(f'({xi}, {yi})', (xi, yi), textcoords="offset points", xytext=(0, 10), ha='center')"""
    plt.ylabel("Price[PLN]")
    plt.xlabel("Day")
    #wykres portfela
    plt.subplot(3, 1, 3)
    plt.plot(x,total[:len(macd)])
    plt.ylabel("Total")
    plt.xlabel("Day")
    plt.legend()
    plt.show()
    
class Person:
    def __init__(self, founds):
        self.wallet = founds
        self.resources = 0
        self.total = []
    
    def buy(self, price):
        #print(f"Buy {self.wallet / price} at {price} for {self.wallet}")
        self.resources += self.wallet / price
        self.wallet = 0
    def sell(self, price):
        #print(f"Sell {self.resources} at {price} for {price * self.resources}")
        self.wallet += price * self.resources
        self.resources = 0

    def set_total(self, price):
        x = self.wallet + self.resources * price
        self.total.append(x)

def simulate(data):
    person = Person(1000)
    macd = calculate_macd(data)
    signal = calculate_signal(macd)
    prices = data[:-35]
    macd = macd[:-9]
    macd.reverse()
    signal.reverse()
    prices.reverse()
    sells, buys = get_sells_buys(macd, signal, prices)
    next_sell = 0
    next_buy = 0
    for i in range(len(prices)):
        if next_sell < len(sells[0]) and i == sells[0][next_sell]:
            person.sell(prices[i])
            next_sell += 1
        if next_buy < len(buys[0]) and i == buys[0][next_buy]:
            person.buy(prices[i])
            next_buy += 1
        person.set_total(prices[i])
    plot(prices, macd, signal, person.total, sells, buys)
        

simulate(data)