import streamlit as st
import openpyxl
import requests
import random
import math
import io
from openpyxl import Workbook

st.title("📍 Random Address Generator using Google Maps API")

# Input fields
lat = st.number_input("Enter Latitude", format="%.6f")
lon = st.number_input("Enter Longitude", format="%.6f")
radius_m = st.number_input("Enter Radius (in meters)", min_value=10, max_value=5000, value=500)
max_addresses = st.number_input("Max Addresses to Fetch", min_value=1, max_value=200, value=50)
api_key = st.text_input("Enter your Google Maps API Key", type="password")

# Generate random coordinates
def generate_random_coordinates(lat, lon, radius_m):
    radius_deg = radius_m / 111320.0
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius_deg)
    new_lat = lat + (distance * math.cos(angle))
    new_lon = lon + (distance * math.sin(angle)) / math.cos(math.radians(lat))
    return new_lat, new_lon

# Get address and its true coordinates from Google
def get_address_from_coordinates(lat, lon, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            for result in data['results']:
                address_components = result.get('address_components', [])
                has_number = any('street_number' in c.get('types', []) for c in address_components)
                has_street = any('route' in c.get('types', []) for c in address_components)
                if has_number and has_street:
                    formatted_address = result['formatted_address']
                    location = result['geometry']['location']
                    real_lat = location['lat']
                    real_lon = location['lng']
                    return formatted_address, real_lat, real_lon
    return None, None, None

# Run process
if st.button("🔍 Generate Addresses"):
    if not api_key:
        st.warning("Please enter your API key.")
    else:
        st.info("Generating addresses. Please wait...")

        unique_addresses = set()
        results = []

        for _ in range(200):
            if len(results) >= max_addresses:
                break
            r_lat, r_lon = generate_random_coordinates(lat, lon, radius_m)
            address, actual_lat, actual_lon = get_address_from_coordinates(r_lat, r_lon, api_key)
            if address and address not in unique_addresses:
                unique_addresses.add(address)
                results.append((round(r_lat, 6), round(r_lon, 6), address, actual_lat, actual_lon))

        if results:
            output = io.BytesIO()
            wb = Workbook()
            ws = wb.active
            ws.append([
                "Random Latitude", "Random Longitude",
                "Address", "Actual Address Latitude", "Actual Address Longitude"
            ])
            for row in results:
                ws.append(row)
            wb.save(output)
            output.seek(0)

            st.success(f"✅ Generated {len(results)} addresses.")
            st.download_button(
                label="📥 Download Excel File",
                data=output,
                file_name="generated_addresses.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("❌ No valid addresses could be generated. Try increasing the radius.")
