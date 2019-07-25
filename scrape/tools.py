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

def get_parsed(url):
    """ get BS html tree from the url"""
    text = get_html(url)
    return BeautifulSoup(text, 'html.parser')

def get_links(url, domain=None):
    """List of all links provided at the given url. 
        If domain is provided, only those at the given domain (containing it as a substring) 
        are considered."""
    parsed = get_parsed(url)
    href = re.compile(domain) if (domain is not None) else None
    return parsed.find_all('a', href=href)