# **Tradutor-Artigos-Tecnicos-AzureAI**

Utilizando Python unido ao recurso Translator do Azure, é possivel criar uma aplicação simples, porém poderosa. 
Nesta demonstração será possível realizar a tradução de textos ou arquivos em formato DOCX e PDF de forma confiável.

![image](https://github.com/user-attachments/assets/30887445-a7ff-4055-83fa-aa7f8ef4d88c)


## Funcionalidades da Aplicação
* **Texto Manual ou Arquivo Upload**:
  * Digite texto no campo ou envie um arquivo (PDF ou DOCX).
* **Seleção do Idioma de Destino**:
  * Escolha entre os 4 idiomas disponíveis no menu suspenso.
* **Resultados**:
  * O idioma detectado (com nome amigável) e a confiança são exibidos.
  * Os textos original e traduzido aparecem lado a lado.


## **Tecnologias usadas**
1. **Python**:
   * Linguagem principal para lógica do servidor.
2. **Flask**:
   * Framework web para criar a aplicação e gerenciar rotas.
3. **Azure Cognitive Services - Translator**:
   * API para detectar idiomas e traduzir textos.
4. **HTML e CSS**:
   * Interface do usuário para interatividade e layout.
5. **Bibliotecas auxiliares**:
   * requests: Para chamadas à API da Azure.
   * python-docx: Para extrair texto de arquivos DOCX.
   * PyPDF2: Para extrair texto de arquivos PDF.
  

## **Como usar**
**Pré-requisitos**
1. **Azure Subscription**:
   * Configure um serviço de Translator no Azure e obtenha:
     * Chave de API (Subscription Key).
     * Endpoint da API.
2. **Python Instalado**:
   * Recomendado: Python 3.9+.
3. **Bibliotecas Python**:
   * Instale com:
     ```bash
      pip install flask requests python-docx PyPDF2
     ```

**Configuração**
1. **Substitua a Chave e Endpoint no Código**:
   * No arquivo `app.py`, insira sua chave e endpoint da Azure:
     ```python
      TRANSLATOR_KEY = "INSIRA_SUA_KEY"
      AZURE_TRANSLATOR_REGION = "INSIRA_SUA_REGIAO"
     ```
2. **Execute o Script**:
   * Inicie o servidor Flask:
     ```bash
      python app.py
     ```
3. **Acesse no Navegador**:
   * Abra `http://127.0.0.1:5000/` para acessar a aplicação.


## **Estrutura do projeto**
```tree
.
├── app.py
├── README.MD
├── templates
   └── index.html
├── README.MD
```

