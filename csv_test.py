import csv

data = {'Brand': 'Renault', 
 'Model': 'K9K', 
 'Generation': 'Scenic II (Phase I)',
 'Production Years': '2003 year',
 'Engine Specs': ' Power: Internal Combustion engine; Power: 101 Hp @ 4000 rpm.; Power: 69.1 Hp/l; Torque: 200 Nm @ 1900 rpm. 147.51 lb.-ft. @ 1900 rpm.;',
 'Body Type': 'Minivan',
 'Fuel Type': 'Diesel',
 'Horsepower': 1,
 'Torque': 200,
 'Drive Type': 'Front wheel drive',
 'Transmission': '5 gears, manual transmission',
 'Image URLs': {'images': ['https://www.auto-data.net/images/f51/Renault-Scenic-II-Phase-I.jpg', 'https://www.auto-data.net/images/f44/Renault-Scenic-II-Phase-I.jpg']}
}
with open("data.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(data)
