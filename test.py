from scrape.tools import get_links


domain = "dominiccummings.com"
baseurl = "https://" + domain
links = get_links(baseurl,domain=domain)
for link in links:
    print(link.get('href'))
