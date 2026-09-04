import json

TRANSPORT_DB = {
    "taj_mahal": [
        {"hub_id": "t_taj_1", "name": "Agra Cantt Railway Station", "type": "railway_station", "lat": 27.1585, "lon": 77.9922},
        {"hub_id": "t_taj_2", "name": "Idgah Bus Stand", "type": "bus_stand", "lat": 27.1685, "lon": 77.9961},
    ],
    "jaipur_city_palace": [
        {"hub_id": "t_jai_1", "name": "Jaipur Junction Railway", "type": "railway_station", "lat": 26.9196, "lon": 75.7880},
        {"hub_id": "t_jai_2", "name": "Sindhi Camp Bus Stand", "type": "bus_stand", "lat": 26.9248, "lon": 75.7951},
    ],
    "goa_baga_beach": [
        {"hub_id": "t_goa_1", "name": "Thivim Railway Station", "type": "railway_station", "lat": 15.6186, "lon": 73.8378},
        {"hub_id": "t_goa_2", "name": "Mapusa Bus Stand", "type": "bus_stand", "lat": 15.5902, "lon": 73.8117},
        {"hub_id": "t_goa_3", "name": "Goa International Airport", "type": "airport", "lat": 15.3803, "lon": 73.8347},
    ],
    "kerala_backwaters": [
        {"hub_id": "t_ker_1", "name": "Alappuzha Railway Station", "type": "railway_station", "lat": 9.4932, "lon": 76.3218},
        {"hub_id": "t_ker_2", "name": "KSRTC Bus Station Alappuzha", "type": "bus_stand", "lat": 9.5028, "lon": 76.3400},
    ],
    "varanasi_ghats": [
        {"hub_id": "t_var_1", "name": "Varanasi Junction", "type": "railway_station", "lat": 25.3283, "lon": 82.9866},
        {"hub_id": "t_var_2", "name": "Lal Bahadur Shastri Airport", "type": "airport", "lat": 25.4519, "lon": 82.8584},
    ],
    "hampi_ruins": [
        {"hub_id": "t_ham_1", "name": "Hosapete Junction", "type": "railway_station", "lat": 15.2750, "lon": 76.3957},
        {"hub_id": "t_ham_2", "name": "Hampi Bus Stand", "type": "bus_stand", "lat": 15.3353, "lon": 76.4616},
    ],
    "manali": [
        {"hub_id": "t_man_1", "name": "Manali Bus Stand", "type": "bus_stand", "lat": 32.2394, "lon": 77.1882},
        {"hub_id": "t_man_2", "name": "Kullu Manali Airport", "type": "airport", "lat": 31.8795, "lon": 77.1554},
    ],
    "mysore_palace": [
        {"hub_id": "t_mys_1", "name": "Mysuru Junction", "type": "railway_station", "lat": 12.3155, "lon": 76.6433},
        {"hub_id": "t_mys_2", "name": "Mysuru City Bus Stand", "type": "bus_stand", "lat": 12.3082, "lon": 76.6548},
    ]
}

def get_hubs(destination_id: str):
    return TRANSPORT_DB.get(destination_id, [])
