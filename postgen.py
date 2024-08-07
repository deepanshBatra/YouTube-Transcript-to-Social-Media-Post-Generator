import os
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv('api.env')

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),  # Ensure the API key is set in your environment variables
)

# Function to get transcript of the video
def videoTranscript(video_id):
    try:
        video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        result = ' '
        for entry in video_transcript:
            result += entry["text"] + " "
        return result 
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None

# Function to call Groq API
def groq_generate(prompt, content):
    print("Generating response with Groq")
    input_text = f"{prompt} {content}"
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_text,
                }
            ],
            model="llama3-8b-8192",  # Specify the Groq model
        )
        response = chat_completion.choices[0].message.content
        print(response)
        return response
    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        return None

# Prompt for the YouTube video ID
video_id = input("Please enter the YouTube video ID: ").strip()

# Get the transcript of the video
my_video = videoTranscript(video_id)
if not my_video:
    print("Failed to retrieve the video transcript. Exiting...")
    exit(1)

# Prompt for generating the type of post
post_type = input("What kind of post would you like to generate (e.g., LinkedIn, Twitter, Blog)? ").strip()

# Prompt for generating post content
prompt = f"Create a {post_type} post based on the following transcript:"

# Generate the post
post_content = groq_generate(prompt, my_video)
if post_content:
    print(f"{post_type.capitalize()} Post:\n", post_content)
else:
    print("Failed to generate the post content.")
