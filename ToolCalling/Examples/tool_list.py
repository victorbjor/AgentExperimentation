private_api_key = '5b63900ecc35423189b92609242310'

def test_func(param1: str, param2: str) -> int:
    """Just a silly test function"""
    return 5

def get_todays_date() -> str:
    """
    Get todays date

    :return: todays date as a string of format %Y-%m-%d
    """
    from datetime import datetime
    return datetime.today().strftime("%Y-%m-%d")

def get_current_weather(city: str, date: str, private_key: str) -> str:
    """Fetches current whether from API

    :param city: city name
    :param private_key: private API key
    :return: current weather from weather API service
    """
    import requests
    private_key = '5b63900ecc35423189b92609242310'
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={private_key}&q={city}&aqi=yes')
    return response.content.decode('utf-8')
