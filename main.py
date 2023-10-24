import requests as api
import datetime as dt
import smtplib as mail
import time

MY_LAT = 38.571278700336684#51.587351
MY_LNG = -9.0388247860927#-0.127758
MY_EMAIL = "alexander.pierson1@gmail.com"
MY_PASSWORD = "yzcwkjxzdookirmh"

def is_iss_overhead():
  response = api.get(url='http://api.open-notify.org/iss-now.json')
  response.raise_for_status()
  data = response.json()

  iss_latitude = float(data["iss_position"]["latitude"])
  iss_longitude = float(data["iss_position"]["longitude"])
  
  #You position is within +5 or -5 degress of the ISS position
  if iss_latitude >= MY_LAT - 5 and iss_latitude <= MY_LAT + 5 and iss_longitude >= MY_LNG - 5 and iss_longitude <= MY_LNG + 5:
    return True


def is_night():
  parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
  }

  response = api.get(url='http://api.sunrise-sunset.org/json', params=parameters)
  response.raise_for_status()
  data = response.json()
  sunrise = int(data["results"]["sunrise"].split('T')[1].split(':')[0])
  sunset = int(data["results"]["sunset"].split('T')[1].split(':')[0])

  time_now = dt.datetime.now().hour

  if time_now.hour >= sunset and time_now.hour <= sunrise:
    return True

while True:
  time.sleep(60)
  if is_iss_overhead() and is_night():
    connection = mail.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
      from_addr=MY_EMAIL,
      to_addrs="botasdario+iss@gmail.com",
      msg="Subject:Look Up\n\nThe ISS is above you in the sky."
    )

#If the ISS is close to my current position
#and it is currently dark
#Then send me an email to tell me to look up.
#Bonus: run the code every 60 seconds
"""
API Status Responses
1XX: Hold On
2XX: Here you go
3XX: Go Away
4XX: You Crewed Up
5XX: I Screwed Up
"""