import streamlit as st


_TEAM = [
    {"name": "Lucca Phelipe Masini", "rm": "RM 564121"},
    {"name": "Luiz Henrique Poss", "rm": "RM 562177"},
    {"name": "Igor Paixão Sarak", "rm": "RM 563726"},
    {"name": "Bernardo Braga Perobeli", "rm": "RM 562468"},
    {"name": "Felipe Stefani Honorato", "rm": "RM 563380"},
]


def render():
    st.title("📰 Analisador de Notícias com NLP")

    st.markdown(
        """
        Bem-vindo à plataforma de análise de notícias! Esta aplicação integra
        **Front-end** e **Processamento de Linguagem Natural (NLP)** para permitir
        que você analise conteúdo jornalístico de forma automatizada.

        ### O que a aplicação faz?

        1. **Coleta** — Informe a URL de uma notícia ou cole o texto diretamente
        2. **Análise de Sentimento** — Identifica o tom geral do texto (positivo, negativo ou neutro)
        3. **Resumo Automático** — Gera uma síntese concisa dos pontos mais importantes

        ---
        """
    )

    st.subheader("👥 Equipe")

    cols = st.columns(len(_TEAM))
    for col, member in zip(cols, _TEAM):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #1e3a5f, #2d5986);
                    padding: 1.5rem;
                    border-radius: 12px;
                    text-align: center;
                    height: 140px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <p style="font-size: 1.1rem; font-weight: 600; margin: 0; color: #fff;">
                        {member['name']}
                    </p>
                    <p style="font-size: 0.85rem; margin: 0.3rem 0 0; color: #a0c4e8;">
                        {member['rm']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    st.subheader("🏗️ Arquitetura do Projeto")

    st.markdown(
        """
        O projeto segue uma separação clara de responsabilidades:

        | Camada | Pasta | Responsabilidade |
        |--------|-------|------------------|
        | **Interface** | `interface/` | Telas Streamlit (home, análise) |
        | **Pipeline** | `pipeline/` | Orquestração do processamento NLP |
        | **Provider** | `provider/` | Scraping de notícias e integração com API Gemini |
        | **Utilitários** | `utils/` | Funções auxiliares compartilhadas |

        O roteamento entre as páginas é feito pelo `app.py`, que atua como
        ponto de entrada e controlador de navegação.
        """
    )

    st.markdown("---")

    st.subheader("🚀 Como usar")

    st.markdown(
        """
        1. Navegue até a página **Análise de Notícia** pelo menu lateral
        2. Cole a **URL** de uma notícia ou o **texto** diretamente
        3. Clique em **Processar** e aguarde os resultados
        4. Veja o sentimento detectado e o resumo gerado
        """
    )
