import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


def extract_image(url):
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    image = soup.find_all("img", class_="wide-image")
    img = [i.get("src") for i in image]
    return "https://marshemispheres.com/" + img[0]


def image_title(url):
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    title = soup.find_all("h2", class_="title")
    title_text = [i.text for i in title]
    return title_text[0]


def get_dict_list(keys, list_of_tups):
    list_of_dict = [dict(zip(keys, values)) for values in list_of_tups]
    return list_of_dict


def scrape():
    # FEATURED IMAGE SCRAPE
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    img = [i.get("src") for i in soup.find_all("img", class_="headerimage fade-in")]
    featured_image_url = url + img[0]

    # TOP NEWS SCRAPE
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    html_1 = browser.html
    soup_1 = bs(html_1, "html.parser")
    latest_news = soup_1.find_all("div", class_="content_title")[0]
    latest_news_title = latest_news.text
    paragraph = soup_1.find_all("div", class_="article_teaser_body")[0]
    latest_news_paragraph = paragraph.text

    # HEMISPHERE IMAGE SCRAPE
    hemi_url = "https://marshemispheres.com/"
    url_path = requests.get(hemi_url)
    soup_2 = bs(url_path.content)
    div_item = soup_2.find_all("div", class_="item")

    links = []
    for i in div_item:
        for a in i.find_all('a', href=True): 
            if a.text:
                links.append(a['href'])

    full_links = [url + i for i in links]
    img_url = [extract_image(i) for i in full_links]
    title = [image_title(i) for i in full_links]
    list_tups = list(zip(title, img_url))

    keys = ("title", "img_url")
    hemisphere_image_urls = get_dict_list(keys, list_tups)

    # COMPARISON TABLE SCRAPE
    table_url = "https://galaxyfacts-mars.com/"
    browser.visit(table_url)
    html_3 = browser.html
    soup_3 = bs(html_3, "html.parser")
    table = soup_3.find_all("table", class_="table")[0]

    table_header = [i.text for i in table("th")]
    mars_column = [i.text for i in table("span", class_="orange")]
    earth_column = [i.text for i in table("span", class_="purple")]

    table_df = {"Description": table_header, "Mars": mars_column, "Earth": earth_column}
    df = pd.DataFrame(table_df)
    df.set_index("Description", inplace=True)
    df["Earth"] = df["Earth"].str.replace("\t", "")
    comparison_table = df.to_html()

    browser.quit()


    # FINAL DICTIONARY FOR MONGO
    
    final_mars_data = {
    "latest_title": latest_news_title,
    "latest_para" : latest_news_paragraph,
    "html_table": comparison_table,
    "hemisphere_scrape": hemisphere_image_urls
    }

    return final_mars_data































