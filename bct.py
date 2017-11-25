import requests
from lxml import html, etree
import html2text
import hashlib


class BctEntry:
    def __init__(self, id, username, userrank, content):
        self.id = id;
        self.username = username;
        self.userrank = userrank;
        self.content = content;


def _get_html2text():
    h2t = html2text.HTML2Text()
    h2t.ignore_images = True
    h2t.ignore_links = True
    return h2t

def _read_url(url):
    result = requests.get(url, headers = {'User-agent': 'cc1'})
    if (result):
        return result.content
    return False

def _get_link_for_last_page_of_thread(forum_thread):
    tree = html.fromstring(forum_thread)
    link_to_last_page_path = "//div[@id='bodyarea']/table[1]//td[1]/a[last()]"
    return tree.xpath(link_to_last_page_path)[0].get("href")

def _get_entries_for_thread_page(forum_thread_page):
    result = requests.get(forum_thread_page, headers = {'User-agent': 'cc1'})
    tree = html.fromstring(result.content)
    entries_path = "//form[@id='quickModForm']//td[@class='windowbg' or @class='windowbg2']/table"
    return tree.xpath(entries_path)

def _create_bctentry_from_html_subtree(subtree, h2t):
    username =  subtree.find(".//td[@class='poster_info']/b/a").text
    rank =  subtree.find(".//td[@class='poster_info']//div[@class='smalltext']").text.strip()
    text =  subtree.find(".//td[@class='td_headerandpost']/div[@class='post']")
    content =  etree.tostring(text).strip()
    #content = h2t.handle(content)
    m = hashlib.md5()
    m.update(etree.tostring(subtree))
    id = m.digest()
    return BctEntry(id, username, rank, content)

def read_last_page(thread_url):
    h2t = _get_html2text()

    forum_html = _read_url(thread_url)
    if forum_html:
        link_to_last_page = _get_link_for_last_page_of_thread(forum_html)
        entries = _get_entries_for_thread_page(link_to_last_page)
        return [_create_bctentry_from_html_subtree(subtree, h2t) for subtree in entries]





