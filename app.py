from flask import Flask, render_template, request
import pyowm

app = Flask(__name__)
owm = pyowm.OWM('f6c37586c1df36f113bd0b8844029b93')
weather_mgr = owm.weather_manager()


class WeatherApp:
    def __init__(self, place=None, temperature=None, humidity=None, wind=None):
        self.temperature = temperature
        self.place = place
        self.humidity = humidity
        self.wind = wind

    def name_of_city(self, city_name):
        self.place = city_name
        observation = weather_mgr.weather_at_place(self.place)
        return observation

    def info(self, observation):
        temperature = observation.weather.temperature("celsius")["temp"]
        humidity = observation.weather.humidity
        wind = observation.weather.wind()
        self.temperature = temperature
        self.humidity = humidity
        self.wind = wind


@app.route('/', methods=['GET', 'POST'])
def home():
    weather_info = None

    if request.method == 'POST':
        city_name = request.form['search_query']
        observation = weather_mgr.weather_at_place(city_name)
        temperature = observation.weather.temperature("celsius")["temp"]
        humidity = observation.weather.humidity
        wind = observation.weather.wind()
        print(city_name)
        print("Temperature:", temperature)  # Add this print statement
        print("Humidity:", humidity)  # Add this print statement
        print("Wind:", wind)  # Add this print statement

        weather_info = {
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind["speed"]
        }

    return render_template('home.html', weather_info=weather_info)
    # return render_template('home.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/faqs')
def faqs():
    return render_template('FAQs.html')


@app.route('/contact')
def contact():
    return render_template('Contact.html')


if __name__ == '__main__':
    app.run()
