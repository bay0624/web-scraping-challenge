# Mission to Mars
## Objective
A web app that scrapes various websites for the latest information, news and images of planet Mars. These information will then be displayed in a single responsive HTML page. Below is a screenshot of the webpage:

![Mission_to_Mars](https://github.com/bay0624/web-scraping-challenge/blob/main/mission_to_mars.png)

## Technologies
- <b>Beautiful Soup & Splinter</b>: For scraping the data from various websites.
- <b>Flask</b>: For building the web application.
- <b>HTML & Bootstrap (CSS)</b>: For designing and styling the web page.
- <b>PyMongo</b>: For interacting with the Mongo Database.
- <b>Pandas</b>: For designing the Mars v. Earth Comparison table.

## Resources
- https://redplanetscience.com/
- https://spaceimages-mars.com/
- https://galaxyfacts-mars.com/
- https://marshemispheres.com/

## Steps
#### Dependencies
```python
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
```
#### Scraping latest Mars news from https://redplanetscience.com/
```python
url = "https://redplanetscience.com/"
browser.visit(url)

html = browser.html
soup = bs(html, "html.parser")

latest_news = soup.find_all("div", class_="content_title")[0]

latest_news_title = latest_news.text
latest_news_title

paragraph = soup.find_all("div", class_="article_teaser_body")[0]
latest_news_paragraph = paragraph.text
browser.quit()
```

#### Scraping featured Mars image from https://spaceimages-mars.com/
```python
url = "https://spaceimages-mars.com/"
browser.visit(url)
html = browser.html
soup = bs(html, "html.parser")
img = [i.get("src") for i in soup.find_all("img", class_="headerimage fade-in")]
img[0]
featured_image_url = url + img[0]
featured_image_url
browser.quit()
```

#### Scraping Mars Hemispheres images from https://marshemispheres.com/
```python
url = "https://marshemispheres.com/"
browser.visit(url)
hemisphere_image_urls = []

for i in range(4):
    html = browser.html
    soup = bs(html, "html.parser")
    
    title = soup.find_all("h3")[i].get_text()
    browser.find_by_tag('h3')[i].click()
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    img_url = soup.find("img", class_="wide-image")["src"]
    
    hemisphere_image_urls.append({
        "title": title,
        "img_url": "https://marshemispheres.com/" + img_url
    })
    browser.back()

hemisphere_image_urls
browser.quit()
```
    
#### Scraping Mars vs Earth Comparison information for the table Hemispheres images from https://galaxyfacts-mars.com/
```python
url = "https://galaxyfacts-mars.com/"
browser.visit(url)
html = browser.html
soup = bs(html, "html.parser")

table = soup.find_all("table", class_="table")[0]

table_header = [i.text for i in table("th")]
mars_column = [i.text for i in table("span", class_="orange")]
earth_column = [i.text for i in table("span", class_="purple")]

table_df = {"Description": table_header, "Mars": mars_column, "Earth": earth_column}

df = pd.DataFrame(table_df)
df.set_index("Description", inplace=True)
df["Earth"] = df["Earth"].str.replace("\t", "")
comparison_table = df.to_html(classes="table table-striped")
browser.quit()
```

#### Flask App
```python
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


@app.route("/")
def echo():
    final_mars_data = mongo.db.collection.find_one()
    return render_template("index.html", final_mars_data=final_mars_data)


@app.route("/scrape")
def scrapping_mars():
    final_mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, final_mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
```
