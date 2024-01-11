import requests

def query_openai(text):
    api_key = 'Bearer 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'
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.text}"

def split_text(file_content, max_length):
    words = file_content.split()
    current_length = 0
    current_text = ""
    for word in words:
        current_length += len(word) + 1
        if current_length > max_length:
            yield current_text.strip()
            current_text = word
            current_length = len(word)
        else:
            current_text += " " + word
    yield current_text.strip()

user_input = input("请输入您的问题: ")

with open('douban_top250.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

combined_content = user_input + "\n\n" + file_content
max_length = 1000

for text_segment in split_text(combined_content, max_length):
    result = query_openai(text_segment)
    print(result)
    break
