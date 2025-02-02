# WebScraping
import requests
import selectorlib
import smtplib, ssl
import os
import time
from dotenv import load_dotenv
import sqlite3


load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
MY_CONTEXT = ssl.create_default_context()
PASSWORD = os.getenv("PASSWORD")
SENDER = os.getenv("USERNAME")
RECEIVER = os.getenv("USERNAME")
URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



# Changing functions to Methods, organised in Classes (Objects)
class Event:
    def scrape(self, url):
        # Scrape the page source from a URL
        # we are setting the User-Agent to make it look like we’re using a popular web browser via headers
        response = requests.get(url, headers=HEADERS)
        content = response.text
        return content

    def extract(self, source):
        # Extracts only the needed info
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        with smtplib.SMTP_SSL(HOST, PORT, context=MY_CONTEXT) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, message)
        print("Mail was sent")


class Database:
    def __init__(self, db_path):
        # Establish a connection and a cursor
        self.connection = sqlite3.connect(db_path)

    def store(self, extracted):
        # Stores the event in the database
        row = extracted.split(',')
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        row = extracted.split(',')
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city,date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == '__main__':
    while True:
        # Create an instance of an event
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            database = Database(db_path='data.db')
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                email = Email()
                email.send(message="Hey, a new event was found")

        time.sleep(2)