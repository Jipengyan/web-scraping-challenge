#!/usr/bin/env python
# coding: utf-8

import requests as req
import time
import os
import pandas as pd
# import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo

# Point out chromedriver directory
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless = False)

# Get latest news from NASA website
news_url = 'https://mars.nasa.gov/news/'
browser.visit(news_url)
html = browser.html


# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')

# Obtain the latest news title and paragraph text
article = soup.find('div', class_='list_text')
news_title = soup.find("div", class_="content_title").text
news_p = soup.find("div", class_="description").text
print(news_title)
print(news_p)

#JPL Mars Space Images - Featured Image
#visit url and extract JPL Featured space image
images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(images_url)
html = browser.html
images_soup = bs(html, 'html.parser')
#Retrieve full size image link
full_size_image_path = images_soup.find_all('img')[3]["src"]
full_size_image_url = f'http://www.jpl.nasa.gov{full_size_image_path}'
print(full_size_image_url)

# Mars weather
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)
time.sleep(5)
weather_html = browser.html
weather_soup = bs(weather_html, 'html.parser')

mars_weather = weather_soup.find('section', attrs={"aria-labelledby":"accessible-list-0"})
mars_weather = mars_weather.find_all('span')

mars_w = []

for x in mars_weather:
    if len(x.get_text())>100:
        mars_w.append(x.get_text())
mars_w

# Mars facts page
url = "https://space-facts.com/mars/"
# Scrape the table of mars facts using pandas
mars_facts = pd.read_html(url)
mars_facts

# extract description and value from the table and put the information in as data frame
mars_facts_df = mars_facts[2]
mars_facts_df.columns = ["Description", "Value"]
mars_facts_df

#  Use Pandas to convert the data to a HTML table string.
mars_html_table = mars_facts_df.to_html()
print(mars_html_table)


### Mars Hemispheres
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemispheres_url)
hemispheres_html = browser.html
hemispheres_soup = bs(hemispheres_html, 'html.parser')

# Mars hemispheres products data
all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

hemisphere_image_urls = []
url = 'https://astrogeology.usgs.gov'
# Iterate through each hemisphere data
for i in mars_hemispheres:
    # Collect Title information
    hemisphere = i.find('div', class_="description")
    title = hemisphere.h3.text
    
    # Collect image link by browsing to hemisphere page
    hemisphere_link = hemisphere.a["href"]    
    browser.visit(url + hemisphere_link)
    
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    
    image_link = image_soup.find('div', class_='downloads')
    image_url = image_link.find('li').a['href']

    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name.
    image_dict = {}
    image_dict['title'] = title
    image_dict['img_url'] = image_url
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    hemisphere_image_urls.append(image_dict)
print(hemisphere_image_urls)

Mars_information ={
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": full_size_image_url,
        "mars_weather": mars_weather,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
}


print(Mars_information)
