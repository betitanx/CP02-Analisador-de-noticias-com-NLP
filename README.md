# CP02 — Analisador de Notícias com NLP

Aplicação Streamlit que analisa notícias jornalísticas usando Processamento de Linguagem Natural. O usuário informa uma URL ou cola o texto, e a aplicação retorna a análise de sentimento e um resumo automático via API do Gemini.

## Equipe

| Nome | RM |
|------|-----|
| Lucca Phelipe Masini | 564121 |
| Luiz Henrique Poss | 562177 |
| Igor Paixão Sarak | 563726 |
| Bernardo Braga Perobeli | 562468 |
| Felipe Stefani Honorato | 563380 |

## Arquitetura

```
├── app.py              # Roteamento entre páginas
├── interface/          # Telas (home e análise)
├── pipeline/           # Orquestração do processamento NLP
├── provider/           # Scraping de notícias e integração com Gemini
└── utils/              # Funções auxiliares
```

## Como executar

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` com sua chave do Gemini:

```
GEMINI_API_KEY=sua_chave_aqui
```

Inicie a aplicação:

```bash
streamlit run app.py
```
