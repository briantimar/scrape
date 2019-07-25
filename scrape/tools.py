import requests
import re
from bs4 import BeautifulSoup
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

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
    if domain is None:
        links = parsed.find_all('a')
    else:
        href = re.compile(domain)
        links = parsed.find_all('a', href=href)
    if verbose:
        print("Found {0} links from {1}".format(len(links),url))
    return links

def get_linked_urls(url, domain=None, verbose=False):
    if url[-1] == '/':
        url = url[:-1]
    links = get_links(url, domain=domain, verbose=verbose)
    urls = [link['href'] for link in links]
    for i in range(len(urls)):
        if urls[i][0]=='/':
            # change rel links to absolute
            urls[i] = url + urls[i]
    return urls

def get_domain_name(url):
    bits = url.split("/")
    if 'http' not in bits[0]:
        domain = bits[0]
    else:
        domain = bits[2]
    if '.' not in domain:
        raise ValueError("Domain extraction failed for url: {0}".format(url))
    return domain

def travserse_site(baseurl):
    """Crawl through the site with provided base url, returning set of all unique URLs with the same 
    domain name.
        - for each link on page:
            if already seen, ignore it
            otherwise:
                - add to list of seen
                - add to queue of links to visit
        repeat until queue of links to visit is empty

        Based on the queueing example at https://docs.python.org/3/library/queue.html
        """
    import threading

    domain = get_domain_name(baseurl)
    urls_to_visit = Queue()
    
    todo = get_linked_urls(baseurl, domain=domain, verbose=False)
    print(todo)
    seen = set(todo)
    modify_seen_lock = threading.Lock()

    for url in todo:
        urls_to_visit.put(url)
    
    def url_processor():
        while True:
            url = urls_to_visit.get()
            if url is None:
                # 'None' plays the role of a kill signal
                break
            new_urls = get_linked_urls(url, domain=domain)
            with modify_seen_lock:
                for url in new_urls:
                    if url not in seen:
                        urls_to_visit.put(url)
                        seen.add(url)
            # tells q that this worker is finished
            urls_to_visit.task_done()

    num_worker_threads = 10
    threads = []
    for __ in range(num_worker_threads):
        t = threading.Thread(target=url_processor)
        t.start()
        threads.append(t)
    
    ## block until all candidate urls have been visited
    urls_to_visit.join()
    ## kill workers
    for __ in range(num_worker_threads):
        urls_to_visit.put(None)
    for t in threads:
        t.join()
    
    return seen

    
