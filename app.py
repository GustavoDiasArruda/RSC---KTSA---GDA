import streamlit as st
import openpyxl
import subprocess
import os

st.set_page_config(page_title="Gerador RSC - KTSA", layout="wide")

st.title("Gerador de Relatório de Serviço de Campo (RSC)")
st.write("Preencha os dados abaixo para gerar o PDF oficial idêntico ao padrão KTSA.")

# Carrega a lista de clientes direto da planilha Excel (ajuste a aba e célula se necessário)
arquivo_excel = 'RSC 08.0000.25 - Relatório de Serviço de Campo - Padrão - Rev.38.xlsx'
lista_clientes = []
if os.path.exists(arquivo_excel):
    wb = openpyxl.load_workbook(arquivo_excel, data_only=True)
    # Exemplo: se os clientes estiverem em uma aba específica de cadastro, ajuste o nome dela aqui
    # Caso contrário, podemos deixar uma lista padrão ou buscar de um intervalo
    lista_clientes = ["Cliente A", "Cliente B", "Cliente C"] # Substitua ou ajuste conforme sua aba de clientes

with st.form("rsc_form"):
    st.subheader("1. Dados do Cliente / Atendimento")
    col1, col2 = st.columns(2)
    
    with col1:
        empresa = st.selectbox("Empresa", options=lista_clientes)
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
