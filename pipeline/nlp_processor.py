from datetime import datetime

from provider.scraper import scrape_news
from provider.llm_provider import analyze_sentiment, generate_summary
from utils.helpers import truncate_text, clean_text


def process_news(url: str | None = None, text: str | None = None) -> dict:
    """
    Pipeline completa de processamento de notícia.

    Aceita URL (faz scraping) ou texto direto.

    Retorna dict com:
      - title: título da notícia
      - original_text: texto completo extraído/informado
      - source: URL de origem ou "Texto manual"
      - sentiment: dict com label, score, explanation
      - summary: string do resumo
      - processed_at: timestamp ISO
    """
    if not url and not text:
        raise ValueError("Informe uma URL ou cole o texto da notícia.")

    title = ""
    source = "Texto manual"
    original_text = ""

    if url and url.strip():
        scraped = scrape_news(url.strip())
        title = scraped["title"]
        original_text = scraped["text"]
        source = scraped["source"]
    elif text and text.strip():
        original_text = clean_text(text.strip())
        title = original_text[:80].split("\n")[0] + "..."
    else:
        raise ValueError("O conteúdo fornecido está vazio.")

    text_for_api = truncate_text(original_text)

    sentiment = analyze_sentiment(text_for_api)
    summary = generate_summary(text_for_api)

    return {
        "title": title,
        "original_text": original_text,
        "source": source,
        "sentiment": sentiment,
        "summary": summary,
        "processed_at": datetime.now().isoformat(),
    }
