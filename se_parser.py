import requests
import json
from bs4 import BeautifulSoup
import logging
import datetime
import dateparser

home_page = "https://stackexchange.com/?pagesize=50"

class tracker:
    def __init__(self):
        self.data_file = "sent.json"
        self.data = []
        self.week = datetime.timedelta(days=7)
    
    def load(self):
        # load data if not loaded
        # data format list of (url, title, date)
        if not self.data:
            with open(self.data_file,"r") as file:
                self.data = json.load(file)
                
    def save(self):
        # load data if not loaded
        # data format list of (url, title, date)
        with open(self.data_file,"w") as file:
            json.dump(self.data, file)
    
    def check_post(self, url):
        for post in self.data:
            if post[0]==url:
                return False
        return True
    
    def ttl(self):
        now = datetime.datetime.now()
        self.data = list(filter(lambda x: now-dateparser.parse(x[2]) < self.week, self.data))
        
    
    def save_post(self, post):
        self.data.append((post['url'],post['title'],post['date']))

def gather_post(url):
    # download post
    # output {url, title, date, question, username}
    page = requests.get(url).text
    soup = BeautifulSoup(page)
    title = soup.find("a",class_='question-hyperlink').get_text()
    #answer = soup.find("div",class_='question').get_text().split("share")[0]
    question = soup.find("div",class_='postcell post-layout--right').find("div","post-text").get_text() #.findAll("div")#.get_text()
    username = soup.find("div",class_='user-details', itemprop="author").get_text().strip("\n").split("\n")[0]
    date = soup.find("span", class_='relativetime')['title']
    return {
        "title":title,
        "question":clear_text(question),
        "url":url,
        "username":username,
        "date":date
    }

def clear_text(text):
    if len(text) > 400:
        return text[:400] + "..."
    return text
    
def post_getter():
    # Download stack exchange hot page
    home_page = "https://stackexchange.com/?pagesize=50"
    page = requests.get(home_page).text
    soup = BeautifulSoup(page)
    # Parse page
    new = soup.find_all("a",class_='question-link')
    # Extract posts and return data
    posts = [elem["href"] for elem in new]
    return posts

def generate_text(payload):
    # output {url, title, date, question, username}
    return f"""Q: {payload['title']}

{payload['question']}

{payload['url']}
{payload['username']}, {payload['date']}
"""

def workflow():
    track = tracker()
    track.load()
    posts = post_getter()
    for post in posts:
        # check post for being previously sent
        if track.check_post(post):
            # download post
            payload = gather_post(post)
            track.save_post(payload)
            track.save()
            return generate_text(payload)