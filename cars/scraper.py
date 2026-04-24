from curl_cffi import requests as cfr
from typing import Any
from cars.processing import extract_cars_href



class CarsParser:
    def __init__(self, cookies):
        self.cookies = cookies
        self.base_url = "https://www.auto-data.net/en/"
        self.headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate, br, zstd",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0"
                }
        
    def scrape_brands(self) -> str:
        """ 
        Example of link : /en/
        Extracts models/barnds or cars: Acura, Alfa Romeo, Alpina, Aston Martin... and returns html object as string
        """
        url = self.base_url
        print(url)
        response = cfr.get(url=url, headers=self.headers, cookies=self.cookies, impersonate="chrome120")
        cars_brands_html = response.text
        return cars_brands_html
    
    def scrape_brand_cars(self, brand_link) -> str:
        """ 
        Example of link : /en/acura-brand-6
        Extracts cars of specific model:  Acura ADX, Acura CL, Acura CSX, Acura EL.. and returns html object as string
        """
        url = f"{self.base_url}{brand_link}" 
        print(url)
        response = cfr.get(url=url, headers=self.headers, cookies=self.cookies, impersonate="chrome120")
        spec_brand_cars_html = response.text
        return spec_brand_cars_html
    
    
    def scrape_generations(self, brand_car_link) -> str:
        """ 
        Example of link : /en/acura-adx-model-3586
        Extracts Specs for all generations of {model of car(Acura ADX)}:  Acura ADX and returns html object as string
        """
        url = f"{self.base_url}{brand_car_link}" 
        print(url)
        response = cfr.get(url=url, headers=self.headers, cookies=self.cookies, impersonate="chrome120")
        generations_html = response.text
        return generations_html
    
    
    def scrape_types_generations(self, type_car_link) -> str:
        """ 
        Example of link : /en/acura-nsx-ii-coupe-generation-5712
        Extracts Specs for all nested types of generations of {model of car(Acura NSX)}:  Acura NSX II Coupe, Acura NSX I and returns html object as string
        """
        
        url = f"{self.base_url}{type_car_link}"
        print(url)
        response = cfr.get(url=url, headers=self.headers, cookies=self.cookies, impersonate="chrome120")
        type_generations_html = response.text
        return type_generations_html
        
    def scrape_car_info(self, nested_types) -> str:
        """ 
        Example of link : en/aston-martin-db6-mark-ii-4.0-330hp-24185
        Extracts all info about car: 
        Brand	Aston Martin
        Model 	DB6
        Generation 	DB6 Mark II
        ...
        """

        url = f"{self.base_url}{nested_types}"
        print(url)
        response = cfr.get(url=url, headers=self.headers, cookies=self.cookies, impersonate="chrome120")
        info_html = response.text
        return info_html