from flask import Flask, request, render_template
from PyPDF2 import PdfReader
import requests

app = Flask(__name__)

# Configurações do Azure Translator
AZURE_TRANSLATOR_KEY = "SUA_CHAVE_AZURE_TRANSLATOR"
AZURE_TRANSLATOR_ENDPOINT = "SEU_ENDPOINT_AURE_TRANSLATOR"
TRANSLATOR_REGION = "REGIAO_AZURE_TRANSLATOR"

# Função para extrair texto do PDF
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Erro ao processar o PDF: {e}"

# Função para detectar o idioma
def detect_language(text):
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/translator/text/v3.0/detect"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }
    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    detected_language = response.json()[0]["language"]
    return detected_language

# Função para traduzir texto
def translate_text(text, to_language="pt-br"):
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/translator/text/v3.0/translate"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }
    body = [{"text": text}]
    params = {"to": to_language}
    response = requests.post(url, headers=headers, params=params, json=body)
    response.raise_for_status()
    translations = response.json()[0]["translations"]
    return translations[0]["text"]

# Rota principal para upload e tradução
@app.route("/", methods=["GET", "POST"])
def upload_and_translate():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return "Por favor, envie um arquivo PDF."
        
        # Salvar o arquivo enviado
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)
        
        # Extrair texto do PDF
        extracted_text = extract_text_from_pdf(file_path)
        if not extracted_text.strip():
            return "O PDF está vazio ou não foi possível extrair o texto."
        
        # Detectar idioma e traduzir texto
        translated_text = translate_text(extracted_text, to_language="pt-br")
        
        # Renderizar a página com o texto traduzido
        return render_template("result.html", translated_text=translated_text)
    
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)