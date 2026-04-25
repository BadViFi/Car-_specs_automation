import asyncio
import aiohttp
import os
import time
import csv
import random
import string
from cars.scraper import CarsParser
from cars.processing import *

cookies = os.getenv("cookies")

car_scraper = CarsParser(cookies)

# ---------- INIT BRANDS ----------
car_brands_general = car_scraper.scrape_brands()
brands_ids = extract_cars_href(car_brands_general)




def generate_password(length=6):
    allowed_specials = "!@#$%^&*-_=+?/"
    chars = string.ascii_letters + string.digits + allowed_specials
    return ''.join(random.choice(chars) for _ in range(length))


# ---------- FETCH ----------
async def fetch(session, slug):
    url = f"https://www.auto-data.net/en/{slug}"
    async with session.get(url) as r:
        return await r.text()


# ---------- WORKERS ----------
async def brand_worker(session, brand_queue, model_queue):
    while True:
        brand_id = await brand_queue.get()

        try:
            print(f"processing brand: {brand_id}")

            html = await fetch(session, brand_id)
            models = get_brand_car(html)

            print(f"found {len(models)} models")

            for model in models:
                print(f"[MODEL] {model}")
                await model_queue.put(model)

        except Exception as e:
            print(f"[ERROR worker:", e)

        finally:
            brand_queue.task_done()

async def model_worker(session, model_queue,  generation_queue):
    while True:
        model_id = await model_queue.get()
        
        try:
            print(f"proccesing models: {model_id}")
            
            html = await fetch(session, model_id)
            generations = get_generations(html)
            
            print(f"found {len(generations)} generations")
            
            for gen in generations:
                print(f"[GENERATION] {gen}")
                await generation_queue.put(gen)
                
        except Exception as e:
            print(f"[ERROR worker:", e)
            
        finally:
            model_queue.task_done()
            



async def generation_worker(session, generation_queue,  types_generations):
    while True:
        gener_id = await generation_queue.get()
        
        try:
            print(f"proccesing generation: {gener_id}")
            
            html = await fetch(session, gener_id)
            types_gens = get_types_generations(html)
            
            print(f"found {len(types_gens)} types of gens")
            
            for type in types_gens:
                print(f"[TYPE_GEN] {type}")
                await types_generations.put(type)
                
        except Exception as e:
            print(f"[ERROR worker:", e)
            
        finally:
            generation_queue.task_done()
            
            
            
            
async def types_gen_worker(session, types_generations_queue, info_car_queue):
    while True:
        type_id = await types_generations_queue.get()

        try:
            html = await fetch(session, type_id)
            all_info = get_raw_info(html)

            print("[INFORMATION]", all_info)

            await info_car_queue.put(all_info)

        except Exception as e:
            print("[ERROR worker]:", e)

        finally:
            types_generations_queue.task_done()
            

async def writer_worker(info_car_queue):
    while True:
        car_info = await info_car_queue.get()
        # car_info.insert(0, generate_password())
        try:
            with open("data.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(car_info)
                
        except Exception as e:
            print("[Error worker]:", e)
            
        finally:
            info_car_queue.task_done()

# ---------- MAIN ----------
async def main():
    brand_queue = asyncio.Queue()
    model_queue = asyncio.Queue()
    generation_queue = asyncio.Queue()
    types_generations_queue = asyncio.Queue()
    info_car_queue = asyncio.Queue()

    # fill queue
    for brand_id in brands_ids:
        await brand_queue.put(brand_id)

    print(f"Loaded {len(brands_ids)} brands\n")

    async with aiohttp.ClientSession() as session:
        start = time.perf_counter()
        # start workers
        brand_workers = [
            asyncio.create_task(
                brand_worker(session, brand_queue, model_queue)
            )
            for i in range(10)
        ]
        
        models_workers = [
            asyncio.create_task(
                model_worker(session, model_queue, generation_queue)
            )
            for i in range(10)
        ]
        
        generations_workers = [
            asyncio.create_task(
                generation_worker(session, generation_queue, types_generations_queue)
            )
            for i in range(10)
        ]
        
        infos_workers = [
            asyncio.create_task(
                types_gen_worker(session, types_generations_queue, info_car_queue)
            )
            for i in range(10)
        ]
        
        write_info_workers = [
            asyncio.create_task(
                writer_worker(info_car_queue)
            )
        ]
        
        await brand_queue.join()

        # stop workers
        for w in brand_workers:
            w.cancel()
            
        await model_queue.join()
        
        for w in models_workers:
            w.cancel()
            
        await generation_queue.join()
        
        for w in generations_workers:
            w.cancel()
            
        await types_generations_queue.join()
        
        for w in infos_workers:
            w.cancel()
        
        await info_car_queue.join()
        
        for w in write_info_workers:
            w.cancel()
            
            
        end = time.perf_counter()
        print("\nDONE: all brands processed")
        print(f"Time elapsed: {end - start:.6f} seconds")
            


# ---------- RUN ----------
asyncio.run(main())