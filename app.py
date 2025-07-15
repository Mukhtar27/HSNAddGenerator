import streamlit as st
import openpyxl
import requests
import random
import math
import io
import time
import pandas as pd
from openpyxl import Workbook
from math import radians, cos, sin

def generate_random_coordinates(lat, lon, radius_m):
    radius_deg = radius_m / 111320.0
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius_deg)
    new_lat = lat + (distance * math.cos(angle))
    new_lon = lon + (distance * math.sin(angle)) / math.cos(math.radians(lat))
    return new_lat, new_lon

def reverse_geocode(lat, lon, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            for result in data['results']:
                comps = result.get('address_components', [])
                if any('street_number' in c.get('types', []) for c in comps) and any('route' in c.get('types', []) for c in comps):
                    return result['formatted_address']
    return None

# 🌍 App Title
st.title("🌐 Global Geocoder (Random Coordinates → Address Only)")
st.write("This app returns only the **resolved address** for randomly generated points within a radius.")

# 🔢 Inputs
lat = st.number_input("Enter Center Latitude", format="%.6f")
lon = st.number_input("Enter Center Longitude", format="%.6f")
radius = st.number_input("Radius (meters)", value=500, min_value=10, max_value=5000)
max_results = st.number_input("Max Addresses", value=50, min_value=1, max_value=200)
api_key = st.text_input("Google Maps API Key", type="password")

if st.but
