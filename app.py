import streamlit as st

st.set_page_config(page_title="RSC - KTSA", layout="wide")

# Estilo visual para imitar o formulário impresso / planilha
st.markdown("""
    <style>
    .rsc-box {
        border: 2px solid #333;
        padding: 10px;
        background-color: #ffffff;
        color: #000000;
        font-family: Arial, sans-serif;
    }
    .rsc-header {
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .table-grid {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .table-grid th, .table-grid td {
        border: 1px solid #999;
        padding: 6px;
        text-align: center;
        font-size: 12px;
        color: #000;
    }
    .table-grid th {
        background-color: #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="rsc-box">
    <div class="rsc-header" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="margin: 0; color: #000;">KTSA Automação Industrial LTDA.</h2>
            <p style="margin: 0; font-weight: bold; color: #555;">RELATÓRIO DE SERVIÇOS DE CAMPO - RSC</p>
        </div>
        <div style="border: 2px solid #000; padding: 5px 15px; font-weight: bold; font-size: 18px;">
            RSC
        </div>
    </div>
""", unsafe_allow_html=True)

# 1. Dados do Cliente (Emulando o layout de grade do Excel)
st.markdown("#### 1. Dados do Cliente / Atendimento")

col1, col2 = st.columns([3, 1])
with col1:
    empresa = st.text_input("Empresa:")
    endereco = st.text_input("Endereço:")
    bairro = st.text_input("Bairro:")
    solicitante = st.text_input("Solicitante:")
    email = st.text_input("E-mail:")
with col2:
    cpm = st.text_input("Número CPM:")
    cidade = st.text_input("Cidade:")
    estado = st.text_input("Estado:")
    departamento = st.text_input("Departamento:")
    telefone = st.text_input("Telefone / Fax:")

# 2. Tipo de Serviço
st.markdown("---")
st.markdown("#### 2. Tipo de Serviço")
servicos_lista = [
    "Levantamento de Campo", "Assistência Técnica", "Comissionamento", 
    "Start-up", "Operação Assistida", "Contrato de Manutenção", "Outro", "Periculosidade"
]
cols_serv = st.columns(4)
servico_selecionado = {}
for i, serv in enumerate(servicos_lista):
    with cols_serv[i % 4]:
        servico_selecionado[serv] = st.checkbox(serv)

servicos_executar = st.text_area("Serviços a executar / Área:")

# 3. Relatório de Horas
st.markdown("---")
st.markdown("#### 3. Relatório de Horas")

dias = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]
tabela_horas = {}

# Criando a tabela interativa idêntica ao PDF
st.markdown('<table class="table-grid">', unsafe_allow_html=True)
st.markdown('<tr><th>DIA DA SEMANA</th>' + "".join([f"<th>{d}</th>" for d in dias]) + '</tr>', unsafe_allow_html=True)

campos_horas = [
    "DATA (Dia/Mês/Ano)", 
    "Horário de Chegada", 
    "Horário de Saída", 
    "Intervalo (Almoço/Jantar)", 
    "Deslocamento Ida", 
    "Deslocamento Volta", 
    "Distância Ida (Km)", 
    "Distância volta (Km)"
]

dados_linhas = {}
for campo in campos_horas:
    cols_inputs = st.columns(8)
    with cols_inputs[0]:
        st.markdown(f"**{campo}**")
    
    dados_linhas[campo] = []
    for i, dia in enumerate(dias):
        with cols_inputs[i + 1]:
            val = st.text_input(f"{campo}_{dia}", key=f"{campo}_{dia}", label_visibility="collapsed")
            dados_linhas[campo].append(val)

st.markdown('</div>', unsafe_allow_html=True)

if st.button("💾 Salvar Relatório de Campo", type="primary"):
    st.success("Relatório estruturado com sucesso no formato oficial!")
