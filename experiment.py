import datetime, requests, random
from bs4 import BeautifulSoup

def fetch_from_tldr(category, date):
    """Fetches TLDR news from tldr.tech
    Input: category (tech, marketing, founders, design, ai)
    """
    if date == str(datetime.date.isoformat(datetime.date.today())): 
        return ValueError
    url = f'https://tldr.tech/{category}/{date}'
    print(f'Fetching news from TLDR for the date: {url}')
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Approach: Select all divs with class 'mt-3'. These are the ones which have the URLs and news content. We will generate headline from news content.
    contents, urls = [], []
    mt3_divs = soup.find_all('div', { 'class': 'mt-3' })
    
    if len(mt3_divs)==0:
        return
    for mt3_div in mt3_divs:
        if mt3_div.find("a", {'class': 'font-bold'}, recursive=False):
            urls.append(mt3_div.find("a", {'class': 'font-bold'}, recursive=False)['href'])
        if mt3_div.find("div", recursive=False):
            content = mt3_div.find("div", recursive=False)
            contents.append(content.get_text())
            
    return contents
    
if __name__=="__main__":
    contents = fetch_from_tldr('tech', '2024-02-02')
    sampled_contents = random.sample(contents, k=6)
    for idx, content in enumerate(sampled_contents):
        print(f'{idx}. {content[:50]}\n')