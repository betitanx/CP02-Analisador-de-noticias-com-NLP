import re
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """Verifica se a string é uma URL HTTP(S) válida."""
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def truncate_text(text: str, max_chars: int = 30_000) -> str:
    """Trunca o texto para respeitar limites de tokens da API."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n[... texto truncado ...]"


def sentiment_color(label: str) -> str:
    """Retorna cor CSS para o label de sentimento."""
    mapping = {
        "positivo": "#28a745",
        "negativo": "#dc3545",
        "neutro": "#6c757d",
    }
    return mapping.get(label.lower(), "#6c757d")


def sentiment_emoji(label: str) -> str:
    """Retorna emoji para o label de sentimento."""
    mapping = {
        "positivo": "😊",
        "negativo": "😟",
        "neutro": "😐",
    }
    return mapping.get(label.lower(), "❓")


_WHITESPACE_RE = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    """Remove espaços em branco excessivos do texto."""
    text = text.strip()
    text = _WHITESPACE_RE.sub("\n\n", text)
    return text
