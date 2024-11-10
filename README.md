# TourBuddy
**Discover local landmarks effortlessly with TourBuddy!** Our app offers one-click tours with real-time guidance, a friendly AI voice assistant, and simulated routes that make exploring both easy and immersive. TourBuddy provides seamless navigation, engaging insights, and interactive experiences. After each tour, users can reflect, rate, and leave reviews, inspiring future travelers and creating a community of explorers who bring destinations to life!
### Tech Stack
- Django (backend)
  - RestAPIs
- Pure HTML, CSS and JS (frontend)
- OpenAI GPT API
- OpenAI Whisper API
- Google Maps API
### Features
- Tracks user location
- Users can get an informational tour of the area with just one-click
- Generates landmarks/POI (points of interest) near user's current location and a route to connect them all
- AI voice assistant notifies when approaching landmarks/POI
- AI voice assistant activates speech-to-text to inform users about fascinating facts about specific landmark/POI
- Review system, allowing users to provide feedback on routes they've just completed
## Before You Begin
- Make sure you have Python installed.
- Run the following command: `pip install -r requirements.txt` (This will download all the dependencies TourBuddy uses)
## Running the project
- Navigate to the outer-level 'TourBuddy' folder: `cd TourBuddy` (directories are not case-sensitive)
- run `python manage.py runserver` on windows or `python3 manage.py runserver` if running on Linux/Ubuntu.
- Once this program has been created, open the html file `index.html` for the application which is navigated in `TourBuddyBackend/TourBuddy/frontend`
- Allow the browser to get your location. Once that is done, sign up or continue as a guest
- Enjoy the generated route and don't forget to leave a review!
