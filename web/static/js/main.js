const apiKey =
  "pk.eyJ1IjoiYWxmcmVkMjAxNiIsImEiOiJja2RoMHkyd2wwdnZjMnJ0MTJwbnVmeng5In0.E4QbAFjiWLY8k3AFhDtErA";
let userLocation = null;
let gridSquares = []; // Keep track of created grid squares
let gridLocked = false; // Flag to lock/unlock the grid
let gridData = []; // Store latitude, longitude, and selection status for each grid box

// Initialize gridData
for (let i = 0; i < 32; i++) {
  gridData[i] = [];
  for (let j = 0; j < 32; j++) {
    gridData[i][j] = {
      lat: null,
      lng: null,
      selected: false,
    };
  }
}

const mymap = L.map("map").setView([40.770116, -73.967909], 8); // Default zoom level

L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
  {
    maxZoom: 18,
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    accessToken: apiKey,
  },
).addTo(mymap);

const finalizeButton = L.control({ position: "bottomleft" });
const resetButton = L.control({ position: "bottomleft" });
const zoomInButton = L.control({ position: "bottomleft" });
const gridButton = L.control({ position: "bottomleft" });

finalizeButton.onAdd = function () {
  const container = L.DomUtil.create("div");
  const button = L.DomUtil.create("button", "", container);
  button.innerHTML = "Finalize";
  button.onclick = function () {
    finalizeGrid();
  };
  return container;
};

resetButton.onAdd = function () {
  const container = L.DomUtil.create("div");
  const button = L.DomUtil.create("button", "", container);
  button.innerHTML = "Reset";
  button.onclick = function () {
    resetMap();
  };
  return container;
};

zoomInButton.onAdd = function () {
  const container = L.DomUtil.create("div");
  const button = L.DomUtil.create("button", "", container);
  button.innerHTML = "Zoom In";
  button.onclick = function () {
    if (userLocation) {
      zoomToArea(userLocation);
      gridLocked = false; // Unlock grid on zoom in
    }
  };
  return container;
};

gridButton.onAdd = function () {
  const container = L.DomUtil.create("div");
  const button = L.DomUtil.create("button", "", container);
  button.innerHTML = "Create Grid";
  button.onclick = function () {
    if (userLocation && !gridLocked) {
      createGrid();
    }
  };
  return container;
};

finalizeButton.addTo(mymap);
resetButton.addTo(mymap);
zoomInButton.addTo(mymap);
gridButton.addTo(mymap);

mymap.on("click", function (e) {
  userLocation = e.latlng;
});

function zoomToArea(location) {
  const bounds = L.latLngBounds(
    [location.lat - 0.144, location.lng - 0.144], // Adjusted for 32km (0.144 is ~32km at latitude 40)
    [location.lat + 0.144, location.lng + 0.144],
  );

  mymap.fitBounds(bounds);
}

function createGrid() {
  const gridSize = 0.009; // 1km in degrees (approximately)

  // Clear existing grid squares if any
  for (let square of gridSquares) {
    square.remove();
  }
  gridSquares = [];

  if (!userLocation) return; // Return if user location is not set

  const bounds = mymap.getBounds();
  const northEast = bounds.getNorthEast();
  const southWest = bounds.getSouthWest();

  const gridSizeLat = (northEast.lat - southWest.lat) / 32;
  const gridSizeLng = (northEast.lng - southWest.lng) / 32;

  let latitudes = [];
  let longitudes = [];
  isDragging = false;

  for (let lat = southWest.lat; lat < northEast.lat; lat += gridSizeLat) {
    latitudes.push(lat);
  }

  for (let lng = southWest.lng; lng < northEast.lng; lng += gridSizeLng) {
    longitudes.push(lng);
  }

  for (let lat of latitudes) {
    for (let lng of longitudes) {
      const polygonPoints = [
        [lat, lng],
        [lat + gridSizeLat, lng],
        [lat + gridSizeLat, lng + gridSizeLng],
        [lat, lng + gridSizeLng],
      ];

      const square = L.polygon(polygonPoints, {
        color: "black",
        weight: 1,
        fillColor: "transparent",
      }).addTo(mymap);

      square.on("click", function () {
        const latIndex = Math.floor((lat - southWest.lat) / gridSizeLat);
        const lngIndex = Math.floor((lng - southWest.lng) / gridSizeLng);

        if (!gridLocked) {
          if (gridData[latIndex][lngIndex].selected) {
            // If the box is already highlighted, de-highlight it
            square.setStyle({ fillColor: "transparent" });
            gridData[latIndex][lngIndex].selected = false;
          } else {
            // If the box is not highlighted, highlight it
            square.setStyle({ fillColor: "red" });
            gridData[latIndex][lngIndex].selected = true;
          }
        }
      });

      square.on("mousemove", function (e) {
        if (isDragging && !gridLocked) {
          square.setStyle({ fillColor: "red" });
          const latIndex = Math.floor((lat - southWest.lat) / gridSizeLat);
          const lngIndex = Math.floor((lng - southWest.lng) / gridSizeLng);
          gridData[latIndex][lngIndex].selected = true;
        }
      });

      square.on("mousedown", function (e) {
        isDragging = true;
        square.fire("mousemove", e); // Manually trigger mousemove event on mousedown
      });

      document.addEventListener("click", function () {
        if (isDragging) {
          console.log("stopped dragging");
          isDragging = false;
        }
      });

      square.on("mouseover", function () {
        mymap.dragging.disable(); // Disable map dragging on square mouseover
      });

      square.on("mouseout", function () {
        mymap.dragging.enable(); // Enable map dragging on square mouseout
      });

      // Store latitude and longitude in gridData
      const latIndex = Math.floor((lat - southWest.lat) / gridSizeLat);
      const lngIndex = Math.floor((lng - southWest.lng) / gridSizeLng);
      gridData[latIndex][lngIndex].lat = lat;
      gridData[latIndex][lngIndex].lng = lng;

      gridSquares.push(square); // Store the created grid squares
    }
  }
}

function finalizeGrid() {
  gridLocked = true; // Lock the grid
}

function resetGridData() {
  for (let i = 0; i < 32; i++) {
    for (let j = 0; j < 32; j++) {
      gridData[i][j] = {
        lat: null,
        lng: null,
        selected: false,
      };
    }
  }
}

function resetMap() {
  // Reset the map to its original state
  userLocation = null;
  mymap.setView([40.770116, -73.967909], 8); // Reset to default view

  // Remove grid squares and their red color
  for (let square of gridSquares) {
    square.remove(); // Remove the grid square from the map
  }

  gridSquares = []; // Clear the stored grid squares

  gridLocked = false; // Unlock the grid
}

// create a function to prepare gridData for python
// need to create a reversed copy of the data and then supersample the original
// supersample by a factor of 2
// lets say we are at index i, j in the original grid,
// then we need to assign the supersampled grid to be at index (2i, 2j), (2i+1, 2j), (2i, 2j+1), (2i+1, 2j+1)
// we can do this by looping through the original grid and assigning the supersampled grid
function prepareData(gridData) {
  // Reverse the gridData without modifying the original array
  let reversedGridData = [];
  for (let i = gridData.length - 1; i >= 0; i--) {
    reversedGridData.push(gridData[i]);
  }

  // Expand gridData from 32x32 to 64x64
  const expandedGridData = [];
  for (let i = 0; i < 64; i++) {
    expandedGridData[i] = [];
    for (let j = 0; j < 64; j++) {
      expandedGridData[i][j] = {
        lat: null,
        lng: null,
        selected: false,
      };
    }
  }

  // Interpolate and update latitude, longitude, and selected status
  for (let i = 0; i < 32; i++) {
    for (let j = 0; j < 32; j++) {
      const originalLat = reversedGridData[i][j].lat;
      const originalLng = reversedGridData[i][j].lng;
      const originalSelected = reversedGridData[i][j].selected;

      expandedGridData[2 * i][2 * j].lat = originalLat;
      expandedGridData[2 * i][2 * j].lng = originalLng;
      expandedGridData[2 * i + 1][2 * j].lat = originalLat;
      expandedGridData[2 * i + 1][2 * j].lng = originalLng;
      expandedGridData[2 * i][2 * j + 1].lat = originalLat;
      expandedGridData[2 * i][2 * j + 1].lng = originalLng;
      expandedGridData[2 * i + 1][2 * j + 1].lat = originalLat;
      expandedGridData[2 * i + 1][2 * j + 1].lng = originalLng;
      expandedGridData[2 * i][2 * j].selected = originalSelected;
      expandedGridData[2 * i + 1][2 * j].selected = originalSelected;
      expandedGridData[2 * i][2 * j + 1].selected = originalSelected;
      expandedGridData[2 * i + 1][2 * j + 1].selected = originalSelected;
    }
  }

  return expandedGridData;
}

document.getElementById("run-python").addEventListener("mouseup", () => {
  let reversedGridData = prepareData(gridData);
  console.log(reversedGridData);

  fetch("/run_script", {
    // Updated URL
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ gridData: reversedGridData }),
  })
    .then((response) => response.json())
    .then((data) => console.log("Success:", data))
    .catch((error) => console.error("Error:", error));
});
