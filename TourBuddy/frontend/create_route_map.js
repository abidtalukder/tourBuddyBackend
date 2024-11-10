let map, directionsService, directionsRenderer;
let carMarker;
let routePath = [];
let currentIndex = 0;
let movingInterval;
let visitedLocations = new Set();
let lastHeading = 0; // Keep track of last heading for smooth rotation
let currentCity = null; 
// Add these at the top of your file
let speechQueue = [];
let isSpeaking = false;

async function generateSpeech(text) {
    // Add the text to the queue
    speechQueue.push(text);
    
    // If not currently speaking, start processing the queue
    if (!isSpeaking) {
        processNextSpeech();
    }
}
async function api_keys(){
    const response = await fetch("http://localhost:8000/get_keys");
    const data = await response.json();
    return data;
}
async function processNextSpeech() {
    if (speechQueue.length === 0) {
        isSpeaking = false;
        return;
    }

    isSpeaking = true;
    const text = speechQueue.shift();
    openai_key = await api_keys();
    openai_key = openai_key.openai;
    try {
        const response = await fetch("https://api.openai.com/v1/audio/speech", {
            method: "POST",
            headers: {
                "Authorization": openai_key,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "tts-1",
                voice: "alloy",
                input: text
            })
        });

        if (!response.ok) throw new Error("Failed to generate speech");

        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        
        // Wait for the audio to finish before processing the next item
        audio.onended = () => {
            URL.revokeObjectURL(audioUrl); // Clean up the URL
            processNextSpeech(); // Process next item in queue
        };

        audio.play();
    } catch (error) {
        console.error("Error generating speech:", error);
        isSpeaking = false;
        processNextSpeech(); // Continue to next item even if there's an error
    }
}
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 42.7320, lng: -73.6884 },
        zoom: 13
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true
    });

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            map.setCenter(userLocation);
            const string_loc = "lat: " + position.coords.latitude + " lng: " + position.coords.longitude;
            
            fetch(`http://127.0.0.1:8000/get-route/?startLocation=${encodeURIComponent(string_loc)}`)
                .then(response => response.json())
                .then(data => {
                    let locations = [];
                    currentCity = data.title; // Store the city
                    document.getElementById('cityBanner').textContent = `Exploring ${currentCity}`;

                    for(let i = 0; i < data.landmarks.length; i++) {
                        locations.push({
                            city: data.title,
                            lat: data.landmarks[i].latitude,
                            lng: data.landmarks[i].longitude,
                            name: data.landmarks[i].name,
                            desc: data.landmarks[i].description,
                        });
                    }

                    // Add markers for all locations
                    locations.forEach(loc => {
                        new google.maps.Marker({
                            position: { lat: loc.lat, lng: loc.lng },
                            map: map,
                            title: loc.name
                        });
                    });

                    const request = {
                        origin: userLocation,
                        destination: new google.maps.LatLng(locations[locations.length - 1].lat, locations[locations.length - 1].lng),
                        waypoints: locations.slice(1, -1).map(loc => ({
                            location: new google.maps.LatLng(loc.lat, loc.lng),
                            stopover: true
                        })),
                        travelMode: google.maps.TravelMode.DRIVING,
                        optimizeWaypoints: true
                    };

                    directionsService.route(request, (result, status) => {
                        if (status === google.maps.DirectionsStatus.OK) {
                            directionsRenderer.setDirections(result);
                            
                            // Create detailed path with interpolated points
                            routePath = [];
                            const path = result.routes[0].overview_path;
                            
                            for (let i = 0; i < path.length - 1; i++) {
                                const segment = interpolatePoints(path[i], path[i + 1], 10);
                                routePath.push(...segment);
                            }

                            // Initialize car marker
                            carMarker = new google.maps.Marker({
                                position: routePath[0],
                                map: map,
                                icon: {
                                    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
                                    scale: 6,
                                    fillColor: "#00F",
                                    fillOpacity: 0.8,
                                    strokeWeight: 1,
                                    rotation: 0
                                }
                            });

                            window.checkpoints = locations;
                        }
                    });
                })
                .catch(error => console.error("Error fetching data:", error));
        }, error => {
            console.error("Error fetching current location:", error);
            alert("Unable to retrieve your location. Please try again.");
        });
    } else {
        console.error("Geolocation is not supported by this browser.");
        alert("Geolocation is not supported by this browser.");
    }
}
// Add these speed control variables at the top with other globals
const FAST_SPEED = 1; // Faster speed between landmarks
const SLOW_SPEED = 75; // Slower speed near landmarks
const SLOW_DOWN_RADIUS = 400; // Distance to start slowing down (meters)
const CHECK_RADIUS = 100; // Distance to trigger landmark visit (meters)
let currentSpeed = FAST_SPEED;

function startRoute() {
    if (!currentUser) {
        alert('Please login or continue as guest first');
        return;
    }
    if (movingInterval) clearInterval(movingInterval);
    currentIndex = 0;
    visitedLocations.clear();
    lastHeading = 0;
    currentSpeed = FAST_SPEED;

    function moveMarker() {
        if (currentIndex < routePath.length - 1) {
            const currentPos = routePath[currentIndex];
            const nextPos = routePath[Math.min(currentIndex + 1, routePath.length - 1)];
            
            // Update car position and rotation
            if (carMarker) {
                carMarker.setPosition(currentPos);
                
                const newHeading = google.maps.geometry.spherical.computeHeading(currentPos, nextPos);
                lastHeading = smoothRotation(lastHeading, newHeading);
                
                carMarker.setIcon({
                    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
                    scale: 6,
                    fillColor: "#00F",
                    fillOpacity: 0.8,
                    strokeWeight: 1,
                    rotation: lastHeading
                });

                // Check proximity to all landmarks
                let nearLandmark = false;
                
                if (window.checkpoints) {
                    window.checkpoints.forEach(loc => {
                        if (!visitedLocations.has(loc.name)) {
                            const distance = google.maps.geometry.spherical.computeDistanceBetween(
                                currentPos,
                                new google.maps.LatLng(loc.lat, loc.lng)
                            );

                            // Check if we're entering the slow-down zone
                            if (distance < SLOW_DOWN_RADIUS) {
                                nearLandmark = true;
                            }

                            // Check if we've reached the landmark
                            if (distance < CHECK_RADIUS) {
                                console.log(`Reaching ${loc.name}`);
                                generateSpeech(`Arriving at ${loc.name}. ${loc.desc}`);
                                visitedLocations.add(loc.name);
                                
                                new google.maps.InfoWindow({
                                    content: `<div style="color: black;">
                                              <b>${loc.name}</b><br>
                                              ${loc.desc}
                                            </div>`,
                                    position: currentPos
                                }).open(map);
                            }
                        }
                    });
                }

                // Update speed without recreating the interval
                currentSpeed = nearLandmark ? SLOW_SPEED : FAST_SPEED;

                map.panTo(currentPos);
            }

            currentIndex++;
            
            // Schedule next movement based on current speed
            setTimeout(moveMarker, currentSpeed);
        } else {
            if (visitedLocations.size > 0) {
                const visitedList = [...visitedLocations].join(", ");
                generateSpeech(`Congratulations! You have completed this tour! You visited: ${visitedList}. Feel free to leave both a review and a journal entry of your experience! We hope you use TourBuddy again!`);
                console.log("Visited locations:", [...visitedLocations]);
                showFeedbackForm();
            } else {
                console.log("No locations were visited during the tour.");
                generateSpeech("The tour has ended, but it seems we didn't reach any of the landmarks. Would you like to try again?");
            }
        }
    }

    // Start the movement
    moveMarker();
}

// Helper function for interpolating points for smoother movement
function interpolatePoints(start, end, numPoints) {
    const points = [];
    for (let i = 0; i <= numPoints; i++) {
        const lat = start.lat() + (end.lat() - start.lat()) * (i / numPoints);
        const lng = start.lng() + (end.lng() - start.lng()) * (i / numPoints);
        points.push(new google.maps.LatLng(lat, lng));
    }
    return points;
}

function interpolatePoints(p1, p2, numPoints) {
    const points = [];
    for (let i = 0; i <= numPoints; i++) {
        const fraction = i / numPoints;
        points.push(new google.maps.LatLng(
            p1.lat() + (p2.lat() - p1.lat()) * fraction,
            p1.lng() + (p2.lng() - p1.lng()) * fraction
        ));
    }
    return points;
}

// Helper function to normalize angle between -180 and 180
function normalizeAngle(angle) {
    while (angle > 180) angle -= 360;
    while (angle < -180) angle += 360;
    return angle;
}

// Helper function to smoothly interpolate between angles
function smoothRotation(oldAngle, newAngle) {
    const diff = normalizeAngle(newAngle - oldAngle);
    return oldAngle + (diff * 0.2); // Only rotate 20% of the way there
}

let currentUser = null;
let feedbackSubmitted = false;
let selectedRating = null;

// Login handling
function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (username && password) {
        currentUser = username;
        document.getElementById('loginForm').classList.add('hidden');
        document.getElementById('startRouteButton').style.display = 'block';
    } else {
        alert('Please enter both username and password');
    }
}

function skipLogin() {
    currentUser = 'guest';
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('startRouteButton').style.display = 'block';
}

// Feedback handling
function showFeedbackForm() {
    document.getElementById('feedbackForm').classList.remove('hidden');
    // Reset rating when showing form
    selectedRating = null;
    updateStarDisplay();
}

function updateStarDisplay() {
    const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        const value = parseInt(star.getAttribute('data-value'));
        if (selectedRating && value <= selectedRating) {
            star.textContent = '★'; // Filled star
            star.style.color = '#FFD700'; // Gold color
        } else {
            star.textContent = '☆'; // Empty star
            star.style.color = '#FFD700';
        }
    });
}

function handleStarClick(event) {
    const star = event.target;
    selectedRating = parseInt(star.getAttribute('data-value'));
    updateStarDisplay();
}

function handleStarHover(event) {
    const stars = document.querySelectorAll('.star');
    const hoveredValue = parseInt(event.target.getAttribute('data-value'));
    
    stars.forEach(star => {
        const value = parseInt(star.getAttribute('data-value'));
        if (value <= hoveredValue) {
            star.textContent = '★';
        } else {
            star.textContent = '☆';
        }
    });
}

function handleStarLeave() {
    updateStarDisplay();
}

function submitFeedback() {
    if (selectedRating === null) {
        alert('Please select a rating before submitting.');
        return;
    }

    const journalEntry = document.getElementById('journalEntry').value;
    
    // Create route points string
    const routePoints = [...visitedLocations];
    
    // Create feedback object
    const feedback = {
        username: currentUser,
        score: selectedRating,
        journal: journalEntry,
        city: currentCity,
        routeid: routePoints.join(''),

        routearray: visitedLocations,
        //timestamp: new Date().toISOString()
    };

    console.log('Feedback submitted:', feedback);

    // Sending 
    /*
        fetch(`http://127.0.0.1:8000/submit-ratings/?startLocation=${encodeURIComponent(string_loc)}`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedback)
    })
    .then(response => response.json())
    .then(data => console.log('Success:', data))
    .catch((error) => console.error('Error:', error));
    */

    feedbackSubmitted = true;
    document.getElementById('feedbackForm').classList.add('hidden');
}

function skipFeedback() {
    feedbackSubmitted = true;
    document.getElementById('feedbackForm').classList.add('hidden');
}

async function loadGoogleMapsScript() {
    google_key = await api_keys();
    google_key = google_key.google;
    const script = document.createElement('script');
    script.src = google_key;
    script.async = true;
    document.head.appendChild(script);
}

// Initialize star rating functionality
document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star');
    
    stars.forEach(star => {
        star.addEventListener('click', handleStarClick);
        star.addEventListener('mouseover', handleStarHover);
        star.addEventListener('mouseout', handleStarLeave);
    });

    // Hide the start button initially
    document.getElementById('startRouteButton').style.display = 'none';
    
    // Add event listener for start button
    const button = document.getElementById('startRouteButton');
    if (button) {
        button.addEventListener('click', startRoute);
    }
});
// Start loading the map
loadGoogleMapsScript();

