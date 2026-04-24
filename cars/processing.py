from bs4 import BeautifulSoup
import json
import re

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
    brand_car = []
    soup = BeautifulSoup(spec_brand_cars_html , 'html.parser') 
    
    cars = soup.find_all("a",class_="modeli")
    
    for car in cars:
        brand_car.append(car["href"].split("/en/")[1])
    return brand_car



def get_generations(scrape_generations_html) -> list:
    """ 
    Recive html object as a string and returns Specs for all generations of car of specs brand: acura-adx-generation-10407
    """
    brands = []
    soup = BeautifulSoup(scrape_generations_html , 'html.parser') 
    
    gen_bloks = soup.find_all("td", class_ = "i")
    
    for block in gen_bloks:
        generation = block.find("a", class_ = "position")
        brands.append(generation["href"].split("/en/")[1])

    return brands
        
        
def get_types_generations(type_car_link) -> list:
    """ 
    Recive html object as a string and returns Specs for all types of generations of car of specs brand: Specs of Acura NSX II Coupe Type S 3.5 V6 (600 Hp) Hybrid SH-AWD DCT /2022/ 
    """
    types_generations = []
    soup = BeautifulSoup(type_car_link , 'html.parser') 
    
    types_blocks = soup.find_all("td", class_ ="i")
    for block in types_blocks:
        types_gen = block.find("a")
        types_generations.append(types_gen["href"].split("/en/")[1])
        
    return types_generations


def get_raw_info(info_html) -> dict:
    """ 
    Get and extract all needed info about car: barnd, model, generation..,
    """
    info = {}
    soup = BeautifulSoup(info_html, "html.parser")

    table = soup.find("table", class_="cardetailsout car2")
    if table:
        for row in table.find_all("tr"):
            key = row.find("th")
            value = row.find("td")

            if not key or not value:
                continue

            k = key.text.strip()
            v = value.get_text(" ", strip=True)

            if "Brand" in k:
                info["Brand"] = v

            elif "Model" in k:
                info["Model"] = v

            elif "Generation" in k:
                info["Generation"] = v

            elif "Start of production" in k:
                info["Production Years"] = v

            elif "Power" in k:
                hp = re.search(r"(\d+)\s*Hp", v)
                if hp:
                    info["Horsepower"] = int(hp.group(1))
                info["Engine Specs"] = info.get("Engine Specs", "") + f" Power: {v};"

            elif "Torque" in k:
                tq = re.search(r"(\d+)\s*Nm", v)
                if tq:
                    info["Torque"] = int(tq.group(1))
                info["Engine Specs"] = info.get("Engine Specs", "") + f" Torque: {v};"

            elif "Fuel Type" in k:
                info["Fuel Type"] = v

            elif "Number of gears" in k:
                info["Transmission"] = v

            elif "Drive wheel" in k:
                info["Drive Type"] = v

            elif "Body type" in k:
                info["Body Type"] = v

    script_text = " ".join([s.get_text() for s in soup.find_all("script")])
    bigs = re.findall(r'bigs\[\d+\]\s*=\s*"([^"]+)"', script_text)
    base_url = "https://www.auto-data.net/images/"
    info["Image URLs"] = {
        "images": [base_url + x for x in bigs[:3]],
    }
    return info