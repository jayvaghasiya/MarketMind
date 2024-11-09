from datetime import datetime
import os
import hashlib

class ArticleSaver:
    def __init__(self, stock_name, articles_location):
        self.stock_name = stock_name
        self.articles_location = articles_location
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.create_directory()

    def create_directory(self):
        """Creates a directory for the stock and date."""
        self.folder_path = os.path.join(self.articles_location, self.stock_name, self.date)
        os.makedirs(self.folder_path, exist_ok=True)

    def article_exists(self, text):
        """Checks if the article already exists using a hash of the text."""
        article_hash = hashlib.md5(text.encode()).hexdigest()
        file_path = os.path.join(self.folder_path, f"{article_hash}.txt")
        return os.path.exists(file_path), file_path

    def save_article(self, article):
        """Saves an individual article if it hasn't been saved already."""
        if article['text'] is None:
            # Skip saving if the article text is None (e.g., filtered out due to error content)
            return

        exists, file_path = self.article_exists(article['text'])
        if not exists:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"URL: {article['url']}\n\n{article['text']}\n")
            print(f"Saved article to {file_path}")
        else:
            print(f"Article already exists at {file_path}, skipping.")