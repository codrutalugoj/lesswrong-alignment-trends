from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd
import json
import os

def save_to_json(data: dict, filename: str):
    filename = os.path.join(os.getcwd(), "lesswrong_data.json")
    
    # Save to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(data['posts'])} posts to {filename}")
    print(f"{os.path.abspath(filename)}")


def scrape_lw(num_posts=10):
    
    base_url = "https://www.lesswrong.com"
    collection_date_start = datetime.datetime.strftime(datetime.datetime.now().date(), "%Y-%m-%d")
    collection_date_end = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=90), "%Y-%m-%d")

    url_timeblock = f"{base_url}/allPosts?after={collection_date_end}&before={collection_date_start}&limit={num_posts}"
    print(url_timeblock)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url_timeblock, headers=headers)
    # .content contains the raw bytes, while .text contains decoded text in human-readable format
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup.prettify())
    all_classes = set()
    for div in soup.find_all('div'):
        classes = div.get('class', [])
        all_classes.update(classes)
    print("Available classes:", sorted(all_classes))

    posts = []
    parent_section = soup.find("div", class_="SingleColumnSection-root")
    print(parent_section)

    post_items = posts.find_all("div", class_="LWPostsItem-row")

   
    posts_data = {"timestamp": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                  "posts": []}


    for i, post_item in enumerate(post_items[:num_posts]):
        # Extract post URL
        post_span = post_item.find("span", class_="PostsTitle-eaTitleDesktopEllipsis")
        post_link = post_span.find("a")
        if not post_link:
            continue
        
        post_url = f"{base_url}{post_link['href']}"
        print(f"Scraping post {i+1}/{num_posts}: {post_url}")
        
        # Get individual post content
        post_page = requests.get(post_url, headers=headers)
        post_soup = BeautifulSoup(post_page.content, "html.parser")
        
        # Extract post title
        title_raw = post_soup.find("h1", class_="PostsPageTitle-root")
        title = title_raw.find("a").text if title_raw else "None"
        print(f"    Post title: {title}")

        # Extract tags
        tags_root = post_soup.find("span", class_="FooterTagList-root")
        tags_list = tags_root.find_all("span", class_="FooterTag-name")
        tags = [tag.text for tag in tags_list]
        print(f"    Tags: {tags}")

        # Extract author names
        authors = post_soup.find("span", class_="PostsAuthors-authorName")
        
        author_names = [author.text for author in authors if author != ", "]

        # Extract author links
        author_links = [author_res['href'] for author_res in authors.find_all("a", class_="UsersNameDisplay-noColor")]

        # Extract upvotes/karma
        karma = post_soup.find("h1", class_="Typography-root Typography-headline LWPostsPageTopHeaderVote-voteScore")
        karma = karma.text if karma else "None"

        # Extract post date
        post_date = post_soup.find("span", class_="PostsPageDate-date").text
        
        post_dict = {"title": title,
                     "url": post_url,
                     "author_names": author_names,
                     "author_links": author_links,
                     "tags": tags,
                     "post_karma": karma,
                     "date": post_date}
        
        posts_data["posts"].append(post_dict)
        time.sleep(2)

    save_to_json(posts_data, filename="raw_data.json")

if __name__ == "__main__":
    scrape_lw(num_posts=20)