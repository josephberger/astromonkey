import yaml
from models.area import Area
from models.location import Location

def area_loader(id):

    area = Area(id)

    with open(f"game_data/area/{id}.yaml", "r") as file:
        area_info = yaml.full_load(file)

    area.id = area_info['id']
    #area.description = area_info['description']
    area.name = area_info['name']
    area.location_index = area_info['location_index']
    area.locations = area_info['locations']

    return area

def locations_loader(info):

    location = []
