# Task 1:
#     Scrape https://ml-ops.org/ -> markdown files
#         - store in ./data/mlops_org
#         - IGNORE IMAGES
#         - should follow all links and generate coherent markdown
#         - use markdownify for parsing

import requests
import time
import random

from typing import Callable
from pathlib import Path
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def crawl_and_scrape_website(curr_url: str, base_output_dir: str, parse_fn: Callable[[str], str] = md, visited: set[str] | None = None):
    # early return for previously visited URLs
    if visited is None:
        visited = set()
    if curr_url in visited:
        return
    
    # add to visited 
    visited.add(curr_url)

    print(f"crawling URL: {curr_url}")

    # scrape and parse
    html = scrape(curr_url)
    parsed_content = parse_fn(html)
    curr_path = urlparse(curr_url).path[1:]

    # make output path
    output_path = Path(base_output_dir) / f"{curr_path or 'home'}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # write parse content to output directory
    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(f"# {output_path.name}\n\n")
        f.write(f"URL: {curr_url}\n\n")
        f.write(parsed_content)

    print(f"markdown content written to path {output_path}")

    # visit internal links on the page 
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a', href=True)
    for link in links:
        link_url = urlparse(link.get('href'))
        # skip links to external domains
        if link_url.netloc == base_url or link_url.netloc == "":
            crawl_and_scrape_website(urljoin(base_url, link_url.path), base_output_dir, parse_fn, visited)
            time.sleep(random.uniform(1, 2))
        


def scrape(url: str) -> str:
    return requests.get(url, timeout=5).text

if __name__ == "__main__":
    base_url = "https://ml-ops.org/"
    base_output_dir = "data/ml-ops-org/"
    crawl_and_scrape_website(base_url, base_output_dir)


