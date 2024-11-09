import time
from websurfer import MarketScraper, ArticleSaver
from analyser import SentimentAnalysisApp
import sys
import streamlit as st
import pandas as pd

sys.dont_write_bytecode = True

class StockSentimentApp:
    def __init__(self, stock_list, articles_location, num_articles=5):
        self.stock_list = stock_list
        self.articles_location = articles_location
        self.num_articles = num_articles
        # Run the sentiment analysis application
        self.analyzer = SentimentAnalysisApp(self.articles_location)

    def run(self):
        result = {
            "Stock": [],
            "Sentiment Score": []
        }
        for stock in self.stock_list:
            scraper = MarketScraper(stock)
            saver = ArticleSaver(stock, self.articles_location)

            # article_links = scraper.fetch_article_links(self.num_articles)
            # for url in article_links:
            #     try:
            #         text = scraper.scrape_article_text(url)
            #         article = {"url": url, "text": text}
            #         saver.save_article(article)
            #         print(f"Processed article from {url}")
            #     except Exception as e:
            #         print(f"Error scraping article from {url}: {e}")

            # Pause between requests to avoid rate-limiting
            stock_name, score = self.analyzer.run_single_stock_analysis(stock, saver.date)
            if score is not None:
                result['Stock'].append(stock_name)
                result["Sentiment Score"].append(score)
        return result


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
data = app.run()
# Sample data
# data = {
#     'Stock': ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'SBI', 'HDFC', 'ITC', 'ASIANPAINT',
#               'MARUTI', 'AXISBANK', 'HCLTECH', 'SUNPHARMA', 'TITAN', 'ULTRACEMCO'],
#     'Sentiment Score': [-50.6, 80.0, -24.8, 68.0, 0.0, -10.0, 47.0, -15.0, -30.0, -100.0, 47.0, -53.0, 87.0, 83.0,
#                         -10.0, 34.0]
# }

# Create DataFrame
# Convert data to DataFrame
df = pd.DataFrame(data)

# Streamlit app setup
st.title("📈 Stock Sentiment Analysis Dashboard")

# Sidebar filters
sentiment_filter = st.sidebar.radio("Filter stocks by sentiment:", ("All", "Positive", "Negative"))

# Filter data based on sidebar selection
if sentiment_filter == "Positive":
    df = df[df['Sentiment Score'] > 0]
elif sentiment_filter == "Negative":
    df = df[df['Sentiment Score'] < 0]

# Display average sentiment
avg_sentiment = df['Sentiment Score'].mean()
st.header(f"Average Sentiment Score: {'📉' if avg_sentiment < 0 else '📈'} {avg_sentiment:.2f}")

# Display each stock with enhanced visual elements
for _, row in df.iterrows():
    stock_name = row['Stock']
    sentiment = row['Sentiment Score']
    sentiment_display = f"{sentiment} {'🔴' if sentiment < 0 else '🟢' if sentiment > 0 else '⚪️'}"

    # Display stock name and sentiment score with emoji
    st.subheader(f"{stock_name} - {sentiment_display}")

    # Progress bar for sentiment score
    progress = (sentiment + 100) / 200  # normalize -100 to 100 scale
    st.progress(progress)

    # Display slider with color gradient for added interactivity
    st.slider(
        label=f"{stock_name} Sentiment",
        min_value=-100,
        max_value=100,
        value=int(sentiment),
        format="%d",
        key=stock_name,
        disabled=True,
    )

st.sidebar.markdown("### About this App")
st.sidebar.info(
    "This app analyzes stock sentiment scores and visualizes them using sliders, progress bars, and emojis.")
