from bs4 import BeautifulSoup
import json


def extract_cars_href(html) -> list:
    """ 
    Recive html object as a string and returns brand names to all of car brands: acura-brand-6, alfa-romeo-brand-11, alpina-brand-16
    """
    car_brand = []
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find_all("a", class_="marki_blok")
    for block in blocks:
        car_brand.append(block["href"].split("/en/")[1])
        
    return car_brand


def get_brand_car(spec_brand_cars_html) -> list:
    """ 
    Recive html object as a string and returns all models of car of specs brand: acura-adx-model-3586, acura-cl-model-138, acura-csx-model-143
    """
    brand_car_links = []
    soup = BeautifulSoup(spec_brand_cars_html , 'html.parser') 
    
    cars = soup.find_all("a",class_="modeli")
    
    for car in cars:
        brand_car_links.append(car["href"].split("/en/")[1])
    return brand_car_links



def get_generations(scrape_generations_html) -> list:
    """ 
    Recive html object as a string and returns Specs for all generations of car of specs brand: acura-adx-generation-10407
    """
    brands_links = []
    soup = BeautifulSoup(scrape_generations_html , 'html.parser') 
    
    gen_blokc = soup.find_all("td", class_ = "i")
    
    for block in gen_blokc:
        generation = block.find_all("a", class_ = "position")
        brands_links.append(generation[0]["href"].split("/en/")[1])

    return brands_links
        
        