import streamlit as st
import openpyxl
import io
import os

st.set_page_config(page_title="Gerador RSC - KTSA", layout="wide")

st.title("Gerador de Relatório de Serviço de Campo (RSC)")
st.write("Preencha os campos abaixo para gerar a planilha preenchida exatamente com o layout padrão KTSA.")

# 1. Dados do Cliente
st.subheader("1. Dados do Cliente / Atendimento")
col1, col2 = st.columns(2)

with col1:
    empresa = st.text_input("Empresa")
    endereco = st.text_input("Endereço")
    bairro = st.text_input("Bairro")
    solicitante = st.text_input("Solicitante")
    email = st.text_input("E-mail")

with col2:
    cpm = st.text_input("Número CPM")
    cidade = st.text_input("Cidade")
    estado = st.text_input("Estado")
    departamento = st.text_input("Departamento")
    telefone = st.text_input("Telefone / Fax")

# 2. Tipo de Serviço
st.subheader("2. Tipo de Serviço")
servico = st.radio(
    "Selecione o Serviço Principal:",
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

servicos_executar = st.text_area("Serviços a executar / Área")

# Botão para gerar a planilha preenchida
if st.button("Gerar Planilha RSC Oficial", type="primary"):
    arquivo_excel = 'RSC 08.0000.25 - Relatório de Serviço de Campo - Padrão - Rev.38.xlsx'
    
    if os.path.exists(arquivo_excel):
        wb = openpyxl.load_workbook(arquivo_excel)
        ws = wb['Frente - Relatório de SC - 1'] # Aba principal da frente do relatório
        
        # Inserindo os dados nas células mapeadas do template original
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
        
        # Salvando em memória para disponibilizar o download
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        st.success("Relatório gerado com sucesso!")
        st.download_button(
            label="Baixar Planilha RSC Preenchida",
            data=output,
            file_name="RSC_Preenchido.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("O arquivo de modelo Excel não foi encontrado no repositório.")
