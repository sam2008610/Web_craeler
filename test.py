'''
class 練習 之 貨幣轉換 及錢包
'''
class Currency:
    from forex_python.converter import CurrencyRates
    c = CurrencyRates()
    
    rates = { 
        'USD': 1,
        'NTD': 30,
    }
    rates.update(c.get_rates('USD'))
    
    from forex_python.bitcoin import BtcConverter
    b = BtcConverter()   # add "force_decimal=True" parmeter to get Decimal rates

    def __init__(self, symbol, amount):
        self.symbol = symbol
        self.amount = amount
    def __repr__(self):
        return "{} ${:.2f}".format(self.symbol, self.amount)
    def convert(self, symbol):
        new_amount = (self.amount * self.rates[symbol]) / self.rates[self.symbol]
        return Currency(symbol, new_amount)
    def __add__(self,other):
        new_amount = self.amount +other.convert(self.symbol).amount
        return Currency(self.symbol,new_amount) 
    def __gt__(self, other): 
        return self.amount > other.convert(self.symbol).amount
class Wallet:
    def __init__(self):
        self.currencies = []
    def put(self, money):
        self.currencies.append(money)
    def __getitem__(self, symbol): #__getitem__() 就是用來定義 [] 運算子的行為
        #__setitem__() 方法是定義「透過 [] 指定 value 給 key」的行為，如 wallet['NTD'] = 300
        sum = 0 
        for c in self.currencies:
            if c.symbol == symbol:
                sum += c.amount
        return sum
    def __iter__(self): #巡覽
        for c in self.currencies:
            yield c #與return之差異在不會結束，直到沒有yield 







c1 = Currency('USD', 10)
c2 = Currency('NTD' , 300 )


print(c1)
print(c2)
c1 = c1.convert('JPY')
print (c1)
print (c1.convert('ILS'))
wallet = Wallet()
wallet.put(Currency('USD', 10))

print(wallet['USD'])
# print("{:.2f}".format(3.1415926))