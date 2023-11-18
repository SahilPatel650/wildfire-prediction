import streamlit as st
import folium

def main():
    st.title("Leaflet Map Integration with Streamlit")
    st.write("Click on the map to add markers.")

    # Initialize a map centered at a location
    m = folium.Map(location=[40.770116, -73.967909], zoom_start=8)

    # Render Folium map as HTML iframe using HTML element
    folium_map_html = m._repr_html_()
    st.components.v1.html(folium_map_html, width=800, height=600)

    # Add button for zoom action
    zoom_in = st.button("Zoom In")

    if zoom_in:
        # Get the current map bounds
        bounds = m.get_bounds()
        north_east = bounds.get('_northEast')
        south_west = bounds.get('_southWest')

        # Calculate center of current view
        lat = (north_east['lat'] + south_west['lat']) / 2
        lon = (north_east['lng'] + south_west['lng']) / 2

        # Zoom into a 32x32 km area around the center of the current view
        m.fit_bounds([[lat - 0.144, lon - 0.144], [lat + 0.144, lon + 0.144]])  # Adjust for 32km

if __name__ == "__main__":
    main()
