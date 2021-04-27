#import pyjokes
import requests
from sqlalchemy import create_engine
import time

webhook_url = ""


# Connect to Postgres database from inside container:
conn = create_engine('postgres://postgres:postgres@postgres:5432/db', echo=True).connect()

# Connect to Postgres database from local machine:
# conn = create_engine('postgres://postgres:postgres@localhost:5555/db', echo=True).connect()

# Query database
query = "SELECT * FROM tweets ORDER BY timestamp DESC LIMIT(1)"


while True:
    result = conn.execute(query).fetchall()
    image_url = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/271/neutral-face_1f610.png'
    if result[0]['sentiment']=='positive':
        image_url = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/271/slightly-smiling-face_1f642.png'
    elif result[0]['sentiment']=='negative':
        image_url = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/271/slightly-frowning-face_1f641.png'

    twitter_text = result[0]['text']
    score = round(result[0]['score'],2)
    sentiment = result[0]['sentiment']


    final_text = '*Feelings about vaccination*\n\n' + twitter_text + '\n\n*Vader score: ' + str(score) + '*\n---'

    data = {'blocks': [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": final_text
                },
                "accessory": {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": sentiment
                }
            }]
    }

    print(data)

    #Posten:
    #requests.post(url=webhook_url, json = data)

    time.sleep(30.0)



