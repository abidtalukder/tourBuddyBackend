from dotenv import load_dotenv
import os
import openai
load_dotenv()
openai.api_key = os.getenv("API_KEY3")
print(openai.api_key)

# Function to generate 10 landmarks near the start location using OpenAI's API.
# The API will return the name, description, latitude, and longitude of each
# landmark and generate a route based on the landmarks.
random_loc = ""
def generateLandmarks(startLocation):
    print(startLocation)
    landmarks = []
    try:
        # Get 10 landmarks near the start location in a specific format
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are in " + startLocation + " as latitude and longitude coordinates. Strictly provide 10 very nearby landmarks/points of interest/cool locations that are in the city of the coordinates in this specific format and make sure its only this format because we need to parse it like that : (name: description: latitude: longitude). for example it should be (Berkshire Theatre Group: performing arts venue known for its great performances: 42.36: -73.29) and seperate each entry by @, like this: (name: description: latitude: longitude)@(name: description: latitude: longitude), etc."},
                {"role": "user", "content": "Generate 10 landmarks very near the location coordinates, these should be in the same city, like if coordinates are in troy ny have it only be in troy ny do not have albany  " + startLocation}
            ]
        )
        answer = response.choices[0]["message"]["content"]
        # Parse the response to format the landmarks
        for landmarks2 in answer.split("@"):
            temp = landmarks2.split(": ")
            random_loc = temp[0].lstrip("(")
            landmarks.append({
                "name": temp[0].lstrip("("),
                "description": temp[1],
                "latitude": float(temp[2]),
                "longitude": float(temp[3].rstrip(")"))
            })
        # Generate a name for the route based on the starting location
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are in " + startLocation + " as latitude and longitude coordinates. Strictly respond with just the city and state of the location you are in. For example, 'Troy, NY'."},
                {"role": "user", "content": "What city and state is this in?" + random_loc + " in?"}
            ]
        )
        answer = response.choices[0]["message"]["content"]
        route = {
            "title": answer,
            "landmarks": landmarks
        }
        return route

    except Exception as e:
        print("An error occured: ", e)
        return None
    
if __name__ == "__main__":
    generateLandmarks("lat: 42.72961654355887 lng: -73.68126988771975")