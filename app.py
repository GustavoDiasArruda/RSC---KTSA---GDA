import streamlit as st
import openpyxl
import subprocess
import os
import io

st.set_page_config(page_title="Gerador RSC - KTSA", layout="wide")

st.title("Gerador de Relatório de Serviço de Campo (RSC)")
st.write("Preencha os dados abaixo para gerar o PDF oficial idêntico ao padrão KTSA.")

with st.form("rsc_form"):
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

    servicos_executar = st.text_area("Serviços a executar / Área")
    
    submitted = st.form_submit_button("Gerar PDF Oficial KTSA")

if submitted:
    arquivo_excel = 'RSC 08.0000.25 - Relatório de Serviço de Campo - Padrão - Rev.38.xlsx'
    
    if os.path.exists(arquivo_excel):
        wb = openpyxl.load_workbook(arquivo_excel)
        ws = wb.active
        
        # Função auxiliar para gravar valores mesmo em células mescladas
        def set_cell(sheet, cell_coord, value):
            try:
                sheet[cell_coord] = value
            except AttributeError:
                # Se for célula mesclada, pega a célula principal superior esquerda do intervalo
                for merged_range in sheet.merged_cells.ranges:
                    if cell_coord in merged_range:
                        top_left_cell = merged_range.start_cell
                        sheet[top_left_cell.coordinate] = value
                        break
        
        set_cell(ws, 'B4', empresa)
        set_cell(ws, 'AE4', cpm)
        set_cell(ws, 'B5', endereco)
        set_cell(ws, 'V5', cidade)
        set_cell(ws, 'AT5', estado)
        set_cell(ws, 'B6', bairro)
        set_cell(ws, 'AE6', departamento)
        set_cell(ws, 'B7', solicitante)
        set_cell(ws, 'AE7', telefone)
        set_cell(ws, 'B8', email)
        set_cell(ws, 'B11', servicos_executar)
        
        temp_excel = "temp_rsc.xlsx"
        wb.save(temp_excel)
        
        # Converte para PDF mantendo o layout exato via LibreOffice
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", 
            "--outdir", ".", temp_excel
        ])
        
        pdf_file = "temp_rsc.pdf"
        
        if os.path.exists(pdf_file):
            with open(pdf_file, "rb") as f:
                pdf_bytes = f.read()
            
            st.success("PDF gerado com sucesso no layout original!")
            st.download_button(
                label="📥 Baixar PDF Oficial RSC",
                data=pdf_bytes,
                file_name="RSC_Oficial.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Erro ao converter o arquivo para PDF.")
    else:
        st.error("Arquivo modelo Excel não encontrado no repositório.")
