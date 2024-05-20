from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BartForConditionalGeneration, BartTokenizer
import fitz  # PyMuPDF
import os

app = Flask(__name__)
CORS(app)

model_dir = "/Users/mbp/Desktop/FLASK-APP/BART_TRAINED-MultiNews"  
tokenizer = BartTokenizer.from_pretrained(model_dir)
model = BartForConditionalGeneration.from_pretrained(model_dir)

def extract_text_from_pdf(pdf_file):
    document = fitz.open(stream=pdf_file, filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def summarize_text(text):
    inputs = tokenizer([text], return_tensors='pt', truncation=True, padding=True, max_length=1024)
    summary_ids = model.generate(
        inputs['input_ids'],
        max_length=1500,      
        min_length=200,        
        length_penalty=1.0,    
        num_beams=5,           
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def ensure_full_stop(summary):
    if '.' in summary:
        summary = summary[:summary.rfind('.') + 1]
    return summary

@app.route('/summarize', methods=['POST'])
def summarize():
    files = request.files.getlist('files')
    if len(files) == 0:
        return jsonify({'error': 'Please upload at least one document.'}), 400

    combined_text = ""
    for file in files:
        if file.filename.endswith('.pdf'):
            combined_text += extract_text_from_pdf(file.read()) + " "
        else:
            combined_text += file.read().decode('utf-8') + " "
    
    combined_summary = summarize_text(combined_text.strip())
    combined_summary = ensure_full_stop(combined_summary)
    return jsonify({'summary': combined_summary})

if __name__ == '__main__':
    app.run(debug=True, port=5004)
