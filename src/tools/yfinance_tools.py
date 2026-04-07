"""
- https://algotrading101.com/learn/yfinance-guide/
- https://ranaroussi.github.io/yfinance/index.html
- https://pypi.org/project/yfinance/

High granularity of data: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo



"""

import time
import yfinance as yf
from yfinance.exceptions import YFRateLimitError
def get_stock_data(ticker="aapl"):
    """Get stock data from Yahoo Finance"""
    apple= yf.Ticker(ticker)

    # show actions (dividends, splits)
    apple.actions

    # show dividends
    apple.dividends

    # show splits
    apple.splits

    # + other methods etc.
    
    
    aapl_historical = apple.history(start="2020-06-02", end="2020-06-07", interval="1m")
    aapl_historical

    return aapl_historical


def get_stock_news(ticker="AAPL", max_items=10):
    """Get latest news for a stock ticker"""
    stock = yf.Ticker(ticker)
    news_list = stock.news[:max_items]  # Limit to max_items
    
    formatted_news = []
    for article in news_list:
        formatted_news.append({
            "title": article.get("title"),
            "source": article.get("source"),
            "link": article.get("link"),
            "published": article.get("providerPublishTime")
        })
    
    return formatted_news
  



def get_stock_news_with_retry(ticker="AAPL", max_items=10, retries=3):
    """Get news with retry on rate limit"""
    for attempt in range(retries):
        try:
            stock = yf.Ticker(ticker)
            news_list = stock.news[:max_items]
            return [{...} for article in news_list]
        except YFRateLimitError:
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
              
              
if __name__ == "__main__":
  # get_stock_data()
  # get_stock_news()
  news = get_stock_news_with_retry()
  for article in news:  
    print(article)
    

