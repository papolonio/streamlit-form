import streamlit as st
from datetime import date
import re
from components.webhook_sender import send_to_webhook

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def render_form():
    tipo_projeto = st.radio("Tipo de Projeto", ["Projeto Pontual", "Assessoria"])
    nome_projeto = st.text_input("Nome do Projeto *")

    st.markdown("### Responsáveis")
    responsaveis = []
    num_responsaveis = st.session_state.get("num_responsaveis", 1)

    for i in range(num_responsaveis):
        with st.container():
            cols = st.columns(3)
            nome = cols[0].text_input(f"Nome do Responsável {i+1} *", key=f"nome_{i}")
            cargo = cols[1].text_input(f"Cargo {i+1} *", key=f"cargo_{i}")
            email = cols[2].text_input(f"Email {i+1} *", key=f"email_{i}")
            responsaveis.append({"nome": nome, "cargo": cargo, "email": email})

    if st.button("Adicionar Responsável"):
        st.session_state["num_responsaveis"] = num_responsaveis + 1
        st.experimental_rerun()

    valor = st.text_input("Valor do Projeto (R$) *", placeholder="Ex: 10000.00")
    analista = st.text_input("Analista Responsável *")
    squad = st.text_input("Squad Responsável *")
    data_inicio = st.date_input("Data de Início", value=date.today())

    data_final = None
    if tipo_projeto == "Projeto Pontual":
        data_final = st.date_input("Data de Finalização", min_value=data_inicio)

    if st.button("Enviar"):
        if not nome_projeto or not valor or not analista or not squad:
            st.error("Por favor, preencha todos os campos obrigatórios.")
            return

        if not all([r["nome"] and r["cargo"] and r["email"] for r in responsaveis]):
            st.error("Preencha todos os dados dos responsáveis.")
            return

        if not all([validate_email(r["email"]) for r in responsaveis]):
            st.error("Algum email informado é inválido.")
            return

        try:
            valor_float = float(valor.replace(",", "."))
        except ValueError:
            st.error("Informe um valor numérico válido para o projeto.")
            return

        payload = {
            "tipo_projeto": tipo_projeto,
            "nome_projeto": nome_projeto,
            "responsaveis": responsaveis,
            "valor": valor_float,
            "analista": analista,
            "squad": squad,
            "data_inicio": str(data_inicio),
            "data_final": str(data_final) if data_final else None,
        }

        success = send_to_webhook(payload)
        if success:
            st.success("✅ Dados enviados com sucesso!")
        else:
            st.error("❌ Erro ao enviar os dados.")
