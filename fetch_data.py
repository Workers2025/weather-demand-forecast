import requests
import pandas as pd
import datetime

OPENWEATHER_API_KEY = "c9e561773201d01884378a1345a9efed"
ABSTRACT_API_KEY = "65ff348e62cf48788773d76b6d0d63df"

def fetch_weather_data(city="Chennai"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    weather_list = []
    for item in data['list']:
        weather = {
            "datetime": item['dt_txt'],
            "temperature": item['main']['temp'],
            "humidity": item['main']['humidity'],
            "wind_speed": item['wind']['speed'],
            "weather_main": item['weather'][0]['main']
        }
        weather_list.append(weather)
    return pd.DataFrame(weather_list)

def fetch_holiday_data(country="IN"):
    today = datetime.date.today()
    url = f"https://holidays.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&country={country}&year={today.year}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list):
                holidays = [item['date'] for item in data]
            elif isinstance(data, dict) and 'date' in data:
                holidays = [data['date']]
            else:
                holidays = []
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            holidays = []
    else:
        print(f"Failed to fetch holidays: {response.status_code}")
        holidays = []
        
    return holidays

if __name__ == "__main__":
    weather_df = fetch_weather_data()
    holidays = fetch_holiday_data()
    print(weather_df.head())
    print(holidays)
