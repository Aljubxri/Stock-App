import yahoo_fin.stock_info as si
import pandas as df



#this function brings the hisorical data from any given start and end date, with 1 month intervals
#input the dates as strings in this format: "01/01/2020" 
#first argument is the ticker, then start date, then end date
#then it takes the pandas table and makes it into a csv file tha is exported

def historicalToCSV(ticker,startDate,endDate):
    company_data = si.get_data(ticker, start_date=startDate, end_date= endDate, interval="1mo")
    #Will send csv file to relative file location, if specific location is needed, then change the argument
    #for example stock_csv = company_data.to_csv('C:\Users\User1\desktop\stock.csv')
    stock_csv = company_data.to_csv('stock.csv')
    print(stock_csv)
    
    
historicalToCSV("aapl", "01/01/2019", "01/01/2020")