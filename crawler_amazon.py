import html5lib
from html5lib import treebuilders
import urllib
from bs4 import BeautifulSoup
import requests

url = 'https://www.amazon.com/b/ref=s9_acss_bw_cg_BHPCB_1a1?node=6960520011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=HGR7E8Y62VPSDXC0K4RE&pf_rd_t=101&pf_rd_p=04f80e12-6678-49ec-8691-dacbfbd4b091&pf_rd_i=283155'  # + str(page) # this is for cars in the orlando area, replace link with w/e
url2='https://www.amazon.com/Hamilton-Revolution-Lin-Manuel-Miranda/dp/1455539740/ref=lp_6960520011_1_1?s=books&ie=UTF8&qid=1477265852&sr=1-1'
def trade_spider():
    fp = requests.get(url).content
#    fp = urllib.urlopen(url)
#    print fp.content
    soup = BeautifulSoup(fp, 'html5lib')
    outputs = soup.find_all('span',{'class':'acswidget-carousel__title'})
    #print outputs[0].text
    for output in outputs:
        book_awards=output.text
        print book_awards
    # for output in outputs:
    #     print(output.text)`

def book_spider():
    fp=requests.get(url2).content
    soup = BeautifulSoup(fp, 'html5lib')
    outputs=soup.find_all('span',{'class':'a-size-large'})
    for output in outputs:
        book_titles=output.text
        print book_titles

#trade_spider()
book_spider()