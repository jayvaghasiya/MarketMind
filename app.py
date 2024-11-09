import time
from websurfer import MarketScraper, ArticleSaver
import sys

sys.dont_write_bytecode = True

class StockSentimentApp:
    def __init__(self, stock_list, articles_location, num_articles=5):
        self.stock_list = stock_list
        self.articles_location = articles_location
        self.num_articles = num_articles

    def run(self):
        for stock in self.stock_list:
            scraper = MarketScraper(stock)
            saver = ArticleSaver(stock, self.articles_location)

            article_links = scraper.fetch_article_links(self.num_articles)
            for url in article_links:
                try:
                    text = scraper.scrape_article_text(url)
                    article = {"url": url, "text": text}
                    saver.save_article(article)
                    print(f"Processed article from {url}")
                except Exception as e:
                    print(f"Error scraping article from {url}: {e}")

                # Pause between requests to avoid rate-limiting
                time.sleep(2)


# Example usage with top 20 Indian stocks
indian_stocks = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
    'HINDUNILVR', 'SBI', 'KOTAKBANK', 'BHARTIARTL', 'BAJFINANCE',
    'HDFC', 'ITC', 'ASIANPAINT', 'LT', 'MARUTI',
    'AXISBANK', 'HCLTECH', 'SUNPHARMA', 'TITAN', 'ULTRACEMCO'
]

# Specify the base directory where articles will be saved
articles_location = "./stock_articles"

# Run the application
app = StockSentimentApp(indian_stocks, articles_location, num_articles=5)
app.run()
