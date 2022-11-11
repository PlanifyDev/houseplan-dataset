import json
from multiprocessing import Pool
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup



def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_url_content(url):
    soup = requests.get(url).content
    return soup


def get_urls_from_soup(soup):
    global internal_urls
    # print(v)
    urls = set()
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        href = urljoin('https://www.houseplans.com/', href)
        if 'houseplans' in href:
            urls.add(href)
    if urls is not set():
        return list(urls)


# def crawl(i):
#     link = f'https://www.houseplans.com/plan/print/{i}'
#     content = get_url_content(link)
#     if 'Page can not be found.' not in content.text:
#         return get_urls_from_soup(content)
#     return content


def crawl(i):
    link = f'https://www.houseplans.com/plan/print/{i}'
    content = str(get_url_content(link))
    return content


if __name__ == "__main__":
    pool = Pool(12)
    with pool:

        final = pool.map(crawl, range(0, 100_000))
    with open(f"houseplans_internal_links.json", "w") as f:
        final = [i for i in final if i is not None]
        json.dump(final, f)

