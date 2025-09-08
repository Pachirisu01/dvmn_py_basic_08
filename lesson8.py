import json
import requests
from dotenv import load_dotenv
import os
from geopy.distance import lonlat, distance
import folium


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def load_coffee_shops():
	with open("coffee.json", "r", encoding="CP1251") as my_file:
		file_content = my_file.read()
	return json.loads(file_content)

def get_coffee_list(coffee_data):
	coffee_shops_list = []
	for shop in coffee_data:
		coffee_shop = {
		'latitude' : shop["geoData"]['coordinates'][1],
		'longitude' : shop["geoData"]['coordinates'][0],
		'title': shop["Name"]
		}
		coffee_shops_list.append(coffee_shop)
	return coffee_shops_list	

def main():
	load_dotenv()
	coffee_data = load_coffee_shops()
	coffee_shops_list = get_coffee_list(coffee_data)

	town = input("Где вы находителсь?")
	apikey = os.getenv('apikey')
	location = fetch_coordinates(apikey, town)


	for shop in coffee_shops_list:
		shop_coord = (shop['longitude'], shop['latitude']) 
		shop['distance'] = distance(lonlat(*location), lonlat(*shop_coord)).km


	sort_coffee_shops = sorted(coffee_shops_list, key=lambda x: x['distance'])
	near_coffee_shops = sort_coffee_shops[:5]


	m = folium.Map(location=[location[1], location[0]])

	for shop in near_coffee_shops:
		folium.Marker(
			location = [shop['latitude'],shop['longitude']],
			tooltip = "Click me",
			popup = shop['title'],
			icon = folium.Icon(color = "pink")
		).add_to(m)

	m.save('coffee.html')


if __name__ == '__main__':
    main()




