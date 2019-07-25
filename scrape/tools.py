import requests
import re
from bs4 import BeautifulSoup

def get_html(url):
    """ Returns a string containing the page's html."""
    r = requests.get(url)
    if r.ok:
        return r.text
    else:
        raise ValueError("get request failed!")

def save(url, fpath):
    """ Write html provided by url into fpath."""
    text = get_html(url)
    with open(fpath, 'w') as f:
        f.write(text)

def get_parsed(url):
    """ get BS html tree from the url"""
    text = get_html(url)
    return BeautifulSoup(text, 'html.parser')

def get_links(url, domain=None, verbose=False):
    """List of all links provided at the given url. 
        If domain is provided, only those at the given domain (containing it as a substring) 
        are considered."""
    parsed = get_parsed(url)
    href = re.compile(domain) if (domain is not None) else None
    links = parsed.find_all('a', href=href)
    if verbose:
        print("Found {0} links from {1}".format(len(links),url))
    return links

def get_domain_name(url):
    bits = url.split("/")
    print(bits)
    if 'http' not in bits[0]:
        domain = bits[0]
    else:
        domain = bits[2]
    if '.' not in domain:
        raise ValueError("Domain extraction failed for url: {0}".format(url))
    return domain
    
def travserse_site(baseurl):
    """Crawl through the site with provided base url, returning set of all unique URLs with the same 
    domain name."""
