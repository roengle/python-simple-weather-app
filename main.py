import requests

# Api keys for geocoding and weather
owm_api_key = ''
myptv_api_key = ''


# A function that gets the latitude and longitude of a given postal code for the United States. Uses the MyPTV
# Geocoding API.
#
# Is a helper method called from within print_weather_for_zip(zipcode).
#
# Takes in one argument - the postal code(zipcode).
# Returns two values - latitude and longitude.
def getLatLongFromZip(zipcode):
    # Define the base url for the GET request, defining what should be replaced
    base_url = "https://api.myptv.com/geocoding/v1/locations/by-address?country=US&postalCode={postal_code}&apiKey={api_key}"
    # Do a GET request on the formatted URL
    response = requests.get(base_url.format(postal_code=zipcode, api_key=myptv_api_key)).json()
    # Get latitude from response
    latitude = response['locations'][0]['referencePosition']['latitude']
    # Get longitude from response
    longitude = response['locations'][0]['referencePosition']['longitude']
    # Return the two values as a tuple
    return latitude, longitude


# A function that prints the weather for a given postal code (zipcode). The function accomplishes this first by
# ascertaining the latitude and longitude for the zip code using a helper method. Then, by using the OpenWeather API,
# retrieves weather statistics for the given latitude and longitude. This method then prints key values from the
# response.
#
# Takes in one argument - the postal code (zipcode).
# Does not return any values.
def print_weather_for_zip(zipcode):
    lat, long = getLatLongFromZip(zipcode)
    formattedUrl = "http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}&mode=json&units=imperial&lang=en"
    response = requests.get(formattedUrl.format(lat=lat, long=long, api_key=owm_api_key)).json()
    print('Weather for {city} ({lat} {long}):'.format(city=response['name'], lat=lat, long=long))
    print('Weather:\n\tMain: {main}\n\tDescription: {desc}'.format(main=response['weather'][0]['main'],
                                                                   desc=response['weather'][0]['description']))
    print(
        'Main:\n\tTemperature: {temp} degrees F\n\tFeels Like: {feels_like} degrees F\n\tMin Temp: {temp_min} degrees F\n\tMax Temp: {temp_max} degrees F\n\tHumidity: {humidity}%'.format(
            temp=response['main']['temp'], feels_like=response['main']['feels_like'],
            temp_min=response['main']['temp_min'],
            temp_max=response['main']['temp_max'], humidity=response['main']['humidity']
        ))


# Main execution
#
# Program requires an internet connection as it makes requests over the internet to various APIs
if __name__ == '__main__':
    # Loop until we want to exit
    while True:
        # Prompt for new zip
        print()
        print('Enter a zipcode to get weather for (enter -1 to exit):')
        # Get input
        zip = input()

        # Do input validation to make sure zipcode is a 5-digit number
        while len(zip) != 5 or (not zip.isnumeric()):
            if zip == '-1':
                break
            print('Invalid input. Please enter a 5-digit number:')
            zip = input()

        # Exit if input is -1
        if zip == '-1':
            print('Goodbye!')
            break
        # Input is valid, call function to print its weather
        print_weather_for_zip(zip)
