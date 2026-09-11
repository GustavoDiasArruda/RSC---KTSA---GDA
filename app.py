import streamlit as st

st.set_page_config(page_title="RSC - KTSA", layout="wide")

st.title("KTSA Automação Industrial")
st.subheader("Relatório de Serviço de Campo - RSC")

# 1. Dados do Cliente
st.markdown("### 1. Dados do Cliente / Atendimento")
col1, col2, col3 = st.columns(3)

with col1:
    empresa = st.text_input("Empresa")
    endereco = st.text_input("Endereço")
    cidade = st.text_input("Cidade")
    solicitante = st.text_input("Solicitante")

with col2:
    cpm = st.text_input("Número CPM")
    bairro = st.text_input("Bairro")
    estado = st.text_input("Estado (UF)")
    departamento = st.text_input("Departamento")

with col3:
    email = st.text_input("E-mail")
    telefone = st.text_input("Telefone / Fax")

# 2. Tipo de Serviço
st.markdown("### 2. Tipo de Serviço")
servico = st.radio(
    "Selecione o Serviço:",
    [
        "Levantamento de Campo",
        "Assistência Técnica",
        "Comissionamento",
        "Start-up",
        "Operação Assistida",
        "Contrato de Manutenção",
        "Outro"
    ],
    horizontal=True
)

servicos_executar = st.text_area("Serviços a Executar / Escopo")

# 3. Relatório de Horas
st.markdown("### 3. Relatório de Horas (Apontamento Semanal)")
dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

horas_data = []
for dia in dias:
    with st.expander(f"Apontamento - {dia}"):
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            data = st.text_input(f"Data ({dia})", key=f"data_{dia}")
        with c2:
            chegada = st.text_input(f"Chegada ({dia})", key=f"chegada_{dia}")
        with c3:
            saida = st.text_input(f"Saída ({dia})", key=f"saida_{dia}")
        with c4:
            intervalo = st.text_input(f"Intervalo ({dia})", key=f"intervalo_{dia}")
        with c5:
            dist_ida = st.number_input(f"Dist. Ida Km ({dia})", key=f"dist_ida_{dia}")

# 4. Despesas
st.markdown("### 4. Despesas de Viagem (R$)")
d1, d2, d3, d4 = st.columns(4)
with d1:
    pedagio = st.number_input("Pedágio", format="%.2f")
with d2:
    refeicao = st.number_input("Refeição", format="%.2f")
with d3:
    hotel = st.number_input("Hotel", format="%.2f")
with d4:
    outros = st.number_input("Outros", format="%.2f")

if st.button("Gerar / Salvar Relatório"):
    st.success("Relatório preenchido com sucesso!")
