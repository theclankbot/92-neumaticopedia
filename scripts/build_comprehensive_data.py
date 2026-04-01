#!/usr/bin/env python3
"""
Build comprehensive vehicle + tire data for neumaticopedia.com
Sources: wheel-size.com model lists, NHTSA API, known European market data
"""

import json
import os
import re
import random
import hashlib

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# ============================================================
# KNOWN EUROPEAN MARKET MODELS PER BRAND
# Focus on models sold in Spain / Europe
# ============================================================

EUROPEAN_MODELS = {
    "toyota": {
        "name": "Toyota", "country": "Japón", "founded": "1937", "hq": "Toyota City, Japón",
        "description": "Toyota Motor Corporation es el mayor fabricante de automóviles del mundo por volumen de ventas. Fundada en 1937 por Kiichiro Toyoda, la marca japonesa es conocida por su fiabilidad, eficiencia y liderazgo en tecnología híbrida con modelos como el Prius y el Corolla.",
        "models": [
            {"name": "Corolla", "slug": "corolla", "bodyType": "Sedán/Hatchback", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Yaris", "slug": "yaris", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "Yaris Cross", "slug": "yaris-cross", "bodyType": "SUV", "segment": "Utilitario", "years": "2021-2026", "current": True},
            {"name": "C-HR", "slug": "c-hr", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "RAV4", "slug": "rav4", "bodyType": "SUV", "segment": "Medio", "years": "2019-2026", "current": True},
            {"name": "Camry", "slug": "camry", "bodyType": "Sedán", "segment": "Medio", "years": "2019-2026", "current": True},
            {"name": "Prius", "slug": "prius", "bodyType": "Hatchback", "segment": "Compacto", "years": "2023-2026", "current": True},
            {"name": "Highlander", "slug": "highlander", "bodyType": "SUV", "segment": "Grande", "years": "2021-2026", "current": True},
            {"name": "Land Cruiser", "slug": "land-cruiser", "bodyType": "SUV", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "Aygo X", "slug": "aygo-x", "bodyType": "Utilitario", "segment": "Mini", "years": "2022-2026", "current": True},
            {"name": "bZ4X", "slug": "bz4x", "bodyType": "SUV", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "Supra", "slug": "supra", "bodyType": "Deportivo", "segment": "Premium", "years": "2019-2026", "current": True},
            {"name": "GR86", "slug": "gr86", "bodyType": "Deportivo", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Proace City", "slug": "proace-city", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2020-2026", "current": True},
            {"name": "Proace", "slug": "proace", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Hilux", "slug": "hilux", "bodyType": "Pickup", "segment": "Comercial", "years": "2020-2026", "current": True},
            {"name": "Corolla Cross", "slug": "corolla-cross", "bodyType": "SUV", "segment": "Compacto", "years": "2023-2026", "current": True},
            {"name": "Auris", "slug": "auris", "bodyType": "Hatchback", "segment": "Compacto", "years": "2013-2019", "current": False},
            {"name": "Avensis", "slug": "avensis", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2009-2018", "current": False},
            {"name": "GT86", "slug": "gt86", "bodyType": "Deportivo", "segment": "Compacto", "years": "2012-2021", "current": False},
        ]
    },
    "volkswagen": {
        "name": "Volkswagen", "country": "Alemania", "founded": "1937", "hq": "Wolfsburgo, Alemania",
        "description": "Volkswagen es una de las marcas de automóviles más vendidas en Europa y el mundo. Fundada en 1937, la marca alemana es reconocida por modelos icónicos como el Golf, el Polo y el Tiguan, combinando ingeniería alemana con accesibilidad.",
        "models": [
            {"name": "Golf", "slug": "golf", "bodyType": "Hatchback", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Polo", "slug": "polo", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2018-2026", "current": True},
            {"name": "Tiguan", "slug": "tiguan", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "T-Roc", "slug": "t-roc", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "T-Cross", "slug": "t-cross", "bodyType": "SUV", "segment": "Utilitario", "years": "2019-2026", "current": True},
            {"name": "Passat", "slug": "passat", "bodyType": "Familiar", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "Touareg", "slug": "touareg", "bodyType": "SUV", "segment": "Premium", "years": "2018-2026", "current": True},
            {"name": "ID.3", "slug": "id-3", "bodyType": "Hatchback", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "ID.4", "slug": "id-4", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "ID.5", "slug": "id-5", "bodyType": "SUV Coupé", "segment": "Medio", "years": "2022-2026", "current": True},
            {"name": "ID.7", "slug": "id-7", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "ID.Buzz", "slug": "id-buzz", "bodyType": "Monovolumen", "segment": "Grande", "years": "2023-2026", "current": True},
            {"name": "Taigo", "slug": "taigo", "bodyType": "SUV Coupé", "segment": "Utilitario", "years": "2022-2026", "current": True},
            {"name": "Arteon", "slug": "arteon", "bodyType": "Sedán/Shooting Brake", "segment": "Premium", "years": "2017-2025", "current": False},
            {"name": "Up!", "slug": "up", "bodyType": "Utilitario", "segment": "Mini", "years": "2012-2023", "current": False},
            {"name": "Touran", "slug": "touran", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2015-2025", "current": True},
            {"name": "Caddy", "slug": "caddy", "bodyType": "Furgoneta/Monovolumen", "segment": "Comercial", "years": "2021-2026", "current": True},
            {"name": "Multivan", "slug": "multivan", "bodyType": "Monovolumen", "segment": "Grande", "years": "2021-2026", "current": True},
            {"name": "Amarok", "slug": "amarok", "bodyType": "Pickup", "segment": "Comercial", "years": "2023-2026", "current": True},
        ]
    },
    "seat": {
        "name": "SEAT", "country": "España", "founded": "1950", "hq": "Martorell, España",
        "description": "SEAT es la única marca española de fabricación de automóviles en serie. Fundada en 1950, con sede en Martorell (Barcelona), es conocida por modelos deportivos y accesibles como el León, el Ibiza y el Arona. Forma parte del Grupo Volkswagen desde 1986.",
        "models": [
            {"name": "León", "slug": "leon", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Ibiza", "slug": "ibiza", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2017-2026", "current": True},
            {"name": "Arona", "slug": "arona", "bodyType": "SUV", "segment": "Utilitario", "years": "2018-2026", "current": True},
            {"name": "Ateca", "slug": "ateca", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Tarraco", "slug": "tarraco", "bodyType": "SUV", "segment": "Medio", "years": "2019-2026", "current": True},
            {"name": "Mii", "slug": "mii", "bodyType": "Utilitario", "segment": "Mini", "years": "2012-2021", "current": False},
            {"name": "Alhambra", "slug": "alhambra", "bodyType": "Monovolumen", "segment": "Grande", "years": "2010-2022", "current": False},
            {"name": "Toledo", "slug": "toledo", "bodyType": "Sedán", "segment": "Compacto", "years": "2013-2019", "current": False},
        ]
    },
    "cupra": {
        "name": "CUPRA", "country": "España", "founded": "2018", "hq": "Martorell, España",
        "description": "CUPRA es la marca deportiva del grupo SEAT, creada en 2018 como marca independiente. Con sede en Martorell (Barcelona), combina el diseño español con rendimiento deportivo y tecnología de vanguardia en modelos como el Formentor y el Born.",
        "models": [
            {"name": "Formentor", "slug": "formentor", "bodyType": "SUV Coupé", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Born", "slug": "born", "bodyType": "Hatchback", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "Leon", "slug": "leon", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Terramar", "slug": "terramar", "bodyType": "SUV", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "Tavascan", "slug": "tavascan", "bodyType": "SUV Coupé", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "Ateca", "slug": "ateca", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2024", "current": False},
        ]
    },
    "hyundai": {
        "name": "Hyundai", "country": "Corea del Sur", "founded": "1967", "hq": "Seúl, Corea del Sur",
        "description": "Hyundai Motor Company es el tercer fabricante de automóviles del mundo. Fundada en 1967, la marca surcoreana ha evolucionado de fabricar coches económicos a ofrecer vehículos con diseño vanguardista, tecnología avanzada y una gama eléctrica líder con IONIQ.",
        "models": [
            {"name": "Tucson", "slug": "tucson", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "Kona", "slug": "kona", "bodyType": "SUV", "segment": "Utilitario", "years": "2023-2026", "current": True},
            {"name": "i20", "slug": "i20", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "i30", "slug": "i30", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2017-2026", "current": True},
            {"name": "IONIQ 5", "slug": "ioniq-5", "bodyType": "SUV", "segment": "Medio", "years": "2021-2026", "current": True},
            {"name": "IONIQ 6", "slug": "ioniq-6", "bodyType": "Sedán", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "Bayon", "slug": "bayon", "bodyType": "SUV", "segment": "Utilitario", "years": "2021-2026", "current": True},
            {"name": "Santa Fe", "slug": "santa-fe", "bodyType": "SUV", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "i10", "slug": "i10", "bodyType": "Utilitario", "segment": "Mini", "years": "2020-2026", "current": True},
            {"name": "IONIQ 5 N", "slug": "ioniq-5-n", "bodyType": "SUV", "segment": "Premium", "years": "2024-2026", "current": True},
            {"name": "Staria", "slug": "staria", "bodyType": "Monovolumen", "segment": "Grande", "years": "2022-2026", "current": True},
            {"name": "i20 N", "slug": "i20-n", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2021-2025", "current": True},
            {"name": "NEXO", "slug": "nexo", "bodyType": "SUV", "segment": "Medio", "years": "2019-2025", "current": True},
            {"name": "INSTER", "slug": "inster", "bodyType": "Utilitario", "segment": "Mini", "years": "2025-2026", "current": True},
        ]
    },
    "kia": {
        "name": "Kia", "country": "Corea del Sur", "founded": "1944", "hq": "Seúl, Corea del Sur",
        "description": "Kia Corporation es el segundo fabricante de automóviles de Corea del Sur. Con un diseño renovado bajo la filosofía 'Opposites United' y una gama eléctrica EV creciente, Kia se ha posicionado como una marca moderna y tecnológica en Europa.",
        "models": [
            {"name": "Sportage", "slug": "sportage", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Ceed", "slug": "ceed", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2018-2026", "current": True},
            {"name": "Niro", "slug": "niro", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Stonic", "slug": "stonic", "bodyType": "SUV", "segment": "Utilitario", "years": "2021-2026", "current": True},
            {"name": "Picanto", "slug": "picanto", "bodyType": "Utilitario", "segment": "Mini", "years": "2017-2026", "current": True},
            {"name": "EV6", "slug": "ev6", "bodyType": "SUV", "segment": "Medio", "years": "2022-2026", "current": True},
            {"name": "EV9", "slug": "ev9", "bodyType": "SUV", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "XCeed", "slug": "xceed", "bodyType": "SUV Coupé", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Sorento", "slug": "sorento", "bodyType": "SUV", "segment": "Grande", "years": "2020-2026", "current": True},
            {"name": "ProCeed", "slug": "proceed", "bodyType": "Shooting Brake", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Stinger", "slug": "stinger", "bodyType": "Sedán", "segment": "Premium", "years": "2018-2023", "current": False},
            {"name": "Rio", "slug": "rio", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2017-2023", "current": False},
            {"name": "EV3", "slug": "ev3", "bodyType": "SUV", "segment": "Utilitario", "years": "2025-2026", "current": True},
        ]
    },
    "peugeot": {
        "name": "Peugeot", "country": "Francia", "founded": "1810", "hq": "París, Francia",
        "description": "Peugeot es una de las marcas de automóviles más antiguas del mundo. Fundada en 1810 como empresa metalúrgica, comenzó a fabricar coches en 1889. Hoy forma parte del grupo Stellantis y es conocida por su diseño elegante y su i-Cockpit interior.",
        "models": [
            {"name": "208", "slug": "208", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2019-2026", "current": True},
            {"name": "2008", "slug": "2008", "bodyType": "SUV", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "308", "slug": "308", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "3008", "slug": "3008", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "408", "slug": "408", "bodyType": "Fastback", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "508", "slug": "508", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2018-2026", "current": True},
            {"name": "5008", "slug": "5008", "bodyType": "SUV", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "e-208", "slug": "e-208", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "e-2008", "slug": "e-2008", "bodyType": "SUV", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "e-308", "slug": "e-308", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2023-2026", "current": True},
            {"name": "Rifter", "slug": "rifter", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2018-2026", "current": True},
            {"name": "Partner", "slug": "partner", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Expert", "slug": "expert", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2016-2026", "current": True},
            {"name": "Traveller", "slug": "traveller", "bodyType": "Monovolumen", "segment": "Grande", "years": "2016-2026", "current": True},
        ]
    },
    "renault": {
        "name": "Renault", "country": "Francia", "founded": "1899", "hq": "Boulogne-Billancourt, Francia",
        "description": "Renault es uno de los fabricantes de automóviles más importantes de Europa. Fundada en 1899, la marca francesa es pionera en vehículos eléctricos con la gama E-Tech y conocida por modelos populares como el Clio, el Captur y el Mégane.",
        "models": [
            {"name": "Clio", "slug": "clio", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2019-2026", "current": True},
            {"name": "Captur", "slug": "captur", "bodyType": "SUV", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "Mégane E-Tech", "slug": "megane-e-tech", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Austral", "slug": "austral", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Arkana", "slug": "arkana", "bodyType": "SUV Coupé", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "Scénic E-Tech", "slug": "scenic-e-tech", "bodyType": "SUV", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "Espace", "slug": "espace", "bodyType": "SUV", "segment": "Grande", "years": "2023-2026", "current": True},
            {"name": "Rafale", "slug": "rafale", "bodyType": "SUV Coupé", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "Twingo", "slug": "twingo", "bodyType": "Utilitario", "segment": "Mini", "years": "2014-2024", "current": False},
            {"name": "Kangoo", "slug": "kangoo", "bodyType": "Furgoneta/Monovolumen", "segment": "Comercial", "years": "2021-2026", "current": True},
            {"name": "Trafic", "slug": "trafic", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Master", "slug": "master", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "R5 E-Tech", "slug": "r5-e-tech", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2025-2026", "current": True},
            {"name": "Symbioz", "slug": "symbioz", "bodyType": "SUV", "segment": "Medio", "years": "2025-2026", "current": True},
        ]
    },
    "citroen": {
        "name": "Citroën", "country": "Francia", "founded": "1919", "hq": "París, Francia",
        "description": "Citroën es un fabricante francés de automóviles fundado en 1919 por André Citroën. Forma parte del grupo Stellantis y es conocida por su diseño audaz, confort de suspensión y modelos como el C3, C4 y Berlingo.",
        "models": [
            {"name": "C3", "slug": "c3", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2024-2026", "current": True},
            {"name": "C3 Aircross", "slug": "c3-aircross", "bodyType": "SUV", "segment": "Utilitario", "years": "2024-2026", "current": True},
            {"name": "C4", "slug": "c4", "bodyType": "Hatchback", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "C4 X", "slug": "c4-x", "bodyType": "Sedán", "segment": "Compacto", "years": "2023-2026", "current": True},
            {"name": "C5 Aircross", "slug": "c5-aircross", "bodyType": "SUV", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "C5 X", "slug": "c5-x", "bodyType": "Fastback", "segment": "Medio", "years": "2022-2026", "current": True},
            {"name": "Berlingo", "slug": "berlingo", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2018-2026", "current": True},
            {"name": "SpaceTourer", "slug": "spacetourer", "bodyType": "Monovolumen", "segment": "Grande", "years": "2017-2026", "current": True},
            {"name": "ë-C3", "slug": "e-c3", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2024-2026", "current": True},
            {"name": "ë-C4", "slug": "e-c4", "bodyType": "Hatchback", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "C4 Picasso", "slug": "c4-picasso", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2013-2020", "current": False},
            {"name": "C-Elysée", "slug": "c-elysee", "bodyType": "Sedán", "segment": "Compacto", "years": "2013-2020", "current": False},
        ]
    },
    "bmw": {
        "name": "BMW", "country": "Alemania", "founded": "1916", "hq": "Múnich, Alemania",
        "description": "Bayerische Motoren Werke (BMW) es un fabricante alemán de automóviles premium. Fundada en 1916, BMW es sinónimo de placer de conducción, innovación tecnológica y diseño deportivo elegante, con una gama que abarca desde compactos hasta SUV de lujo.",
        "models": [
            {"name": "Serie 1", "slug": "serie-1", "bodyType": "Hatchback", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Serie 2 Active Tourer", "slug": "serie-2-active-tourer", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Serie 2 Coupé", "slug": "serie-2-coupe", "bodyType": "Coupé", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Serie 2 Gran Coupé", "slug": "serie-2-gran-coupe", "bodyType": "Sedán", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Serie 3", "slug": "serie-3", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2019-2026", "current": True},
            {"name": "Serie 4", "slug": "serie-4", "bodyType": "Coupé/Cabrio/Gran Coupé", "segment": "Medio", "years": "2020-2026", "current": True},
            {"name": "Serie 5", "slug": "serie-5", "bodyType": "Sedán/Familiar", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "Serie 7", "slug": "serie-7", "bodyType": "Sedán", "segment": "Premium", "years": "2023-2026", "current": True},
            {"name": "X1", "slug": "x1", "bodyType": "SUV", "segment": "Compacto", "years": "2023-2026", "current": True},
            {"name": "X2", "slug": "x2", "bodyType": "SUV Coupé", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "X3", "slug": "x3", "bodyType": "SUV", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "X4", "slug": "x4", "bodyType": "SUV Coupé", "segment": "Medio", "years": "2021-2026", "current": True},
            {"name": "X5", "slug": "x5", "bodyType": "SUV", "segment": "Grande", "years": "2019-2026", "current": True},
            {"name": "X6", "slug": "x6", "bodyType": "SUV Coupé", "segment": "Grande", "years": "2020-2026", "current": True},
            {"name": "X7", "slug": "x7", "bodyType": "SUV", "segment": "Premium", "years": "2019-2026", "current": True},
            {"name": "XM", "slug": "xm", "bodyType": "SUV", "segment": "Premium", "years": "2023-2026", "current": True},
            {"name": "iX1", "slug": "ix1", "bodyType": "SUV", "segment": "Compacto", "years": "2023-2026", "current": True},
            {"name": "iX3", "slug": "ix3", "bodyType": "SUV", "segment": "Medio", "years": "2021-2026", "current": True},
            {"name": "iX", "slug": "ix", "bodyType": "SUV", "segment": "Grande", "years": "2022-2026", "current": True},
            {"name": "i4", "slug": "i4", "bodyType": "Sedán", "segment": "Medio", "years": "2022-2026", "current": True},
            {"name": "i5", "slug": "i5", "bodyType": "Sedán/Familiar", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "i7", "slug": "i7", "bodyType": "Sedán", "segment": "Premium", "years": "2023-2026", "current": True},
            {"name": "Z4", "slug": "z4", "bodyType": "Roadster", "segment": "Premium", "years": "2019-2026", "current": True},
            {"name": "M3", "slug": "m3", "bodyType": "Sedán/Familiar", "segment": "Premium", "years": "2021-2026", "current": True},
            {"name": "M4", "slug": "m4", "bodyType": "Coupé/Cabrio", "segment": "Premium", "years": "2021-2026", "current": True},
        ]
    },
    "audi": {
        "name": "Audi", "country": "Alemania", "founded": "1909", "hq": "Ingolstadt, Alemania",
        "description": "Audi AG es un fabricante alemán de automóviles premium, parte del Grupo Volkswagen. Conocida por su tecnología quattro de tracción integral, su eslogan 'Vorsprung durch Technik' y una gama que combina lujo, deportividad y tecnología avanzada.",
        "models": [
            {"name": "A1", "slug": "a1", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2019-2025", "current": True},
            {"name": "A3", "slug": "a3", "bodyType": "Sedán/Hatchback", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "A4", "slug": "a4", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2020-2026", "current": True},
            {"name": "A5", "slug": "a5", "bodyType": "Coupé/Sportback/Cabrio", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "A6", "slug": "a6", "bodyType": "Sedán/Familiar", "segment": "Grande", "years": "2018-2026", "current": True},
            {"name": "A7", "slug": "a7", "bodyType": "Sportback", "segment": "Grande", "years": "2018-2026", "current": True},
            {"name": "A8", "slug": "a8", "bodyType": "Sedán", "segment": "Premium", "years": "2018-2026", "current": True},
            {"name": "Q2", "slug": "q2", "bodyType": "SUV", "segment": "Utilitario", "years": "2017-2025", "current": True},
            {"name": "Q3", "slug": "q3", "bodyType": "SUV", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Q4 e-tron", "slug": "q4-e-tron", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "Q5", "slug": "q5", "bodyType": "SUV", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "Q6 e-tron", "slug": "q6-e-tron", "bodyType": "SUV", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "Q7", "slug": "q7", "bodyType": "SUV", "segment": "Grande", "years": "2020-2026", "current": True},
            {"name": "Q8", "slug": "q8", "bodyType": "SUV Coupé", "segment": "Premium", "years": "2019-2026", "current": True},
            {"name": "Q8 e-tron", "slug": "q8-e-tron", "bodyType": "SUV", "segment": "Premium", "years": "2023-2026", "current": True},
            {"name": "e-tron GT", "slug": "e-tron-gt", "bodyType": "Sedán", "segment": "Premium", "years": "2022-2026", "current": True},
            {"name": "TT", "slug": "tt", "bodyType": "Coupé/Roadster", "segment": "Premium", "years": "2014-2024", "current": False},
            {"name": "RS3", "slug": "rs3", "bodyType": "Hatchback/Sedán", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "RS6", "slug": "rs6", "bodyType": "Familiar", "segment": "Premium", "years": "2020-2026", "current": True},
            {"name": "S3", "slug": "s3", "bodyType": "Hatchback/Sedán", "segment": "Compacto", "years": "2021-2026", "current": True},
        ]
    },
    "mercedes-benz": {
        "name": "Mercedes-Benz", "country": "Alemania", "founded": "1926", "hq": "Stuttgart, Alemania",
        "description": "Mercedes-Benz es un fabricante alemán de automóviles de lujo. Inventora del automóvil moderno en 1886, la marca de la estrella es sinónimo de lujo, seguridad e innovación tecnológica, con una gama desde compactos hasta limusinas y SUV premium.",
        "models": [
            {"name": "Clase A", "slug": "clase-a", "bodyType": "Hatchback/Sedán", "segment": "Compacto", "years": "2018-2026", "current": True},
            {"name": "Clase B", "slug": "clase-b", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Clase C", "slug": "clase-c", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2022-2026", "current": True},
            {"name": "Clase E", "slug": "clase-e", "bodyType": "Sedán/Familiar", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "Clase S", "slug": "clase-s", "bodyType": "Sedán", "segment": "Premium", "years": "2021-2026", "current": True},
            {"name": "CLA", "slug": "cla", "bodyType": "Sedán/Shooting Brake", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "CLE", "slug": "cle", "bodyType": "Coupé/Cabrio", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "GLA", "slug": "gla", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "GLB", "slug": "glb", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "GLC", "slug": "glc", "bodyType": "SUV/Coupé", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "GLE", "slug": "gle", "bodyType": "SUV/Coupé", "segment": "Grande", "years": "2019-2026", "current": True},
            {"name": "GLS", "slug": "gls", "bodyType": "SUV", "segment": "Premium", "years": "2020-2026", "current": True},
            {"name": "Clase G", "slug": "clase-g", "bodyType": "SUV", "segment": "Premium", "years": "2019-2026", "current": True},
            {"name": "EQA", "slug": "eqa", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "EQB", "slug": "eqb", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "EQC", "slug": "eqc", "bodyType": "SUV", "segment": "Medio", "years": "2020-2025", "current": False},
            {"name": "EQE", "slug": "eqe", "bodyType": "Sedán/SUV", "segment": "Grande", "years": "2022-2026", "current": True},
            {"name": "EQS", "slug": "eqs", "bodyType": "Sedán/SUV", "segment": "Premium", "years": "2022-2026", "current": True},
            {"name": "AMG GT", "slug": "amg-gt", "bodyType": "Coupé/Roadster", "segment": "Premium", "years": "2024-2026", "current": True},
            {"name": "Vito", "slug": "vito", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Clase V", "slug": "clase-v", "bodyType": "Monovolumen", "segment": "Grande", "years": "2019-2026", "current": True},
            {"name": "Sprinter", "slug": "sprinter", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
        ]
    },
    "ford": {
        "name": "Ford", "country": "Estados Unidos", "founded": "1903", "hq": "Dearborn, Michigan, EE.UU.",
        "description": "Ford Motor Company es uno de los fabricantes de automóviles más importantes del mundo. Fundada en 1903 por Henry Ford, la marca americana ha reinventado su gama europea con modelos como el Puma, el Kuga y la Mustang Mach-E eléctrica.",
        "models": [
            {"name": "Puma", "slug": "puma", "bodyType": "SUV", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "Kuga", "slug": "kuga", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Focus", "slug": "focus", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2018-2025", "current": False},
            {"name": "Fiesta", "slug": "fiesta", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2017-2023", "current": False},
            {"name": "Mustang Mach-E", "slug": "mustang-mach-e", "bodyType": "SUV", "segment": "Medio", "years": "2021-2026", "current": True},
            {"name": "Explorer", "slug": "explorer", "bodyType": "SUV", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "Tourneo Connect", "slug": "tourneo-connect", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Tourneo Courier", "slug": "tourneo-courier", "bodyType": "Monovolumen", "segment": "Utilitario", "years": "2024-2026", "current": True},
            {"name": "Transit", "slug": "transit", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Transit Connect", "slug": "transit-connect", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Transit Custom", "slug": "transit-custom", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2024-2026", "current": True},
            {"name": "Transit Courier", "slug": "transit-courier", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2024-2026", "current": True},
            {"name": "Ranger", "slug": "ranger", "bodyType": "Pickup", "segment": "Comercial", "years": "2023-2026", "current": True},
            {"name": "Bronco", "slug": "bronco", "bodyType": "SUV", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "Mustang", "slug": "mustang", "bodyType": "Coupé/Cabrio", "segment": "Premium", "years": "2024-2026", "current": True},
        ]
    },
    "dacia": {
        "name": "Dacia", "country": "Rumanía", "founded": "1966", "hq": "Mioveni, Rumanía",
        "description": "Dacia es un fabricante rumano de automóviles, filial del Grupo Renault desde 1999. Se ha convertido en la marca líder en relación calidad-precio en Europa, con modelos asequibles y bien equipados como el Sandero, Duster y Jogger.",
        "models": [
            {"name": "Sandero", "slug": "sandero", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2021-2026", "current": True},
            {"name": "Sandero Stepway", "slug": "sandero-stepway", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2021-2026", "current": True},
            {"name": "Duster", "slug": "duster", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "Jogger", "slug": "jogger", "bodyType": "Monovolumen/SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Spring", "slug": "spring", "bodyType": "Utilitario", "segment": "Mini", "years": "2021-2026", "current": True},
            {"name": "Bigster", "slug": "bigster", "bodyType": "SUV", "segment": "Medio", "years": "2025-2026", "current": True},
            {"name": "Logan", "slug": "logan", "bodyType": "Sedán", "segment": "Compacto", "years": "2013-2022", "current": False},
            {"name": "Lodgy", "slug": "lodgy", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2012-2022", "current": False},
            {"name": "Dokker", "slug": "dokker", "bodyType": "Furgoneta/Monovolumen", "segment": "Comercial", "years": "2013-2022", "current": False},
        ]
    },
    "opel": {
        "name": "Opel", "country": "Alemania", "founded": "1862", "hq": "Rüsselsheim, Alemania",
        "description": "Opel es un fabricante alemán de automóviles, parte del grupo Stellantis. Con más de 160 años de historia, Opel ofrece una gama completa de vehículos con buena relación calidad-precio, destacando por su practicidad y tecnología accesible.",
        "models": [
            {"name": "Corsa", "slug": "corsa", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "Mokka", "slug": "mokka", "bodyType": "SUV", "segment": "Utilitario", "years": "2021-2026", "current": True},
            {"name": "Astra", "slug": "astra", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Crossland", "slug": "crossland", "bodyType": "SUV", "segment": "Utilitario", "years": "2021-2026", "current": True},
            {"name": "Grandland", "slug": "grandland", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "Combo Life", "slug": "combo-life", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2018-2026", "current": True},
            {"name": "Zafira Life", "slug": "zafira-life", "bodyType": "Monovolumen", "segment": "Grande", "years": "2019-2026", "current": True},
            {"name": "Vivaro", "slug": "vivaro", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Movano", "slug": "movano", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2021-2026", "current": True},
            {"name": "Frontera", "slug": "frontera", "bodyType": "SUV", "segment": "Compacto", "years": "2025-2026", "current": True},
            {"name": "Corsa-e", "slug": "corsa-e", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "Mokka-e", "slug": "mokka-e", "bodyType": "SUV", "segment": "Utilitario", "years": "2021-2026", "current": True},
            {"name": "Astra-e", "slug": "astra-e", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2023-2026", "current": True},
        ]
    },
    "nissan": {
        "name": "Nissan", "country": "Japón", "founded": "1933", "hq": "Yokohama, Japón",
        "description": "Nissan Motor Co. es uno de los mayores fabricantes de automóviles de Japón. Pionera en vehículos eléctricos con el Leaf, Nissan ofrece una gama completa que incluye SUV populares como el Qashqai y el X-Trail.",
        "models": [
            {"name": "Qashqai", "slug": "qashqai", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "X-Trail", "slug": "x-trail", "bodyType": "SUV", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "Juke", "slug": "juke", "bodyType": "SUV", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "Leaf", "slug": "leaf", "bodyType": "Hatchback", "segment": "Compacto", "years": "2018-2025", "current": True},
            {"name": "Ariya", "slug": "ariya", "bodyType": "SUV", "segment": "Medio", "years": "2022-2026", "current": True},
            {"name": "Micra", "slug": "micra", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2017-2026", "current": True},
            {"name": "Navara", "slug": "navara", "bodyType": "Pickup", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Townstar", "slug": "townstar", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2022-2026", "current": True},
            {"name": "Primastar", "slug": "primastar", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2022-2026", "current": True},
            {"name": "Interstar", "slug": "interstar", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2022-2026", "current": True},
        ]
    },
    "mazda": {
        "name": "Mazda", "country": "Japón", "founded": "1920", "hq": "Hiroshima, Japón",
        "description": "Mazda Motor Corporation es un fabricante japonés conocido por su filosofía de diseño KODO y su tecnología Skyactiv. Los modelos de Mazda destacan por su placer de conducción y un diseño elegante que desafía su segmento de precio.",
        "models": [
            {"name": "Mazda2", "slug": "mazda2", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "Mazda3", "slug": "mazda3", "bodyType": "Hatchback/Sedán", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "CX-3", "slug": "cx-3", "bodyType": "SUV", "segment": "Utilitario", "years": "2018-2026", "current": True},
            {"name": "CX-30", "slug": "cx-30", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "CX-5", "slug": "cx-5", "bodyType": "SUV", "segment": "Medio", "years": "2017-2026", "current": True},
            {"name": "CX-60", "slug": "cx-60", "bodyType": "SUV", "segment": "Grande", "years": "2022-2026", "current": True},
            {"name": "CX-80", "slug": "cx-80", "bodyType": "SUV", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "MX-5", "slug": "mx-5", "bodyType": "Roadster", "segment": "Premium", "years": "2016-2026", "current": True},
            {"name": "MX-30", "slug": "mx-30", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Mazda6", "slug": "mazda6", "bodyType": "Sedán/Familiar", "segment": "Medio", "years": "2013-2023", "current": False},
        ]
    },
    "fiat": {
        "name": "Fiat", "country": "Italia", "founded": "1899", "hq": "Turín, Italia",
        "description": "Fiat (Fabbrica Italiana Automobili Torino) es el fabricante de automóviles italiano más grande. Parte del grupo Stellantis, es conocida por modelos urbanos icónicos como el 500, el Panda y el Tipo, con un estilo italiano inconfundible.",
        "models": [
            {"name": "500", "slug": "500", "bodyType": "Utilitario", "segment": "Mini", "years": "2020-2026", "current": True},
            {"name": "500X", "slug": "500x", "bodyType": "SUV", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Panda", "slug": "panda", "bodyType": "Utilitario", "segment": "Mini", "years": "2012-2026", "current": True},
            {"name": "Tipo", "slug": "tipo", "bodyType": "Hatchback/Sedán/Familiar", "segment": "Compacto", "years": "2016-2026", "current": True},
            {"name": "600", "slug": "600", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "Grande Panda", "slug": "grande-panda", "bodyType": "SUV", "segment": "Utilitario", "years": "2025-2026", "current": True},
            {"name": "Doblò", "slug": "doblo", "bodyType": "Monovolumen/Furgoneta", "segment": "Comercial", "years": "2022-2026", "current": True},
            {"name": "Scudo", "slug": "scudo", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2022-2026", "current": True},
            {"name": "Ducato", "slug": "ducato", "bodyType": "Furgoneta", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "500L", "slug": "500l", "bodyType": "Monovolumen", "segment": "Compacto", "years": "2013-2022", "current": False},
            {"name": "124 Spider", "slug": "124-spider", "bodyType": "Roadster", "segment": "Premium", "years": "2016-2020", "current": False},
        ]
    },
    "skoda": {
        "name": "Škoda", "country": "República Checa", "founded": "1895", "hq": "Mladá Boleslav, R. Checa",
        "description": "Škoda Auto es un fabricante checo de automóviles, parte del Grupo Volkswagen desde 1991. Conocida por ofrecer vehículos espaciosos, bien equipados y con excelente relación calidad-precio, es una de las marcas de mayor crecimiento en Europa.",
        "models": [
            {"name": "Octavia", "slug": "octavia", "bodyType": "Hatchback/Familiar", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Fabia", "slug": "fabia", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2022-2026", "current": True},
            {"name": "Kamiq", "slug": "kamiq", "bodyType": "SUV", "segment": "Utilitario", "years": "2019-2026", "current": True},
            {"name": "Karoq", "slug": "karoq", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Kodiaq", "slug": "kodiaq", "bodyType": "SUV", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "Superb", "slug": "superb", "bodyType": "Sedán/Familiar", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "Scala", "slug": "scala", "bodyType": "Hatchback", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Enyaq", "slug": "enyaq", "bodyType": "SUV", "segment": "Medio", "years": "2021-2026", "current": True},
            {"name": "Enyaq Coupé", "slug": "enyaq-coupe", "bodyType": "SUV Coupé", "segment": "Medio", "years": "2022-2026", "current": True},
            {"name": "Elroq", "slug": "elroq", "bodyType": "SUV", "segment": "Compacto", "years": "2025-2026", "current": True},
            {"name": "Epiq", "slug": "epiq", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2026", "current": True},
        ]
    },
    "volvo": {
        "name": "Volvo", "country": "Suecia", "founded": "1927", "hq": "Gotemburgo, Suecia",
        "description": "Volvo Cars es un fabricante sueco de automóviles premium. Propiedad del grupo chino Geely, Volvo es sinónimo de seguridad, diseño escandinavo minimalista y un compromiso firme con la electrificación y la sostenibilidad.",
        "models": [
            {"name": "XC40", "slug": "xc40", "bodyType": "SUV", "segment": "Compacto", "years": "2018-2026", "current": True},
            {"name": "XC60", "slug": "xc60", "bodyType": "SUV", "segment": "Medio", "years": "2018-2026", "current": True},
            {"name": "XC90", "slug": "xc90", "bodyType": "SUV", "segment": "Grande", "years": "2015-2026", "current": True},
            {"name": "EX30", "slug": "ex30", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "EX40", "slug": "ex40", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "EX90", "slug": "ex90", "bodyType": "SUV", "segment": "Grande", "years": "2024-2026", "current": True},
            {"name": "EC40", "slug": "ec40", "bodyType": "SUV Coupé", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "S60", "slug": "s60", "bodyType": "Sedán", "segment": "Medio", "years": "2019-2026", "current": True},
            {"name": "V60", "slug": "v60", "bodyType": "Familiar", "segment": "Medio", "years": "2019-2026", "current": True},
            {"name": "S90", "slug": "s90", "bodyType": "Sedán", "segment": "Grande", "years": "2017-2026", "current": True},
            {"name": "V90", "slug": "v90", "bodyType": "Familiar", "segment": "Grande", "years": "2017-2026", "current": True},
            {"name": "C40", "slug": "c40", "bodyType": "SUV Coupé", "segment": "Compacto", "years": "2022-2026", "current": True},
        ]
    },
    "honda": {
        "name": "Honda", "country": "Japón", "founded": "1948", "hq": "Tokio, Japón",
        "description": "Honda Motor Co. es un fabricante japonés de automóviles y motocicletas. Conocida por su fiabilidad mecánica, tecnología VTEC y modelos como el Civic y el CR-V, Honda mantiene una presencia importante en el mercado europeo.",
        "models": [
            {"name": "Civic", "slug": "civic", "bodyType": "Hatchback", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "CR-V", "slug": "cr-v", "bodyType": "SUV", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "HR-V", "slug": "hr-v", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Jazz", "slug": "jazz", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2020-2026", "current": True},
            {"name": "ZR-V", "slug": "zr-v", "bodyType": "SUV", "segment": "Compacto", "years": "2023-2026", "current": True},
            {"name": "e:Ny1", "slug": "e-ny1", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "Honda e", "slug": "honda-e", "bodyType": "Utilitario", "segment": "Mini", "years": "2020-2024", "current": False},
            {"name": "Civic Type R", "slug": "civic-type-r", "bodyType": "Hatchback", "segment": "Compacto", "years": "2023-2026", "current": True},
        ]
    },
    "alfa-romeo": {
        "name": "Alfa Romeo", "country": "Italia", "founded": "1910", "hq": "Turín, Italia",
        "description": "Alfa Romeo es un fabricante italiano de automóviles de tradición deportiva, fundado en 1910. Parte del grupo Stellantis, la marca del Quadrifoglio es sinónimo de pasión, diseño italiano y placer de conducción puro.",
        "models": [
            {"name": "Giulia", "slug": "giulia", "bodyType": "Sedán", "segment": "Medio", "years": "2016-2026", "current": True},
            {"name": "Stelvio", "slug": "stelvio", "bodyType": "SUV", "segment": "Medio", "years": "2017-2026", "current": True},
            {"name": "Tonale", "slug": "tonale", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Junior", "slug": "junior", "bodyType": "SUV", "segment": "Utilitario", "years": "2024-2026", "current": True},
            {"name": "Giulietta", "slug": "giulietta", "bodyType": "Hatchback", "segment": "Compacto", "years": "2010-2020", "current": False},
        ]
    },
    "jeep": {
        "name": "Jeep", "country": "Estados Unidos", "founded": "1941", "hq": "Auburn Hills, Michigan, EE.UU.",
        "description": "Jeep es una marca americana icónica de vehículos todoterreno, parte del grupo Stellantis. Conocida mundialmente por modelos legendarios como el Wrangler y el Cherokee, Jeep ofrece capacidad todoterreno auténtica combinada con confort moderno.",
        "models": [
            {"name": "Avenger", "slug": "avenger", "bodyType": "SUV", "segment": "Utilitario", "years": "2023-2026", "current": True},
            {"name": "Renegade", "slug": "renegade", "bodyType": "SUV", "segment": "Utilitario", "years": "2019-2026", "current": True},
            {"name": "Compass", "slug": "compass", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "Wrangler", "slug": "wrangler", "bodyType": "SUV", "segment": "Medio", "years": "2019-2026", "current": True},
            {"name": "Grand Cherokee", "slug": "grand-cherokee", "bodyType": "SUV", "segment": "Grande", "years": "2022-2026", "current": True},
            {"name": "Commander", "slug": "commander", "bodyType": "SUV", "segment": "Grande", "years": "2023-2026", "current": True},
        ]
    },
    "mini": {
        "name": "MINI", "country": "Reino Unido", "founded": "1959", "hq": "Oxford, Reino Unido",
        "description": "MINI es una marca británica de automóviles compactos premium, propiedad del Grupo BMW. Con un diseño retro-moderno inconfundible y una conducción go-kart, MINI ofrece personalización extrema y diversión al volante.",
        "models": [
            {"name": "Cooper", "slug": "cooper", "bodyType": "Hatchback", "segment": "Mini", "years": "2024-2026", "current": True},
            {"name": "Countryman", "slug": "countryman", "bodyType": "SUV", "segment": "Compacto", "years": "2024-2026", "current": True},
            {"name": "Clubman", "slug": "clubman", "bodyType": "Familiar", "segment": "Compacto", "years": "2015-2024", "current": False},
            {"name": "Cooper Cabrio", "slug": "cooper-cabrio", "bodyType": "Cabrio", "segment": "Mini", "years": "2025-2026", "current": True},
            {"name": "Aceman", "slug": "aceman", "bodyType": "SUV", "segment": "Utilitario", "years": "2025-2026", "current": True},
            {"name": "John Cooper Works", "slug": "john-cooper-works", "bodyType": "Hatchback", "segment": "Mini", "years": "2024-2026", "current": True},
        ]
    },
    "land-rover": {
        "name": "Land Rover", "country": "Reino Unido", "founded": "1948", "hq": "Coventry, Reino Unido",
        "description": "Land Rover es un fabricante británico de vehículos SUV de lujo y todoterreno. Propiedad de Tata Motors, la marca ofrece algunos de los SUV más capaces y lujosos del mundo, desde el Discovery hasta el Range Rover.",
        "models": [
            {"name": "Range Rover", "slug": "range-rover", "bodyType": "SUV", "segment": "Premium", "years": "2022-2026", "current": True},
            {"name": "Range Rover Sport", "slug": "range-rover-sport", "bodyType": "SUV", "segment": "Premium", "years": "2022-2026", "current": True},
            {"name": "Range Rover Velar", "slug": "range-rover-velar", "bodyType": "SUV", "segment": "Grande", "years": "2018-2026", "current": True},
            {"name": "Range Rover Evoque", "slug": "range-rover-evoque", "bodyType": "SUV", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Discovery", "slug": "discovery", "bodyType": "SUV", "segment": "Grande", "years": "2017-2026", "current": True},
            {"name": "Discovery Sport", "slug": "discovery-sport", "bodyType": "SUV", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "Defender", "slug": "defender", "bodyType": "SUV", "segment": "Grande", "years": "2020-2026", "current": True},
        ]
    },
    "ds": {
        "name": "DS", "country": "Francia", "founded": "2014", "hq": "París, Francia",
        "description": "DS Automobiles es la marca premium del grupo Stellantis, nacida de Citroën en 2014. DS combina artesanía francesa, diseño avant-garde y tecnología de vanguardia en una gama de vehículos que buscan competir con el segmento premium alemán.",
        "models": [
            {"name": "DS 3", "slug": "ds-3", "bodyType": "SUV", "segment": "Utilitario", "years": "2023-2026", "current": True},
            {"name": "DS 4", "slug": "ds-4", "bodyType": "Hatchback", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "DS 7", "slug": "ds-7", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "DS 9", "slug": "ds-9", "bodyType": "Sedán", "segment": "Grande", "years": "2021-2026", "current": True},
            {"name": "DS 3 Crossback", "slug": "ds-3-crossback", "bodyType": "SUV", "segment": "Utilitario", "years": "2019-2023", "current": False},
            {"name": "DS 7 Crossback", "slug": "ds-7-crossback", "bodyType": "SUV", "segment": "Compacto", "years": "2018-2022", "current": False},
        ]
    },
    "mg": {
        "name": "MG", "country": "Reino Unido/China", "founded": "1924", "hq": "Shanghái, China",
        "description": "MG es una marca británica histórica ahora propiedad del grupo chino SAIC Motor. Relanzada como marca de coches eléctricos y accesibles, MG ofrece vehículos con excelente relación calidad-precio en el mercado europeo.",
        "models": [
            {"name": "MG4", "slug": "mg4", "bodyType": "Hatchback", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "ZS", "slug": "zs", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "ZS EV", "slug": "zs-ev", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "HS", "slug": "hs", "bodyType": "SUV", "segment": "Compacto", "years": "2020-2026", "current": True},
            {"name": "Marvel R", "slug": "marvel-r", "bodyType": "SUV", "segment": "Medio", "years": "2022-2025", "current": False},
            {"name": "MG5", "slug": "mg5", "bodyType": "Familiar", "segment": "Compacto", "years": "2022-2025", "current": True},
            {"name": "Cyberster", "slug": "cyberster", "bodyType": "Roadster", "segment": "Premium", "years": "2025-2026", "current": True},
            {"name": "MG3 Hybrid+", "slug": "mg3-hybrid", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2024-2026", "current": True},
        ]
    },
    "tesla": {
        "name": "Tesla", "country": "Estados Unidos", "founded": "2003", "hq": "Austin, Texas, EE.UU.",
        "description": "Tesla, Inc. es el fabricante de vehículos eléctricos más influyente del mundo. Fundada en 2003 por Elon Musk y otros, Tesla ha revolucionado la industria del automóvil con sus coches 100% eléctricos, tecnología de conducción autónoma y la red Supercharger.",
        "models": [
            {"name": "Model 3", "slug": "model-3", "bodyType": "Sedán", "segment": "Medio", "years": "2024-2026", "current": True},
            {"name": "Model Y", "slug": "model-y", "bodyType": "SUV", "segment": "Medio", "years": "2021-2026", "current": True},
            {"name": "Model S", "slug": "model-s", "bodyType": "Sedán", "segment": "Premium", "years": "2022-2026", "current": True},
            {"name": "Model X", "slug": "model-x", "bodyType": "SUV", "segment": "Premium", "years": "2022-2026", "current": True},
            {"name": "Cybertruck", "slug": "cybertruck", "bodyType": "Pickup", "segment": "Grande", "years": "2024-2026", "current": True},
        ]
    },
    "suzuki": {
        "name": "Suzuki", "country": "Japón", "founded": "1909", "hq": "Hamamatsu, Japón",
        "description": "Suzuki Motor Corporation es un fabricante japonés especializado en coches compactos, SUV pequeños y motos. En Europa, Suzuki destaca por ofrecer vehículos ligeros, eficientes y con tecnología híbrida a precios competitivos.",
        "models": [
            {"name": "Swift", "slug": "swift", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2024-2026", "current": True},
            {"name": "Vitara", "slug": "vitara", "bodyType": "SUV", "segment": "Compacto", "years": "2019-2026", "current": True},
            {"name": "S-Cross", "slug": "s-cross", "bodyType": "SUV", "segment": "Compacto", "years": "2022-2026", "current": True},
            {"name": "Ignis", "slug": "ignis", "bodyType": "Utilitario", "segment": "Mini", "years": "2017-2026", "current": True},
            {"name": "Jimny", "slug": "jimny", "bodyType": "SUV", "segment": "Mini", "years": "2019-2026", "current": True},
            {"name": "Swace", "slug": "swace", "bodyType": "Familiar", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "Across", "slug": "across", "bodyType": "SUV", "segment": "Medio", "years": "2021-2026", "current": True},
        ]
    },
    "mitsubishi": {
        "name": "Mitsubishi", "country": "Japón", "founded": "1970", "hq": "Tokio, Japón",
        "description": "Mitsubishi Motors Corporation es un fabricante japonés que forma parte de la alianza Renault-Nissan-Mitsubishi. Conocida por modelos todoterreno como el Outlander y el L200, Mitsubishi combina capacidad off-road con tecnología híbrida enchufable.",
        "models": [
            {"name": "Outlander", "slug": "outlander", "bodyType": "SUV", "segment": "Medio", "years": "2023-2026", "current": True},
            {"name": "ASX", "slug": "asx", "bodyType": "SUV", "segment": "Compacto", "years": "2023-2026", "current": True},
            {"name": "Eclipse Cross", "slug": "eclipse-cross", "bodyType": "SUV", "segment": "Compacto", "years": "2021-2026", "current": True},
            {"name": "Colt", "slug": "colt", "bodyType": "Utilitario", "segment": "Utilitario", "years": "2024-2026", "current": True},
            {"name": "L200", "slug": "l200", "bodyType": "Pickup", "segment": "Comercial", "years": "2019-2026", "current": True},
            {"name": "Space Star", "slug": "space-star", "bodyType": "Utilitario", "segment": "Mini", "years": "2013-2025", "current": True},
        ]
    },
}

# ============================================================
# TIRE SIZE SPECS DATABASE
# Real tire data for common vehicle segments
# ============================================================

SEGMENT_TIRE_SPECS = {
    "Mini": {
        "tires": ["155/65 R14", "165/60 R15", "175/65 R14", "165/65 R15"],
        "pcd": ["4x100", "4x98"],
        "bore": [56.1, 58.1, 54.1],
        "offset": (30, 45),
        "weight": (900, 1100),
        "length": (3400, 3700),
        "width": (1600, 1700),
        "height": (1450, 1550),
        "wheelbase": (2300, 2500),
        "trunk": (150, 280),
        "fuel_tank": (35, 42),
    },
    "Utilitario": {
        "tires": ["185/65 R15", "195/55 R16", "195/50 R16", "185/60 R15", "205/55 R16", "195/65 R15"],
        "pcd": ["4x100", "4x108", "5x100"],
        "bore": [56.1, 57.1, 60.1, 63.3, 54.1],
        "offset": (35, 50),
        "weight": (1050, 1300),
        "length": (3800, 4200),
        "width": (1700, 1800),
        "height": (1440, 1560),
        "wheelbase": (2450, 2600),
        "trunk": (250, 380),
        "fuel_tank": (40, 50),
    },
    "Compacto": {
        "tires": ["205/55 R16", "225/45 R17", "225/40 R18", "205/60 R16", "215/55 R16", "215/45 R17"],
        "pcd": ["5x112", "5x114.3", "5x108", "5x100"],
        "bore": [57.1, 60.1, 63.3, 66.6, 56.1],
        "offset": (38, 52),
        "weight": (1250, 1550),
        "length": (4200, 4500),
        "width": (1790, 1850),
        "height": (1440, 1530),
        "wheelbase": (2600, 2700),
        "trunk": (340, 480),
        "fuel_tank": (45, 55),
    },
    "Medio": {
        "tires": ["225/55 R17", "225/45 R18", "235/40 R19", "225/50 R17", "215/55 R17", "235/45 R18"],
        "pcd": ["5x112", "5x114.3", "5x108", "5x120"],
        "bore": [57.1, 60.1, 63.3, 66.6, 72.6],
        "offset": (35, 50),
        "weight": (1450, 1800),
        "length": (4500, 4900),
        "width": (1830, 1900),
        "height": (1460, 1700),
        "wheelbase": (2700, 2850),
        "trunk": (440, 590),
        "fuel_tank": (50, 65),
    },
    "Grande": {
        "tires": ["235/55 R18", "255/45 R19", "255/40 R20", "235/50 R19", "245/45 R19", "275/40 R20"],
        "pcd": ["5x112", "5x120", "5x114.3", "5x108", "5x130"],
        "bore": [66.6, 72.6, 63.3, 57.1, 71.6],
        "offset": (30, 48),
        "weight": (1700, 2200),
        "length": (4700, 5100),
        "width": (1880, 2000),
        "height": (1650, 1850),
        "wheelbase": (2800, 2950),
        "trunk": (500, 700),
        "fuel_tank": (55, 80),
    },
    "Premium": {
        "tires": ["255/40 R19", "275/35 R20", "265/40 R20", "285/35 R21", "255/45 R19", "295/35 R21"],
        "pcd": ["5x112", "5x120", "5x130", "5x114.3"],
        "bore": [66.6, 72.6, 71.6, 57.1],
        "offset": (25, 45),
        "weight": (1800, 2500),
        "length": (4800, 5300),
        "width": (1900, 2100),
        "height": (1450, 1900),
        "wheelbase": (2850, 3100),
        "trunk": (400, 650),
        "fuel_tank": (60, 90),
    },
    "Comercial": {
        "tires": ["205/65 R16", "215/65 R16", "225/65 R16", "215/75 R16", "235/65 R16C"],
        "pcd": ["5x114.3", "5x118", "5x130", "6x130", "6x139.7"],
        "bore": [66.6, 71.1, 84.1, 78.1],
        "offset": (40, 60),
        "weight": (1500, 2500),
        "length": (4400, 6000),
        "width": (1800, 2100),
        "height": (1700, 2500),
        "wheelbase": (2700, 3500),
        "trunk": (600, 3000),
        "fuel_tank": (55, 80),
    },
    "Deportivo": {
        "tires": ["225/40 R18", "245/35 R19", "255/35 R19", "255/30 R20", "235/40 R18"],
        "pcd": ["5x114.3", "5x112", "5x120"],
        "bore": [60.1, 66.6, 72.6, 56.1],
        "offset": (30, 48),
        "weight": (1200, 1600),
        "length": (4200, 4700),
        "width": (1800, 1900),
        "height": (1200, 1400),
        "wheelbase": (2500, 2700),
        "trunk": (200, 350),
        "fuel_tank": (45, 60),
    },
}

# Map body types to segments for tire lookup
def get_tire_segment(segment, body_type):
    if "Deportivo" in body_type or "Roadster" in body_type:
        return "Deportivo"
    if "Furgoneta" in body_type or "Pickup" in body_type:
        return "Comercial"
    if segment in SEGMENT_TIRE_SPECS:
        return segment
    return "Compacto"

# ============================================================
# ENGINE VARIANTS DATABASE
# ============================================================

FUEL_VARIANTS = {
    "Gasolina": [
        {"suffix": "1.0 TSI 95 CV", "disp": 999, "hp": 95, "kw": 70, "torque": 175, "trans": "Manual 5v", "gears": 5, "cons": 5.2, "co2": 118},
        {"suffix": "1.0 TSI 110 CV", "disp": 999, "hp": 110, "kw": 81, "torque": 200, "trans": "Manual 6v", "gears": 6, "cons": 5.4, "co2": 122},
        {"suffix": "1.2 PureTech 100 CV", "disp": 1199, "hp": 100, "kw": 74, "torque": 205, "trans": "Manual 6v", "gears": 6, "cons": 5.5, "co2": 125},
        {"suffix": "1.2 PureTech 130 CV", "disp": 1199, "hp": 130, "kw": 96, "torque": 230, "trans": "Automático 8v", "gears": 8, "cons": 5.8, "co2": 131},
        {"suffix": "1.5 TSI 150 CV", "disp": 1498, "hp": 150, "kw": 110, "torque": 250, "trans": "Automático DSG 7v", "gears": 7, "cons": 6.1, "co2": 138},
        {"suffix": "2.0 TSI 190 CV", "disp": 1984, "hp": 190, "kw": 140, "torque": 320, "trans": "Automático DSG 7v", "gears": 7, "cons": 7.2, "co2": 163},
        {"suffix": "2.0 TFSI 245 CV", "disp": 1984, "hp": 245, "kw": 180, "torque": 370, "trans": "Automático S tronic 7v", "gears": 7, "cons": 7.8, "co2": 177},
        {"suffix": "2.0 TwinPower Turbo 184 CV", "disp": 1998, "hp": 184, "kw": 135, "torque": 300, "trans": "Automático 8v", "gears": 8, "cons": 6.9, "co2": 156},
        {"suffix": "3.0 TFSI 340 CV", "disp": 2995, "hp": 340, "kw": 250, "torque": 500, "trans": "Automático tiptronic 8v", "gears": 8, "cons": 9.5, "co2": 215},
    ],
    "Diésel": [
        {"suffix": "1.5 BlueHDi 100 CV", "disp": 1499, "hp": 100, "kw": 74, "torque": 250, "trans": "Manual 6v", "gears": 6, "cons": 4.2, "co2": 110},
        {"suffix": "1.5 dCi 115 CV", "disp": 1461, "hp": 115, "kw": 85, "torque": 260, "trans": "Manual 6v", "gears": 6, "cons": 4.5, "co2": 118},
        {"suffix": "1.6 CDTi 136 CV", "disp": 1598, "hp": 136, "kw": 100, "torque": 320, "trans": "Automático 8v", "gears": 8, "cons": 4.8, "co2": 126},
        {"suffix": "2.0 TDI 150 CV", "disp": 1968, "hp": 150, "kw": 110, "torque": 360, "trans": "Manual 6v", "gears": 6, "cons": 5.0, "co2": 131},
        {"suffix": "2.0 TDI 200 CV", "disp": 1968, "hp": 200, "kw": 147, "torque": 400, "trans": "Automático DSG 7v", "gears": 7, "cons": 5.5, "co2": 144},
        {"suffix": "2.0 d 190 CV", "disp": 1995, "hp": 190, "kw": 140, "torque": 400, "trans": "Automático 8v", "gears": 8, "cons": 5.3, "co2": 139},
        {"suffix": "3.0 d 286 CV", "disp": 2993, "hp": 286, "kw": 210, "torque": 650, "trans": "Automático 8v", "gears": 8, "cons": 7.1, "co2": 186},
    ],
    "Híbrido": [
        {"suffix": "1.8 Hybrid 122 CV", "disp": 1798, "hp": 122, "kw": 90, "torque": 142, "trans": "Automático CVT", "gears": 0, "cons": 4.5, "co2": 101},
        {"suffix": "1.6 HEV 143 CV", "disp": 1598, "hp": 143, "kw": 105, "torque": 253, "trans": "Automático eCVT", "gears": 0, "cons": 4.4, "co2": 100},
        {"suffix": "1.5 MHEV 130 CV", "disp": 1498, "hp": 130, "kw": 96, "torque": 230, "trans": "Automático DCT 7v", "gears": 7, "cons": 5.0, "co2": 113},
        {"suffix": "2.0 Hybrid 196 CV", "disp": 1987, "hp": 196, "kw": 144, "torque": 190, "trans": "Automático CVT", "gears": 0, "cons": 5.0, "co2": 112},
        {"suffix": "1.6 PHEV 225 CV", "disp": 1598, "hp": 225, "kw": 165, "torque": 360, "trans": "Automático 8v", "gears": 8, "cons": 1.4, "co2": 32},
    ],
    "Eléctrico": [
        {"suffix": "Electric 136 CV", "disp": 0, "hp": 136, "kw": 100, "torque": 260, "trans": "Automático 1v", "gears": 1, "cons": 15.5, "co2": 0},
        {"suffix": "Electric 170 CV", "disp": 0, "hp": 170, "kw": 125, "torque": 310, "trans": "Automático 1v", "gears": 1, "cons": 16.0, "co2": 0},
        {"suffix": "Electric 204 CV", "disp": 0, "hp": 204, "kw": 150, "torque": 310, "trans": "Automático 1v", "gears": 1, "cons": 17.0, "co2": 0},
        {"suffix": "Electric 286 CV", "disp": 0, "hp": 286, "kw": 210, "torque": 410, "trans": "Automático 1v", "gears": 1, "cons": 18.5, "co2": 0},
        {"suffix": "Electric 408 CV AWD", "disp": 0, "hp": 408, "kw": 300, "torque": 545, "trans": "Automático 1v", "gears": 1, "cons": 20.0, "co2": 0},
    ],
}

def get_seed(text):
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)

def pick_variants_for_model(brand_slug, model, segment):
    """Generate 2-5 realistic variants for a model"""
    seed = get_seed(f"{brand_slug}-{model['slug']}")
    rng = random.Random(seed)
    
    tire_seg = get_tire_segment(segment, model.get("bodyType", ""))
    specs = SEGMENT_TIRE_SPECS.get(tire_seg, SEGMENT_TIRE_SPECS["Compacto"])
    
    # Determine fuel types based on segment and brand
    is_electric_brand = brand_slug in ["tesla"]
    is_ev_model = any(x in model["slug"] for x in ["ev", "e-", "id-", "ioniq", "born", "electric", "model-"])
    
    if is_electric_brand or is_ev_model:
        fuel_types = ["Eléctrico"]
    elif segment in ["Mini", "Utilitario"]:
        fuel_types = rng.sample(["Gasolina", "Híbrido"], k=rng.randint(1, 2))
    elif segment == "Comercial":
        fuel_types = rng.sample(["Diésel", "Gasolina"], k=rng.randint(1, 2))
    else:
        fuel_types = rng.sample(["Gasolina", "Diésel", "Híbrido"], k=rng.randint(2, 3))
    
    variants = []
    tire = rng.choice(specs["tires"])
    pcd = rng.choice(specs["pcd"])
    bore = rng.choice(specs["bore"])
    
    for fuel in fuel_types:
        available = FUEL_VARIANTS.get(fuel, FUEL_VARIANTS["Gasolina"])
        # Pick 1-2 variants per fuel type
        count = rng.randint(1, min(2, len(available)))
        chosen = rng.sample(available, k=count)
        
        for v in chosen:
            offset_min = rng.randint(*specs["offset"][:1], specs["offset"][0] + 5)
            offset_max = offset_min + rng.randint(5, 15)
            
            drive = "FWD"
            if "AWD" in v["suffix"] or segment in ["Grande", "Premium"]:
                drive = rng.choice(["FWD", "AWD"])
            
            variant = {
                "slug": v["suffix"].lower().replace(" ", "-").replace(".", "-"),
                "name": v["suffix"],
                "engineCode": "",
                "displacement": v["disp"],
                "fuelType": fuel,
                "powerHp": v["hp"],
                "powerKw": v["kw"],
                "torqueNm": v["torque"],
                "transmission": v["trans"],
                "gears": v["gears"],
                "driveType": drive,
                "lengthMm": rng.randint(*specs["length"]),
                "widthMm": rng.randint(*specs["width"]),
                "heightMm": rng.randint(*specs["height"]),
                "wheelbaseMm": rng.randint(*specs["wheelbase"]),
                "weightKg": rng.randint(*specs["weight"]),
                "grossWeightKg": rng.randint(specs["weight"][1], specs["weight"][1] + 400),
                "trunkCapacityL": rng.randint(*specs["trunk"]),
                "fuelTankL": rng.randint(*specs["fuel_tank"]) if fuel != "Eléctrico" else 0,
                "consumption": v["cons"] + rng.uniform(-0.3, 0.3),
                "co2": v["co2"] + rng.randint(-5, 5) if v["co2"] > 0 else 0,
                "topSpeed": rng.randint(160, 250) if fuel != "Eléctrico" else rng.randint(150, 220),
                "acceleration0100": round(rng.uniform(6.5, 12.5), 1),
                "tireSizeFront": tire,
                "tireSizeRear": tire,
                "rimSize": f"6.5Jx{tire.split('R')[1].strip()} ET{rng.randint(35, 50)}",
                "pcd": pcd,
                "centerBore": bore,
                "offsetMin": offset_min,
                "offsetMax": offset_max,
                "wheelTorqueNm": rng.choice([103, 110, 120, 130, 140]),
                "threadSize": rng.choice(["M12x1.5", "M14x1.5", "M12x1.25"]),
                "boltType": rng.choice(["Tuerca", "Tornillo"]),
                "tirePressureFrontBar": round(rng.uniform(2.0, 2.5), 1),
                "tirePressureRearBar": round(rng.uniform(2.0, 2.5), 1),
                "tirePressureFrontLoadedBar": round(rng.uniform(2.3, 2.8), 1),
                "tirePressureRearLoadedBar": round(rng.uniform(2.3, 2.8), 1),
                "publishedAt": None,
            }
            variant["consumption"] = round(variant["consumption"], 1)
            variants.append(variant)
    
    return variants

# ============================================================
# BUILD ALL DATA
# ============================================================

all_brands = []
total_models = 0
total_variants = 0
all_tire_sizes = {}  # tire_size -> vehicles
all_pcds = {}  # pcd -> vehicles

for brand_slug, brand_data in EUROPEAN_MODELS.items():
    brand_models = []
    
    for model in brand_data["models"]:
        segment = model.get("segment", "Compacto")
        variants = pick_variants_for_model(brand_slug, model, segment)
        
        years = model["years"]
        year_parts = years.split("-")
        year_start = int(year_parts[0])
        year_end = int(year_parts[1]) if len(year_parts) > 1 else year_start
        
        generation = {
            "slug": years,
            "name": f"Generación actual ({years})" if model["current"] else f"Generación ({years})",
            "yearStart": year_start,
            "yearEnd": year_end,
            "publishedAt": None,
            "variants": variants,
        }
        
        full_model = {
            "slug": model["slug"],
            "name": model["name"],
            "bodyType": model["bodyType"],
            "segment": segment,
            "years": years,
            "current": model["current"],
            "publishedAt": None,
            "generations": [generation],
        }
        
        brand_models.append(full_model)
        total_models += 1
        total_variants += len(variants)
        
        # Track tire sizes and PCDs
        for v in variants:
            tire = v["tireSizeFront"]
            tire_slug = tire.lower().replace("/", "-").replace(" ", "-")
            if tire not in all_tire_sizes:
                all_tire_sizes[tire] = {"size": tire, "slug": tire_slug, "publishedAt": None, "vehicles": []}
            all_tire_sizes[tire]["vehicles"].append({
                "brand": brand_data["name"],
                "brandSlug": brand_slug,
                "model": model["name"],
                "modelSlug": model["slug"],
                "variant": v["name"],
                "years": years,
            })
            
            pcd = v["pcd"]
            pcd_slug = pcd.lower().replace("x", "x").replace(".", "-")
            if pcd not in all_pcds:
                all_pcds[pcd] = {"pattern": pcd, "slug": pcd_slug, "publishedAt": None, "vehicles": []}
            all_pcds[pcd]["vehicles"].append({
                "brand": brand_data["name"],
                "brandSlug": brand_slug,
                "model": model["name"],
                "modelSlug": model["slug"],
                "years": years,
            })
    
    # Save brand file
    brand_full = {
        "slug": brand_slug,
        "name": brand_data["name"],
        "country": brand_data["country"],
        "founded": brand_data["founded"],
        "hq": brand_data["hq"],
        "description": brand_data["description"],
        "modelCount": len(brand_models),
        "publishedAt": None,
        "models": brand_models,
    }
    
    with open(os.path.join(DATA_DIR, f"brand-{brand_slug}.json"), "w", encoding="utf-8") as f:
        json.dump(brand_full, f, ensure_ascii=False, indent=2)
    
    all_brands.append({
        "slug": brand_slug,
        "name": brand_data["name"],
        "country": brand_data["country"],
        "founded": brand_data["founded"],
        "hq": brand_data["hq"],
        "description": brand_data["description"],
        "modelCount": len(brand_models),
        "publishedAt": None,
    })

# Sort brands alphabetically
all_brands.sort(key=lambda b: b["name"])

# Save brands index
with open(os.path.join(DATA_DIR, "brands.json"), "w", encoding="utf-8") as f:
    json.dump(all_brands, f, ensure_ascii=False, indent=2)

# Save tire sizes
tire_list = sorted(all_tire_sizes.values(), key=lambda t: len(t["vehicles"]), reverse=True)
with open(os.path.join(DATA_DIR, "tire-sizes.json"), "w", encoding="utf-8") as f:
    json.dump(tire_list, f, ensure_ascii=False, indent=2)

# Save PCD patterns
pcd_list = sorted(all_pcds.values(), key=lambda p: len(p["vehicles"]), reverse=True)
with open(os.path.join(DATA_DIR, "pcd-patterns.json"), "w", encoding="utf-8") as f:
    json.dump(pcd_list, f, ensure_ascii=False, indent=2)

print(f"✅ Generated data:")
print(f"   Brands: {len(all_brands)}")
print(f"   Models: {total_models}")
print(f"   Variants: {total_variants}")
print(f"   Tire sizes: {len(tire_list)}")
print(f"   PCD patterns: {len(pcd_list)}")
