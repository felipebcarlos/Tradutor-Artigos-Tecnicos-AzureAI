import os
import requests
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF para PDFs
from docx import Document  # python-docx para DOCX

# Configurações da API Azure
AZURE_TRANSLATOR_KEY = "CNtn3XfqWiMyHtJ5Dx3a9wH41R8ANGfYui8VW1Cn1PDn9JqbsI6JJQQJ99AKACHYHv6XJ3w3AAAbACOGmkjy"
AZURE_TRANSLATOR_REGION = "eastus2"
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
DETECT_URL = f"{TRANSLATOR_ENDPOINT}/detect?api-version=3.0"
TRANSLATE_URL = f"{TRANSLATOR_ENDPOINT}/translate?api-version=3.0"

# Configurações de Upload
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Função para detectar o idioma
def detect_language(text):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }
    data = [{"Text": text}]
    response = requests.post(DETECT_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        detections = response.json()
        language = detections[0]["language"]
        confidence = detections[0]["score"]
        return language, confidence
    else:
        return None, None

# Função para traduzir o texto
def translate_text(text, target_language):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }
    params = {"to": target_language}
    data = [{"Text": text}]
    response = requests.post(TRANSLATE_URL, headers=headers, params=params, json=data)
    
    if response.status_code == 200:
        translations = response.json()
        translated_text = translations[0]["translations"][0]["text"]
        return translated_text
    else:
        return None

# Função para extrair texto de um PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Função para extrair texto de um arquivo DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Função para verificar a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Verificar se o arquivo foi enviado
        file = request.files.get('file')
        text = request.form.get("text")  # Pega o texto digitado pelo usuário
        target_language = request.form.get("language")  # Pega o idioma escolhido para a tradução
        
        if file and allowed_file(file.filename):
            # Salva o arquivo
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extrair o texto dependendo do tipo de arquivo
            if filename.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(filepath)
            elif filename.endswith('.docx'):
                extracted_text = extract_text_from_docx(filepath)
        else:
            # Se não houver arquivo, usa o texto digitado
            extracted_text = text
        
        # Detectar o idioma do texto extraído
        detected_language, confidence = detect_language(extracted_text)
        
        # Traduzir o texto para o idioma escolhido
        translated_text = translate_text(extracted_text, target_language)
        
        # Exibir o idioma detectado, confiança e o texto traduzido
        return render_template("index.html", detected_language=detected_language, confidence=confidence,
                               original_text=extracted_text, translated_text=translated_text, target_language=target_language)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)