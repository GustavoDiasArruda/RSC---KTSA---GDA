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

    st.subheader("2. Tipo de Serviço")
    c_serv1, c_serv2, c_serv3, c_serv4 = st.columns(4)
    with c_serv1:
        s_levantamento = st.checkbox("Levantamento de Campo")
        s_startup = st.checkbox("Start-up")
    with c_serv2:
        s_assistencia = st.checkbox("Assistência Técnica")
        s_operacao = st.checkbox("Operação Assistida")
    with c_serv3:
        s_comissionamento = st.checkbox("Comissionamento")
        s_contrato = st.checkbox("Contrato de Manutenção")
    with c_serv4:
        s_outro = st.checkbox("Outro")
        s_periculosidade = st.checkbox("Periculosidade")

    servicos_executar = st.text_area("Serviços a executar / Área")
    
    submitted = st.form_submit_button("Gerar PDF Oficial KTSA")

if submitted:
    arquivo_excel = 'RSC 08.0000.25 - Relatório de Serviço de Campo - Padrão - Rev.38.xlsx'
    
    if os.path.exists(arquivo_excel):
        wb = openpyxl.load_workbook(arquivo_excel)
        ws = wb.active
        
        def set_cell(sheet, cell_coord, value):
            try:
                sheet[cell_coord] = value
            except AttributeError:
                for merged_range in sheet.merged_cells.ranges:
                    if cell_coord in merged_range:
                        top_left_cell = merged_range.start_cell
                        sheet[top_left_cell.coordinate] = value
                        break
        
        # Dados cadastrais
        set_cell(ws, 'B5', empresa)
        set_cell(ws, 'R5', cpm)
        set_cell(ws, 'B6', endereco)
        set_cell(ws, 'T6', cidade)
        set_cell(ws, 'AE6', estado)
        set_cell(ws, 'B7', bairro)
        set_cell(ws, 'B8', solicitante)
        set_cell(ws, 'T8', departamento)
        set_cell(ws, 'B9', email)
        set_cell(ws, 'T9', telefone)
        set_cell(ws, 'B12', servicos_executar)
        
        # Marcações exatas nas colunas das caixas de seleção da linha 10 e 11
        if s_levantamento: set_cell(ws, 'B10', 'X')
        if s_comissionamento: set_cell(ws, 'L10', 'X')
        if s_startup: set_cell(ws, 'V10', 'X')
        if s_operacao: set_cell(ws, 'AF10', 'X')
        
        if s_assistencia: set_cell(ws, 'B11', 'X')
        if s_contrato: set_cell(ws, 'L11', 'X')
        if s_outro: set_cell(ws, 'V11', 'X')
        if s_periculosidade: set_cell(ws, 'AF11', 'X')
        
        temp_excel = "temp_rsc.xlsx"
        wb.save(temp_excel)
        
        # Conversão via LibreOffice
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", 
            "--outdir", ".", temp_excel
        ])
        
        pdf_file = "temp_rsc.pdf"
        
        if os.path.exists(pdf_file):
            with open(pdf_file, "rb") as f:
                pdf_bytes = f.read()
            
            st.success("PDF gerado com sucesso!")
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
