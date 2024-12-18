import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime

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
    # Placeholder for performance metrics
    # Use libraries like `lighthouse` or `Google PageSpeed API` for actual metrics
    return {
        "response_time_ms": requests.get(url).elapsed.total_seconds() * 1000
    }

def extract_content_analysis(soup):
    content_analysis = {
        "word_count": len(re.findall(r'\w+', soup.get_text())),
        "image_count": len(soup.find_all('img')),
        "link_count": len(soup.find_all('a'))
    }
    return content_analysis

def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

def main():
    url = input("Enter the URL to analyze: ")
    html_content = fetch_page_data(url)
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        meta_tags = extract_meta_tags(soup)
        performance_metrics = extract_performance_metrics(url)
        content_analysis = extract_content_analysis(soup)
        
        # Combine all data
        data = {
            "url": url,
            "meta_tags": meta_tags,
            **performance_metrics,
            **content_analysis,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Flatten meta tags for CSV
        flat_meta_tags = {f"meta_{k}": v for k, v in meta_tags.items()}
        flat_data = {**data, **flat_meta_tags}
        
        save_to_csv([flat_data], "webpage_analysis.csv")

if __name__ == "__main__":
    main()
