'''
Created on Aug 7, 2013

Fetch pictures from JavaScript based web-sites using Windmill framework.
Change the "next_url" to your base URL page and botton.get("class") to your
botton (Archor) class (botton to next page/picture).

It's not bullet proof, just a basic home-made script

@author: darionascimento
'''
from windmill.authoring import  WindmillTestClient
from BeautifulSoup import BeautifulSoup

import re,  urllib
import time
from copy import copy

counter = 401

#Download all images from current page
def get_image_info(client):
    response = client.commands.getPageText()
    
    #soup from HTML
    soup = BeautifulSoup(response['result'])
    soup.prettify()
    links = soup.findAll('img')
    for link in links:
        url = link.get('src')
        if(url != '/img/spacer.gif' and url != ''):
            #print "new img"
            saveImage(url)
    
    #Find the button for next page and extract url
    nextUrlBotton = soup.findAll("a")
    for botton in nextUrlBotton:
        if botton.get("class") == "sm-button sm-button-size-large sm-button-skin-submit sm-button-nochrome sm-pagination-button-right":
            return botton.get("href")
 
#store image @ folder        
def saveImage(url):
    global counter
    
    #Download image
    fileURL = urllib.urlopen(url)
    doc = fileURL.read()
    print "save image: "+str(counter)
    #Storage with file name: imgXXX.jpg
    f = open('img'+str(counter)+'.jpg','w')
    f.write(doc)
    f.close()
    counter = counter+1


#Open each page, wait for pictures load and go to next page
def test_scrape_iotd_gallery():
    client = WindmillTestClient(__name__)
    #init URL
    next_url = "http://www.joao-viegas.com/Eventos-e-Reportagens/CRISMAS-2013/i-TbNRhxj"
    while True:
        print "next page: "+str(next_url)
        client.open(url=next_url)
        #Wait for loading
        client.waits.forElement(xpath=u"//ul[@class='sm-tiles-list']",timeout=60000)
        next_url = get_image_info(client)
        if next_url == '' or next_url == '#' or next_url is None:
            break
    print "DONE!!!"

