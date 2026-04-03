import requests
from bs4 import BeautifulSoup
from newspaper import Article, Config as NewsConfig

from utils.helpers import is_valid_url


_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

_HEADERS = {"User-Agent": _USER_AGENT}

_NOISE_TAGS = [
    "script", "style", "nav", "footer", "header",
    "aside", "iframe", "noscript", "form",
]


def _detect_language(url: str) -> str:
    """Detecta idioma provável pela URL (pt ou en)."""
    pt_indicators = [".br", "/portuguese", "/pt/", "globo.com", "uol.com", "folha.uol"]
    url_lower = url.lower()
    return "pt" if any(ind in url_lower for ind in pt_indicators) else "en"


def _extract_with_newspaper(url: str) -> dict | None:
    """Tenta extrair o artigo usando a biblioteca newspaper3k."""
    try:
        config = NewsConfig()
        config.browser_user_agent = _USER_AGENT
        config.request_timeout = 15

        lang = _detect_language(url)
        article = Article(url, language=lang, config=config)
        article.download()
        article.parse()

        if not article.text or len(article.text.strip()) < 80:
            return None

        return {
            "title": article.title or "",
            "text": article.text.strip(),
            "source": url,
        }
    except Exception:
        return None


def _extract_with_bs4(url: str) -> dict | None:
    """Fallback: extrai o artigo usando requests + BeautifulSoup."""
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding

        soup = BeautifulSoup(resp.text, "lxml")

        for tag in soup.find_all(_NOISE_TAGS):
            tag.decompose()

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""
        if not title:
            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else "Sem título"

        article_el = (
            soup.find("article")
            or soup.find("main")
            or soup.find("div", class_=lambda c: c and any(
                k in (c if isinstance(c, str) else " ".join(c))
                for k in ["content", "article", "post", "texto", "materia"]
            ))
        )

        container = article_el if article_el else soup.body
        if container is None:
            return None

        paragraphs = container.find_all("p")
        text = "\n".join(
            p.get_text(strip=True)
            for p in paragraphs
            if len(p.get_text(strip=True)) > 30
        )

        if len(text.strip()) < 80:
            return None

        return {
            "title": title,
            "text": text.strip(),
            "source": url,
        }
    except Exception:
        return None


def scrape_news(url: str) -> dict:
    """
    Extrai título e corpo de uma notícia a partir da URL.

    Retorna dict com chaves: title, text, source.
    Levanta ValueError se não conseguir extrair.
    """
    if not is_valid_url(url):
        raise ValueError(f"URL inválida: {url}")

    result = _extract_with_newspaper(url)
    if result:
        return result

    result = _extract_with_bs4(url)
    if result:
        return result

    raise ValueError(
        "Não foi possível extrair o conteúdo da notícia. "
        "Verifique se a URL aponta para um artigo acessível."
    )
