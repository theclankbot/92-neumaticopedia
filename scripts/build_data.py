#!/usr/bin/env python3
"""
Build comprehensive tire/vehicle data from multiple sources.
Sources:
  1. NHTSA vPIC API - model lists, basic specs (free, no auth)
  2. Known tire specifications for common European/Japanese vehicles
  3. Cross-referenced data
"""

import json
import os
import sys
import time
import urllib.request
import re
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# BRAND DEFINITIONS (with proper Spanish market data)
# ============================================================
BRANDS = [
    {"slug": "toyota", "name": "Toyota", "country": "Japón", "founded": "1937", "hq": "Toyota City, Japón", "description": "Toyota Motor Corporation es el mayor fabricante de automóviles del mundo por volumen de ventas. Fundada en 1937 por Kiichiro Toyoda, la marca japonesa es conocida por su fiabilidad, eficiencia y liderazgo en tecnología híbrida con modelos como el Prius y el Corolla."},
    {"slug": "volkswagen", "name": "Volkswagen", "country": "Alemania", "founded": "1937", "hq": "Wolfsburgo, Alemania", "description": "Volkswagen es una de las marcas de automóviles más vendidas en Europa y el mundo. Fundada en 1937, la marca alemana es reconocida por modelos icónicos como el Golf, el Polo y el Tiguan, combinando ingeniería alemana con accesibilidad."},
    {"slug": "seat", "name": "SEAT", "country": "España", "founded": "1950", "hq": "Martorell, España", "description": "SEAT es la única marca española de fabricación de automóviles en serie. Fundada en 1950, con sede en Martorell (Barcelona), es conocida por modelos deportivos y accesibles como el León, el Ibiza y el Arona. Forma parte del Grupo Volkswagen desde 1986."},
    {"slug": "cupra", "name": "CUPRA", "country": "España", "founded": "2018", "hq": "Martorell, España", "description": "CUPRA nació en 2018 como marca independiente del grupo SEAT, especializada en vehículos deportivos y de alto rendimiento. Con modelos como el Formentor y el Born eléctrico, combina diseño español con tecnología del Grupo Volkswagen."},
    {"slug": "hyundai", "name": "Hyundai", "country": "Corea del Sur", "founded": "1967", "hq": "Seúl, Corea del Sur", "description": "Hyundai Motor Company es el tercer mayor fabricante de automóviles del mundo. Fundada en 1967, la marca surcoreana ha experimentado un crecimiento espectacular con modelos como el Tucson, el i30 y la gama IONIQ de vehículos eléctricos."},
    {"slug": "kia", "name": "Kia", "country": "Corea del Sur", "founded": "1944", "hq": "Seúl, Corea del Sur", "description": "Kia Corporation es uno de los fabricantes de automóviles con mayor crecimiento en Europa. Fundada en 1944, la marca surcoreana ofrece modelos con excelente relación calidad-precio como el Sportage, el Ceed y el EV6, con 7 años de garantía."},
    {"slug": "peugeot", "name": "Peugeot", "country": "Francia", "founded": "1810", "hq": "París, Francia", "description": "Peugeot es una de las marcas de automóviles más antiguas del mundo. Fundada en 1810, la marca francesa forma parte del grupo Stellantis y es conocida por modelos como el 208, el 308 y el 3008, con un diseño distintivo y motorización eficiente."},
    {"slug": "renault", "name": "Renault", "country": "Francia", "founded": "1899", "hq": "Boulogne-Billancourt, Francia", "description": "Renault es uno de los mayores fabricantes europeos de automóviles. Fundada en 1899, la marca francesa lidera la electrificación en Europa con modelos como el Megane E-Tech y mantiene clásicos como el Clio y el Captur entre los más vendidos."},
    {"slug": "citroen", "name": "Citroën", "country": "Francia", "founded": "1919", "hq": "París, Francia", "description": "Citroën es una marca francesa conocida por su innovación en confort y diseño. Fundada en 1919 por André Citroën, forma parte del grupo Stellantis y ofrece modelos como el C3, C4 y C5 X, con su característico confort de suspensión."},
    {"slug": "bmw", "name": "BMW", "country": "Alemania", "founded": "1916", "hq": "Múnich, Alemania", "description": "BMW (Bayerische Motoren Werke) es un fabricante premium alemán fundado en 1916. Conocida por sus vehículos deportivos y de lujo como las series 3, 5 y X, BMW combina rendimiento dinámico con tecnología avanzada y ahora lidera la electrificación premium con la serie i."},
    {"slug": "audi", "name": "Audi", "country": "Alemania", "founded": "1909", "hq": "Ingolstadt, Alemania", "description": "Audi es una marca premium alemana perteneciente al Grupo Volkswagen. Fundada en 1909, es reconocida por su tecnología Quattro de tracción integral y modelos como el A3, A4, Q5 y la gama e-tron de vehículos eléctricos. Su lema 'Vorsprung durch Technik' refleja su compromiso con la innovación."},
    {"slug": "mercedes", "name": "Mercedes-Benz", "country": "Alemania", "founded": "1926", "hq": "Stuttgart, Alemania", "description": "Mercedes-Benz es una marca de lujo alemana y una de las más reconocidas del mundo. Fundada en 1926, es heredera de Karl Benz, inventor del automóvil. Con modelos como las Clases A, C, E y S, y los SUV GLA, GLC y GLE, Mercedes-Benz define el segmento premium."},
    {"slug": "ford", "name": "Ford", "country": "Estados Unidos", "founded": "1903", "hq": "Dearborn, Michigan, EE.UU.", "description": "Ford Motor Company es uno de los fabricantes de automóviles más importantes del mundo. Fundada en 1903 por Henry Ford, la marca estadounidense es popular en Europa con modelos como el Focus, el Kuga y el Puma, combinando practicidad con tecnología moderna."},
    {"slug": "dacia", "name": "Dacia", "country": "Rumanía", "founded": "1966", "hq": "Mioveni, Rumanía", "description": "Dacia es la marca del grupo Renault especializada en vehículos accesibles y con excelente relación calidad-precio. Fundada en 1966, la marca rumana ha revolucionado el mercado europeo con modelos como el Sandero (el coche más vendido en Europa), el Duster y el Jogger."},
    {"slug": "opel", "name": "Opel", "country": "Alemania", "founded": "1862", "hq": "Rüsselsheim, Alemania", "description": "Opel es una marca alemana perteneciente al grupo Stellantis. Fundada en 1862, es conocida por vehículos prácticos y bien equipados como el Corsa, el Astra y el Mokka, ofreciendo tecnología moderna a precios competitivos en el mercado europeo."},
    {"slug": "nissan", "name": "Nissan", "country": "Japón", "founded": "1933", "hq": "Yokohama, Japón", "description": "Nissan Motor Company es uno de los mayores fabricantes japoneses de automóviles. Fundada en 1933, la marca es pionera en vehículos eléctricos con el LEAF y ofrece una amplia gama de modelos como el Qashqai, el Juke y el X-Trail, muy populares en Europa."},
    {"slug": "mazda", "name": "Mazda", "country": "Japón", "founded": "1920", "hq": "Hiroshima, Japón", "description": "Mazda Motor Corporation es un fabricante japonés conocido por su filosofía de conducción 'Jinba Ittai' (jinete y caballo como uno). Fundada en 1920, ofrece modelos como el Mazda3, CX-5 y MX-5 con su exclusiva tecnología SKYACTIV y diseño Kodo."},
    {"slug": "fiat", "name": "Fiat", "country": "Italia", "founded": "1899", "hq": "Turín, Italia", "description": "Fiat (Fabbrica Italiana Automobili Torino) es la marca italiana más emblemática del automóvil. Fundada en 1899, forma parte del grupo Stellantis y es reconocida por modelos urbanos como el 500, el Panda y el Tipo, con diseño italiano y practicidad urbana."},
    {"slug": "skoda", "name": "Škoda", "country": "República Checa", "founded": "1895", "hq": "Mladá Boleslav, Rep. Checa", "description": "Škoda Auto es uno de los fabricantes de automóviles más antiguos del mundo. Fundada en 1895, la marca checa pertenece al Grupo Volkswagen y ofrece modelos como el Octavia, el Fabia y el Kodiaq, con excelente relación calidad-espacio-precio."},
    {"slug": "volvo", "name": "Volvo", "country": "Suecia", "founded": "1927", "hq": "Gotemburgo, Suecia", "description": "Volvo Cars es una marca sueca reconocida mundialmente por su compromiso con la seguridad. Fundada en 1927, ofrece modelos como el XC60, XC90 y la gama eléctrica EX, combinando diseño escandinavo minimalista con las tecnologías de seguridad más avanzadas."},
    {"slug": "honda", "name": "Honda", "country": "Japón", "founded": "1948", "hq": "Tokio, Japón", "description": "Honda Motor Company es un fabricante japonés reconocido por la fiabilidad de sus motores. Fundada en 1948 por Soichiro Honda, la marca ofrece modelos como el Civic, el CR-V y el Jazz/Fit, con especial atención a la eficiencia y la tecnología híbrida e:HEV."},
]

# ============================================================
# COMPREHENSIVE VEHICLE DATA
# Real tire sizes, PCD, and specs for popular models in Spain
# ============================================================
VEHICLE_DATA = {
    "toyota": [
        {
            "slug": "corolla", "name": "Corolla", "bodyType": "Sedán/Hatchback", "segment": "Compacto",
            "years": "2019-2025", "current": True,
            "generations": [{
                "slug": "2019-2025", "name": "XII Generación (E210)", "yearStart": 2019, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-8-hybrid-122cv", "name": "1.8 Hybrid 122 CV", "engineCode": "2ZR-FXE", "displacement": 1798, "fuelType": "Híbrido", "powerHp": 122, "powerKw": 90, "torqueNm": 142, "transmission": "Automático CVT", "gears": 0, "driveType": "FWD",
                     "lengthMm": 4370, "widthMm": 1790, "heightMm": 1435, "wheelbaseMm": 2640, "weightKg": 1350, "grossWeightKg": 1780,
                     "trunkCapacityL": 361, "fuelTankL": 43, "consumption": 4.5, "co2": 101, "topSpeed": 180, "acceleration0100": 10.9,
                     "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET45",
                     "pcd": "5x114.3", "centerBore": 60.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 103, "threadSize": "M12x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
                    {"slug": "2-0-hybrid-196cv", "name": "2.0 Hybrid 196 CV", "engineCode": "M20A-FXS", "displacement": 1987, "fuelType": "Híbrido", "powerHp": 196, "powerKw": 144, "torqueNm": 190, "transmission": "Automático CVT", "gears": 0, "driveType": "FWD",
                     "lengthMm": 4370, "widthMm": 1790, "heightMm": 1435, "wheelbaseMm": 2640, "weightKg": 1395, "grossWeightKg": 1810,
                     "trunkCapacityL": 361, "fuelTankL": 43, "consumption": 4.8, "co2": 108, "topSpeed": 200, "acceleration0100": 7.5,
                     "tireSizeFront": "225/40 R18", "tireSizeRear": "225/40 R18", "rimSize": "8Jx18 ET50",
                     "pcd": "5x114.3", "centerBore": 60.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 103, "threadSize": "M12x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
                ]
            }]
        },
        {
            "slug": "yaris", "name": "Yaris", "bodyType": "Utilitario", "segment": "Utilitario",
            "years": "2020-2025", "current": True,
            "generations": [{
                "slug": "2020-2025", "name": "IV Generación", "yearStart": 2020, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-hybrid-116cv", "name": "1.5 Hybrid 116 CV", "engineCode": "M15A-FXE", "displacement": 1490, "fuelType": "Híbrido", "powerHp": 116, "powerKw": 85, "torqueNm": 120, "transmission": "Automático CVT", "gears": 0, "driveType": "FWD",
                     "lengthMm": 3940, "widthMm": 1745, "heightMm": 1500, "wheelbaseMm": 2560, "weightKg": 1085, "grossWeightKg": 1480,
                     "trunkCapacityL": 286, "fuelTankL": 36, "consumption": 3.8, "co2": 87, "topSpeed": 175, "acceleration0100": 9.7,
                     "tireSizeFront": "185/65 R15", "tireSizeRear": "185/65 R15", "rimSize": "5.5Jx15 ET45",
                     "pcd": "4x100", "centerBore": 54.1, "offsetMin": 39, "offsetMax": 50, "wheelTorqueNm": 103, "threadSize": "M12x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.3},
                ]
            }]
        },
        {
            "slug": "rav4", "name": "RAV4", "bodyType": "SUV", "segment": "Compacto",
            "years": "2019-2025", "current": True,
            "generations": [{
                "slug": "2019-2025", "name": "V Generación (XA50)", "yearStart": 2019, "yearEnd": 2025,
                "variants": [
                    {"slug": "2-5-hybrid-222cv", "name": "2.5 Hybrid 222 CV", "engineCode": "A25A-FXS", "displacement": 2487, "fuelType": "Híbrido", "powerHp": 222, "powerKw": 163, "torqueNm": 221, "transmission": "Automático CVT", "gears": 0, "driveType": "AWD",
                     "lengthMm": 4600, "widthMm": 1855, "heightMm": 1685, "wheelbaseMm": 2690, "weightKg": 1690, "grossWeightKg": 2155,
                     "trunkCapacityL": 580, "fuelTankL": 55, "consumption": 5.6, "co2": 127, "topSpeed": 180, "acceleration0100": 8.1,
                     "tireSizeFront": "225/60 R18", "tireSizeRear": "225/60 R18", "rimSize": "7Jx18 ET45",
                     "pcd": "5x114.3", "centerBore": 60.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 103, "threadSize": "M12x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.4, "tirePressureRearBar": 2.2, "tirePressureFrontLoadedBar": 2.6, "tirePressureRearLoadedBar": 2.6},
                    {"slug": "2-5-plug-in-hybrid-306cv", "name": "2.5 Plug-in Hybrid 306 CV", "engineCode": "A25A-FXS", "displacement": 2487, "fuelType": "Híbrido enchufable", "powerHp": 306, "powerKw": 225, "torqueNm": 227, "transmission": "Automático CVT", "gears": 0, "driveType": "AWD",
                     "lengthMm": 4600, "widthMm": 1855, "heightMm": 1685, "wheelbaseMm": 2690, "weightKg": 1900, "grossWeightKg": 2350,
                     "trunkCapacityL": 520, "fuelTankL": 55, "consumption": 1.0, "co2": 22, "topSpeed": 180, "acceleration0100": 6.0,
                     "tireSizeFront": "235/55 R19", "tireSizeRear": "235/55 R19", "rimSize": "7.5Jx19 ET45",
                     "pcd": "5x114.3", "centerBore": 60.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 103, "threadSize": "M12x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.5, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.7, "tirePressureRearLoadedBar": 2.7},
                ]
            }]
        },
        {
            "slug": "c-hr", "name": "C-HR", "bodyType": "SUV", "segment": "Compacto",
            "years": "2024-2025", "current": True,
            "generations": [{
                "slug": "2024-2025", "name": "II Generación", "yearStart": 2024, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-8-hybrid-140cv", "name": "1.8 Hybrid 140 CV", "engineCode": "2ZR-FXE", "displacement": 1798, "fuelType": "Híbrido", "powerHp": 140, "powerKw": 103, "torqueNm": 185, "transmission": "Automático CVT", "gears": 0, "driveType": "FWD",
                     "lengthMm": 4360, "widthMm": 1831, "heightMm": 1563, "wheelbaseMm": 2640, "weightKg": 1415, "grossWeightKg": 1830,
                     "trunkCapacityL": 422, "fuelTankL": 43, "consumption": 4.7, "co2": 106, "topSpeed": 175, "acceleration0100": 9.9,
                     "tireSizeFront": "215/60 R17", "tireSizeRear": "215/60 R17", "rimSize": "7Jx17 ET45",
                     "pcd": "5x114.3", "centerBore": 60.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 103, "threadSize": "M12x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
                ]
            }]
        },
        {
            "slug": "yaris-cross", "name": "Yaris Cross", "bodyType": "SUV", "segment": "Utilitario",
            "years": "2021-2025", "current": True,
            "generations": [{
                "slug": "2021-2025", "name": "I Generación", "yearStart": 2021, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-hybrid-116cv", "name": "1.5 Hybrid 116 CV", "engineCode": "M15A-FXE", "displacement": 1490, "fuelType": "Híbrido", "powerHp": 116, "powerKw": 85, "torqueNm": 120, "transmission": "Automático CVT", "gears": 0, "driveType": "FWD",
                     "lengthMm": 4180, "widthMm": 1765, "heightMm": 1560, "wheelbaseMm": 2560, "weightKg": 1190, "grossWeightKg": 1560,
                     "trunkCapacityL": 397, "fuelTankL": 36, "consumption": 4.4, "co2": 100, "topSpeed": 170, "acceleration0100": 11.2,
                     "tireSizeFront": "205/65 R16", "tireSizeRear": "205/65 R16", "rimSize": "6.5Jx16 ET45",
                     "pcd": "4x100", "centerBore": 54.1, "offsetMin": 39, "offsetMax": 50, "wheelTorqueNm": 103, "threadSize": "M12x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
                ]
            }]
        },
        {
            "slug": "camry", "name": "Camry", "bodyType": "Sedán", "segment": "Medio",
            "years": "2019-2025", "current": True,
            "generations": [{
                "slug": "2019-2025", "name": "VIII Generación (XV70)", "yearStart": 2019, "yearEnd": 2025,
                "variants": [
                    {"slug": "2-5-hybrid-218cv", "name": "2.5 Hybrid 218 CV", "engineCode": "A25A-FXS", "displacement": 2487, "fuelType": "Híbrido", "powerHp": 218, "powerKw": 160, "torqueNm": 221, "transmission": "Automático CVT", "gears": 0, "driveType": "FWD",
                     "lengthMm": 4885, "widthMm": 1840, "heightMm": 1445, "wheelbaseMm": 2825, "weightKg": 1595, "grossWeightKg": 2060,
                     "trunkCapacityL": 524, "fuelTankL": 50, "consumption": 4.3, "co2": 98, "topSpeed": 180, "acceleration0100": 8.3,
                     "tireSizeFront": "215/55 R17", "tireSizeRear": "215/55 R17", "rimSize": "7Jx17 ET40",
                     "pcd": "5x114.3", "centerBore": 60.1, "offsetMin": 35, "offsetMax": 50, "wheelTorqueNm": 103, "threadSize": "M12x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
                ]
            }]
        },
        {
            "slug": "land-cruiser", "name": "Land Cruiser", "bodyType": "SUV", "segment": "Grande",
            "years": "2024-2025", "current": True,
            "generations": [{
                "slug": "2024-2025", "name": "Land Cruiser 250", "yearStart": 2024, "yearEnd": 2025,
                "variants": [
                    {"slug": "2-8-diesel-204cv", "name": "2.8 Diesel 204 CV", "engineCode": "1GD-FTV", "displacement": 2755, "fuelType": "Diésel", "powerHp": 204, "powerKw": 150, "torqueNm": 500, "transmission": "Automático 8 vel.", "gears": 8, "driveType": "AWD",
                     "lengthMm": 4925, "widthMm": 1980, "heightMm": 1935, "wheelbaseMm": 2850, "weightKg": 2290, "grossWeightKg": 3060,
                     "trunkCapacityL": 479, "fuelTankL": 80, "consumption": 8.5, "co2": 222, "topSpeed": 175, "acceleration0100": 9.7,
                     "tireSizeFront": "265/65 R18", "tireSizeRear": "265/65 R18", "rimSize": "7.5Jx18 ET55",
                     "pcd": "6x139.7", "centerBore": 106.1, "offsetMin": 50, "offsetMax": 60, "wheelTorqueNm": 130, "threadSize": "M14x1.5", "boltType": "Tuerca",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
    ],
    "volkswagen": [
        {
            "slug": "golf", "name": "Golf", "bodyType": "Hatchback", "segment": "Compacto",
            "years": "2020-2025", "current": True,
            "generations": [{
                "slug": "2020-2025", "name": "VIII Generación (CD)", "yearStart": 2020, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DPCA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                     "lengthMm": 4284, "widthMm": 1789, "heightMm": 1456, "wheelbaseMm": 2636, "weightKg": 1315, "grossWeightKg": 1830,
                     "trunkCapacityL": 381, "fuelTankL": 50, "consumption": 5.6, "co2": 127, "topSpeed": 224, "acceleration0100": 8.5,
                     "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET46",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 42, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                    {"slug": "2-0-tdi-150cv", "name": "2.0 TDI 150 CV", "engineCode": "DFYA", "displacement": 1968, "fuelType": "Diésel", "powerHp": 150, "powerKw": 110, "torqueNm": 360, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                     "lengthMm": 4284, "widthMm": 1789, "heightMm": 1456, "wheelbaseMm": 2636, "weightKg": 1385, "grossWeightKg": 1880,
                     "trunkCapacityL": 381, "fuelTankL": 50, "consumption": 4.4, "co2": 116, "topSpeed": 223, "acceleration0100": 8.6,
                     "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET46",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 42, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                    {"slug": "gti-2-0-tsi-245cv", "name": "GTI 2.0 TSI 245 CV", "engineCode": "DNUA", "displacement": 1984, "fuelType": "Gasolina", "powerHp": 245, "powerKw": 180, "torqueNm": 370, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                     "lengthMm": 4296, "widthMm": 1789, "heightMm": 1456, "wheelbaseMm": 2636, "weightKg": 1430, "grossWeightKg": 1920,
                     "trunkCapacityL": 374, "fuelTankL": 50, "consumption": 7.1, "co2": 161, "topSpeed": 250, "acceleration0100": 6.3,
                     "tireSizeFront": "225/40 R18", "tireSizeRear": "225/40 R18", "rimSize": "7.5Jx18 ET51",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "polo", "name": "Polo", "bodyType": "Utilitario", "segment": "Utilitario",
            "years": "2017-2025", "current": True,
            "generations": [{
                "slug": "2017-2025", "name": "VI Generación (AW)", "yearStart": 2017, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-0-tsi-95cv", "name": "1.0 TSI 95 CV", "engineCode": "DKRF", "displacement": 999, "fuelType": "Gasolina", "powerHp": 95, "powerKw": 70, "torqueNm": 175, "transmission": "Manual 5 vel.", "gears": 5, "driveType": "FWD",
                     "lengthMm": 4074, "widthMm": 1751, "heightMm": 1451, "wheelbaseMm": 2564, "weightKg": 1140, "grossWeightKg": 1610,
                     "trunkCapacityL": 351, "fuelTankL": 40, "consumption": 5.3, "co2": 120, "topSpeed": 187, "acceleration0100": 10.8,
                     "tireSizeFront": "185/65 R15", "tireSizeRear": "185/65 R15", "rimSize": "6Jx15 ET40",
                     "pcd": "5x100", "centerBore": 57.1, "offsetMin": 35, "offsetMax": 43, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "tiguan", "name": "Tiguan", "bodyType": "SUV", "segment": "Compacto",
            "years": "2024-2025", "current": True,
            "generations": [{
                "slug": "2024-2025", "name": "III Generación", "yearStart": 2024, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DPCA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                     "lengthMm": 4539, "widthMm": 1842, "heightMm": 1660, "wheelbaseMm": 2681, "weightKg": 1540, "grossWeightKg": 2100,
                     "trunkCapacityL": 652, "fuelTankL": 58, "consumption": 6.5, "co2": 148, "topSpeed": 207, "acceleration0100": 9.5,
                     "tireSizeFront": "215/65 R17", "tireSizeRear": "215/65 R17", "rimSize": "7Jx17 ET40",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "t-roc", "name": "T-Roc", "bodyType": "SUV", "segment": "Compacto",
            "years": "2017-2025", "current": True,
            "generations": [{
                "slug": "2017-2025", "name": "I Generación", "yearStart": 2017, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DADA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                     "lengthMm": 4236, "widthMm": 1819, "heightMm": 1573, "wheelbaseMm": 2603, "weightKg": 1355, "grossWeightKg": 1840,
                     "trunkCapacityL": 445, "fuelTankL": 50, "consumption": 6.1, "co2": 139, "topSpeed": 212, "acceleration0100": 8.4,
                     "tireSizeFront": "205/60 R16", "tireSizeRear": "205/60 R16", "rimSize": "6.5Jx16 ET44",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "t-cross", "name": "T-Cross", "bodyType": "SUV", "segment": "Utilitario",
            "years": "2019-2025", "current": True,
            "generations": [{
                "slug": "2019-2025", "name": "I Generación", "yearStart": 2019, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-0-tsi-110cv", "name": "1.0 TSI 110 CV", "engineCode": "DKLA", "displacement": 999, "fuelType": "Gasolina", "powerHp": 110, "powerKw": 81, "torqueNm": 200, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                     "lengthMm": 4235, "widthMm": 1760, "heightMm": 1584, "wheelbaseMm": 2551, "weightKg": 1260, "grossWeightKg": 1720,
                     "trunkCapacityL": 385, "fuelTankL": 40, "consumption": 5.6, "co2": 128, "topSpeed": 195, "acceleration0100": 10.0,
                     "tireSizeFront": "205/60 R16", "tireSizeRear": "205/60 R16", "rimSize": "6.5Jx16 ET44",
                     "pcd": "5x100", "centerBore": 57.1, "offsetMin": 38, "offsetMax": 48, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "passat", "name": "Passat", "bodyType": "Familiar", "segment": "Medio",
            "years": "2023-2025", "current": True,
            "generations": [{
                "slug": "2023-2025", "name": "IX Generación (B9)", "yearStart": 2023, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DPCA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                     "lengthMm": 4917, "widthMm": 1852, "heightMm": 1510, "wheelbaseMm": 2841, "weightKg": 1595, "grossWeightKg": 2160,
                     "trunkCapacityL": 690, "fuelTankL": 66, "consumption": 6.0, "co2": 136, "topSpeed": 224, "acceleration0100": 8.8,
                     "tireSizeFront": "215/55 R17", "tireSizeRear": "215/55 R17", "rimSize": "7Jx17 ET44",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
    ],
    "seat": [
        {
            "slug": "leon", "name": "León", "bodyType": "Hatchback/Familiar", "segment": "Compacto",
            "years": "2020-2025", "current": True,
            "generations": [{
                "slug": "2020-2025", "name": "IV Generación (KL)", "yearStart": 2020, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DPCA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                     "lengthMm": 4368, "widthMm": 1800, "heightMm": 1456, "wheelbaseMm": 2686, "weightKg": 1310, "grossWeightKg": 1830,
                     "trunkCapacityL": 380, "fuelTankL": 50, "consumption": 5.6, "co2": 127, "topSpeed": 224, "acceleration0100": 8.4,
                     "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET46",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 42, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "ibiza", "name": "Ibiza", "bodyType": "Utilitario", "segment": "Utilitario",
            "years": "2017-2025", "current": True,
            "generations": [{
                "slug": "2017-2025", "name": "V Generación (6F)", "yearStart": 2017, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-0-tsi-110cv", "name": "1.0 TSI 110 CV", "engineCode": "DKLA", "displacement": 999, "fuelType": "Gasolina", "powerHp": 110, "powerKw": 81, "torqueNm": 200, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                     "lengthMm": 4059, "widthMm": 1780, "heightMm": 1444, "wheelbaseMm": 2564, "weightKg": 1155, "grossWeightKg": 1630,
                     "trunkCapacityL": 355, "fuelTankL": 40, "consumption": 5.1, "co2": 116, "topSpeed": 200, "acceleration0100": 9.3,
                     "tireSizeFront": "185/65 R15", "tireSizeRear": "185/65 R15", "rimSize": "6Jx15 ET40",
                     "pcd": "5x100", "centerBore": 57.1, "offsetMin": 35, "offsetMax": 43, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "arona", "name": "Arona", "bodyType": "SUV", "segment": "Utilitario",
            "years": "2017-2025", "current": True,
            "generations": [{
                "slug": "2017-2025", "name": "I Generación", "yearStart": 2017, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-0-tsi-110cv", "name": "1.0 TSI 110 CV", "engineCode": "DKLA", "displacement": 999, "fuelType": "Gasolina", "powerHp": 110, "powerKw": 81, "torqueNm": 200, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                     "lengthMm": 4145, "widthMm": 1780, "heightMm": 1552, "wheelbaseMm": 2564, "weightKg": 1225, "grossWeightKg": 1695,
                     "trunkCapacityL": 400, "fuelTankL": 40, "consumption": 5.5, "co2": 125, "topSpeed": 195, "acceleration0100": 10.0,
                     "tireSizeFront": "205/60 R16", "tireSizeRear": "205/60 R16", "rimSize": "6.5Jx16 ET44",
                     "pcd": "5x100", "centerBore": 57.1, "offsetMin": 38, "offsetMax": 48, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "ateca", "name": "Ateca", "bodyType": "SUV", "segment": "Compacto",
            "years": "2016-2025", "current": True,
            "generations": [{
                "slug": "2016-2025", "name": "I Generación", "yearStart": 2016, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DADA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                     "lengthMm": 4381, "widthMm": 1841, "heightMm": 1615, "wheelbaseMm": 2631, "weightKg": 1375, "grossWeightKg": 1900,
                     "trunkCapacityL": 510, "fuelTankL": 50, "consumption": 6.3, "co2": 143, "topSpeed": 207, "acceleration0100": 8.6,
                     "tireSizeFront": "215/55 R17", "tireSizeRear": "215/55 R17", "rimSize": "7Jx17 ET44",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
    ],
    "cupra": [
        {
            "slug": "formentor", "name": "Formentor", "bodyType": "SUV", "segment": "Compacto",
            "years": "2020-2025", "current": True,
            "generations": [{
                "slug": "2020-2025", "name": "I Generación", "yearStart": 2020, "yearEnd": 2025,
                "variants": [
                    {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DPCA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                     "lengthMm": 4450, "widthMm": 1839, "heightMm": 1511, "wheelbaseMm": 2680, "weightKg": 1420, "grossWeightKg": 1930,
                     "trunkCapacityL": 420, "fuelTankL": 50, "consumption": 6.4, "co2": 146, "topSpeed": 212, "acceleration0100": 8.7,
                     "tireSizeFront": "225/45 R18", "tireSizeRear": "225/45 R18", "rimSize": "8Jx18 ET44",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                    {"slug": "2-0-tsi-310cv-4drive", "name": "VZ 2.0 TSI 310 CV 4Drive", "engineCode": "DNUE", "displacement": 1984, "fuelType": "Gasolina", "powerHp": 310, "powerKw": 228, "torqueNm": 400, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "AWD",
                     "lengthMm": 4450, "widthMm": 1839, "heightMm": 1511, "wheelbaseMm": 2680, "weightKg": 1565, "grossWeightKg": 2080,
                     "trunkCapacityL": 420, "fuelTankL": 55, "consumption": 8.0, "co2": 182, "topSpeed": 250, "acceleration0100": 4.9,
                     "tireSizeFront": "245/35 R19", "tireSizeRear": "245/35 R19", "rimSize": "8.5Jx19 ET44",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.5, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.7, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "born", "name": "Born", "bodyType": "Hatchback", "segment": "Compacto",
            "years": "2021-2025", "current": True,
            "generations": [{
                "slug": "2021-2025", "name": "I Generación", "yearStart": 2021, "yearEnd": 2025,
                "variants": [
                    {"slug": "58-kwh-204cv", "name": "58 kWh 204 CV", "engineCode": "APP310", "displacement": 0, "fuelType": "Eléctrico", "powerHp": 204, "powerKw": 150, "torqueNm": 310, "transmission": "Automático 1 vel.", "gears": 1, "driveType": "RWD",
                     "lengthMm": 4322, "widthMm": 1809, "heightMm": 1540, "wheelbaseMm": 2765, "weightKg": 1810, "grossWeightKg": 2270,
                     "trunkCapacityL": 385, "fuelTankL": 0, "consumption": 15.8, "co2": 0, "topSpeed": 160, "acceleration0100": 7.3,
                     "tireSizeFront": "215/50 R19", "tireSizeRear": "215/50 R19", "rimSize": "8Jx19 ET45",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.5, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.7, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
        {
            "slug": "leon", "name": "León", "bodyType": "Hatchback", "segment": "Compacto",
            "years": "2020-2025", "current": True,
            "generations": [{
                "slug": "2020-2025", "name": "I Generación CUPRA", "yearStart": 2020, "yearEnd": 2025,
                "variants": [
                    {"slug": "2-0-tsi-300cv", "name": "VZ 2.0 TSI 300 CV", "engineCode": "DNUE", "displacement": 1984, "fuelType": "Gasolina", "powerHp": 300, "powerKw": 221, "torqueNm": 400, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                     "lengthMm": 4398, "widthMm": 1800, "heightMm": 1456, "wheelbaseMm": 2686, "weightKg": 1475, "grossWeightKg": 1980,
                     "trunkCapacityL": 380, "fuelTankL": 50, "consumption": 7.6, "co2": 173, "topSpeed": 250, "acceleration0100": 5.7,
                     "tireSizeFront": "235/35 R19", "tireSizeRear": "235/35 R19", "rimSize": "8Jx19 ET44",
                     "pcd": "5x112", "centerBore": 57.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                     "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                ]
            }]
        },
    ],
}

# Continue with more brands - adding essential models for each
VEHICLE_DATA.update({
    "hyundai": [
        {"slug": "tucson", "name": "Tucson", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "IV Generación (NX4)", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-6-tgdi-hybrid-230cv", "name": "1.6 T-GDi Hybrid 230 CV", "engineCode": "G4FP", "displacement": 1598, "fuelType": "Híbrido", "powerHp": 230, "powerKw": 169, "torqueNm": 350, "transmission": "Automático 6 vel.", "gears": 6, "driveType": "AWD",
                  "lengthMm": 4500, "widthMm": 1865, "heightMm": 1650, "wheelbaseMm": 2680, "weightKg": 1645, "grossWeightKg": 2200,
                  "trunkCapacityL": 616, "fuelTankL": 54, "consumption": 5.9, "co2": 134, "topSpeed": 193, "acceleration0100": 8.0,
                  "tireSizeFront": "235/55 R18", "tireSizeRear": "235/55 R18", "rimSize": "7.5Jx18 ET49.5",
                  "pcd": "5x114.3", "centerBore": 67.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 110, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "i20", "name": "i20", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "III Generación", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-84cv", "name": "1.2 84 CV", "engineCode": "G4LA", "displacement": 1197, "fuelType": "Gasolina", "powerHp": 84, "powerKw": 62, "torqueNm": 118, "transmission": "Manual 5 vel.", "gears": 5, "driveType": "FWD",
                  "lengthMm": 4040, "widthMm": 1775, "heightMm": 1450, "wheelbaseMm": 2580, "weightKg": 1120, "grossWeightKg": 1555,
                  "trunkCapacityL": 352, "fuelTankL": 40, "consumption": 5.6, "co2": 128, "topSpeed": 180, "acceleration0100": 12.5,
                  "tireSizeFront": "185/65 R15", "tireSizeRear": "185/65 R15", "rimSize": "5.5Jx15 ET46",
                  "pcd": "4x100", "centerBore": 54.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 88, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.3},
             ]}]},
        {"slug": "kona", "name": "Kona", "bodyType": "SUV", "segment": "Utilitario", "years": "2023-2025", "current": True,
         "generations": [{"slug": "2023-2025", "name": "II Generación", "yearStart": 2023, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-6-tgdi-hybrid-141cv", "name": "1.6 T-GDi Hybrid 141 CV", "engineCode": "G4FP", "displacement": 1598, "fuelType": "Híbrido", "powerHp": 141, "powerKw": 104, "torqueNm": 265, "transmission": "Automático DCT 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4355, "widthMm": 1825, "heightMm": 1575, "wheelbaseMm": 2660, "weightKg": 1420, "grossWeightKg": 1875,
                  "trunkCapacityL": 466, "fuelTankL": 42, "consumption": 5.2, "co2": 119, "topSpeed": 185, "acceleration0100": 10.4,
                  "tireSizeFront": "215/60 R17", "tireSizeRear": "215/60 R17", "rimSize": "7Jx17 ET51",
                  "pcd": "5x114.3", "centerBore": 67.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 110, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "kia": [
        {"slug": "sportage", "name": "Sportage", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2025", "current": True,
         "generations": [{"slug": "2022-2025", "name": "V Generación (NQ5)", "yearStart": 2022, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-6-tgdi-hybrid-230cv", "name": "1.6 T-GDi Hybrid 230 CV", "engineCode": "G4FP", "displacement": 1598, "fuelType": "Híbrido", "powerHp": 230, "powerKw": 169, "torqueNm": 350, "transmission": "Automático 6 vel.", "gears": 6, "driveType": "AWD",
                  "lengthMm": 4515, "widthMm": 1865, "heightMm": 1650, "wheelbaseMm": 2680, "weightKg": 1660, "grossWeightKg": 2230,
                  "trunkCapacityL": 591, "fuelTankL": 54, "consumption": 5.9, "co2": 134, "topSpeed": 193, "acceleration0100": 8.2,
                  "tireSizeFront": "235/55 R18", "tireSizeRear": "235/55 R18", "rimSize": "7.5Jx18 ET49.5",
                  "pcd": "5x114.3", "centerBore": 67.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 110, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "ceed", "name": "Ceed", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2018-2025", "current": True,
         "generations": [{"slug": "2018-2025", "name": "III Generación (CD)", "yearStart": 2018, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-6-crdi-136cv", "name": "1.6 CRDi 136 CV", "engineCode": "D4FE", "displacement": 1598, "fuelType": "Diésel", "powerHp": 136, "powerKw": 100, "torqueNm": 320, "transmission": "Automático DCT 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4310, "widthMm": 1800, "heightMm": 1447, "wheelbaseMm": 2650, "weightKg": 1380, "grossWeightKg": 1870,
                  "trunkCapacityL": 395, "fuelTankL": 50, "consumption": 4.9, "co2": 129, "topSpeed": 204, "acceleration0100": 10.1,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET50",
                  "pcd": "5x114.3", "centerBore": 67.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 110, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "niro", "name": "Niro", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2025", "current": True,
         "generations": [{"slug": "2022-2025", "name": "II Generación (DE)", "yearStart": 2022, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-6-hev-141cv", "name": "1.6 HEV 141 CV", "engineCode": "G4LE", "displacement": 1580, "fuelType": "Híbrido", "powerHp": 141, "powerKw": 104, "torqueNm": 265, "transmission": "Automático DCT 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4420, "widthMm": 1825, "heightMm": 1570, "wheelbaseMm": 2720, "weightKg": 1420, "grossWeightKg": 1870,
                  "trunkCapacityL": 451, "fuelTankL": 42, "consumption": 4.4, "co2": 100, "topSpeed": 165, "acceleration0100": 10.4,
                  "tireSizeFront": "205/60 R16", "tireSizeRear": "205/60 R16", "rimSize": "6.5Jx16 ET50",
                  "pcd": "5x114.3", "centerBore": 67.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 110, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "peugeot": [
        {"slug": "208", "name": "208", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2019-2025", "current": True,
         "generations": [{"slug": "2019-2025", "name": "II Generación (P21)", "yearStart": 2019, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-puretech-100cv", "name": "1.2 PureTech 100 CV", "engineCode": "EB2ADTS", "displacement": 1199, "fuelType": "Gasolina", "powerHp": 100, "powerKw": 74, "torqueNm": 205, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4055, "widthMm": 1745, "heightMm": 1430, "wheelbaseMm": 2540, "weightKg": 1130, "grossWeightKg": 1580,
                  "trunkCapacityL": 309, "fuelTankL": 44, "consumption": 5.2, "co2": 118, "topSpeed": 188, "acceleration0100": 10.5,
                  "tireSizeFront": "195/55 R16", "tireSizeRear": "195/55 R16", "rimSize": "6.5Jx16 ET23",
                  "pcd": "4x108", "centerBore": 65.1, "offsetMin": 18, "offsetMax": 28, "wheelTorqueNm": 90, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "2008", "name": "2008", "bodyType": "SUV", "segment": "Utilitario", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "II Generación (P24)", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-puretech-130cv", "name": "1.2 PureTech 130 CV", "engineCode": "EB2ADTS", "displacement": 1199, "fuelType": "Gasolina", "powerHp": 130, "powerKw": 96, "torqueNm": 230, "transmission": "Automático EAT8 8 vel.", "gears": 8, "driveType": "FWD",
                  "lengthMm": 4300, "widthMm": 1770, "heightMm": 1530, "wheelbaseMm": 2605, "weightKg": 1240, "grossWeightKg": 1730,
                  "trunkCapacityL": 434, "fuelTankL": 44, "consumption": 5.8, "co2": 131, "topSpeed": 198, "acceleration0100": 9.1,
                  "tireSizeFront": "215/60 R17", "tireSizeRear": "215/60 R17", "rimSize": "7Jx17 ET27",
                  "pcd": "4x108", "centerBore": 65.1, "offsetMin": 22, "offsetMax": 32, "wheelTorqueNm": 90, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "3008", "name": "3008", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2025", "current": True,
         "generations": [{"slug": "2024-2025", "name": "III Generación (P84)", "yearStart": 2024, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-mhev-136cv", "name": "1.2 MHEV 136 CV", "engineCode": "EB2ADTM", "displacement": 1199, "fuelType": "Gasolina MHEV", "powerHp": 136, "powerKw": 100, "torqueNm": 230, "transmission": "Automático eDCT 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4542, "widthMm": 1895, "heightMm": 1641, "wheelbaseMm": 2739, "weightKg": 1520, "grossWeightKg": 2100,
                  "trunkCapacityL": 520, "fuelTankL": 52, "consumption": 5.6, "co2": 127, "topSpeed": 200, "acceleration0100": 9.0,
                  "tireSizeFront": "225/55 R18", "tireSizeRear": "225/55 R18", "rimSize": "7.5Jx18 ET34",
                  "pcd": "5x108", "centerBore": 65.1, "offsetMin": 29, "offsetMax": 39, "wheelTorqueNm": 105, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.4, "tirePressureRearBar": 2.2, "tirePressureFrontLoadedBar": 2.6, "tirePressureRearLoadedBar": 2.6},
             ]}]},
        {"slug": "308", "name": "308", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "III Generación (P51)", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-puretech-130cv", "name": "1.2 PureTech 130 CV", "engineCode": "EB2ADTS", "displacement": 1199, "fuelType": "Gasolina", "powerHp": 130, "powerKw": 96, "torqueNm": 230, "transmission": "Automático EAT8 8 vel.", "gears": 8, "driveType": "FWD",
                  "lengthMm": 4367, "widthMm": 1852, "heightMm": 1441, "wheelbaseMm": 2675, "weightKg": 1307, "grossWeightKg": 1830,
                  "trunkCapacityL": 412, "fuelTankL": 52, "consumption": 5.5, "co2": 124, "topSpeed": 207, "acceleration0100": 9.1,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET25",
                  "pcd": "5x108", "centerBore": 65.1, "offsetMin": 20, "offsetMax": 30, "wheelTorqueNm": 105, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "renault": [
        {"slug": "clio", "name": "Clio", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2019-2025", "current": True,
         "generations": [{"slug": "2019-2025", "name": "V Generación", "yearStart": 2019, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-0-tce-90cv", "name": "1.0 TCe 90 CV", "engineCode": "H4D", "displacement": 999, "fuelType": "Gasolina", "powerHp": 90, "powerKw": 66, "torqueNm": 160, "transmission": "Manual 5 vel.", "gears": 5, "driveType": "FWD",
                  "lengthMm": 4050, "widthMm": 1798, "heightMm": 1440, "wheelbaseMm": 2583, "weightKg": 1140, "grossWeightKg": 1575,
                  "trunkCapacityL": 391, "fuelTankL": 42, "consumption": 5.1, "co2": 116, "topSpeed": 181, "acceleration0100": 12.3,
                  "tireSizeFront": "195/55 R16", "tireSizeRear": "195/55 R16", "rimSize": "6Jx16 ET44",
                  "pcd": "4x100", "centerBore": 60.1, "offsetMin": 38, "offsetMax": 48, "wheelTorqueNm": 105, "threadSize": "M12x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "captur", "name": "Captur", "bodyType": "SUV", "segment": "Utilitario", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "II Generación", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-3-tce-140cv", "name": "1.3 TCe 140 CV", "engineCode": "H5H", "displacement": 1332, "fuelType": "Gasolina", "powerHp": 140, "powerKw": 103, "torqueNm": 240, "transmission": "Automático EDC 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4227, "widthMm": 1797, "heightMm": 1576, "wheelbaseMm": 2639, "weightKg": 1310, "grossWeightKg": 1800,
                  "trunkCapacityL": 422, "fuelTankL": 48, "consumption": 5.9, "co2": 133, "topSpeed": 200, "acceleration0100": 9.5,
                  "tireSizeFront": "205/65 R16", "tireSizeRear": "205/65 R16", "rimSize": "6.5Jx16 ET37",
                  "pcd": "5x114.3", "centerBore": 66.1, "offsetMin": 32, "offsetMax": 42, "wheelTorqueNm": 105, "threadSize": "M12x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "megane-e-tech", "name": "Megane E-Tech", "bodyType": "Hatchback", "segment": "Compacto", "years": "2022-2025", "current": True,
         "generations": [{"slug": "2022-2025", "name": "I Generación eléctrica", "yearStart": 2022, "yearEnd": 2025,
             "variants": [
                 {"slug": "ev60-220cv", "name": "EV60 220 CV", "engineCode": "5AQ", "displacement": 0, "fuelType": "Eléctrico", "powerHp": 220, "powerKw": 160, "torqueNm": 300, "transmission": "Automático 1 vel.", "gears": 1, "driveType": "FWD",
                  "lengthMm": 4200, "widthMm": 1768, "heightMm": 1505, "wheelbaseMm": 2685, "weightKg": 1636, "grossWeightKg": 2100,
                  "trunkCapacityL": 440, "fuelTankL": 0, "consumption": 16.1, "co2": 0, "topSpeed": 160, "acceleration0100": 7.4,
                  "tireSizeFront": "215/45 R20", "tireSizeRear": "215/45 R20", "rimSize": "8Jx20 ET44",
                  "pcd": "5x114.3", "centerBore": 66.1, "offsetMin": 38, "offsetMax": 48, "wheelTorqueNm": 105, "threadSize": "M12x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.6, "tirePressureRearBar": 2.4, "tirePressureFrontLoadedBar": 2.8, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "arkana", "name": "Arkana", "bodyType": "SUV Coupé", "segment": "Compacto", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "I Generación (Europa)", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-6-e-tech-hybrid-145cv", "name": "1.6 E-Tech Hybrid 145 CV", "engineCode": "H4M", "displacement": 1598, "fuelType": "Híbrido", "powerHp": 145, "powerKw": 107, "torqueNm": 148, "transmission": "Automático Multi-modo", "gears": 4, "driveType": "FWD",
                  "lengthMm": 4568, "widthMm": 1821, "heightMm": 1571, "wheelbaseMm": 2720, "weightKg": 1430, "grossWeightKg": 1940,
                  "trunkCapacityL": 480, "fuelTankL": 50, "consumption": 4.8, "co2": 109, "topSpeed": 172, "acceleration0100": 10.8,
                  "tireSizeFront": "215/55 R18", "tireSizeRear": "215/55 R18", "rimSize": "7Jx18 ET40",
                  "pcd": "5x114.3", "centerBore": 66.1, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 105, "threadSize": "M12x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "citroen": [
        {"slug": "c3", "name": "C3", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2024-2025", "current": True,
         "generations": [{"slug": "2024-2025", "name": "IV Generación", "yearStart": 2024, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-puretech-100cv", "name": "1.2 PureTech 100 CV", "engineCode": "EB2ADTS", "displacement": 1199, "fuelType": "Gasolina", "powerHp": 100, "powerKw": 74, "torqueNm": 205, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4015, "widthMm": 1755, "heightMm": 1577, "wheelbaseMm": 2540, "weightKg": 1160, "grossWeightKg": 1600,
                  "trunkCapacityL": 310, "fuelTankL": 40, "consumption": 5.0, "co2": 113, "topSpeed": 185, "acceleration0100": 10.9,
                  "tireSizeFront": "195/55 R16", "tireSizeRear": "195/55 R16", "rimSize": "6.5Jx16 ET23",
                  "pcd": "4x108", "centerBore": 65.1, "offsetMin": 18, "offsetMax": 28, "wheelTorqueNm": 90, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "c4", "name": "C4", "bodyType": "Hatchback", "segment": "Compacto", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "III Generación", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-puretech-130cv", "name": "1.2 PureTech 130 CV", "engineCode": "EB2ADTS", "displacement": 1199, "fuelType": "Gasolina", "powerHp": 130, "powerKw": 96, "torqueNm": 230, "transmission": "Automático EAT8 8 vel.", "gears": 8, "driveType": "FWD",
                  "lengthMm": 4360, "widthMm": 1800, "heightMm": 1530, "wheelbaseMm": 2670, "weightKg": 1337, "grossWeightKg": 1850,
                  "trunkCapacityL": 380, "fuelTankL": 50, "consumption": 5.5, "co2": 124, "topSpeed": 205, "acceleration0100": 9.4,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET25",
                  "pcd": "5x108", "centerBore": 65.1, "offsetMin": 20, "offsetMax": 30, "wheelTorqueNm": 105, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "c5-aircross", "name": "C5 Aircross", "bodyType": "SUV", "segment": "Compacto", "years": "2019-2025", "current": True,
         "generations": [{"slug": "2019-2025", "name": "I Generación", "yearStart": 2019, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-5-bluehdi-130cv", "name": "1.5 BlueHDi 130 CV", "engineCode": "DV5RD", "displacement": 1499, "fuelType": "Diésel", "powerHp": 130, "powerKw": 96, "torqueNm": 300, "transmission": "Automático EAT8 8 vel.", "gears": 8, "driveType": "FWD",
                  "lengthMm": 4500, "widthMm": 1859, "heightMm": 1690, "wheelbaseMm": 2730, "weightKg": 1530, "grossWeightKg": 2070,
                  "trunkCapacityL": 580, "fuelTankL": 52, "consumption": 5.0, "co2": 131, "topSpeed": 195, "acceleration0100": 10.4,
                  "tireSizeFront": "215/55 R18", "tireSizeRear": "215/55 R18", "rimSize": "7Jx18 ET33",
                  "pcd": "5x108", "centerBore": 65.1, "offsetMin": 28, "offsetMax": 38, "wheelTorqueNm": 105, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.4, "tirePressureRearBar": 2.2, "tirePressureFrontLoadedBar": 2.6, "tirePressureRearLoadedBar": 2.6},
             ]}]},
    ],
})

# Add remaining brands with key models
VEHICLE_DATA.update({
    "bmw": [
        {"slug": "serie-3", "name": "Serie 3", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2019-2025", "current": True,
         "generations": [{"slug": "2019-2025", "name": "VII Generación (G20/G21)", "yearStart": 2019, "yearEnd": 2025,
             "variants": [
                 {"slug": "320d-190cv", "name": "320d 190 CV", "engineCode": "B47D20", "displacement": 1995, "fuelType": "Diésel", "powerHp": 190, "powerKw": 140, "torqueNm": 400, "transmission": "Automático 8 vel.", "gears": 8, "driveType": "RWD",
                  "lengthMm": 4709, "widthMm": 1827, "heightMm": 1442, "wheelbaseMm": 2851, "weightKg": 1560, "grossWeightKg": 2060,
                  "trunkCapacityL": 480, "fuelTankL": 59, "consumption": 4.7, "co2": 124, "topSpeed": 235, "acceleration0100": 6.8,
                  "tireSizeFront": "225/45 R18", "tireSizeRear": "255/40 R18", "rimSize": "7.5Jx18 / 8.5Jx18 ET30",
                  "pcd": "5x112", "centerBore": 66.5, "offsetMin": 25, "offsetMax": 40, "wheelTorqueNm": 140, "threadSize": "M14x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.5, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
                 {"slug": "320i-184cv", "name": "320i 184 CV", "engineCode": "B48B20", "displacement": 1998, "fuelType": "Gasolina", "powerHp": 184, "powerKw": 135, "torqueNm": 300, "transmission": "Automático 8 vel.", "gears": 8, "driveType": "RWD",
                  "lengthMm": 4709, "widthMm": 1827, "heightMm": 1442, "wheelbaseMm": 2851, "weightKg": 1530, "grossWeightKg": 2030,
                  "trunkCapacityL": 480, "fuelTankL": 59, "consumption": 6.1, "co2": 139, "topSpeed": 235, "acceleration0100": 7.1,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "7Jx16 ET31",
                  "pcd": "5x112", "centerBore": 66.5, "offsetMin": 25, "offsetMax": 40, "wheelTorqueNm": 140, "threadSize": "M14x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.5, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "serie-1", "name": "Serie 1", "bodyType": "Hatchback", "segment": "Compacto", "years": "2019-2025", "current": True,
         "generations": [{"slug": "2019-2025", "name": "III Generación (F40/F44)", "yearStart": 2019, "yearEnd": 2025,
             "variants": [
                 {"slug": "118i-140cv", "name": "118i 140 CV", "engineCode": "B38B15", "displacement": 1499, "fuelType": "Gasolina", "powerHp": 140, "powerKw": 103, "torqueNm": 220, "transmission": "Automático 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4319, "widthMm": 1799, "heightMm": 1434, "wheelbaseMm": 2670, "weightKg": 1365, "grossWeightKg": 1860,
                  "trunkCapacityL": 380, "fuelTankL": 42, "consumption": 5.9, "co2": 134, "topSpeed": 213, "acceleration0100": 8.5,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "7Jx16 ET40",
                  "pcd": "5x112", "centerBore": 66.5, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 140, "threadSize": "M14x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.4, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "x1", "name": "X1", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2025", "current": True,
         "generations": [{"slug": "2022-2025", "name": "III Generación (U11)", "yearStart": 2022, "yearEnd": 2025,
             "variants": [
                 {"slug": "xdrive23d-211cv", "name": "xDrive23d 211 CV", "engineCode": "B47D20", "displacement": 1995, "fuelType": "Diésel", "powerHp": 211, "powerKw": 155, "torqueNm": 400, "transmission": "Automático 7 vel.", "gears": 7, "driveType": "AWD",
                  "lengthMm": 4500, "widthMm": 1845, "heightMm": 1642, "wheelbaseMm": 2692, "weightKg": 1700, "grossWeightKg": 2250,
                  "trunkCapacityL": 540, "fuelTankL": 49, "consumption": 5.4, "co2": 142, "topSpeed": 224, "acceleration0100": 7.4,
                  "tireSizeFront": "225/55 R17", "tireSizeRear": "225/55 R17", "rimSize": "7.5Jx17 ET32",
                  "pcd": "5x112", "centerBore": 66.5, "offsetMin": 28, "offsetMax": 38, "wheelTorqueNm": 140, "threadSize": "M14x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.5, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "x3", "name": "X3", "bodyType": "SUV", "segment": "Medio", "years": "2024-2025", "current": True,
         "generations": [{"slug": "2024-2025", "name": "IV Generación (G45)", "yearStart": 2024, "yearEnd": 2025,
             "variants": [
                 {"slug": "xdrive20d-197cv", "name": "xDrive20d 197 CV", "engineCode": "B47D20", "displacement": 1995, "fuelType": "Diésel", "powerHp": 197, "powerKw": 145, "torqueNm": 400, "transmission": "Automático 8 vel.", "gears": 8, "driveType": "AWD",
                  "lengthMm": 4755, "widthMm": 1920, "heightMm": 1660, "wheelbaseMm": 2865, "weightKg": 1940, "grossWeightKg": 2510,
                  "trunkCapacityL": 570, "fuelTankL": 65, "consumption": 5.5, "co2": 144, "topSpeed": 213, "acceleration0100": 7.7,
                  "tireSizeFront": "245/50 R19", "tireSizeRear": "245/50 R19", "rimSize": "8Jx19 ET32",
                  "pcd": "5x112", "centerBore": 66.5, "offsetMin": 28, "offsetMax": 38, "wheelTorqueNm": 140, "threadSize": "M14x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.5, "tirePressureRearBar": 2.7, "tirePressureFrontLoadedBar": 2.7, "tirePressureRearLoadedBar": 3.0},
             ]}]},
    ],
    "audi": [
        {"slug": "a3", "name": "A3", "bodyType": "Hatchback/Sedán", "segment": "Compacto", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "IV Generación (8Y)", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "35-tdi-150cv", "name": "35 TDI 150 CV", "engineCode": "DFYA", "displacement": 1968, "fuelType": "Diésel", "powerHp": 150, "powerKw": 110, "torqueNm": 360, "transmission": "Automático S tronic 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4343, "widthMm": 1816, "heightMm": 1458, "wheelbaseMm": 2636, "weightKg": 1420, "grossWeightKg": 1920,
                  "trunkCapacityL": 380, "fuelTankL": 45, "consumption": 4.5, "co2": 119, "topSpeed": 227, "acceleration0100": 8.4,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET46",
                  "pcd": "5x112", "centerBore": 57.1, "offsetMin": 42, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "a4", "name": "A4", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2024-2025", "current": True,
         "generations": [{"slug": "2024-2025", "name": "Ahora A5 (F5/PQ46)", "yearStart": 2024, "yearEnd": 2025,
             "variants": [
                 {"slug": "35-tdi-163cv", "name": "35 TDI 163 CV", "engineCode": "DFYA", "displacement": 1968, "fuelType": "Diésel", "powerHp": 163, "powerKw": 120, "torqueNm": 380, "transmission": "Automático S tronic 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4829, "widthMm": 1860, "heightMm": 1484, "wheelbaseMm": 2900, "weightKg": 1620, "grossWeightKg": 2130,
                  "trunkCapacityL": 480, "fuelTankL": 58, "consumption": 4.8, "co2": 126, "topSpeed": 238, "acceleration0100": 8.0,
                  "tireSizeFront": "225/45 R18", "tireSizeRear": "225/45 R18", "rimSize": "8Jx18 ET47",
                  "pcd": "5x112", "centerBore": 57.1, "offsetMin": 42, "offsetMax": 52, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.5, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "q3", "name": "Q3", "bodyType": "SUV", "segment": "Compacto", "years": "2018-2025", "current": True,
         "generations": [{"slug": "2018-2025", "name": "II Generación (F3)", "yearStart": 2018, "yearEnd": 2025,
             "variants": [
                 {"slug": "35-tdi-150cv", "name": "35 TDI 150 CV", "engineCode": "DETA", "displacement": 1968, "fuelType": "Diésel", "powerHp": 150, "powerKw": 110, "torqueNm": 340, "transmission": "Automático S tronic 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4484, "widthMm": 1856, "heightMm": 1616, "wheelbaseMm": 2680, "weightKg": 1560, "grossWeightKg": 2060,
                  "trunkCapacityL": 530, "fuelTankL": 60, "consumption": 5.2, "co2": 137, "topSpeed": 207, "acceleration0100": 9.2,
                  "tireSizeFront": "215/65 R17", "tireSizeRear": "215/65 R17", "rimSize": "7Jx17 ET43",
                  "pcd": "5x112", "centerBore": 57.1, "offsetMin": 38, "offsetMax": 48, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
    ],
    "mercedes": [
        {"slug": "clase-a", "name": "Clase A", "bodyType": "Hatchback", "segment": "Compacto", "years": "2018-2025", "current": True,
         "generations": [{"slug": "2018-2025", "name": "IV Generación (W177)", "yearStart": 2018, "yearEnd": 2025,
             "variants": [
                 {"slug": "a200-163cv", "name": "A 200 163 CV", "engineCode": "M282", "displacement": 1332, "fuelType": "Gasolina", "powerHp": 163, "powerKw": 120, "torqueNm": 250, "transmission": "Automático 7G-DCT 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4419, "widthMm": 1796, "heightMm": 1440, "wheelbaseMm": 2729, "weightKg": 1390, "grossWeightKg": 1870,
                  "trunkCapacityL": 370, "fuelTankL": 43, "consumption": 5.8, "co2": 132, "topSpeed": 225, "acceleration0100": 8.0,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET49",
                  "pcd": "5x112", "centerBore": 66.6, "offsetMin": 44, "offsetMax": 54, "wheelTorqueNm": 130, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "clase-c", "name": "Clase C", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "V Generación (W206)", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "c220d-200cv", "name": "C 220 d 200 CV", "engineCode": "OM654", "displacement": 1993, "fuelType": "Diésel", "powerHp": 200, "powerKw": 147, "torqueNm": 440, "transmission": "Automático 9G-TRONIC 9 vel.", "gears": 9, "driveType": "RWD",
                  "lengthMm": 4751, "widthMm": 1820, "heightMm": 1437, "wheelbaseMm": 2865, "weightKg": 1670, "grossWeightKg": 2175,
                  "trunkCapacityL": 455, "fuelTankL": 66, "consumption": 4.9, "co2": 128, "topSpeed": 244, "acceleration0100": 7.3,
                  "tireSizeFront": "225/45 R18", "tireSizeRear": "245/40 R18", "rimSize": "7.5Jx18 / 8.5Jx18 ET44",
                  "pcd": "5x112", "centerBore": 66.6, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 130, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.5, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "glc", "name": "GLC", "bodyType": "SUV", "segment": "Medio", "years": "2022-2025", "current": True,
         "generations": [{"slug": "2022-2025", "name": "II Generación (X254)", "yearStart": 2022, "yearEnd": 2025,
             "variants": [
                 {"slug": "glc-220d-197cv", "name": "GLC 220 d 197 CV", "engineCode": "OM654", "displacement": 1993, "fuelType": "Diésel", "powerHp": 197, "powerKw": 145, "torqueNm": 440, "transmission": "Automático 9G-TRONIC 9 vel.", "gears": 9, "driveType": "AWD",
                  "lengthMm": 4716, "widthMm": 1890, "heightMm": 1640, "wheelbaseMm": 2888, "weightKg": 1915, "grossWeightKg": 2460,
                  "trunkCapacityL": 620, "fuelTankL": 62, "consumption": 5.8, "co2": 153, "topSpeed": 217, "acceleration0100": 8.0,
                  "tireSizeFront": "235/55 R19", "tireSizeRear": "255/50 R19", "rimSize": "8Jx19 / 9Jx19 ET39",
                  "pcd": "5x112", "centerBore": 66.6, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 130, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.5, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
    ],
    "ford": [
        {"slug": "puma", "name": "Puma", "bodyType": "SUV", "segment": "Utilitario", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "I Generación", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-0-ecoboost-mhev-125cv", "name": "1.0 EcoBoost MHEV 125 CV", "engineCode": "M1JC", "displacement": 999, "fuelType": "Gasolina MHEV", "powerHp": 125, "powerKw": 92, "torqueNm": 210, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4207, "widthMm": 1805, "heightMm": 1537, "wheelbaseMm": 2588, "weightKg": 1250, "grossWeightKg": 1740,
                  "trunkCapacityL": 456, "fuelTankL": 42, "consumption": 5.3, "co2": 120, "topSpeed": 193, "acceleration0100": 10.0,
                  "tireSizeFront": "205/60 R16", "tireSizeRear": "205/60 R16", "rimSize": "6.5Jx16 ET47.5",
                  "pcd": "5x108", "centerBore": 63.4, "offsetMin": 42, "offsetMax": 52, "wheelTorqueNm": 133, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "kuga", "name": "Kuga", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "III Generación", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "2-5-fhev-190cv", "name": "2.5 FHEV 190 CV", "engineCode": "Duratec 2.5", "displacement": 2488, "fuelType": "Híbrido", "powerHp": 190, "powerKw": 140, "torqueNm": 200, "transmission": "Automático CVT", "gears": 0, "driveType": "FWD",
                  "lengthMm": 4614, "widthMm": 1883, "heightMm": 1669, "wheelbaseMm": 2710, "weightKg": 1680, "grossWeightKg": 2210,
                  "trunkCapacityL": 475, "fuelTankL": 54, "consumption": 5.6, "co2": 128, "topSpeed": 196, "acceleration0100": 9.1,
                  "tireSizeFront": "225/60 R17", "tireSizeRear": "225/60 R17", "rimSize": "7Jx17 ET50",
                  "pcd": "5x108", "centerBore": 63.4, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 133, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "focus", "name": "Focus", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2018-2025", "current": True,
         "generations": [{"slug": "2018-2025", "name": "IV Generación (Mk4)", "yearStart": 2018, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-0-ecoboost-125cv", "name": "1.0 EcoBoost 125 CV", "engineCode": "M1DA", "displacement": 999, "fuelType": "Gasolina", "powerHp": 125, "powerKw": 92, "torqueNm": 170, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4378, "widthMm": 1825, "heightMm": 1454, "wheelbaseMm": 2700, "weightKg": 1305, "grossWeightKg": 1815,
                  "trunkCapacityL": 375, "fuelTankL": 52, "consumption": 5.3, "co2": 121, "topSpeed": 198, "acceleration0100": 10.4,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET50",
                  "pcd": "5x108", "centerBore": 63.4, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 133, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "dacia": [
        {"slug": "sandero", "name": "Sandero", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "III Generación", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-0-tce-90cv", "name": "1.0 TCe 90 CV", "engineCode": "H4D", "displacement": 999, "fuelType": "Gasolina", "powerHp": 90, "powerKw": 67, "torqueNm": 160, "transmission": "Manual 5 vel.", "gears": 5, "driveType": "FWD",
                  "lengthMm": 4088, "widthMm": 1848, "heightMm": 1499, "wheelbaseMm": 2604, "weightKg": 1072, "grossWeightKg": 1515,
                  "trunkCapacityL": 328, "fuelTankL": 50, "consumption": 5.3, "co2": 120, "topSpeed": 180, "acceleration0100": 12.1,
                  "tireSizeFront": "185/65 R15", "tireSizeRear": "185/65 R15", "rimSize": "6Jx15 ET40",
                  "pcd": "4x100", "centerBore": 60.1, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 105, "threadSize": "M12x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "duster", "name": "Duster", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2025", "current": True,
         "generations": [{"slug": "2024-2025", "name": "III Generación", "yearStart": 2024, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-tce-hybrid-140cv", "name": "1.2 TCe Hybrid 140 CV", "engineCode": "HR12", "displacement": 1199, "fuelType": "Híbrido", "powerHp": 140, "powerKw": 103, "torqueNm": 205, "transmission": "Automático Multi-modo", "gears": 4, "driveType": "FWD",
                  "lengthMm": 4343, "widthMm": 1813, "heightMm": 1656, "wheelbaseMm": 2657, "weightKg": 1365, "grossWeightKg": 1875,
                  "trunkCapacityL": 478, "fuelTankL": 48, "consumption": 4.7, "co2": 107, "topSpeed": 175, "acceleration0100": 10.1,
                  "tireSizeFront": "215/60 R17", "tireSizeRear": "215/60 R17", "rimSize": "7Jx17 ET37",
                  "pcd": "5x114.3", "centerBore": 66.1, "offsetMin": 32, "offsetMax": 42, "wheelTorqueNm": 105, "threadSize": "M12x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "jogger", "name": "Jogger", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2022-2025", "current": True,
         "generations": [{"slug": "2022-2025", "name": "I Generación", "yearStart": 2022, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-0-tce-110cv", "name": "1.0 TCe 110 CV", "engineCode": "H5H", "displacement": 999, "fuelType": "Gasolina", "powerHp": 110, "powerKw": 81, "torqueNm": 200, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4547, "widthMm": 1784, "heightMm": 1632, "wheelbaseMm": 2897, "weightKg": 1284, "grossWeightKg": 1800,
                  "trunkCapacityL": 708, "fuelTankL": 50, "consumption": 5.9, "co2": 133, "topSpeed": 183, "acceleration0100": 11.2,
                  "tireSizeFront": "195/65 R16", "tireSizeRear": "195/65 R16", "rimSize": "6.5Jx16 ET37",
                  "pcd": "4x100", "centerBore": 60.1, "offsetMin": 32, "offsetMax": 42, "wheelTorqueNm": 105, "threadSize": "M12x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "spring", "name": "Spring", "bodyType": "SUV", "segment": "Mini", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "I Generación", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "electric-65cv", "name": "Electric 65 CV", "engineCode": "Eléctrico", "displacement": 0, "fuelType": "Eléctrico", "powerHp": 65, "powerKw": 48, "torqueNm": 113, "transmission": "Automático 1 vel.", "gears": 1, "driveType": "FWD",
                  "lengthMm": 3734, "widthMm": 1620, "heightMm": 1516, "wheelbaseMm": 2423, "weightKg": 1042, "grossWeightKg": 1400,
                  "trunkCapacityL": 308, "fuelTankL": 0, "consumption": 14.6, "co2": 0, "topSpeed": 125, "acceleration0100": 13.7,
                  "tireSizeFront": "165/70 R14", "tireSizeRear": "165/70 R14", "rimSize": "5Jx14 ET35",
                  "pcd": "4x100", "centerBore": 60.1, "offsetMin": 30, "offsetMax": 40, "wheelTorqueNm": 105, "threadSize": "M12x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "opel": [
        {"slug": "corsa", "name": "Corsa", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2019-2025", "current": True,
         "generations": [{"slug": "2019-2025", "name": "VI Generación (F)", "yearStart": 2019, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-turbo-100cv", "name": "1.2 Turbo 100 CV", "engineCode": "EB2ADTS", "displacement": 1199, "fuelType": "Gasolina", "powerHp": 100, "powerKw": 74, "torqueNm": 205, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4060, "widthMm": 1765, "heightMm": 1433, "wheelbaseMm": 2538, "weightKg": 1155, "grossWeightKg": 1610,
                  "trunkCapacityL": 309, "fuelTankL": 44, "consumption": 5.0, "co2": 113, "topSpeed": 188, "acceleration0100": 10.5,
                  "tireSizeFront": "195/55 R16", "tireSizeRear": "195/55 R16", "rimSize": "6.5Jx16 ET23",
                  "pcd": "4x108", "centerBore": 65.1, "offsetMin": 18, "offsetMax": 28, "wheelTorqueNm": 90, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "mokka", "name": "Mokka", "bodyType": "SUV", "segment": "Utilitario", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "II Generación", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-turbo-130cv", "name": "1.2 Turbo 130 CV", "engineCode": "EB2ADTS", "displacement": 1199, "fuelType": "Gasolina", "powerHp": 130, "powerKw": 96, "torqueNm": 230, "transmission": "Automático EAT8 8 vel.", "gears": 8, "driveType": "FWD",
                  "lengthMm": 4151, "widthMm": 1791, "heightMm": 1531, "wheelbaseMm": 2557, "weightKg": 1275, "grossWeightKg": 1765,
                  "trunkCapacityL": 350, "fuelTankL": 44, "consumption": 5.8, "co2": 131, "topSpeed": 198, "acceleration0100": 9.2,
                  "tireSizeFront": "215/60 R17", "tireSizeRear": "215/60 R17", "rimSize": "7Jx17 ET27",
                  "pcd": "4x108", "centerBore": 65.1, "offsetMin": 22, "offsetMax": 32, "wheelTorqueNm": 90, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "astra", "name": "Astra", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2022-2025", "current": True,
         "generations": [{"slug": "2022-2025", "name": "VI Generación (L)", "yearStart": 2022, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-2-turbo-130cv", "name": "1.2 Turbo 130 CV", "engineCode": "EB2ADTS", "displacement": 1199, "fuelType": "Gasolina", "powerHp": 130, "powerKw": 96, "torqueNm": 230, "transmission": "Automático EAT8 8 vel.", "gears": 8, "driveType": "FWD",
                  "lengthMm": 4374, "widthMm": 1860, "heightMm": 1442, "wheelbaseMm": 2675, "weightKg": 1352, "grossWeightKg": 1860,
                  "trunkCapacityL": 422, "fuelTankL": 52, "consumption": 5.5, "co2": 124, "topSpeed": 207, "acceleration0100": 9.4,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET25",
                  "pcd": "5x108", "centerBore": 65.1, "offsetMin": 20, "offsetMax": 30, "wheelTorqueNm": 105, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "nissan": [
        {"slug": "qashqai", "name": "Qashqai", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "III Generación (J12)", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-3-dig-t-mhev-158cv", "name": "1.3 DIG-T MHEV 158 CV", "engineCode": "HR13DDT", "displacement": 1332, "fuelType": "Gasolina MHEV", "powerHp": 158, "powerKw": 116, "torqueNm": 270, "transmission": "Automático Xtronic CVT", "gears": 0, "driveType": "FWD",
                  "lengthMm": 4425, "widthMm": 1838, "heightMm": 1635, "wheelbaseMm": 2665, "weightKg": 1440, "grossWeightKg": 1950,
                  "trunkCapacityL": 504, "fuelTankL": 55, "consumption": 6.0, "co2": 136, "topSpeed": 200, "acceleration0100": 9.5,
                  "tireSizeFront": "215/65 R17", "tireSizeRear": "215/65 R17", "rimSize": "7Jx17 ET40",
                  "pcd": "5x114.3", "centerBore": 66.1, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 108, "threadSize": "M12x1.25", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "juke", "name": "Juke", "bodyType": "SUV", "segment": "Utilitario", "years": "2019-2025", "current": True,
         "generations": [{"slug": "2019-2025", "name": "II Generación (F16)", "yearStart": 2019, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-0-dig-t-114cv", "name": "1.0 DIG-T 114 CV", "engineCode": "HR10DET", "displacement": 999, "fuelType": "Gasolina", "powerHp": 114, "powerKw": 84, "torqueNm": 200, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4210, "widthMm": 1800, "heightMm": 1595, "wheelbaseMm": 2636, "weightKg": 1210, "grossWeightKg": 1690,
                  "trunkCapacityL": 422, "fuelTankL": 46, "consumption": 5.8, "co2": 132, "topSpeed": 190, "acceleration0100": 10.7,
                  "tireSizeFront": "205/60 R16", "tireSizeRear": "205/60 R16", "rimSize": "6.5Jx16 ET40",
                  "pcd": "5x114.3", "centerBore": 66.1, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 108, "threadSize": "M12x1.25", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "mazda": [
        {"slug": "cx-5", "name": "CX-5", "bodyType": "SUV", "segment": "Compacto", "years": "2017-2025", "current": True,
         "generations": [{"slug": "2017-2025", "name": "II Generación (KF)", "yearStart": 2017, "yearEnd": 2025,
             "variants": [
                 {"slug": "2-0-skyactiv-g-165cv", "name": "2.0 SKYACTIV-G 165 CV", "engineCode": "PE-VPS", "displacement": 1998, "fuelType": "Gasolina", "powerHp": 165, "powerKw": 121, "torqueNm": 213, "transmission": "Automático 6 vel.", "gears": 6, "driveType": "AWD",
                  "lengthMm": 4550, "widthMm": 1842, "heightMm": 1680, "wheelbaseMm": 2700, "weightKg": 1530, "grossWeightKg": 2060,
                  "trunkCapacityL": 506, "fuelTankL": 58, "consumption": 7.1, "co2": 162, "topSpeed": 194, "acceleration0100": 9.4,
                  "tireSizeFront": "225/55 R19", "tireSizeRear": "225/55 R19", "rimSize": "7Jx19 ET45",
                  "pcd": "5x114.3", "centerBore": 67.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 108, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "mazda3", "name": "Mazda3", "bodyType": "Hatchback/Sedán", "segment": "Compacto", "years": "2019-2025", "current": True,
         "generations": [{"slug": "2019-2025", "name": "IV Generación (BP)", "yearStart": 2019, "yearEnd": 2025,
             "variants": [
                 {"slug": "2-0-skyactiv-g-122cv", "name": "2.0 SKYACTIV-G 122 CV", "engineCode": "PE-VPH", "displacement": 1998, "fuelType": "Gasolina MHEV", "powerHp": 122, "powerKw": 90, "torqueNm": 213, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4460, "widthMm": 1795, "heightMm": 1435, "wheelbaseMm": 2725, "weightKg": 1352, "grossWeightKg": 1820,
                  "trunkCapacityL": 358, "fuelTankL": 51, "consumption": 5.8, "co2": 132, "topSpeed": 197, "acceleration0100": 10.4,
                  "tireSizeFront": "205/60 R16", "tireSizeRear": "205/60 R16", "rimSize": "6.5Jx16 ET50",
                  "pcd": "5x114.3", "centerBore": 67.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 108, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "fiat": [
        {"slug": "500", "name": "500", "bodyType": "Utilitario", "segment": "Mini", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "500 Eléctrico", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "electric-118cv", "name": "Electric 118 CV", "engineCode": "Eléctrico", "displacement": 0, "fuelType": "Eléctrico", "powerHp": 118, "powerKw": 87, "torqueNm": 220, "transmission": "Automático 1 vel.", "gears": 1, "driveType": "FWD",
                  "lengthMm": 3631, "widthMm": 1683, "heightMm": 1527, "wheelbaseMm": 2322, "weightKg": 1320, "grossWeightKg": 1700,
                  "trunkCapacityL": 185, "fuelTankL": 0, "consumption": 14.0, "co2": 0, "topSpeed": 150, "acceleration0100": 9.0,
                  "tireSizeFront": "205/45 R17", "tireSizeRear": "205/45 R17", "rimSize": "7Jx17 ET40",
                  "pcd": "4x98", "centerBore": 58.1, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 85, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "tipo", "name": "Tipo", "bodyType": "Hatchback/Sedán/Familiar", "segment": "Compacto", "years": "2016-2025", "current": True,
         "generations": [{"slug": "2016-2025", "name": "I Generación (356)", "yearStart": 2016, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-6-mjet-130cv", "name": "1.6 MJet 130 CV", "engineCode": "55280444", "displacement": 1598, "fuelType": "Diésel", "powerHp": 130, "powerKw": 96, "torqueNm": 320, "transmission": "Automático DCT 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4368, "widthMm": 1792, "heightMm": 1497, "wheelbaseMm": 2638, "weightKg": 1330, "grossWeightKg": 1820,
                  "trunkCapacityL": 440, "fuelTankL": 50, "consumption": 4.3, "co2": 113, "topSpeed": 200, "acceleration0100": 9.8,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET40",
                  "pcd": "5x98", "centerBore": 58.1, "offsetMin": 35, "offsetMax": 45, "wheelTorqueNm": 85, "threadSize": "M12x1.25", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "skoda": [
        {"slug": "octavia", "name": "Octavia", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "IV Generación (NX)", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DPCA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Manual 6 vel.", "gears": 6, "driveType": "FWD",
                  "lengthMm": 4689, "widthMm": 1829, "heightMm": 1470, "wheelbaseMm": 2686, "weightKg": 1350, "grossWeightKg": 1880,
                  "trunkCapacityL": 600, "fuelTankL": 50, "consumption": 5.6, "co2": 127, "topSpeed": 224, "acceleration0100": 8.3,
                  "tireSizeFront": "205/55 R16", "tireSizeRear": "205/55 R16", "rimSize": "6.5Jx16 ET46",
                  "pcd": "5x112", "centerBore": 57.1, "offsetMin": 42, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "fabia", "name": "Fabia", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2021-2025", "current": True,
         "generations": [{"slug": "2021-2025", "name": "IV Generación (PJ)", "yearStart": 2021, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-0-tsi-110cv", "name": "1.0 TSI 110 CV", "engineCode": "DKLA", "displacement": 999, "fuelType": "Gasolina", "powerHp": 110, "powerKw": 81, "torqueNm": 200, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4108, "widthMm": 1780, "heightMm": 1460, "wheelbaseMm": 2564, "weightKg": 1200, "grossWeightKg": 1680,
                  "trunkCapacityL": 380, "fuelTankL": 40, "consumption": 5.1, "co2": 116, "topSpeed": 200, "acceleration0100": 9.7,
                  "tireSizeFront": "185/65 R15", "tireSizeRear": "185/65 R15", "rimSize": "6Jx15 ET40",
                  "pcd": "5x100", "centerBore": 57.1, "offsetMin": 35, "offsetMax": 43, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.2, "tirePressureRearBar": 2.0, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "kodiaq", "name": "Kodiaq", "bodyType": "SUV", "segment": "Medio", "years": "2024-2025", "current": True,
         "generations": [{"slug": "2024-2025", "name": "II Generación", "yearStart": 2024, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-5-tsi-150cv", "name": "1.5 TSI 150 CV", "engineCode": "DPCA", "displacement": 1498, "fuelType": "Gasolina", "powerHp": 150, "powerKw": 110, "torqueNm": 250, "transmission": "Automático DSG 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4758, "widthMm": 1864, "heightMm": 1664, "wheelbaseMm": 2791, "weightKg": 1605, "grossWeightKg": 2200,
                  "trunkCapacityL": 910, "fuelTankL": 58, "consumption": 6.3, "co2": 143, "topSpeed": 200, "acceleration0100": 9.8,
                  "tireSizeFront": "215/65 R17", "tireSizeRear": "215/65 R17", "rimSize": "7Jx17 ET44",
                  "pcd": "5x112", "centerBore": 57.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 120, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.8},
             ]}]},
    ],
    "volvo": [
        {"slug": "xc60", "name": "XC60", "bodyType": "SUV", "segment": "Medio", "years": "2017-2025", "current": True,
         "generations": [{"slug": "2017-2025", "name": "II Generación (SPA)", "yearStart": 2017, "yearEnd": 2025,
             "variants": [
                 {"slug": "b4-197cv", "name": "B4 Diesel 197 CV", "engineCode": "D4204T23", "displacement": 1969, "fuelType": "Diésel MHEV", "powerHp": 197, "powerKw": 145, "torqueNm": 420, "transmission": "Automático 8 vel.", "gears": 8, "driveType": "AWD",
                  "lengthMm": 4688, "widthMm": 1902, "heightMm": 1658, "wheelbaseMm": 2865, "weightKg": 1890, "grossWeightKg": 2420,
                  "trunkCapacityL": 483, "fuelTankL": 71, "consumption": 5.8, "co2": 152, "topSpeed": 210, "acceleration0100": 7.6,
                  "tireSizeFront": "235/55 R19", "tireSizeRear": "235/55 R19", "rimSize": "8Jx19 ET42",
                  "pcd": "5x108", "centerBore": 63.3, "offsetMin": 37, "offsetMax": 47, "wheelTorqueNm": 140, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.5, "tirePressureRearBar": 2.5, "tirePressureFrontLoadedBar": 2.7, "tirePressureRearLoadedBar": 2.8},
             ]}]},
        {"slug": "xc40", "name": "XC40", "bodyType": "SUV", "segment": "Compacto", "years": "2018-2025", "current": True,
         "generations": [{"slug": "2018-2025", "name": "I Generación (CMA)", "yearStart": 2018, "yearEnd": 2025,
             "variants": [
                 {"slug": "b3-163cv", "name": "B3 163 CV", "engineCode": "B3154T5", "displacement": 1477, "fuelType": "Gasolina MHEV", "powerHp": 163, "powerKw": 120, "torqueNm": 265, "transmission": "Automático 7 vel.", "gears": 7, "driveType": "FWD",
                  "lengthMm": 4425, "widthMm": 1863, "heightMm": 1652, "wheelbaseMm": 2702, "weightKg": 1585, "grossWeightKg": 2100,
                  "trunkCapacityL": 452, "fuelTankL": 54, "consumption": 6.5, "co2": 148, "topSpeed": 200, "acceleration0100": 8.9,
                  "tireSizeFront": "225/55 R18", "tireSizeRear": "225/55 R18", "rimSize": "7.5Jx18 ET42",
                  "pcd": "5x108", "centerBore": 63.3, "offsetMin": 37, "offsetMax": 47, "wheelTorqueNm": 140, "threadSize": "M14x1.5", "boltType": "Tornillo",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
    "honda": [
        {"slug": "civic", "name": "Civic", "bodyType": "Hatchback", "segment": "Compacto", "years": "2022-2025", "current": True,
         "generations": [{"slug": "2022-2025", "name": "XI Generación (FL/FE)", "yearStart": 2022, "yearEnd": 2025,
             "variants": [
                 {"slug": "2-0-ehev-184cv", "name": "2.0 e:HEV 184 CV", "engineCode": "LFB", "displacement": 1993, "fuelType": "Híbrido", "powerHp": 184, "powerKw": 135, "torqueNm": 315, "transmission": "Automático eCVT", "gears": 0, "driveType": "FWD",
                  "lengthMm": 4550, "widthMm": 1800, "heightMm": 1415, "wheelbaseMm": 2735, "weightKg": 1457, "grossWeightKg": 1900,
                  "trunkCapacityL": 404, "fuelTankL": 40, "consumption": 4.7, "co2": 108, "topSpeed": 180, "acceleration0100": 7.8,
                  "tireSizeFront": "235/40 R18", "tireSizeRear": "235/40 R18", "rimSize": "8Jx18 ET55",
                  "pcd": "5x114.3", "centerBore": 64.1, "offsetMin": 50, "offsetMax": 60, "wheelTorqueNm": 108, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "cr-v", "name": "CR-V", "bodyType": "SUV", "segment": "Compacto", "years": "2023-2025", "current": True,
         "generations": [{"slug": "2023-2025", "name": "VI Generación", "yearStart": 2023, "yearEnd": 2025,
             "variants": [
                 {"slug": "2-0-ehev-184cv", "name": "2.0 e:HEV 184 CV", "engineCode": "LFC", "displacement": 1993, "fuelType": "Híbrido", "powerHp": 184, "powerKw": 135, "torqueNm": 315, "transmission": "Automático eCVT", "gears": 0, "driveType": "AWD",
                  "lengthMm": 4703, "widthMm": 1866, "heightMm": 1680, "wheelbaseMm": 2700, "weightKg": 1740, "grossWeightKg": 2250,
                  "trunkCapacityL": 587, "fuelTankL": 57, "consumption": 6.1, "co2": 139, "topSpeed": 180, "acceleration0100": 8.8,
                  "tireSizeFront": "235/55 R19", "tireSizeRear": "235/55 R19", "rimSize": "7.5Jx19 ET50",
                  "pcd": "5x114.3", "centerBore": 64.1, "offsetMin": 45, "offsetMax": 55, "wheelTorqueNm": 108, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.3, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
        {"slug": "jazz", "name": "Jazz", "bodyType": "Monovolumen", "segment": "Utilitario", "years": "2020-2025", "current": True,
         "generations": [{"slug": "2020-2025", "name": "IV Generación (GR)", "yearStart": 2020, "yearEnd": 2025,
             "variants": [
                 {"slug": "1-5-ehev-109cv", "name": "1.5 e:HEV 109 CV", "engineCode": "LEB", "displacement": 1498, "fuelType": "Híbrido", "powerHp": 109, "powerKw": 80, "torqueNm": 253, "transmission": "Automático eCVT", "gears": 0, "driveType": "FWD",
                  "lengthMm": 4044, "widthMm": 1694, "heightMm": 1526, "wheelbaseMm": 2519, "weightKg": 1179, "grossWeightKg": 1575,
                  "trunkCapacityL": 304, "fuelTankL": 40, "consumption": 4.5, "co2": 102, "topSpeed": 175, "acceleration0100": 9.4,
                  "tireSizeFront": "185/60 R15", "tireSizeRear": "185/60 R15", "rimSize": "5.5Jx15 ET45",
                  "pcd": "4x100", "centerBore": 56.1, "offsetMin": 40, "offsetMax": 50, "wheelTorqueNm": 108, "threadSize": "M12x1.5", "boltType": "Tuerca",
                  "tirePressureFrontBar": 2.3, "tirePressureRearBar": 2.1, "tirePressureFrontLoadedBar": 2.5, "tirePressureRearLoadedBar": 2.5},
             ]}]},
    ],
})


def build_brand_json(brand_info, models):
    """Build a complete brand JSON file."""
    brand_slug = brand_info["slug"]
    
    processed_models = []
    for model in models:
        processed_model = {
            "slug": model["slug"],
            "name": model["name"],
            "bodyType": model["bodyType"],
            "segment": model["segment"],
            "years": model["years"],
            "current": model["current"],
            "publishedAt": None,  # All unpublished initially
            "generations": [],
        }
        
        for gen in model.get("generations", []):
            processed_gen = {
                "slug": gen["slug"],
                "name": gen["name"],
                "yearStart": gen["yearStart"],
                "yearEnd": gen["yearEnd"],
                "publishedAt": None,
                "variants": [],
            }
            
            for variant in gen.get("variants", []):
                v = dict(variant)
                v["publishedAt"] = None
                processed_gen["variants"].append(v)
            
            processed_model["generations"].append(processed_gen)
        
        processed_models.append(processed_model)
    
    return {
        "slug": brand_slug,
        "name": brand_info["name"],
        "country": brand_info["country"],
        "founded": brand_info["founded"],
        "hq": brand_info.get("hq", ""),
        "description": brand_info.get("description", ""),
        "publishedAt": None,
        "models": processed_models,
    }


def build_tire_size_index():
    """Build reverse lookup: tire size → vehicles."""
    tire_sizes = {}
    
    for brand_slug, models in VEHICLE_DATA.items():
        brand_info = next(b for b in BRANDS if b["slug"] == brand_slug)
        for model in models:
            for gen in model.get("generations", []):
                for variant in gen.get("variants", []):
                    for ts_field in ["tireSizeFront", "tireSizeRear"]:
                        ts = variant.get(ts_field)
                        if not ts:
                            continue
                        ts_slug = ts.lower().replace("/", "-").replace(" ", "-")
                        if ts_slug not in tire_sizes:
                            tire_sizes[ts_slug] = {
                                "size": ts,
                                "slug": ts_slug,
                                "vehicles": [],
                                "publishedAt": None,
                            }
                        
                        vehicle_ref = {
                            "brand": brand_info["name"],
                            "brandSlug": brand_slug,
                            "model": model["name"],
                            "modelSlug": model["slug"],
                            "variant": variant["name"],
                            "years": model["years"],
                        }
                        
                        # Avoid duplicates
                        existing = [v for v in tire_sizes[ts_slug]["vehicles"] 
                                   if v["brandSlug"] == brand_slug and v["modelSlug"] == model["slug"]]
                        if not existing:
                            tire_sizes[ts_slug]["vehicles"].append(vehicle_ref)
    
    return list(tire_sizes.values())


def build_pcd_index():
    """Build reverse lookup: PCD pattern → vehicles."""
    pcds = {}
    
    for brand_slug, models in VEHICLE_DATA.items():
        brand_info = next(b for b in BRANDS if b["slug"] == brand_slug)
        for model in models:
            for gen in model.get("generations", []):
                for variant in gen.get("variants", []):
                    pcd = variant.get("pcd")
                    if not pcd:
                        continue
                    pcd_slug = pcd.lower().replace("x", "x")
                    if pcd_slug not in pcds:
                        pcds[pcd_slug] = {
                            "pattern": pcd,
                            "slug": pcd_slug,
                            "vehicles": [],
                            "publishedAt": None,
                        }
                    
                    vehicle_ref = {
                        "brand": brand_info["name"],
                        "brandSlug": brand_slug,
                        "model": model["name"],
                        "modelSlug": model["slug"],
                        "years": model["years"],
                    }
                    
                    existing = [v for v in pcds[pcd_slug]["vehicles"]
                               if v["brandSlug"] == brand_slug and v["modelSlug"] == model["slug"]]
                    if not existing:
                        pcds[pcd_slug]["vehicles"].append(vehicle_ref)
    
    return list(pcds.values())


def main():
    print("Building vehicle data JSON files...")
    
    # Build brands index
    brands_index = []
    for brand_info in BRANDS:
        slug = brand_info["slug"]
        models = VEHICLE_DATA.get(slug, [])
        
        brand_json = build_brand_json(brand_info, models)
        
        # Save per-brand file
        filepath = os.path.join(DATA_DIR, f"brand-{slug}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(brand_json, f, ensure_ascii=False, indent=2)
        
        model_count = len(models)
        variant_count = sum(
            len(v.get("variants", []))
            for m in models
            for g in m.get("generations", [])
            for v in [g]
        )
        
        brands_index.append({
            "slug": slug,
            "name": brand_info["name"],
            "country": brand_info["country"],
            "founded": brand_info["founded"],
            "hq": brand_info.get("hq", ""),
            "description": brand_info.get("description", ""),
            "modelCount": model_count,
            "publishedAt": None,
        })
        
        print(f"  {brand_info['name']}: {model_count} models, {variant_count} variants")
    
    # Save brands index
    with open(os.path.join(DATA_DIR, "brands.json"), "w", encoding="utf-8") as f:
        json.dump(brands_index, f, ensure_ascii=False, indent=2)
    print(f"\nBrands index: {len(brands_index)} brands")
    
    # Build tire size index
    tire_sizes = build_tire_size_index()
    with open(os.path.join(DATA_DIR, "tire-sizes.json"), "w", encoding="utf-8") as f:
        json.dump(tire_sizes, f, ensure_ascii=False, indent=2)
    print(f"Tire sizes index: {len(tire_sizes)} unique sizes")
    
    # Build PCD index
    pcds = build_pcd_index()
    with open(os.path.join(DATA_DIR, "pcd-patterns.json"), "w", encoding="utf-8") as f:
        json.dump(pcds, f, ensure_ascii=False, indent=2)
    print(f"PCD patterns index: {len(pcds)} unique patterns")
    
    print(f"\nAll data saved to {DATA_DIR}")


if __name__ == "__main__":
    main()
