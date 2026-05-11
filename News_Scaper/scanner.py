import requests
from bs4 import BeautifulSoup
from database import get_keywords
from database import get_seen_titles
from database import insert_seen_news


def fetch_headlines():
    url = "https://www.bbc.com/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_data = []
        
        
        for item in soup.find_all('a', {'data-testid': 'internal-link'}): 
            title = item.get_text(strip=True)
            link = item.get('href') 
            
            
            if title and link and len(title) > 10:
                if link.startswith('/'):
                    link = f"https://www.bbc.com{link}"
                
                news_data.append((title, link))
        
        return news_data

    except Exception as e:
        print(f"Error finding news: {e}")
        return []


def runscaner(user_id):
    headlines = fetch_headlines()
    key_words = get_keywords(user_id)
    seen_titles = get_seen_titles(user_id)
    news =[]

    
    print("-" * 40)
    for title,url in headlines:  # for each headline
        if title not in seen_titles:

            for keyword, preference in key_words:  # for each key word
                if keyword.lower() in title.lower():
                    if preference == 2:
                        news.append((title,url))
                        insert_seen_news(title,url)
                    break
    return news




