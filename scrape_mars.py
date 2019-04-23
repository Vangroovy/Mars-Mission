from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    MarsData = {}
    ##Scrape NASA Mars News##
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #Retrieve the parent divs for all the articles
    results = soup.find_all(class_='list_text')
    news_titles = []
    articles = []

    # Loop through returned results to find title and articles
    for result in results:
            
            # Identify and return title of a news item
            title_div= result.find(class_='content_title')
            news_title = title_div.find('a').text
            news_titles.append(news_title)
            
            # Identify and return paragraph of the news item
            news_paragraph = result.find(class_='article_teaser_body').text
            articles.append(news_paragraph)
    
    #Add data into mars dataframe
    MarsData["headlines"]= news_titles
    MarsData["articles"]= articles

    ## Scrape and store Mars images from JPL ##
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Capture Feature area box image url
    mars = soup.find_all(class_="carousel_container")
    for m in mars:
        image_url = m.find('a')['data-fancybox-href']
    MarsData["feature_image"] = 'https://www.jpl.nasa.gov'+image_url
    
    ##Scrape and store Mars Weather##
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # Retrieve page with the requests module
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    #Find and store mars_weather
    MarsData['weather'] = soup.find(class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text', limit=1).get_text

    ##Scrape Mars Facts##
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    #Scrape table and put into a panda dataframe
    table = soup.find(class_="tablepress tablepress-id-mars")
    table_rows = table.find_all('tr')
    headers=[]
    facts = []

    #Use a loop to find content of each row
    for tr in table_rows:
        header = tr.find('td', class_="column-1").text
        headers.append(header)
        fact = tr.find('td', class_="column-2").text
        facts.append(fact)
    
    mars_facts=pd.DataFrame({"header":headers, "fact": facts})

    #Remove non-data elements
    mars_facts['fact']=mars_facts['fact'].str.replace('\n','')
    mars_facts.head(10)

    ##Scrape images from Mars Hemispheres##
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    titles = []
    image_urls=[]

    #Retrieve the hemisphere names
    hemispheres = soup.find_all(class_='description')

    for h in hemispheres:
        #find web address of high res image
        web_loc = h.find('a',class_="itemLink product-item" )['href']
        image_url = 'https://astrogeology.usgs.gov' + web_loc
        image_urls.append(image_url)
        
        #find name of hemisphere   
        title = h.find('h3').text
        titles.append(title)

        #Go to each individual page to pull high res image
        full_images=[]
        for image_url in image_urls:
            browser.visit(image_url)
            
            # Retrieve page with the requests module
            html = browser.html
            soup = bs(html, 'html.parser')
            full= soup.find(class_='downloads')
            full_image = full.find('a')['href']
            full_images.append(full_image)
        
    #Create python dictionary
    MarsData['title'] = titles
    MarsData['img_url'] = full_images

    return MarsData