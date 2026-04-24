from cars.scraper import CarsParser
from cars.processing import *
import os
cookies = os.getenv("cookies")

car_scraper = CarsParser(cookies)

# brands
car_brands_general = car_scraper.scrape_brands()
href_list = extract_cars_href(car_brands_general)

# model of brand
for i in range(3):
    car_spec_brand = car_scraper.scrape_brand_cars(href_list[i])
    spec_brand_cars_list = get_brand_car(car_spec_brand)

    # generations
    car_generations_html = car_scraper.scrape_generations(spec_brand_cars_list[0])
    generations = get_generations(car_generations_html)

    # nested types of generations
    type_generations_html = car_scraper.scrape_types_generations(generations[0])
    nested_types = get_types_generations(type_generations_html)

    #info about car
    car_info = car_scraper.scrape_car_info(nested_types[0])
    info = get_raw_info(car_info)
    print(info, end="\n\n")

