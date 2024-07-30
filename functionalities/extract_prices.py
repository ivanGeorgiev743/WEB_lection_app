import pandas as pd
import yfinance as yf


def get_prices(ticker):
    msft = yf.Ticker(ticker)

    # get historical market data
    hist = msft.history(period="1mo")
    hist.reset_index(inplace=True)
    hist["Date"] = hist["Date"].apply(lambda x: x.strftime("%d-%m-%Y"))
    hist.set_index("Date", inplace=True)
    return hist[["Close"]].reset_index().to_dict("records")


def upload_via_pandas(ticker, conn):
    msft = yf.Ticker(ticker)

    # get historical market data
    hist = msft.history(period="1mo")
    hist.reset_index(inplace=True)
    hist["Date"] = hist["Date"].apply(lambda x: x.strftime("%d-%m-%Y"))
    hist["Ticker"] = ticker
    hist.to_sql(name="hist_from_pandas", con=conn, if_exists="replace", index=False)


if __name__ == "__main__":
    print(get_prices("msft"))