import yfinance as yf
import json

def save_data_as_json(ticker, start_date, end_date, filename):

    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    
    if df.empty:
        print("No price data found for the ticker symbol.")
        return
    else:
        df = df.drop(columns=['Dividends','Stock Splits'])
        df['td_D'] = ((df['Close']-df['Open'])/df['Open'])*100
        df['yd_D'] = df['td_D'].shift(1)
        df.dropna(inplace=True)
        df = df[['td_D', 'yd_D']]

    # Convert the DataFrame to a list of dictionaries
    data = df.reset_index().to_dict(orient='records')
    
    # Convert Timestamp to string for JSON serialization
    for record in data:
        if 'Date' in record:
            record['Date'] = record['Date'].strftime('%Y-%m-%d')
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    save_data_as_json('^NDX', '2023-01-01', '2024-01-01', 'stock_data.json')
