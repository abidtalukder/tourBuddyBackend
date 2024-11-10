from dotenv import load_dotenv
import os
import openai

# Function to generate 10 landmarks near the start location using OpenAI's API.
# The API will return the name, description, latitude, and longitude of each
# landmark.
def generateLandmarks(startLocation):
    landmarks = []
    print("WUNZIR")
    try:
        # Get 10 landmarks near the start location in a specific format
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are in " + startLocation + ". Strictly Provide landmarks separated by a comma in this order, : (name, description, latitude, longitude). for example it should be (Berkshire Theatre Group, performing arts venue known for its great performances, 42.36, -73.29)"},
                {"role": "user", "content": "Generate 10 landmarks near " + startLocation}
            ]
        )
        answer = response.choices[0]["message"]["content"].split("\n")
        print(answer[0].split(", "))
        # Parse the response to get the landmarks
        # for message in response.choices[0]["message"]["content"]:
            # print("WUNZIR")
            # if message["role"] == "system":
            #     continue
            # print(message)
            # landmark = message["content"].split(", ")
            # print(landmark)
            # name = landmark[0]
            # description = landmark[1]
            # latitude = landmark[2]
            # longitude = landmark[3]

            # landmarks.append({
            #     "name": landmark[0],
            #     "description": landmark[1],
            #     "latitude": float(landmark[2]),
            #     "longitude": float(landmark[3])
            # })
            # print(name, description, latitude, longitude)
        # return landmarks

    except Exception as e:
        print("An error occured: ", e)
        return None
    
if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    generateLandmarks("(42.43, -73.40)")