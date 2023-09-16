import requests
import json
import boto3
import re
import os
import io
from pdf2image import convert_from_path
from PIL import Image

# for AWS textract
ACCESS_KEY = 'AKIASHJPS4BPKYQFEEPV'
SECRET_KEY = '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'
REGION_NAME = 'eu-central-1'

# for ChatGPT
API_KEY = "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"
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"


def generate_chat_completion(messages, model="gpt-3.5-turbo", temperature=1, max_tokens=None):
    gpt_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    gpt_data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        gpt_data["max_tokens"] = max_tokens

    response2 = requests.post(API_ENDPOINT, headers=gpt_headers, data=json.dumps(gpt_data))

    if response2.status_code == 200:
        return response2.json()["choices"][0]["message"]["content"]
    

def textract_analysis(image_binary):
    client = boto3.client(
        'textract',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME)
    
    response = client.detect_document_text(Document={'Bytes': image_binary})
    
    # Extract the detected text data
    detected_text = []

    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            detected_text.append(item["Text"])
                
    # Return the detected text data
    return detected_text

def find_numbers(string):
    return [float(num) if '.' in num else int(num) for num in re.findall(r'\b\d+\.?\d*\b', string)]

def ocr_check(pdf_path):
    # Create a folder to save the images
    folder_name = 'pdf_images'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Convert the PDF pages to images using pdf2image library
    images = convert_from_path(pdf_path)

    # Loop through each page in the PDF file
    # for i, image in enumerate(images):
    # Save the image to a byte stream
    img_bytes = io.BytesIO()
    images[0].save(img_bytes, format='PNG')

    # Load the image from the byte stream into PIL
    img = Image.open(img_bytes)
    
    # Define the filename and path for the current image
    filename = f"page_0.png"
    filepath = os.path.join(folder_name, filename)
    
    # Save the image to the specified path
    img.save(filepath)

    block = ""
    lot = ""
    file_name = "pdf_images/page_0.png"
    with open(file_name, 'rb') as image_file:
        content=image_file.read()
        
    # Run the OCR on the image
    results = textract_analysis(content)
    
    script = " ".join(results)
    
    message_content = "Here is the full text\n\n" + " ".join(script) + "\n" + "Don't reponse other words, you must give me only one array with block number and lot number. Provide an array evenif block and lot are 'N/A'."

    messages = [
        {"role": "user", "content": message_content}
    ]

    response = generate_chat_completion(messages)

    # print("response: ", response)
    blocks = find_numbers(response)
    if len(blocks) > 0 and (blocks[0] != ''):
        blockFound = True
        block = blocks[0]
    # print("block: ", block)
    # print("block: ", type(block))

    lots = find_numbers(response)
    if len(lots) > 0 and (lots[0] != ''):
        lotFound = True
        lot = lots[-1]
    # print("block: ", lot)
    # print("lot: ", type(lot))

    return block, lot


