from bs4 import BeautifulSoup
import requests

### Only Inputs Needed: Add as many stocks as needed
Equity_Tickers = ["AAPL", "GOOGL", "FB", "SNAP", "VOOG"]
Owned_Shares = [25, 5, 10, 50, 15]
Average_Cost = [150, 900, 110, 7.20, 159.6]   


### Class Share: Scrapes NASDAQ for current share price.
class Share:
    def __init__(self, ticker):
        self.ticker = ticker
        base_url = "https://www.nasdaq.com/symbol/"
        url = base_url + ticker
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, "html.parser")

    def Price(self):
        for price in self.soup.find('div',{'id':'qwidget_lastsale'}):
            Unedited_Price = (price.string)
            Edited_Price = Unedited_Price.replace("$","").replace(",","")
            Final_Price = float(Edited_Price)
            return Final_Price

### Class Individual_Performance: Calculates Equity Performance (Formatted in Individual Lists)
class Individual_Performance(Share):
    def __init__(self, ticker, share, cost):
        self.ticker = ticker
        self.share = share
        self.cost = cost

        Cost = []
        Value = []
        for i in range(0, len(self.ticker)):
            Original_Cost = (self.share[i] * self.cost[i])
            Cost.append(Original_Cost)
            Equity = Share(self.ticker[i])
            T_Val = Equity.Price()
            Market_Value = round(T_Val * self.share[i], 2)
            Value.append(Market_Value)

        self.O_Cost = Cost
        self.M_Value = Value

    def Profit(self):
        Equities = []
        for i in range(0, len(self.ticker)):
            x = float(round(self.M_Value[i] - self.O_Cost[i], 2))
            Equities.append(x)
        return Equities

    def Percent(self): 
        Equity_Percentages = []
        for i in range(0, len(self.ticker)):
            y = float(round(((self.M_Value[i] - self.O_Cost[i])/self.O_Cost[i]) * 100, 2))
            Equity_Percentages.append(y)
        return Equity_Percentages

### Class Portfolio_Performance: Calculates Equity Performance (Formatted in Totals)
class Portfolio_Performance(Share):
    def __init__(self, ticker, share, cost):
        self.ticker = ticker
        self.share = share
        self.cost = cost

        Total_C = []
        for i in range(0, len(self.ticker)):
            Cost = (self.share[i] * self.cost[i])
            Total_C.append(Cost)
        Total_MV = []
        for i in range(0, len(self.ticker)):
            Equity = Share(self.ticker[i])
            T_Val = Equity.Price()
            Market_Val = round(T_Val * self.share[i], 2)
            Total_MV.append(Market_Val)

        self.sum = round(sum(Total_MV) - sum(Total_C), 2)
        self.percent = round((sum(Total_MV) - sum(Total_C))/sum(Total_C)*100, 2)
        
    def Profit(self): 
        total_profit = self.sum
        return total_profit

    def Percentage(self):
        total_percentage = self.percent
        return total_percentage

### Class Prompt: Displays the Prompt for Portfolio Inquiry
class Prompt(Portfolio_Performance):
    def __init__(self, ticker, share, cost):
        self.ticker = ticker
        self.share = share
        self.cost = cost
        
        Var = Portfolio_Performance(self.ticker, self.share, self.cost)
        x = Var.Profit()
        y = Var.Percentage()

        self.total_profit = x
        self.total_percent = y

    def Portfolio_Prompt(self):
        Answer = input("Do you want your updated portfolio performance?: ")
        if Answer == "yes":
            if self.total_profit >= 0:
                Profit = " portfolio gain."
            else:
                Profit = " portfolio loss."
            Performance = ((str(self.total_profit)) + str(Profit))
            if self.total_percent >= 0:
                Change = "% gain, "
            else:
                Change = "% loss, "
            Performance2 = ((str(self.total_percent)) + str(Change))
            print("Your cumulative return is a " + Performance2 + "with a " + Performance)

            Answer2 = input("Would you like to know the specific movers?: ")
            if Answer2 == "yes":
                Overview = Individual_Performance(self.ticker, self.share, self.cost)
                x = Overview.Profit()
                Profit_List = []
                for i in range(0, len(x)):
                    z = (str(Equity_Tickers[i])  + " " + str(x[i]))
                    Profit_List.append(z)
                print("Portfolio List: " + str(Profit_List))
            else:
                print("Thanks Anyways! Have a Great Day!")

        else:
            print("Thanks Anyways!")

### Calls All Function & Display Portfolio Overview
Overview = Prompt(Equity_Tickers, Owned_Shares, Average_Cost)
Overview.Portfolio_Prompt()