'''
A python scraper that scrapes daily news that has at least 100 points on hacker news
'''
import requests
from bs4 import BeautifulSoup
import pprint


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True)

def create_custom_hn(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.titleline')
    subtext = soup.select('.subtext')
    hn = []
    for i, item in enumerate(links):
        title = item.getText()
        href = item.find('a').get('href', None) if item.find('a') else None
        vote = subtext[i].select('.score')
        if vote:
            points = int(vote[0].getText().replace(' points',''))
            if points > 99:
                hn.append({'title':title, 'link':href, 'votes':points})

    more_link = soup.select_one('.morelink')
    next_page_url = more_link.get('href', None) if more_link else None

    return hn, next_page_url

def scrape_hn(initial_url, pages):
    all_hn = []
    url = initial_url

    for _ in range(pages):
        if not url:
            break
        hn, next_page_url = create_custom_hn(url)
        all_hn.extend(hn)
        url = f'https://news.ycombinator.com/{next_page_url}'
    return sort_stories_by_votes(all_hn)


initial_url = 'https://news.ycombinator.com/'
num_page = 2
pprint.pprint(scrape_hn(initial_url,num_page))