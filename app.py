from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

app = Flask(__name__)
api = Api(app)

SONGS = {}

class Song(Resource):

    def get(self):
        return SONGS


api.add_resource(Song, '/')


class SongList(Resource):

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
  driver = webdriver.Chrome(options=chrome_options)
  # access the billboard site dynamically
  driver.get("https://www.billboard.com/charts/hot-100/")
  # optain and parse the lines of the table
  lines = driver.find_elements(By.XPATH, "//div[@class='o-chart-results-list-row-container']")
  driver.implicitly_wait(10)
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
    if data[i][1] == 'NEW':
      temp.append(data[i][2])
      temp.append(data[i][3])
    else:
      temp.append(data[i][1])
      temp.append(data[i][2])
    wantedData.append(temp)
  # output the data to a csv
  with open("output.csv", "w") as f:
    csvWriter = csv.writer(f, delimiter=',')
    csvWriter.writerows(wantedData)
    
  with open("output.csv", 'r') as data_file:
    data = csv.DictReader(data_file, delimiter=",")
    for row in data:
        item = SONGS.get(row["Position"], dict())
        item["name"] = row["Title"]
        item["rank"] = row["Position"]

        SONGS[row["Position"]] = item



if __name__ == "__main__":
    main()
    app.run(host="0.0.0.0", port=5000, debug=True)


    




