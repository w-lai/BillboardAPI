# BillboardAPI
This is a simple Python API deployed on Heroku. Uses Selenium and Flask to webscrape from Billboard Hot 100.

Deployed [here](https://webscrapingpythonapi.herokuapp.com/).

*This application is written in python3.*

To deploy this locally, simply clone the repository for app.py and remove all of the os related files.
Specifically, remove the following:

`chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")`
`s = Service(os.environ.get("CHROMEDRIVER_PATH"))`
`service=s`

For the last one of the 3, remove the service argument in the webdriver declaration, not the entire line.

This application also requires Flask and Selenium:
`pip install Flask`
`pip install flask-restful`
`pip install selenium`
