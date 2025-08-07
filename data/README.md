# 📊 KhartouMap Initiative Data Repository 🇸🇩

Welcome to the comprehensive data collection for the Greater Khartoum area's transportation network. This repository contains geospatial datasets, transit information, and mobility research data collected through field surveys, GPS tracking, and on-ground mapping efforts.

## 🎯 Dataset Overview

Our data collection spans multiple transportation modes and urban features, providing researchers, planners, and developers with essential information for understanding Khartoum's mobility patterns and transit infrastructure.

---

## 📁 Available Datasets

### 🏢 [accessibility](./accessibility/)
**Points of Interest (POI) Data**
- GeoJSON files for essential urban amenities (banks, hospitals, schools, universities, etc.)
- Marketplace and commercial area locations
- Educational institution mapping (colleges, schools, universities)
- *8 categories covering key urban services and facilities*

### 🗺️ [gis](./gis/)
**Geographic Information Systems Data**
- Bus routes and stops information (JSON format with Excel documentation)
- Neighborhood boundaries for Greater Khartoum area
- Structured geospatial data ready for GIS analysis
- *Complete transit network topology and administrative boundaries*

### 📍 [gpx](./gpx/)
**GPS Tracking & Route Processing**
- 50+ GPX files from field-collected bus route tracking
- Python processing scripts with Valhalla map-matching integration
- Route validation and coordinate conversion tools
- *Real-world GPS traces covering BHR, JBL, KRT, OMD, and SHR route families*

### 🚌 [gtfs](./gtfs/)
**General Transit Feed Specification**
- Beta GTFS feed for Khartoum's public transit system
- Schedule, route, and stop information in standardized format
- *Industry-standard transit data for trip planning and analysis*

### 📋 [mobility-survey](./mobility-survey/)
**Khartoum Mobility Survey Data**
- Origin-destination survey responses with geographic visualization
- Encoded and matched response datasets (Excel format)
- Travel pattern analysis for Greater Khartoum residents
- *Primary research data with Arabic text support (UTF-8)*

### 🗃️ [transit-map](./transit-map/)
**Reference Transit Maps**
- Historical and current transit network visualizations
- Paper map digitization (PDF and PNG formats)
- Visual reference materials for route validation
- *Documentation of existing transit infrastructure and services*

---

## 🚀 Getting Started

1. **Browse by Category**: Each subfolder contains domain-specific datasets with their own documentation
2. **Check File Formats**: Data available in GeoJSON, Excel, GPX, GTFS, and standard image formats
3. **Review Processing Scripts**: Python tools available in `/gpx/` for data processing and validation
4. **Coordinate Systems**: Geographic data uses standard WGS84 (EPSG:4326) unless otherwise specified

*For questions about specific datasets or data processing, please refer to individual subfolder documentation or open an issue.*

---

## ✍️ Suggested Citation
Abdelhalim, Awad and Ali, Ilham and Ziedan, Abubakr, KhartouMap: Mapping the Semi-formal Public Transit System of Khartoum (October 07, 2023). Available at SSRN: https://ssrn.com/abstract=5382811 or http://dx.doi.org/10.2139/ssrn.5382811

---

## 📜 License

MIT License © 2025