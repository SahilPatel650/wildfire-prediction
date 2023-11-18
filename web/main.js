const apiKey = 'pk.eyJ1IjoiYWxmcmVkMjAxNiIsImEiOiJja2RoMHkyd2wwdnZjMnJ0MTJwbnVmeng5In0.E4QbAFjiWLY8k3AFhDtErA';
let userLocation = null;
let gridSquares = []; // Keep track of created grid squares

const mymap = L.map('map').setView([40.770116, -73.967909], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: apiKey,
}).addTo(mymap);

const finalizeButton = L.control({ position: 'bottomleft' });
const resetButton = L.control({ position: 'bottomleft' });

finalizeButton.onAdd = function() {
  const container = L.DomUtil.create('div');
  const button = L.DomUtil.create('button', '', container);
  button.innerHTML = 'Finalize';
  button.onclick = function() {
    if (userLocation) {
      mymap.setView(userLocation, 16); // Zoom into the chosen location
      createGrid();
      finalizeButton.remove();
      resetButton.remove();
      showResetButton();
    }
  };
  return container;
};

resetButton.onAdd = function() {
  const container = L.DomUtil.create('div');
  const button = L.DomUtil.create('button', '', container);
  button.innerHTML = 'Reset';
  button.onclick = function() {
    resetMap();
  };
  return container;
};

finalizeButton.addTo(mymap);

mymap.on('click', function(e) {
  userLocation = e.latlng;
});

function createGrid() {
  const gridSize = 0.002; // Size of each square in degrees
  const latitudes = [];
  const longitudes = [];

  for (let lat = userLocation.lat - (gridSize * 16); lat < userLocation.lat + (gridSize * 16); lat += gridSize) {
    latitudes.push(lat);
  }

  for (let lng = userLocation.lng - (gridSize * 16); lng < userLocation.lng + (gridSize * 16); lng += gridSize) {
    longitudes.push(lng);
  }

  for (let lat of latitudes) {
    for (let lng of longitudes) {
      const polygonPoints = [
        [lat, lng],
        [lat + gridSize, lng],
        [lat + gridSize, lng + gridSize],
        [lat, lng + gridSize],
      ];

      const square = L.polygon(polygonPoints, {
        color: 'black',
        weight: 1,
        fillColor: 'transparent',
      }).addTo(mymap);

      square.on('click', function() {
        square.setStyle({ fillColor: 'red' });
      });

      gridSquares.push(square); // Store the created grid squares
    }
  }
}

function showResetButton() {
  resetButton.addTo(mymap);
}

function resetMap() {
  // Reset the map to its original state
  userLocation = null;
  mymap.setView([40.770116, -73.967909], 13); // Reset to default view
  finalizeButton.addTo(mymap); // Add finalize button back

  // Remove grid squares and their red color
  for (let square of gridSquares) {
    square.setStyle({ fillColor: 'transparent' });
    square.off('click'); // Remove click event listeners
    square.remove(); // Remove the grid square from the map
  }

  gridSquares = []; // Clear the stored grid squares
}