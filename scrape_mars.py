from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    mars = []
    ##Scrape NASA Mars News##
    browser = init_browser() 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')    
    #Retrieve the parent divs for all the articles
    results = soup.find_all(class_='list_text')
    news = [] 
    # Loop through returned results to find title and articles
    for result in results:
            
            # Identify and return title of a news item
            title_div= result.find(class_='content_title')
            headline = title_div.find('a').text            
            # Identify and return paragraph of the news item
            article = result.find(class_='article_teaser_body').text            
            #Create dictionary
            news.append({ "title": headline, "content": article})

    ## Scrape and store Mars images from JPL ##
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Capture Feature area box image url
    mars_pic = soup.find_all(class_="carousel_container")
    for m in mars_pic:
        image_url = m.find('a')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov'+image_url
    
    ##Scrape and store Mars Weather##
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # Retrieve page with the requests module
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    #Find and store mars_weather
    mars_weather = soup.find(class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    twitter_url = mars_weather.find("a").text
    mars_weather = mars_weather.text.replace(twitter_url, "")

    ##Scrape Mars Facts##
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_data = []
    #Scrape table and put into a panda dataframe
    table = soup.find(class_="tablepress tablepress-id-mars")
    mars_data = pd.read_html(str(table))
    headers = mars_data[0][0].values
    facts = mars_data[0][1].values
    mars_facts = list(zip(headers, facts))

    ##Scrape images from Mars Hemispheres##
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemispheres=[]

    #Retrieve the hemisphere names
    hem_names = soup.find_all(class_='description')

    for h in hem_names:
        #find web address of high res image
        web_loc = h.find('a',class_="itemLink product-item" )['href']
        image_url = 'https://astrogeology.usgs.gov' + web_loc
        #Go to the page with the high res image and scrape the image
        browser.visit(image_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        full= soup.find(class_='downloads')
        full_image = full.find('a')['href']
        
        #find name of hemisphere   
        title = h.find('h3').text
        #save in the hemisphere dictionary
        hemispheres.append({'title': title, 'image_url': full_image})
        
    ##Create python dictionary for the scraped data##
    mars = {"news":news,
            "picture":featured_image_url, 
            "weather":mars_weather,
            "facts": mars_facts, 
            "hemispheres": hemispheres
            }
    #Close browser
    browser.quit()

    return mars