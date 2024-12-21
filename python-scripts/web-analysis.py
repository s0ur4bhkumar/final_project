# prompt: optimize the above code for unique word cound

import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
from collections import Counter

def fetch_page_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTP errors
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

def extract_performance_metrics(url):
    return {
        "response_time_ms": requests.get(url).elapsed.total_seconds() * 1000
    }

def extract_content_analysis(soup):
    text = soup.get_text()
    words = re.findall(r'\b\w+\b', text.lower()) # Find all words, convert to lowercase
    word_counts = Counter(words)
    
    content_analysis = {
        "word_count": len(words),
        "unique_word_count": len(word_counts), # Count unique words
        "image_count": len(soup.find_all('img')),
        "link_count": len(soup.find_all('a'))
    }
    return content_analysis, word_counts # Return word counts


def save_to_csv(data, filename, word_counts=None):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")
    
    if word_counts:
        with open("word_counts.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["word", "count"])
            writer.writerows(word_counts.items())
        print("Word counts saved to word_counts.csv")


def main():
    url = input("Enter the URL to analyze: ")
    html_content = fetch_page_data(url)
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        meta_tags = extract_meta_tags(soup)
        performance_metrics = extract_performance_metrics(url)
        content_analysis, word_counts = extract_content_analysis(soup)
        
        data = {
            "url": url,
            "meta_tags": meta_tags,
            **performance_metrics,
            **content_analysis,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        flat_meta_tags = {f"meta_{k}": v for k, v in meta_tags.items()}
        flat_data = {**data, **flat_meta_tags}
        
        save_to_csv([flat_data], "webpage_analysis.csv", word_counts)

if __name__ == "__main__":
    main()