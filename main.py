import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info


model_name = "gemini-2.5-flash"

print(system_prompt)
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Chadbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
user_prompt = args.user_prompt
verbose = args.verbose
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)
response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions],),
)
if response.usage_metadata != None:
    ptc = response.usage_metadata.prompt_token_count
    ctc = response.usage_metadata.candidates_token_count
else:
    raise RuntimeError("usage_metadata doesn't exist")

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {ptc}")
    print(f"Response tokens: {ctc}")
print("Response:")
print(response.text)
if response.function_calls != None:
    for item in response.function_calls:
       print(f"Calling function: {item.name}({item.args})")
