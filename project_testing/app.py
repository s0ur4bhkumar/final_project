from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

app = Flask(__name__)

def fetch_page_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_meta_tags(soup):
    meta_tags = {}
    for tag in soup.find_all('meta'):
        if tag.get('name') or tag.get('property'):
            key = tag.get('name') or tag.get('property')
            meta_tags[key] = tag.get('content', '')
    return meta_tags

def extract_content_analysis(soup):
    text = soup.get_text()
    words = re.findall(r'\b\w+\b', text.lower())  # Find all words, convert to lowercase
    word_counts = Counter(words)
    content_analysis = {
        "word_count": len(words),
        "unique_word_count": len(word_counts),
        "image_count": len(soup.find_all('img')),
        "link_count": len(soup.find_all('a'))
    }
    return content_analysis, word_counts

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        html_content = fetch_page_data(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            meta_tags = extract_meta_tags(soup)
            content_analysis, word_counts = extract_content_analysis(soup)
            return render_template('results.html', url=url, meta_tags=meta_tags, content_analysis=content_analysis, word_counts=word_counts)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
