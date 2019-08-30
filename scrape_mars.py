# Modules
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # Initialize the Browser. It'll be call by scrape function
    return Browser("chrome")


def scrape():
    browser = init_browser()

    # Visit visit mars.nasa.gov --> NASA Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get title of the most recent news about mars
    title_news = soup.find('div', class_='content_title').text
    #Get the most recent news 
    p_news = soup.find('div', class_='article_teaser_body').text

    # Visit jpl.nasa.gov (Nasa Jet Propulsion Laboratories) --> JPL Mars Space Images - Featured Image
    url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url1)
    time.sleep(1)

    # Using splinter to  get image url
    browser.find_link_by_partial_text('FULL IMAGE').click()
    browser.is_element_present_by_text('more info', wait_time=1)
    browser.find_link_by_partial_text('more info').click()

    html1 = browser.html
    soup1 = bs(html1, "html.parser")

    url_ini = "https://www.jpl.nasa.gov"
    featured_image_url = url_ini + soup1.find('figure', class_="lede").find('a')['href']

    # Visit twitter.com --> Mars Weather
    url2 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url2)
    time.sleep(1)

    html2 = browser.html
    soup2 = bs(html2, "html.parser")

    # Get text from the last tweet
    mars_weather = soup2.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather.a.extract()
    mars_weather.text
    mars_weather = mars_weather.text.replace('\n', ". ")

    # Visit space-facts.com --> Mars Facts
    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)
    time.sleep(1)

    # Get table from url address and format it
    tables = pd.read_html(url3)
    mars_facts = tables[1]
    mars_facts = mars_facts.rename(columns={0: 'description', 1: 'value'}).set_index('description')

    # Convert table to html page
    mars_facts.to_html('mars_facts.html')

    # Visit USGS Astrogeology site --> Mars Hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    time.sleep(1)

    html4 = browser.html
    soup4 = bs(html4, "html.parser")

    #Get all the images in a div group
    group = soup4.find('div', class_="collapsible results")
    group1 = group.find_all('div', class_="item")
    main_url = "https://astrogeology.usgs.gov"

    # List and dictionary to store title and image for each hemisphere
    hemisphere_image_urls = []
    dict_hem = {}

    # Loop through the image links
    for item in group1:
        hem_img_url = main_url + item.find('a', class_="itemLink product-item")['href']
        browser.visit(hem_img_url)
        browser.find_link_by_partial_text('Open').click()
        
        html_hem = browser.html
        soup_hem = bs(html_hem, "html.parser")
        
        img_url = main_url + soup_hem.find('img', class_="wide-image")['src']
        title = soup_hem.find('h2', class_="title").text.split(" ")
        title = title[0] + " " + title[1]
        
        dict_hem = {
            "title": title,
            "img_url": img_url
        }
        hemisphere_image_urls.append(dict_hem)

    # Store all the data in a dictionary
    scrape = {
        "title_news": title_news,
        "body_news": p_news,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return scrape