# 📰 Analisador de Notícias com NLP

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50-FF4B4B?logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)
![Status](https://img.shields.io/badge/Status-Deployed-brightgreen)

## 📌 Sobre o Projeto

Este projeto consiste em uma plataforma interativa de análise de notícias desenvolvida para as disciplinas de **Front End e Mobile Development** e **Natural Language Processing (NLP)**. A aplicação permite que o usuário informe uma notícia via URL ou texto e obtenha automaticamente a **análise de sentimento** e um **resumo conciso** do conteúdo, utilizando a API do **Google Gemini**.

A arquitetura do projeto foi desenhada sob os princípios de **separação de responsabilidades** e **modularização**, garantindo clareza estrutural entre interface, processamento e aquisição de dados.

---

## 🚀 Principais Features e Arquitetura Técnica

### 📥 Coleta de Notícias (Web Scraping)

- **Extração inteligente com fallback:** Utiliza `newspaper3k` como estratégia primária e `BeautifulSoup` como fallback para garantir a extração do conteúdo.
- **Suporte a portais brasileiros e internacionais:** User-Agent configurado e parsing otimizado para portais de notícia em português e inglês.
- **Entrada flexível:** O usuário pode informar a URL da notícia ou colar o texto diretamente.

### 🤖 Análise de Sentimento

- **Classificação via LLM:** Prompt estruturado enviado ao Google Gemini retornando classificação (positivo, negativo, neutro), score de confiança e justificativa.
- **Visualização semântica:** Indicadores visuais com cores condicionais e emojis para comunicação rápida do resultado.

### 📝 Resumo Automático

- **Sumarização via LLM:** Geração de resumo conciso (3-5 frases) mantendo os fatos mais relevantes da notícia original.
- **Temperatura controlada (0.3):** Respostas consistentes e determinísticas.

### 📊 Histórico e Analytics

- **Histórico de sessão:** Tabela interativa com `st.dataframe` registrando todas as análises realizadas, incluindo barra de progresso para o score de confiança.
- **Persistência em sessão:** Dados mantidos via `st.session_state` durante toda a sessão do usuário.

---

## 🏗️ Arquitetura do Projeto

```
├── app.py                  # Entry point and page routing
├── interface/              # Presentation layer (Streamlit)
│   ├── home.py             # Home screen: team, architecture and instructions
│   └── analysis.py         # Analysis screen: input, results and history
├── pipeline/               # NLP processing layer
│   └── nlp_processor.py    # Orchestration: scraping → sentiment → summary
├── provider/               # Data acquisition layer
│   ├── scraper.py          # Web scraping (newspaper3k + BeautifulSoup)
│   └── llm_provider.py     # Google Gemini API integration
└── utils/                  # Shared utilities
    └── helpers.py          # URL validation, formatting, truncation
```

---

## 🛠️ Instalação e Uso Local

### 1. Clonando o Repositório

```bash
git clone https://github.com/betitanx/CP02-Analisador-de-noticias-com-NLP.git
cd CP02-Analisador-de-noticias-com-NLP
```

### 2. Instalando Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurando a API Key

Crie um arquivo `.env` na raiz do projeto:

```
GEMINI_API_KEY=your_api_key_here
```

### 4. Executando o App

```bash
streamlit run app.py
```

---

## 📦 Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **Streamlit** | Interactive web interface |
| **Google Gemini** | Sentiment analysis and summarization |
| **newspaper3k** | News article extraction |
| **BeautifulSoup** | HTML parsing (fallback) |
| **python-dotenv** | Environment variables management |
| **Pandas** | History data handling |
