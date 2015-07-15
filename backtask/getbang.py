#coding:utf-8

import threading
import requests
from bs4 import BeautifulSoup
from model import *


def update_bang_qidian():
    threads = []
    for x in xrange(1, 11):
        threads.append(threading.Thread(target=update_page_bang_qidian, args=(x,)))

    [t.start() for t in threads]
    [t.join() for t in threads]


def update_page_bang_qidian(x):
    qidian_url = "http://m.qidian.com/"
    out_url = 'http://m.qidian.com/topdetail.aspx?recid=-1&toptype=-113&categoryid=-1&pageindex=' + str(x)
    r = requests.get(out_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    int_urls = []
    for x in soup.find("div", class_="tab_cont").find_all("div", class_="book-list-detail"):
        int_urls.append(qidian_url + x.find("a")["href"])

    for int_url in int_urls:
        r_in = requests.get(int_url)
        soup_in = BeautifulSoup(r_in.content, 'html.parser')
        book_info = soup_in.find("div", class_="book_info")
        img_src = book_info.find("div", class_="pic").find("img")["src"]
        title = book_info.find("div", class_="book_r_box").find("dt", class_="name").text.strip()
        author = book_info.find_all("dd", class_="dd_box")[0].find_all("a", class_="linkcl")[1].text
        type_ = book_info.find_all("dd", class_="dd_box")[0].find_all("a", class_="linkcl")[1].text
        words = book_info.find_all("dd", class_="dd_box")[1].find_all("span")[1].text
        description = soup_in.find_all("div", class_="chapter_tabs_cont")[1].find("div", class_="book_about").text.strip()
        last_update = soup_in.find_all("div", class_="chapter_tabs_cont")[0].find_all("a")[-1].text

        print title
        print img_src
        print author
        print type_
        print words
        print description
        print last_update


if __name__ == "__main__":
    update_page_bang_qidian(3)