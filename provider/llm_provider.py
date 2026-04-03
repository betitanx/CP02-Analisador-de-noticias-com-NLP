import json
import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_API_KEY = os.getenv("GEMINI_API_KEY", "")
_MODEL_NAME = "gemini-3.1-flash-lite-preview"


def _get_client() -> genai.Client:
    if not _API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY não configurada. "
            "Crie um arquivo .env com sua chave (veja .env.example)."
        )
    return genai.Client(api_key=_API_KEY)


def analyze_sentiment(text: str) -> dict:
    """
    Analisa o sentimento do texto jornalístico.

    Retorna dict com:
      - label: "positivo" | "negativo" | "neutro"
      - score: float 0-1 (confiança)
      - explanation: justificativa breve
    """
    client = _get_client()

    prompt = f"""Você é um analista de sentimentos especializado em textos jornalísticos em português.
Analise o sentimento geral do texto abaixo e responda EXCLUSIVAMENTE com um JSON válido (sem markdown, sem ```).

O JSON deve ter exatamente estas chaves:
- "label": classificação do sentimento ("positivo", "negativo" ou "neutro")
- "score": número de 0 a 1 representando a confiança na classificação
- "explanation": justificativa breve (1-2 frases) em português

Texto para análise:
\"\"\"
{text}
\"\"\"

Responda APENAS o JSON:"""

    try:
        response = client.models.generate_content(
            model=_MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3),
        )
        raw = response.text.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(raw)

        return {
            "label": result.get("label", "neutro"),
            "score": float(result.get("score", 0.5)),
            "explanation": result.get("explanation", ""),
        }
    except json.JSONDecodeError:
        return {
            "label": "neutro",
            "score": 0.5,
            "explanation": "Não foi possível interpretar a resposta do modelo.",
        }
    except Exception as e:
        raise RuntimeError(f"Erro na análise de sentimento: {e}") from e


def generate_summary(text: str) -> str:
    """
    Gera um resumo conciso da notícia em português.

    Retorna a string do resumo.
    """
    client = _get_client()

    prompt = f"""Você é um jornalista especialista em criar resumos concisos e informativos.
Gere um resumo do texto abaixo em português. O resumo deve:
- Ter entre 3 e 5 frases
- Manter os fatos mais importantes
- Ser claro e objetivo
- Não adicionar informações que não estejam no texto original

Texto para resumir:
\"\"\"
{text}
\"\"\"

Resumo:"""

    try:
        response = client.models.generate_content(
            model=_MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3),
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Erro na geração do resumo: {e}") from e
