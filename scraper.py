from bs4 import BeautifulSoup
import requests

URL = "https://www.lesswrong.com/posts/fMqgLGoeZFFQqAGyC/how-do-we-solve-the-alignment-problem"
page = requests.get(URL)

# .content contains the raw bytes, while .text contains decoded text in human-readable format
soup = BeautifulSoup(page.content, "html.parser")


content = soup.find(id="postBody")
# look for the tags so we can filter on the AI tag
tags = soup.find_all("div", class_="LWPostsPageHeaderTopRight-tagList")

for elem in tags:
    tag_list = elem.find("span", class_="FooterTag-name")
    print(tag_list)
    print()

