from cars.scraper import CarsParser
from cars.processing import extract_cars_href, get_brand_car, get_generations
import os
cookies = os.getenv("cookies")

car_scraper = CarsParser(cookies)

# brands
car_brands_general = car_scraper.scrape_brands()
href_list = extract_cars_href(car_brands_general)

# model of brand
car_spec_brand = car_scraper.scrape_brand_cars(href_list[0])
spec_brand_cars_list = get_brand_car(car_spec_brand)

# generations
car_generations_html = car_scraper.scrape_generations(spec_brand_cars_list[7])
generations = get_generations(car_generations_html)


print(generations)

