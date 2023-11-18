const apiKey = 'pk.eyJ1IjoiYWxmcmVkMjAxNiIsImEiOiJja2RoMHkyd2wwdnZjMnJ0MTJwbnVmeng5In0.E4QbAFjiWLY8k3AFhDtErA';
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

const mymap = L.map('map').setView([40.770116, -73.967909], 8); // Default zoom level

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: apiKey,
}).addTo(mymap);

const finalizeButton = L.control({ position: 'bottomleft' });
const resetButton = L.control({ position: 'bottomleft' });
const zoomInButton = L.control({ position: 'bottomleft' });
const gridButton = L.control({ position: 'bottomleft' });

finalizeButton.onAdd = function () {
  const container = L.DomUtil.create('div');
  const button = L.DomUtil.create('button', '', container);
  button.innerHTML = 'Finalize';
  button.onclick = function () {
    finalizeGrid();
  };
  return container;
};

resetButton.onAdd = function () {
  const container = L.DomUtil.create('div');
  const button = L.DomUtil.create('button', '', container);
  button.innerHTML = 'Reset';
  button.onclick = function () {
    resetMap();
  };
  return container;
};

zoomInButton.onAdd = function () {
  const container = L.DomUtil.create('div');
  const button = L.DomUtil.create('button', '', container);
  button.innerHTML = 'Zoom In';
  button.onclick = function () {
    if (userLocation) {
      zoomToArea(userLocation);
      gridLocked = false; // Unlock grid on zoom in
    }
  };
  return container;
};

gridButton.onAdd = function () {
  const container = L.DomUtil.create('div');
  const button = L.DomUtil.create('button', '', container);
  button.innerHTML = 'Create Grid';
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

mymap.on('click', function (e) {
  userLocation = e.latlng;
});

function zoomToArea(location) {
  const bounds = L.latLngBounds(
    [location.lat - 0.144, location.lng - 0.144], // Adjusted for 32km (0.144 is ~32km at latitude 40)
    [location.lat + 0.144, location.lng + 0.144]
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
        color: 'black',
        weight: 1,
        fillColor: 'transparent',
      }).addTo(mymap);

      square.on('click', function () {
        if (!gridLocked) {
          console.log('clicked at' + lat + ', ' + lng)
          square.setStyle({ fillColor: 'red' });
          // Find the corresponding grid box in gridData and update its selected status
          const latIndex = Math.floor((lat - southWest.lat) / gridSizeLat);
          const lngIndex = Math.floor((lng - southWest.lng) / gridSizeLng);
          gridData[latIndex][lngIndex].selected = true;
        }
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

function reverseArray(gridData) {
  return gridData.map(row => row.reverse()).reverse();
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
console.log(gridData);
gridData = [...reverseArray(gridData)];
console.log(gridData);
