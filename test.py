from scrape.tools import get_linked_urls
from scrape.tools import save
from scrape.tools import travserse_site

baseurl = "https://briantimar.github.io"
seen = travserse_site(baseurl)
