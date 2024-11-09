import requests
from bs4 import BeautifulSoup
import re


class MarketScraper:
    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_google_news_links(self, num_articles=5):
        """Fetches links from Google News for the stock."""
        base_url = f'https://www.google.com/search?q={self.stock_name}+stock+news&tbm=nws'
        response = requests.get(base_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        for item in soup.select('a'):
            href = item.get('href')
            if href and '/url?q=' in href:
                url = re.search(r'/url\?q=(.*?)&', href)
                if url:
                    links.append(url.group(1))
            if len(links) >= num_articles:
                break
        return links

    def get_economic_times_links(self, num_articles=5):
        """Fetches links from Economic Times for the stock."""
        base_url = f'https://economictimes.indiatimes.com/definition/{self.stock_name}-news'
        response = requests.get(base_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        for item in soup.select('a'):
            href = item.get('href')
            if href and href.startswith('https://economictimes.indiatimes.com'):
                links.append(href)
            if len(links) >= num_articles:
                break
        return links

    def get_moneycontrol_links(self, num_articles=5):
        """Fetches links from Moneycontrol for the stock."""
        base_url = f'https://www.moneycontrol.com/news/tags/{self.stock_name}.html'
        response = requests.get(base_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        for item in soup.select('a'):
            href = item.get('href')
            if href and href.startswith('https://www.moneycontrol.com/news/'):
                links.append(href)
            if len(links) >= num_articles:
                break
        return links

    def fetch_article_links(self, num_articles=5):
        """Combines sources to fetch article links."""
        links = (
            self.get_google_news_links(num_articles) +
            self.get_economic_times_links(num_articles) +
            self.get_moneycontrol_links(num_articles)
        )
        return links[:num_articles]  # Limit to the number specified

    def scrape_article_text(self, url):
        """Scrapes and extracts main text from an article, filtering out error messages."""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs if p.get_text()])

        # Check for common error patterns to avoid saving them
        error_patterns = [
            "404. That’s an error.",
            "The requested URL was not found on this server.",
            "That’s all we know"
        ]
        if any(error in article_text for error in error_patterns):
            print(f"Skipping article due to error content: {url}")
            return None

        return article_text