import requests
import datetime
import time
import smtplib

now = datetime.datetime.now()
ABH_LAT = 19.186354
ABH_LNG = 73.191948
ABH_TIMEZONE = "Asia/Kolkata"
MY_EMAIL = "prav64.dev@gmail.com"
MY_PASSWORD = "vbfwjkxnoxvhaozo"


def is_iss_nearby(loc_lat, loc_lng):
    notifier_response = requests.get(url='http://api.open-notify.org/iss-now.json')
    # print(response.status_code)
    notifier_response.raise_for_status()
    current_position = notifier_response.json()['iss_position']
    longitude = float(current_position['longitude'])
    latitude = float(current_position['latitude'])
    print(f"ISS Location: \t\t\t{latitude} {longitude}")
    if (loc_lat - 5 <= latitude <= loc_lat + 5) and (loc_lng - 5 <= longitude <= loc_lng + 5):
        return True
    else:
        return False


params_for_sunrise_sunset = {
    "lat":ABH_LAT,
    "lng":ABH_LNG,
    "tzid":ABH_TIMEZONE,
    "formatted": 0
}
response = requests.get(url="https://api.sunrise-sunset.org/json", params=params_for_sunrise_sunset)
response.raise_for_status()
data = response.json()["results"]


print(f"Ambarnath's Location: \t{ABH_LAT} {ABH_LNG}")
while True:
    sunrise_hour = int(data["sunrise"].split("T")[1].split("+")[0].split(":")[0])
    sunset_hour = int(data["sunset"].split("T")[1].split("+")[0].split(":")[0])
    time_now = str(now).split(" ")[1].split(".")[0]

    if is_iss_nearby(ABH_LAT, ABH_LNG):
        if now.hour >= sunset_hour or now.hour <= sunrise_hour:
            with smtplib.SMTP(host="smtp.google.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg="Subject: Watchout the ISS is in the sky!\n\nLook up Look up!"
                )
        else:
            print("Lookup but you can't see it")

    time.sleep(60)
