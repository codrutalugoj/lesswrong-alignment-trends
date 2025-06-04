from bs4 import BeautifulSoup
import requests
import time
import datetime
import json
import os
from tqdm import tqdm

from selenium.webdriver import FirefoxService, Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_to_json(data: dict, filename: str):
    filename = os.path.join(os.getcwd(), "lesswrong_data.json" if not filename else filename)
    
    # Save to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(data['posts'])} posts to {filename}")
    print(f"{os.path.abspath(filename)}")

def get_dynamic_content(url):
    driver_service = FirefoxService(executable_path="/snap/bin/geckodriver")
    options = FirefoxOptions()
    options.add_argument('--headless')
    driver = Firefox(options=options, service=driver_service)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "LWPostsItem-row"))
        )
        return driver.page_source
    finally:
        driver.quit()

def extract_text_content(element):
    text_body = []
    
    # Base case - if element is just text
    if isinstance(element, str):
        return element.strip()
    
    # Recursively process all children
    for child in element.children:
        # Skip empty strings and images
        if isinstance(child, str) and not child.strip():
            continue
        if child.name == 'figure':
            continue
            
        # Handle paragraphs and headers
        if child.name and (child.name == 'p' or "h" in child.name):
            text = child.get_text()
            if text:
                text_body.append(text)
        # Recursive call for nested elements
        else:
            text = extract_text_content(child)
            if text:
                text_body.append(text)
                
    return '\n'.join(filter(None, text_body))

def scrape_lw(num_posts=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    base_url = "https://www.lesswrong.com"
    collection_date_start = datetime.datetime.strftime(datetime.datetime.now().date(), "%Y-%m-%d")
    collection_date_end = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=90), "%Y-%m-%d")
   
    posts_data = {"timestamp": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                  "posts": []}
    

    # Deal with pagination 
    offset = 0
    page_size = 50
    total_scraped = 0

    while total_scraped < num_posts:
        # Update URL with offset
        url_timeblock = f"{base_url}/allPosts?after={collection_date_end}&before={collection_date_start}&limit={page_size}&offset={offset}"
        print(f"Getting dynamic content from {url_timeblock}...")
        page = get_dynamic_content(url_timeblock)
        soup = BeautifulSoup(page, "html.parser")

        post_items = soup.find_all("div", class_="LWPostsItem-row")

        for post_item in tqdm(post_items[:num_posts]):
            # Extract post URL
            post_span = post_item.find("span", class_="PostsTitle-eaTitleDesktopEllipsis")
            post_link = post_span.find("a")
            if not post_link:
                continue
            
            post_url = f"{base_url}{post_link['href']}"
            
            # Get individual post content
            post_page = requests.get(post_url, headers=headers)
            post_soup = BeautifulSoup(post_page.content, "html.parser")
            
            # Extract post title
            title_raw = post_soup.find("h1", class_="PostsPageTitle-root")
            title = title_raw.find("a").text if title_raw else "None"

            # Extract tags
            tags_root = post_soup.find("span", class_="FooterTagList-root")
            tags_list = tags_root.find_all("span", class_="FooterTag-name")
            tags = [tag.text for tag in tags_list]

            # Only get posts related to AI
            if "AI" not in tags:
                continue

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

            # Extract post text
            post_wrapper = post_soup.find("div", class_="InlineReactSelectionWrapper-root")
            post_text = extract_text_content(post_wrapper)
            
            post_dict = {"title": title,
                        "url": post_url,
                        "author_names": author_names,
                        "author_links": author_links,
                        "tags": tags,
                        "post_karma": karma,
                        "date": post_date,
                        "text": post_text}
            
            posts_data["posts"].append(post_dict)
            total_scraped += 1
            time.sleep(5)

        offset += page_size
        print(f"Scraped {total_scraped} posts so far...")
        time.sleep(10)
        
    save_to_json(posts_data, filename="lesswrong_data.json")

if __name__ == "__main__":
    scrape_lw(num_posts=200)