import streamlit as st
import openpyxl
import io
import os

st.set_page_config(page_title="RSC - KTSA", layout="wide")

# CSS personalizado para replicar o layout de grade do Excel/PDF
st.markdown("""
    <style>
    .excel-container {
        border: 2px solid #000;
        background-color: #fff;
        padding: 10px;
        color: #000;
        font-family: Arial, sans-serif;
    }
    .excel-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    .excel-table td, .excel-table th {
        border: 1px solid #000;
        padding: 4px 8px;
        font-size: 11px;
        vertical-align: middle;
    }
    .header-title {
        font-weight: bold;
        font-size: 14px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("### Relatório de Serviço de Campo - Visualizador de Layout KTSA")

# Formulário simulando a exata grade do Excel
with st.form("rsc_form"):
    st.markdown("""
    <div class="excel-container">
        <table class="excel-table">
            <tr>
                <td colspan="6" class="header-title">RELATÓRIO DE SERVIÇOS DE CAMPO - RSC</td>
                <td colspan="2" style="text-align: center; font-weight: bold;">KTSA Automação</td>
            </tr>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
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

    servicos_executar = st.text_area("Serviços a executar / Área:")
    
    submitted = st.form_submit_button("Gerar Planilha Excel Oficial Preenchida")

if submitted:
    arquivo_excel = 'RSC 08.0000.25 - Relatório de Serviço de Campo - Padrão - Rev.38.xlsx'
    
    if os.path.exists(arquivo_excel):
        wb = openpyxl.load_workbook(arquivo_excel)
        ws = wb['Frente - Relatório de SC - 1']
        
        ws['B4'] = empresa
        ws['AE4'] = cpm
        ws['B5'] = endereco
        ws['V5'] = cidade
        ws['AT5'] = estado
        ws['B6'] = bairro
        ws['AE6'] = departamento
        ws['B7'] = solicitante
        ws['AE7'] = telefone
        ws['B8'] = email
        ws['B11'] = servicos_executar
        
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        st.success("Planilha gerada com sucesso mantendo o layout original!")
        st.download_button(
            label="📥 Baixar Excel Oficial Preenchido",
            data=output,
            file_name="RSC_KTSA_Preenchido.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Arquivo modelo Excel não encontrado no repositório.")
