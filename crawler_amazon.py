import json
import html5lib
from html5lib import treebuilders
from bs4 import BeautifulSoup
import requests
import time
import os.path as path
import csv


url = 'https://www.amazon.com/b/ref=s9_acss_bw_cg_BHPCB_1a1?node=6960520011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=HGR7E8Y62VPSDXC0K4RE&pf_rd_t=101&pf_rd_p=04f80e12-6678-49ec-8691-dacbfbd4b091&pf_rd_i=283155'
url2='https://www.amazon.com/Hamilton-Revolution-Lin-Manuel-Miranda/dp/1455539740/ref=lp_6960520011_1_1?s=books&ie=UTF8&qid=1477265852&sr=1-1'
book_path= "C:\Users\Vinaya Tinguria\Documents\GitHub\Web Crawler\data\\book-pages"
book_list_path= "C:\Users\Vinaya Tinguria\Documents\GitHub\Web Crawler\data\\book-list-pages"
max_pages_to_crawl=50


class Book:

    def __init__(self):
        self.title = {}
        self.author = {}
        self.reviews = {}
        self.price = {}
        self.category = {}
        self.isbn = {}

    def __repr__(self):
        return "-------------------------------\nTitle: " + str(self.title) + "\nAuthor: " + str(self.author) + "\nReviews: " + str(self.reviews) + "\nPrice: " + str(self.price) + "\nCategory: " + str(self.category) + "\nISBN: " + str(self.isbn) + "\n-------------------------------"



def fetch_book_list_site(url, filepath):
    while True:
        f = requests.get(url)
        fp = f.content
        if f.status_code < 500:
            break
    write_site_to_file(fp, filepath)
    return fp


def fetch_book_site(url, filepath):
    while True:
        f = requests.get(url)
        fp = f.content
        if f.status_code < 500:
            break
    write_site_to_file(fp, filepath)
    return fp


def get_book_title_from_url (url):
    values = url.split("/")
    return values[3]


def write_site_to_file (site_content, filename):
    f = open (filename, "wb")
    f.write (site_content + '\n')
    f.close()


def read_soup_from_file (filename):
    return BeautifulSoup(open(filename), 'html5lib')


def get_book_title (soup):
    output = soup.find(id="productTitle")
    return unicode(output.string).encode('utf-8')

def get_book_author (soup):
    outputs = soup.select('a.a-link-normal.contributorNameID')
    for output in outputs:
        return unicode(output.string).encode('utf-8')

def get_book_reviews (soup):
    output=soup.find(id="acrCustomerReviewText")
    return unicode(output.string).encode('utf-8')

def get_book_price (soup):
    output=soup.find_all('span',{'class':'a-color-price'})
    return unicode(output[0].string).encode('utf-8')

def get_book_category (soup):
    outputs=soup.find_all('span',{'class':'cat-link'})
    for output in outputs:
        return str(output.string)
    return "none"

def get_isbn (soup):
    outputs=soup.find_all('b');
    for output in outputs:
        if output.string != None and "ISBN-10:" in output.string:
            return output.parent.text.split(":")[1]

def get_stuff_we_want (url):
    filename = get_book_title_from_url(url)
    filepath = book_path + "\\" + filename + ".html"

    if not path.isfile(filepath):
        fetch_book_site(url, filepath)

    soup = read_soup_from_file(filepath)

    book = Book()
    book.title = get_book_title(soup)
    book.author = get_book_author(soup)
    book.reviews = get_book_reviews(soup)
    book.price = get_book_price(soup)
    book.category = get_book_category (soup)
    book.isbn = get_isbn(soup)
    book_json = unicode(json.dumps(book, default=lambda o: o.__dict__)).encode('utf-8')
    write_book_to_csv(json.loads(book_json))

def write_book_to_csv (book):
    print "Adding book: " + str(unicode(book["title"]).encode('utf-8'))
    writer = csv.writer(open(book_path + "/books.csv", 'a'))
    writer.writerow([unicode(book["title"]).encode('utf-8'),
                     unicode(book["author"]).encode('utf-8'),
                     unicode(book["reviews"]).encode('utf-8'),
                     unicode(book["price"]).encode('utf-8'),
                     unicode(book["category"]).encode('utf-8'),
                     unicode(book["isbn"]).encode('utf-8')])

def get_books_from_list_page (url, count):
    filename = str(count)
    filepath = book_list_path + "\\" + filename + ".html"

    if not path.isfile(filepath):
        fetch_book_site(url, filepath)

    soup = read_soup_from_file(filepath)
    outputs = soup.select("a.a-link-normal.s-access-detail-page")
    for output in outputs:
        href = output.get('href')
        get_stuff_we_want(href)

    count += 1
    if count < max_pages_to_crawl:
        next_url = get_next_page_url(soup)
        if "amazon.com" in next_url:
            get_books_from_list_page(next_url, count)


def get_next_page_url (soup):
    link = soup.find(id="pagnNextLink")
    return "https://www.amazon.com" + str(link.get('href'))


get_books_from_list_page(url, 1)
