# Import necessary modules
import requests
from bs4 import BeautifulSoup
import pprint

# Send requests to the Hacker News website for the first and second pages of news articles, and parse the HTML content using BeautifulSoup.
res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

# Extract the links and subtext (which includes the vote count) for the articles using CSS selectors.
links = soup.select('.titleline > a')
subtext = soup.select('.subtext')
links2 = soup2.select('.titleline > a')
subtext2 = soup2.select('.subtext')

# Combine the links and subtext from both pages into two mega-lists.
mega_links = links + links2
mega_subtext = subtext + subtext2

# Define a function that sorts a list of articles by their vote counts in descending order.


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

# Define a function that creates a custom list of articles by filtering out those with fewer than 100 votes and creating a list of dictionaries for each article with its title, link, and vote count.


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


# Call the create_custom_hn() function with the mega-lists of links and subtext, and print the output using the pprint module for better formatting.
pprint.pprint(create_custom_hn(mega_links, mega_subtext))
