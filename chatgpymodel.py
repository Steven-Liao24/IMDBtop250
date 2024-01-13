import requests

def query_openai(text):
    api_key = 'Bearer key'
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

def split_text(file_content, max_length=800):  # Adjusted max_length
    words = file_content.split()
    current_length = 0
    current_text = ""
    for word in words:
        word_length = len(word) + 1  # Adding 1 for the space or newline character
        if current_length + word_length > max_length:
            yield current_text.strip()
            current_text = word + ' '  # Start the new text chunk with the current word
            current_length = word_length
        else:
            current_text += word + ' '
            current_length += word_length
    if current_text:
        yield current_text.strip()  # Yield the last chunk of text
