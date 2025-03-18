from transformers import pipeline
from datasets import load_dataset
from openai import OpenAI
import json
import os

ds = load_dataset("diffusers/pokemon-gpt4-captions")

pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

def generate_headline(description, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Guess the Pokemon based on this description."},
            {"role": "user", "content": description}
        ]
    )
    return response.choices[0].message.content

def process_images(dataset, num_samples=10):
    results = []
    
    # Get total number of samples to process
    total_samples = min(num_samples, len(dataset['train']))
    print(f"Starting to process {total_samples} images...")
    
    for i, item in enumerate(dataset['train'].select(range(total_samples))):
        try:
            # Generate caption using BLIP directly from item
            generated_caption = pipe(item['image'])[0]['generated_text']
            
            # Get text directly from item
            text = item['text']
            
            # Generate headline
            try:
                headline = generate_headline(generated_caption, os.getenv('OPENAI_API_KEY'))
            except Exception as e:
                print(f"Headline generation error: {str(e)}")
                headline = "Error generating headline"
            
            results.append({
                'original_text': text,
                'caption': generated_caption,
                'headline': headline
            })
            print(f"Successfully processed image {i+1}/{total_samples}")
            
        except Exception as e:
            print(f"Error processing image {i}: {str(e)}")
            continue
    
    return results