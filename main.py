import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
# prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

parser = argparse.ArgumentParser(description="Chadbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

user_prompt = args.user_prompt
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
# response = client.models.generate_content(model="gemini-2.5-flash",contents=prompt)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
)
if response.usage_metadata != None:
    ptc = response.usage_metadata.prompt_token_count
    ctc = response.usage_metadata.candidates_token_count
else:
    raise RuntimeError("usage_metadata doesn't exist")

print(f"User prompt: {user_prompt}")
print(f"Prompt tokens: {ptc}")
print(f"Response tokens: {ctc}")
print("Response:")
print(response.text)


