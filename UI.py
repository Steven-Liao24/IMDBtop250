import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import requests 
from lxml import etree
from chatgpymodel import query_openai

def get_first_text(lst):
    return lst[0].strip() if lst else ''

def start_scraping():

    base_url = 'https://www.imdb.com/chart/top/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    }

    with open('IMDB_top250.txt', 'w', encoding='utf-8') as f:
            response = requests.get(url=base_url, headers=headers)           
            if response.status_code == 200:
                html = etree.HTML(response.text)
                lis = html.xpath('//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li')[:50]
                
                for li in lis:
                    title = get_first_text(li.xpath('./div[2]/div/div/div[1]/a/h3/text()'))
                    link = get_first_text(li.xpath('./div[2]/div/div/div[1]/a/@href'))
                    full_link = 'https://www.imdb.com' + link
                    score = get_first_text(li.xpath('./div[2]/div/div/span/div/span/text()'))
                    
                    f.write(f'{title}\t{full_link}\t{score}\n')
            else:
                print('Failed to retrieve data from:', base_url)
    
    with open('IMDB_top250.txt', 'r', encoding='utf-8') as file:
        file_content = file.read()
    text_area.delete('1.0', tk.END)  
    text_area.insert(tk.END, file_content)  

            

def ask_question():
    question = entry.get()
    with open('IMDB_top250.txt', 'r', encoding='utf-8') as file:
        context = file.read() 

    combined_text = context + "\n" + question
    print(combined_text)

    try:
        response = query_openai(combined_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        response = "There was an error processing your question."
    
    answer_area.delete('1.0', tk.END)  
    answer_area.insert(tk.END, response)


# GUI setup
window = tk.Tk()
window.title("IMDB Top 250 Chatgpt")
font_style = ("Helvetica", 12)

# Left frame for the Crawler button
left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Start button inside the left frame, at the top
start_button = tk.Button(left_frame, text="Crawler", command=lambda: threading.Thread(target=start_scraping).start())
start_button.pack(side=tk.TOP, fill=tk.X)  

# ScrolledText for the IMDB data, below the Crawler button
text_area = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=40, height=10, font=font_style)
text_area.pack(fill=tk.BOTH, expand=True)

# Frame for the question entry, ask button, and answer area
right_frame = tk.Frame(window)
right_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Entry for the question
entry = tk.Entry(right_frame, width=40, font=font_style)
entry.pack(pady=5)

# Ask button
ask_button = tk.Button(right_frame, text="Ask Question", command=ask_question)
ask_button.pack(pady=5)

# ScrolledText for the ChatGPT answer
answer_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=40, height=8, font=font_style)
answer_area.pack(pady=5)

window.mainloop()