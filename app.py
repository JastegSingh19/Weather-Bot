from flask import Flask,request,jsonify
import requests
import datetime

app=Flask(__name__)
@app.route('/',methods=['POST'])
def index():
    data=request.get_json()
    action = data.get('queryResult').get('action')
    if action=="Present_Prediction":
        print(action)
        location = data['queryResult']['parameters']['geo-city']
        date = data['queryResult']['parameters']['date']
        current_day = datetime.date.today()
        date = date[8:10]
        date = int(date)
        current_day = current_day.day
        days = date - current_day
        print(days)
        cf = fetch_weather_data(location, days)
        days=days-1
        cf = cf['forecast']['forecastday'][days]['day']['avgtemp_c']
        if (cf < 25):
            response = {
                'fulfillmentText': "The temperature is {}C/{}F. It's chilly on {}th in {}. Wear a Jacket".format(cf,
                                                                                                               round((
                                                                                                                       9 / 5 * cf + 32),
                                                                                                                   2),
                                                                                                               date,
                                                                                                               location)
            }
        else:
            response = {
                'fulfillmentText': "The temperature is {}C/{}F. It's hot on {}th in {}. Wear some light clothes".format(
                    cf, round((9 / 5 * cf + 32), 2), date, location, )
            }
    elif action=="Holiday_Prediction":
        location=data['queryResult']['parameters']['geo-city']
        date=data['queryResult']['parameters']['date']
        date=date[:10]
        ck=fetch_holiday_prediction(location,date)
        sum=0
        for x in range(0,8):
           sum=sum +ck['forecast']['forecastday'][0]['hour'][x]['chance_of_rain']
        sum=sum/7
        sum=round(sum,2)
        if (sum < 50):
            response={
                'fulfillmentText':"The avg temperature of the day will be {} C/{} F.The chance of rain is{} mm. You can plan your holiday".format(ck['forecast']['forecastday'][0]['day']['avgtemp_c'],ck['forecast']['forecastday'][0]['day']['avgtemp_f'],sum)
            }
        else:

            response={
                'fulfillmentText':"The avg temperature of the day will be {} C/{} F.The chance of rain is {} mm. Your holiday may be runied by rain".format(ck['forecast']['forecastday'][0]['day']['avgtemp_c'],ck['forecast']['forecastday'][0]['day']['avgtemp_f'],sum)
            }
    elif action=="Time_Zone":
        location = data['queryResult']['parameters']['geo-city']
        ck=fetch_time(location)
        response={
            'fulfillmentText':"The time in {} is {}".format(ck['location']['name'],ck['location']['localtime'])
        }
    elif action=="Astronomical_data":
        location=data['queryResult']['parameters']['geo-city']
        date = data['queryResult']['parameters']['date-time']
        date = date[:10]
        print(date)
        ck=fetch_astronomy(location,date)
        response={
            'fulfillmentText':"The sun will rise at {} and will set at {}.The moon wil rise at {} and set at {}.The moonphase will be {}".format(ck['astronomy']['astro']['sunrise'],ck['astronomy']['astro']['sunset'],ck['astronomy']['astro']['moonrise'],ck['astronomy']['astro']['moonset'],ck['astronomy']['astro']['moon_phase'])
        }

    return jsonify(response)
def fetch_weather_data(location,days):

    url="http://api.weatherapi.com/v1/forecast.json?key=7f5cef1229d04af08a953540230904&q={}&days={}&aqi=no&alerts=no".format(location,days)
    response=requests.get(url)
    response=response.json()
    print(response)
    return response
def fetch_holiday_prediction(location,dat):
    url="http://api.weatherapi.com/v1/future.json?key=7f5cef1229d04af08a953540230904&q={}&dt={}".format(location,dat)
    response=requests.get(url)
    response=response.json()
    print(response)
    return response
def fetch_time(location):
    url="http://api.weatherapi.com/v1/timezone.json?key=7f5cef1229d04af08a953540230904&q={}".format(location)
    response = requests.get(url)
    response = response.json()
    return response
def fetch_astronomy(location,date):
    url="http://api.weatherapi.com/v1/astronomy.json?key=7f5cef1229d04af08a953540230904&q={}&dt={}".format(location,date)
    response = requests.get(url)
    response = response.json()
    return response
if __name__=="__main__":
    app.run(debug=True,port=5001)

