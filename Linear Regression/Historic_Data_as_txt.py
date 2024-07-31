import yfinance as yf
import pandas as pd

def save_data_as_custom_txt(ticker, start_date, end_date, filename):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    
    if df.empty:
        print("No price data found for the ticker symbol.")
        return
    else:
        df['Deviation_of_present_day'] = ((df['Close'] - df['Open']) / df['Open']) * 100
        df['Average_Deviation_of_past_5days'] = (df['Deviation_of_present_day'].shift(1)+df['Deviation_of_present_day'].shift(2)+df['Deviation_of_present_day'].shift(3)+df['Deviation_of_present_day'].shift(4)+df['Deviation_of_present_day'].shift(5))/5
        df.dropna(inplace=True)
        df = df[['Deviation_of_present_day', 'Average_Deviation_of_past_5days']]

    # Save the DataFrame to a custom plain text file
    with open(filename, 'w') as f:
        for index, row in df.iterrows():
            f.write(f"{row['Deviation_of_present_day']} {row['Average_Deviation_of_past_5days']}\n")

if __name__ == "__main__":
    save_data_as_custom_txt('^NDX', '2010-01-01', '2024-01-01', 'stock_data.txt')


