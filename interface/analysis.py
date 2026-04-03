import streamlit as st
import pandas as pd
from datetime import datetime

from pipeline.nlp_processor import process_news
from utils.helpers import sentiment_color, sentiment_emoji


def _init_history():
    if "history" not in st.session_state:
        st.session_state.history = []


def _save_to_history(result: dict):
    st.session_state.history.append({
        "Horário": datetime.fromisoformat(result["processed_at"]).strftime("%d/%m/%Y %H:%M"),
        "Título": result["title"][:60],
        "Fonte": result["source"][:50],
        "Sentimento": result["sentiment"]["label"].capitalize(),
        "Confiança": result["sentiment"]["score"],
    })


def _render_input() -> tuple[str, str]:
    """Renderiza a seção de entrada e retorna (url, text)."""
    st.subheader("📥 Entrada da Notícia")

    input_mode = st.radio(
        "Como deseja informar a notícia?",
        ["URL da notícia", "Colar texto"],
        horizontal=True,
    )

    url = ""
    text = ""

    if input_mode == "URL da notícia":
        url = st.text_input(
            "Cole a URL da notícia:",
            placeholder="https://g1.globo.com/...",
        )
    else:
        text = st.text_area(
            "Cole o texto da notícia:",
            height=200,
            placeholder="Cole aqui o conteúdo da notícia para análise...",
        )

    return url, text


def _render_results(result: dict):
    """Renderiza os resultados da análise."""
    st.markdown("---")
    st.subheader("📊 Resultados da Análise")

    st.markdown(f"### {result['title']}")

    sent = result["sentiment"]
    color = sentiment_color(sent["label"])
    emoji = sentiment_emoji(sent["label"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sentimento", f"{emoji} {sent['label'].capitalize()}")
    with col2:
        st.metric("Confiança", f"{sent['score']:.0%}")
    with col3:
        st.metric("Fonte", "URL" if result["source"] != "Texto manual" else "Texto")

    st.markdown(
        f"""
        <div style="
            background-color: {color}22;
            border-left: 4px solid {color};
            padding: 1rem;
            border-radius: 6px;
            margin: 1rem 0;
        ">
            <strong>Justificativa:</strong> {sent['explanation']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.markdown("#### 📝 Resumo Gerado")
        st.info(result["summary"])

    with res_col2:
        st.markdown("#### 📄 Texto Original")
        display_text = result["original_text"]
        if len(display_text) > 1500:
            display_text = display_text[:1500] + "\n\n[... texto truncado para exibição ...]"
        st.text_area(
            "Conteúdo extraído",
            value=display_text,
            height=300,
            disabled=True,
            label_visibility="collapsed",
        )


def _render_history():
    """Renderiza o histórico de análises da sessão."""
    if not st.session_state.history:
        return

    st.markdown("---")
    st.subheader("📋 Histórico de Análises")

    df = pd.DataFrame(st.session_state.history)
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Confiança": st.column_config.ProgressColumn(
                min_value=0, max_value=1, format="%.0%%",
            ),
        },
        hide_index=True,
    )


def render():
    _init_history()

    st.title("🔍 Análise de Notícia")

    url, text = _render_input()

    has_input = bool(url.strip()) or bool(text.strip())

    if st.button("⚡ Processar Notícia", type="primary", disabled=not has_input):
        with st.status("Processando notícia...", expanded=True) as status:
            try:
                if url.strip():
                    st.write("🌐 Extraindo conteúdo da URL...")
                else:
                    st.write("📄 Processando texto informado...")

                st.write("🤖 Analisando sentimento...")
                st.write("📝 Gerando resumo...")

                result = process_news(
                    url=url.strip() if url.strip() else None,
                    text=text.strip() if text.strip() else None,
                )

                status.update(label="Análise concluída!", state="complete")

            except ValueError as e:
                status.update(label="Erro na entrada", state="error")
                st.error(f"⚠️ {e}")
                return
            except RuntimeError as e:
                status.update(label="Erro no processamento", state="error")
                st.error(f"🚨 {e}")
                return
            except Exception as e:
                status.update(label="Erro inesperado", state="error")
                st.error(f"❌ Erro inesperado: {e}")
                return

        _render_results(result)
        _save_to_history(result)

    _render_history()
