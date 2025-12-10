import os
import argparse
from dotenv import load_dotenv
import time
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

model_name = "gemini-2.5-flash"


def main():
    parser = argparse.ArgumentParser(description="Chadbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    verbose = args.verbose

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]    
    iters = 0
    
    while True:
        iters += 1
        if iters >20:
            print("Maximum iterations reached.")
            break
    
        try:
            final_text = generate_content(client, messages,verbose)
            if final_text:
                print("Final response:")
                print(final_text)
                break
        except Exception as e:
            if "503 UNAVAILABLE" in str(e):
                time.sleep(5)
                continue
            if verbose:
                print(f"Error in generate_content: {e}")
            break

def generate_content(client,messages,verbose):
    
    #generate_content section
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions],),
    )

    if not response.usage_metadata:
        raise RuntimeError("usage_metadata doesn't exist")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    
    if not response.function_calls:
        # final answer
        return response.text
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part,verbose=verbose)
        if(
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting")

    messages.append(types.Content(role="user", parts=function_responses))
    return None


if __name__ == "__main__":
    main()
