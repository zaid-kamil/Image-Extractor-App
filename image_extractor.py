import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


def is_valid(url):
    '''
    check if the website address is ok or not
    '''
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    ''' collect images from website '''
    soup = bs(requests.get(url).content,'html.parser')
    urls = []
    for img in tqdm(soup.find_all("img"),"Extracting images"):
        img_url = img.attrs.get('src')
        if not img_url:
            continue
        if img_url.startswith(url):
            img_url = urljoin(url,img_url)
        try:
            pos = img_url.index('?')
            img_url =  img_url[:pos]
        except:
            pass
        if img_url.startswith('//'):
            img_url = 'https:'+img_url
        if img_url.startswith("http"):
            img_url = img_url
        if is_valid(img_url):
            print(img_url)
            urls.append(img_url)
        else:
            print('pro',img_url)
    return urls

def download(url, pathname):
    '''
    Downloads a file from a url
    '''
    if not os.path.isdir(pathname):  # if folder is not created
        os.makedirs(pathname)          # create a new folder
    res = requests.get(url, stream=True) # make the url downloadable using stream = True
    file_size = int(res.headers.get('Content-Length',0)) # check the file size
    file_name = os.path.join(pathname,url.split('/')[-1])  # get the image name
    
    # set up progress bar
    progress = tqdm(res.iter_content(1024),f'downloading {file_name}',
                  total=file_size,unit='B',unit_scale=True,unit_divisor=1024)
  
    # download the data and save in file
    with open(file_name,'wb') as f:
          for data in progress.iterable:
            f.write(data)
            progress.update(len(data))
  

import os

def load_img_from_folder(folder):
    if os.path.exists(folder):
        files =  os.listdir(folder)
        files = [os.path.join(folder,file) for file in files]
        return files
    