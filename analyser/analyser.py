import os
import glob
import re
import ollama


class ArticleManager:
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def get_combined_article_text(self, stock_name, date):
        """Combines all articles for a specified stock and date."""
        folder_path = os.path.join(self.base_directory, stock_name, date)
        article_paths = glob.glob(os.path.join(folder_path, "*.txt"))

        combined_text = ""
        for path in article_paths:
            with open(path, "r", encoding="utf-8") as f:
                combined_text += f.read() + " "  # Combine articles with a space separator
        return combined_text


class TextPreprocessor:
    def clean_text(self, text):
        """Clean and preprocess text data for sentiment analysis."""
        # Remove non-ASCII characters
        text = text.encode("ascii", "ignore").decode()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        # Remove special characters and extra whitespace
        text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def preprocess_articles(self, articles):
        """Preprocess a dictionary of articles."""
        cleaned_articles = {}
        for path, text in articles.items():
            cleaned_text = self.clean_text(text)
            cleaned_articles[path] = cleaned_text
        return cleaned_articles


class LlamaSentimentAnalyzer:
    def __init__(self):
        # Create an Ollama client
        self.client = ollama.Client()

    def get_sentiment_score(self, text):
        """Gets a sentiment score from LLaMA on a scale of -100 to +100."""
        # Example prompt for LLaMA
        prompt = f"Please analyze the sentiment of the following text on a scale from -100 to +100, where -100 is highly negative, 0 is neutral, and +100 is highly positive: only output number and if you are not confident give me None \n\n{text}\n\nSentiment Score:"

        # Call LLaMA model inference here (this is a placeholder function)
        response = self.llama_inference(prompt)
        # Parse and convert the response to a numeric score
        try:
            score = float(response)
            score = max(min(score, 100), -100)  # Ensure it's within -100 to +100
        except ValueError:
            score = None  # Handle any errors in parsing response

        return score

    def llama_inference(self, prompt):
        # Generate text
        response = self.client.generate(
            model="llama3.2:3b-instruct-fp16",
            prompt=prompt
        )
        return response["response"]


class SentimentAnalysisApp:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.article_manager = ArticleManager(base_directory)
        self.preprocessor = TextPreprocessor()
        self.analyzer = LlamaSentimentAnalyzer()

    def run_single_stock_analysis(self, stock_name, date):
        """Combines articles for a given stock and date, and analyzes sentiment."""
        # Step 1: Read combined article text for the stock and date
        combined_text = self.article_manager.get_combined_article_text(stock_name, date)

        # Step 2: Preprocess combined text
        cleaned_text = self.preprocessor.clean_text(combined_text)

        # Step 3: Analyze sentiment and print result
        score = self.analyzer.get_sentiment_score(cleaned_text)

        return stock_name, score
