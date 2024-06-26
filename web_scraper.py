import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to scrape quotes
def scrape_quotes():
    quotes = []
    authors = []
    tags = []
    url = 'http://quotes.toscrape.com/page/{}'

    for page in range(1, 3):  # Scrape the first two pages as an example
        response = requests.get(url.format(page))
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote in soup.select('.quote'):
            text = quote.select_one('.text').get_text()
            author = quote.select_one('.author').get_text()
            tag_list = [tag.get_text() for tag in quote.select('.tags .tag')]

            quotes.append(text)
            authors.append(author)
            tags.append(', '.join(tag_list))

    return pd.DataFrame({
        'Quote': quotes,
        'Author': authors,
        'Tags': tags
    })

# Scrape the data
df = scrape_quotes()

# Save to CSV
df.to_csv('quotes.csv', index=False)

# Load the data
data = pd.read_csv('quotes.csv')

# Analysis: Most frequent authors
author_counts = data['Author'].value_counts()

# Visualization: Bar plot of most frequent authors
plt.figure(figsize=(10, 6))
sns.barplot(x=author_counts.index, y=author_counts.values, palette='viridis')
plt.title('Most Frequent Authors')
plt.xlabel('Author')
plt.ylabel('Number of Quotes')
plt.xticks(rotation=45)
plt.show()
