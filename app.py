import streamlit as st
import openpyxl
import requests
import random
import math
import io
import time
import pandas as pd
from openpyxl import Workbook
from math import radians, cos, sin, sqrt, atan2

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

def forward_geocode(address, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={requests.utils.quote(address)}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 🌍 App Title
st.title("🌐 Global Hybrid Geocoder (Random Area → Verified Address & Lat/Lon)")
st.write("This app works from **any country or region**, and uses Google's global Geocoding API to return verified street-level addresses and coordinates.")

# 🔢 Input fields
lat = st.number_input("Enter Center Latitude", format="%.6f")
lon = st.number_input("Enter Center Longitude", format="%.6f")
radius = st.number_input("Radius (meters)", value=500, min_value=10, max_value=5000)
max_results = st.number_input("Max Addresses", value=50, min_value=1, max_value=200)
api_key = st.text_input("Google Maps API Key", type="password")

if st.button("🔍 Run Hybrid Geocoding"):
    if not api_key:
        st.error("Please enter a valid API Key.")
    else:
        st.info("Fetching addresses globally... please wait.")
        results = []
        unique_addresses = set()
        progress = st.progress(0)
        status = st.empty()
        start_time = time.time()

        for i in range(300):
            if len(results) >= max_results:
                break

            r_lat, r_lon = generate_random_coordinates(lat, lon, radius)
            address = reverse_geocode(r_lat, r_lon, api_key)

            if address and address not in unique_addresses:
                actual_lat, actual_lon = forward_geocode(address, api_key)
                if actual_lat is not None:
                    dist = haversine_distance(r_lat, r_lon, actual_lat, actual_lon)
                    results.append((
                        round(r_lat, 6), round(r_lon, 6),
                        address,
                        round(actual_lat, 6), round(actual_lon, 6),
                        round(dist, 2)
                    ))
                    unique_addresses.add(address)

            # Update UI progress
            progress.progress(min(int((len(results) / max_results) * 100), 100))
            status.text(f"Found {len(results)} / {max_results} addresses...")

        end_time = time.time()
        elapsed = round(end_time - start_time, 2)

        if results:
            df = pd.DataFrame(results, columns=[
                "Random Lat", "Random Lon", "Address", "Verified Lat", "Verified Lon", "Distance (m)"
            ])
            st.success(f"✅ {len(results)} addresses found and verified in {elapsed} seconds.")

            st.subheader("📋 Preview of Results")
            st.dataframe(df.head(10))

            output = io.BytesIO()
            df.to_excel(output, index=False, engine="openpyxl")
            output.seek(0)

            st.download_button(
                "📥 Download Results as Excel",
                data=output,
                file_name="hybrid_geocoded_addresses.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No valid addresses found. Try increasing the radius or check your API key quota.")
