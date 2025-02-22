from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

base_url = "https://www.lesswrong.com"
#recent_posts_url = f"{base_url}/allPosts"
#recent_posts_url = f"{base_url}/allPosts?after=2025-02-19&before=2025-02-20&limit=100"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
page = requests.get(base_url, headers=headers)
# .content contains the raw bytes, while .text contains decoded text in human-readable format
soup = BeautifulSoup(page.content, "html.parser")


post_items = soup.find_all("div", class_="LWPostsItem-row")
posts_data = []



for i, post_item in enumerate(post_items[:2]):
    # Extract post URL
    post_span = post_item.find("span", class_="PostsTitle-eaTitleDesktopEllipsis")
    post_link = post_span.find("a")
    if not post_link:
        continue
    
    post_url = f"{base_url}{post_link['href']}"
    print(f"Scraping post {i+1}/20: {post_url}")
    
    # Get individual post content
    post_page = requests.get(post_url, headers=headers)
    post_soup = BeautifulSoup(post_page.content, "html.parser")
    
    # Extract post title
    title = post_soup.find("h1", class_="PostsPageTitle-root")
    title_text = title.find("a").text if title else "No title found"
    print(f"    Post title: {title_text}")

    # Extract tags
    tags_root = post_soup.find("span", class_="FooterTagList-root")
    tags_list = tags_root.find_all("span", class_="FooterTag-name")
    tags = [tag.text for tag in tags_list]
    print(f"    Tags: {tags}")

    # Extract author names
    authors = post_soup.find("span", class_="PostsAuthors-authorName")
    
    author_names = [author.text for author in authors if author != ", "]

    # Extract author links
    authors_links = [author_res['href'] for author_res in authors.find_all("a", class_="UsersNameDisplay-noColor")]

    # Extract upvotes/karma
    karma = post_soup.find("h1", class_="Typography-root Typography-headline LWPostsPageTopHeaderVote-voteScore")
    
    print(f"    Author Names: {author_names}")
    print(f"    Author links: {authors_links}")
    print(f"    Post Karma: {karma.text}")

    time.sleep(1)

print(f"Successfully scraped {len(posts_data)} posts")