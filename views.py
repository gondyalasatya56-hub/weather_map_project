from django.shortcuts import render
import requests


def weather_home(request):

    weather = None
    error = None

    if request.method == "POST":

        city = request.POST.get("city")

        # Put your OpenWeather API key here
        api_key = "your api key"

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }

        try:

            response = requests.get(url, params=params)

            data = response.json()

            if response.status_code == 200:

                weather = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"]
                }

            elif response.status_code == 401:

                error = "Invalid API key. Please check your OpenWeather API key."

            elif response.status_code == 404:

                error = "City not found. Please enter a valid city."

            else:

                error = f"Weather API error: {response.status_code}"

        except requests.exceptions.RequestException:

            error = "Unable to connect to the weather service."

        except Exception:

            error = "Something went wrong. Please try again."

    return render(
        request,
        "weather/weather.html",
        {
            "weather": weather,
            "error": error
        }
    )