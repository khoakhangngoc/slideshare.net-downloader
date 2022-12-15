#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys, os
import img2pdf
import re

from time import localtime, strftime
from os import listdir, walk
from os.path import isfile, join
from lxml import html
try: from urllib.request import urlopen #python3
except ImportError: from urllib2 import urlopen #python2
try: from bs4 import BeautifulSoup #python3
except ImportError: from BeautifulSoup import BeautifulSoup #python2
try: input = raw_input #python2
except NameError: pass #python3

CURRENT = os.path.dirname(__file__)

def download_images(url):
    response = urlopen(url).read()
    # print(response)
    # try:
    #     tree = html.fromstring(response)
    #     # images = tree.xpath('.//div[contains(@id,"slide-5")]/picture/source/@srcset')
    #     images = tree.xpath('.//div[contains(@id,"slide-container")]/div')
    #     print(len(images))
    #     # for image in images:
            
    #     #     t = image.split(',',1)
    #         # print(t)
    # except Exception:
    #     raise Exception('eee')
    soup = BeautifulSoup(response)
    title = '_'.join(( 'pdf_images', strftime("%Y/%m/%d_%H:%M:%S", localtime()) ))  #soup.title.string
    slides = soup.findAll('div', id=lambda x: x and x.startswith('slide-'))
    for slide in slides:
        sources = slide.find('source')
        # print("sources")
        
        img = sources.get("srcset").split(',')[-1]
        image_url = img.strip().split(' ')[0].split('?')[0]
        print(image_url)
    
    #     image_url = image.get('data-full').split('?')[0]
        command = "curl --create-dirs -O --output-dir /Users/nguyenhuutinh/Downloads/slideshare-downloader-master/pdf_result/%s '%s' -o '%s'" % (title, image_url, title)
        os.system(command)

    convert_pdf("/Users/nguyenhuutinh/Downloads/slideshare-downloader-master/pdf_result/%s" % (title))

def convert_pdf(img_dir_name):
    f = []
    for (dirpath, dirnames, filenames) in walk(join(CURRENT, img_dir_name)):
        f.extend(filenames)
        break
    f = ["%s/%s" % (img_dir_name, x) for x in f]
    
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ atoi(c) for c in re.split('(\d+)', text) ]

    f.sort(key=natural_keys)
    
    print(f)

    pdf_bytes = img2pdf.convert(f, dpi=300, x=None, y=None)
    doc = open(pdf_f, 'wb')
    doc.write(pdf_bytes)
    doc.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = " ".join(sys.argv[1:])
    else:
        url = input('Slideshare URL: ').strip()
    if (url.startswith("'") and url.endswith("'")) or (url.startswith('"') and url.endswith('"')):
        url = url[1:-1]
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    pdf_f = re.sub('[^0-9a-zA-Z]+', '_', url.split("/")[-1]) #get url basename and replace non-alpha with '_'
    if pdf_f.strip() == '':
        print("Something wrong to get filename from URL, fallback to result.pdf")
        pdf_f = "result.pdf"
    else:
        pdf_f+=".pdf"
    print("url", url)
    download_images(url)


