from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from transformers import pipeline

import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Replace with your actual API key
API_KEY = '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'

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    else:
        return None

def summarize_text(text):
    summarizer = pipeline('summarization', model="facebook/bart-large-cnn")

    # Split the text into smaller chunks
    max_chunk_length = 512  # You can adjust this value based on your model's max token limit
    text_chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]

    summaries = []
    for chunk in text_chunks:
        summary = summarizer(chunk, max_length=50, min_length=10, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    return ' '.join(summaries)

def generate_investment_strategy(summary):
    # Hypothetical investment strategy generator
    return "Based on the website content, it's recommended to consider diversifying your portfolio across different sectors and allocating a portion to high-growth technology stocks."

def main():
    website_url = input("Enter the website URL: ")

    website_text = scrape_website(website_url)
    if website_text:
        summary = summarize_text(website_text)
        print("Website Summary:")
        print(summary)

        investment_strategy = generate_investment_strategy(summary)
        print("\nInvestment Strategy:")
        print(investment_strategy)
    else:
        print("Failed to retrieve website content.")

if __name__ == "__main__":
    main()
