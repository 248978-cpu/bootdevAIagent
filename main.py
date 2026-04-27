import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("no api key found")


def main():
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = messages,
        config=types.GenerateContentConfig(
            tools=available_functions,
            system_instruction=system_prompt,
            temperature=0))
    if response.usage_metadata == None:
        raise RuntimeError("no usage_metadata")
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    if response.function_calls:
        function_results = []
        for function in response.function_calls:
            print(f"Calling function: {function.name}({function.args})")
            function_result = call_function(function)
            if not function_result.parts:
                raise Exception("something went wrong, no content") 
            if function_result.parts[0].function_response == None:
                raise Exception("no function response object")
            if function_result.parts[0].function_response.response == None:
                raise Exception("no response")
            function_results.append(function_result.parts)
            if args.verbose:
                print(f"-> {function_result.parts[0].function_response.response}")

    
        

if __name__ == "__main__":
    main()
