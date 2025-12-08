import requests
from openai import OpenAI

vllm_gpt_oss_120b_1="http://210.61.209.139:45014/v1/"
vllm_gpt_oss_120b_2="http://210.61.209.139:45005/v1/"

base_url = vllm_gpt_oss_120b_1
try:
    response = requests.get(base_url+"models")
    models = response.json()
    print("Available models:", models)
    
    if models.get("data"):
        model_name = models["data"][0]["id"]
        print(f"Using model: {model_name}")
    else:
        print("No models available!")
        model_name = "gpt-oss-120b" 
except Exception as e:
    print(f"Error connecting to vLLM server: {e}")
    model_name = "gpt-oss-120b"


client = OpenAI(
    base_url=base_url,
    api_key="dummy-key"
)

message="Once upon a time in a magical forest,"

try:
    
    response = client.completions.create(
        model=model_name,
        prompt=message,
        max_tokens=100,
        temperature=0.8
    )
    

    
    generated_text = response.choices[0].text
    print("Prompt:", message)
    print("Generated text:", generated_text)
    
        
except Exception as e:
    print(f"Error: {e}")