// Initialize the map

if (L.DomUtil.get('map') !== null) {
    L.DomUtil.get('map')._leaflet_id = null;
}



export var map = L.map('map').setView([30.0444, 31.2357], 6); // Center on Egypt

// Load OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);


// Color scheme definition
export const colorScheme = {
    excellent: "#11a342",
    veryGood: "#b8fcb6",
    good: "#ffbe00",
    acceptable: "#ff0",
    weak: "#dc3545",
};

// Function to determine color based on percentage
export function getColor(percentage) {
    if (percentage >= 86 && percentage <= 100) return colorScheme.excellent;
    if (percentage >= 76 && percentage <= 85) return colorScheme.veryGood;
    if (percentage >= 66 && percentage <= 75) return colorScheme.good;
    if (percentage >= 50 && percentage <= 65) return colorScheme.acceptable;
    return colorScheme.weak;


    
}




// Function to create SVG icon with dynamic color
export function createSVGIcon(color, name) {
    return L.divIcon({
        className: "custom-icon",

        html: `
            <div class="marker-container">
                <svg class="glowing-marker"   style="--glow-color: ${color};"  data-glow="${color}" width="30" height="40" viewBox="0 0 24 36" xmlns="http://www.w3.org/2000/svg">
                    <path fill="${color}" stroke="black" stroke-width="2"
                          d="M12,2 C7,2 2,7 2,12 C2,20 12,34 12,34 C12,34 22,20 22,12 C22,7 17,2 12,2 Z M12,17 C10,17 8,15 8,13 C8,11 10,9 12,9 C14,9 16,11 16,13 C16,15 14,17 12,17 Z"/>
                </svg>
                <div class="marker-label">${name}</div>
            </div>
        `,
        
        // html: `
        //     <div class="marker-container">
        //         <svg class="glowing-marker" width="30" height="40" viewBox="0 0 24 36" xmlns="http://www.w3.org/2000/svg">
        //             <path fill="${color}" stroke="black" stroke-width="2"
        //                   d="M12,2 C7,2 2,7 2,12 C2,20 12,34 12,34 C12,34 22,20 22,12 C22,7 17,2 12,2 Z M12,17 C10,17 8,15 8,13 C8,11 10,9 12,9 C14,9 16,11 16,13 C16,15 14,17 12,17 Z"/>
        //         </svg>
        //         <div class="marker-label">${name}</div>
        //     </div>
        // `,
        iconSize: [30, 50],
        iconAnchor: [15, 40]
    });
}

// Governorate class
export  class Governorate {
    constructor(name, lat, lon, degree, data, coordinates = []) {
        this.name = name;
        this.lat = lat;
        this.lon = lon;
        this.degree = degree;
        this.data = data;
        this.coordinates = coordinates; // Polygon coordinates
    }

    getColor() {
        return getColor(this.degree);
    }

    addToMap(map) {
        const color = this.getColor();

        // Draw polygon (use real coordinates for each governorate)
        if (this.coordinates.length > 0) {
            L.polygon(this.coordinates, {
                color: "black",
                fillColor: color,
                fillOpacity: 0.5,
                weight: 1
            }).addTo(map);
        }

        // Add marker inside the governorate
        const marker = L.marker([this.lat, this.lon], { icon: createSVGIcon(color, this.name) }).addTo(map);
        marker.bindPopup(`<b>${this.name}</b><br>${this.data}<br>Degree: ${this.degree}`);
    }
}

// Place class
export class Place {
    constructor(name, lat, lon, data, degree) {
        this.name = name;
        this.lat = lat;
        this.lon = lon;
        this.data = data;
        this.degree = degree;
    }

    getColor() {
        return getColor(this.degree);
    }

    addToMap(map) {
        const color = this.getColor();
        const marker = L.marker([this.lat, this.lon], { icon: createSVGIcon(color, this.name) }).addTo(map);
        marker.bindPopup(`<p>${this.name}</p><p>${this.data}</p><hr><strong><p class='degree'>Degree: %${this.degree}</p></strong>`);
    }
}

// // Define Governorates (example coordinates for polygons)
// const governorates = [
//     new Governorate("Cairo", 30.0444, 31.2357, 75, "Population: 20M", [
//         [30.1, 31.3], [30.1, 31.1], [29.9, 31.1], [29.9, 31.3]
//     ]),
//     new Governorate("Alexandria", 31.2001, 29.9187, 60, "Population: 5.2M", [
//         [31.3, 30.0], [31.3, 29.8], [31.1, 29.8], [31.1, 30.0]
//     ]),
//     new Governorate("Aswan", 24.0889, 32.8998, 40, "Population: 1.5M"),
//     new Governorate("Luxor", 25.6872, 32.6396, 30, "Population: 1.3M")
// ];

// // Define Places
// const places = [
//     new Place("Cairo", 30.0444, 31.2357, "Population: 20M", 125),
//     new Place("Alexandria", 31.2001, 29.9187, "Population: 5.2M", 60),
//     new Place("Aswan", 24.0889, 32.8998, "Population: 1.5M", 40),
//     new Place("Luxor", 25.6872, 32.6396, "Population: 1.3M", 30)
// ];

// // Add all elements to the map
// governorates.forEach(gov => gov.addToMap(map));
// places.forEach(place => place.addToMap(map));
