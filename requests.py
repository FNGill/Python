import requests
import re
from bs4 import BeautifulSoup


url = "http://TARGET:PORT"

def get_html(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"ERROR CODE {response.status_code}. Was expecting 200..")
        exit(1)

    return response.content.decode()

html = (get_html(url))
print(html)

soup = BeautifulSoup(html, 'html.parser')
raw_data = soup.get_text()
all_words = re.findall(r'\w+', raw_data)

word_count = {}


for word in all_words:
    if word not in all_words:
        word_count[word] = 1
    else:
         current_count = word_count.get(word, 0)
         word_count[word] = current_count + 1

top_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)

for i in range(10):
    print(top_words[i])

