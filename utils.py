import datetime, requests, os, openai, random
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

#^ SIDE FUNCTIONS 👇 

def write_to_txt_file(news_headlines, news_contents, urls):
    with open('content.txt', 'w', encoding='utf-8') as f:
        text = """"""
        for i in range(len(news_headlines)):    
            text += f"""{news_headlines[i]}
            Full article: {urls[i]}
            {news_contents[i]}\n"""
        f.write(text)
        print('Written to > content.txt')

def _generate_headline(content):
    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Generate a short news headline in a funny and witty way using this:\n{content}"
            }
        ],
        model='gpt-3.5-turbo',
        temperature=0,
        stream=False
    )
    return response.choices[0].message.content
    
def _generate_news(content):
    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Rewrite this news content in a single short paragraph, in a funny, witty and original manner:\n{content}"
            }
        ],
        model='gpt-3.5-turbo',
        temperature=0,
        stream=False
    )
    return response.choices[0].message.content

#* MAIN FUNCTIONS 👇

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
            
    print(f'Total news fetched: {len(contents)}')
    
    # Sampling 6 random news from contents
    sampled_contents = random.sample(contents, k=6)
    print(f'Fetched {len(sampled_contents)}/{len(contents)} news')
    
    # Calling OpenAI helper functions
    print('Now calling OpenAI API...')
    news_headlines = [_generate_headline(content) for content in sampled_contents]
    news_contents = [_generate_news(content) for content in sampled_contents]

    return {
        "headlines": news_headlines, 
        "contents": news_contents,
        "urls": urls
    }