# 📍 Google Hybrid Geocoder: Randomized Address Generator + Reverse & Forward Geocoding

This Streamlit app generates **random points** around a user-defined central latitude and longitude, fetches addresses using **Google Maps Reverse Geocoding**, then verifies each address by performing **Forward Geocoding** to retrieve accurate coordinates and compute the **distance offset**.

---

## 💡 Use Case

Ideal for:
- Location-based sampling
- Synthetic address generation for GIS
- Urban analysis and address validation

---

## 🌐 Features

- User inputs:
  - Latitude and Longitude (center point)
  - Radius in meters
  - Max number of addresses to fetch
  - Google Maps API Key
- Generates random points in the radius
- Performs:
  - 🔁 Reverse Geocoding → Get human-readable address
  - ➡️ Forward Geocoding → Get real lat/lon of address
  - 📏 Calculates distance offset (Haversine)
- Download results as Excel with:
  - Random coordinates
  - Matched address
  - Verified lat/lon
  - Distance in meters

---

## 🚀 How to Use

1. Visit the app: [Launch Hybrid Geocoder](https://mukhtar27-hsnaddgenerator-app-xpk1ue.streamlit.app/)
2. Enter:
   - Latitude, Longitude (center point)
   - Radius (in meters)
   - Max addresses (e.g., 50)
   - Your Google Maps API key
3. Click **Run Hybrid Geocoding**
4. Download results in Excel

---

## 🧾 Output Example

| Random Lat | Random Lon | Address | Verified Lat | Verified Lon | Distance (m) |
|------------|------------|---------|---------------|---------------|---------------|
| 12.9712    | 77.5946    | XYZ St. | 12.9713        | 77.5944        | 15.42         |

---

## 🔒 License & Usage Restriction

```text
Copyright (c) 2025 Mukhtar G.

All rights reserved.

This code and deployed application are for demonstration and educational purposes only.

You may **NOT**:
- Use or clone this repository for personal or commercial projects
- Modify, republish, or redistribute any part of this codebase
- Integrate any component into other products or services

Unauthorized usage, adaptation, or distribution is strictly prohibited.
