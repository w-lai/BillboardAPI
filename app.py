from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import csv
import os

# api set up w/ Flask
app = Flask(__name__)
api = Api(app)

# holds API info
SONGS = {}

# API requests

class Song(Resource):
    # get entire list
    def get(self):
        return SONGS

api.add_resource(Song, '/')


class SongList(Resource):
    # get by song number
    def get(self, songnumber):
        if songnumber not in SONGS:
            return "Not found", 404
        else:
            return SONGS[songnumber]

api.add_resource(SongList, '/songs/<string:songnumber>')

def main():
  # set up the selenium parser to use chrome
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  s = Service(os.environ.get("CHROMEDRIVER_PATH"))
  driver = webdriver.Chrome(service=s, options=chrome_options)
  # access the billboard site dynamically
  driver.get("https://www.billboard.com/charts/hot-100/")
  # optain and parse the lines of the table
  lines = driver.find_elements(By.XPATH, "//div[@class='o-chart-results-list-row-container']")
  driver.implicitly_wait(10)
  # if webscraper fails, we're left with empty table/array
  data = []
  for line in lines:
    data.append(line.text)
  
  for i in range(len(data)):
    data[i] = data[i].split('\n')
  driver.quit()
  # take only the stuff that we want
  wantedData = []
  wantedData.append(["Position", "Title", "Artist"])
  for i in range(len(data)):
    temp = []
    temp.append(data[i][0])
    # remove unnecessary tags
    if (len(data[i]) == 7):
      temp.append(data[i][2])
      temp.append(data[i][3]) 
    else:
      temp.append(data[i][1])
      temp.append(data[i][2])
    wantedData.append(temp)
  # if the data is not empty / webscraper pulled something
  if (len(wantedData) != 0):
      # output the data to a csv
      with open("output.csv", "w") as f:
        csvWriter = csv.writer(f, delimiter=',')
        csvWriter.writerows(wantedData)

      # read new output data into songs (api storage)
      with open("output.csv", 'r') as data_file:
        data_file = csv.DictReader(data_file, delimiter=",")
        for row in data_file:
            item = SONGS.get(row["Position"], dict())
            item["name"] = row["Title"]
            item["rank"] = row["Position"]

            SONGS[row["Position"]] = item


if __name__ == "__main__":
    # webscrape into songs
    main()
    # run on Heroku / local port
    myPort = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=myPort, debug=True)


    




