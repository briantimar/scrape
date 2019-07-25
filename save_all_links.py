from scrape.tools import get_linked_urls
from scrape.tools import save
from scrape.tools import travserse_site

baseurl = "https://dominiccummings.com"
linkdump = "cummings_links.txt"
seen = travserse_site(baseurl, num_worker_threads=20)
print("Collected {0} urls.".format(len(seen)))
with open(linkdump, 'w') as f:
    for url in seen:
        f.write(url+"\n")
