import requests

# 檢查可用模型
vllm_gpt_oss_120b_1="http://210.61.209.139:45014/v1/"
vllm_gpt_oss_120b_2="http://210.61.209.139:45005/v1/"

base_url = vllm_gpt_oss_120b_1
try:
    response = requests.get(base_url+"models")
    models = response.json()
    print("Available models:", models)
    
    # 取得實際的模型名稱
    if models.get("data"):
        model_name = models["data"][0]["id"]
        print(f"Using model: {model_name}")
    else:
        print("No models available!")
        model_name = "gpt-oss-120b"  # 預設值
except Exception as e:
    print(f"Error connecting to vLLM server: {e}")
    model_name = "gpt-oss-120b"

# 初始化 OpenAI 客戶端
from openai import OpenAI

client = OpenAI(
    base_url=base_url,
    api_key="dummy-key"
)

message="我想將1加到100 for(int i = 1;i <= 100;i++){ sum += i; }這段code有錯誤嗎，以及這樣的複雜度是多少，可以在非常數時間上再優化嗎如果可以的話，給我一個關於優化建議的json檔包含 type(錯誤/優化) 、原本複雜度、優化後複雜度、優化後的程式碼、英文解釋邏輯不用其他解釋，只要json檔"

try:
    
    response = client.completions.create(
        model=model_name,
        prompt=message,
        max_tokens=1000,
        temperature=0.8
    )
    
    
    generated_text = response.choices[0].text
    #print("Prompt:", message)

    f: int = 0
    for i in generated_text:
        if( i == '{' ): f = 1
        if( f == 1 ): print(i, end="")

        if( i == '}' ): break


   # print("Generated text:", generated_text)
    
        
except Exception as e:
    print(f"Error: {e}")