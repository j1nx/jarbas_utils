from geopy.geocoders import Nominatim
import geocoder
from timezonefinder import TimezoneFinder


def get_timezone(latitude, longitude):
    tf = TimezoneFinder()
    return tf.timezone_at(lng=longitude, lat=latitude)


def geolocate(address, service="geocodefarm"):
    data = {}
    if service == "geocodefarm":
        location_data = geocoder.geocodefarm(address)
    elif service == "osm":
        location_data = geocoder.osm(address)
    elif service == "google":
        location_data = geocoder.google(address)
    elif service == "arcis":
        location_data = geocoder.arcgis(address)
    elif service == "bing":
        location_data = geocoder.bing(address)
    elif service == "canadapost":
        location_data = geocoder.canadapost(address)
    elif service == "yandex":
        location_data = geocoder.yandex(address)
    elif service == "tgos":
        location_data = geocoder.tgos(address)
    else:
        raise ValueError("Unknown geocoder service")

    if location_data.ok:
        location_data = location_data.json
        data["country"] = location_data.get("country")
        data["country_code"] = location_data.get("country_code")
        data["region"] = location_data.get("region")
        data["address"] = location_data.get("address")
        data["state"] = location_data.get("state")
        data["confidence"] = location_data.get("confidence")
        data["lat"] = location_data.get("lat")
        data["lon"] = location_data.get("lng")
        data["city"] = location_data.get("city")
        data["postal"] = location_data.get("postal")
        data["timezone"] = location_data.get("timezone_short")
    else:
        return None
    location = {
        "city": {
            "name": data["city"],
            "state": {
                "name": data["state"],
                "country": {
                    "code": data["country_code"],
                    "name": data["country"]
                }
            }
        },
        "coordinate": {
            "latitude": data["lat"],
            "longitude": data["lon"]
        },
        "timezone": {
            "name": data["timezone"]
        }
    }
    return location


def reverse_geolocate(lat, lon, service="nominatim"):
    if service == "nominatim":
        geolocator = Nominatim()
    else:
        raise ValueError("Unknown geolocator service")
    location = geolocator.reverse(str(lat) + ", " + str(lon), timeout=10).raw
    data = location["address"]

    # config format used by mycroft
    location = {
        "city": {
            "code": data["postcode"],
            "name": data["city"],
            "state": {
                "name": data["state"],
                "country": {
                    "code": data["country_code"],
                    "name": data["country"]
                }
            }
        },
        "coordinate": {
            "latitude": lat,
            "longitude": lon
        }
    }
    return location



