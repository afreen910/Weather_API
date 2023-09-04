
from dateutil import parser,tz
from random import shuffle
import requests
import pandas as pd


URL = 'http://api.weatherapi.com/v1/history.json'
API_KEY = 'xxx'

class WeatherApi:

  def get_historical_data(self):

    """
    Make one request to the history.json url with the required parameters.
    Return the JSON data
    """
    city = 'Amsterdam'
    start_date = '2023-08-01'
    end_date = '2023-08-25'
    history_url = URL \
                  +'?q='+city \
                  +'&dt='+start_date \
                  +'&end_dt='+end_date \
                  +'&key='+API_KEY

    response = requests.get(url=history_url)
    json_data = response.json()
    return json_data


# new func
  def temprature_info(self,raw_data):
    """

    """

    day_dict={}
    # raw_data = self.get_historical_data()

    for i,day_info in enumerate(raw_data['forecast']['forecastday']):
      sub_dict={}

      sub_dict['max_temp_c'] = day_info['day']['maxtemp_c']
      sub_dict['min_temp_c'] = day_info['day']['mintemp_c']
      sub_dict['condition'] = day_info['day']['condition']['text']

      var_sum=0

      for temp_info in day_info['hour']:
        var_sum= var_sum+temp_info['temp_c']

      max_temp=day_info['hour'][0]['temp_c']
      max_hour=''

      for temp_info in day_info['hour']:
        if max_temp < temp_info['temp_c']:
          max_temp= temp_info['temp_c']
          max_hour= temp_info['time']

      sub_dict['avg_temp_c'] = var_sum/len(day_info['hour'])
      sub_dict['max_temp_hour'] = max_hour

      day_dict[day_info['date']] = sub_dict

    return day_dict

  def export_to_csv(self):
    df=pd.DataFrame(self.temprature_info())
    df.to_csv('/content/Weather_API/sample.csv')

# new func
  def astro_timings(self,raw_data):

    # raw_data = self.get_historical_data()
    print(raw_data.keys())
    max_sunrise = parser.parse(raw_data['forecast']['forecastday'][0]['astro']['sunrise']).time()
    min_sunrise = parser.parse(raw_data['forecast']['forecastday'][0]['astro']['sunrise']).time()
    max_sunset = parser.parse(raw_data['forecast']['forecastday'][0]['astro']['sunset']).time()
    min_sunset = parser.parse(raw_data['forecast']['forecastday'][0]['astro']['sunset']).time()
    max_date=min_date=max_sunset_date=min_sunset_date = raw_data['forecast']['forecastday'][0]['date']

    print(max_date,min_date,max_sunset_date,min_sunset_date)
    daily_data = raw_data['forecast']['forecastday']
    shuffle(daily_data)
    for day_info in daily_data :
      print(day_info['date'], day_info['astro']['sunrise'], day_info['astro']['sunset'])
      time1= day_info['astro']['sunrise']
      time2 =day_info['astro']['sunset']

      sunrise_time = parser.parse(time1).time()
      sunset_time =  parser.parse(time2).time()

      if max_sunrise < sunrise_time:
        max_sunrise= sunrise_time
        max_date = day_info['date']

      if min_sunrise > sunrise_time:
        min_sunrise= sunrise_time
        min_date = day_info['date']

      if max_sunset < sunset_time:
        max_sunset = sunset_time
        max_sunset_date = day_info['date']

      if min_sunset > sunset_time:
        min_sunset= sunset_time
        min_sunset_date = day_info['date']

    return(f"The maximum sunrise time is {max_sunrise} and the date is {max_date}\n"
          f"The minimum sunrise time is {min_sunrise} and the date is {min_date}\n"
          f"The maximum sunset time is {max_sunset} and the date is {max_sunset_date}\n"
          f"The minimum sunset time is {min_sunset} and the hour is {min_sunset_date}\n")




