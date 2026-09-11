import streamlit as st
import openpyxl
import subprocess
import os

st.set_page_config(page_title="Gerador RSC - KTSA", layout="wide")

st.title("Gerador de Relatório de Serviço de Campo (RSC)")
st.write("Preencha os dados abaixo para gerar o PDF oficial idêntico ao padrão KTSA.")

arquivo_excel = 'RSC 08.0000.25 - Relatório de Serviço de Campo - Padrão - Rev.38.xlsx'

# Dicionário para armazenar os dados de cada cliente vindos da aba "KM e Tempo Percurso"
clientes_dict = {}
if os.path.exists(arquivo_excel):
    wb_temp = openpyxl.load_workbook(arquivo_excel, data_only=True)
    if 'KM e Tempo Percurso' in wb_temp.sheetnames:
        ws_km = wb_temp['KM e Tempo Percurso']
        for r in range(7, ws_km.max_row + 1):
            destino = ws_km.cell(row=r, column=1).value
            if destino:
                clientes_dict[str(destino).strip()] = {
                    'cidade': ws_km.cell(row=r, column=2).value or '',
                    'estado': ws_km.cell(row=r, column=3).value or '',
                    'endereco': ws_km.cell(row=r, column=4).value or '',
                    'bairro': ws_km.cell(row=r, column=5).value or '',
                    'solicitante': ws_km.cell(row=r, column=6).value or '',
                    'area': ws_km.cell(row=r, column=7).value or '',
                    'email': ws_km.cell(row=r, column=8).value or '',
                    'telefone': ws_km.cell(row=r, column=9).value or ''
                }

lista_clientes = list(clientes_dict.keys())

with st.form("rsc_form"):
    st.subheader("1. Dados do Cliente / Atendimento")
    
    # Seleção da empresa puxa automaticamente os dados cadastrados
    empresa_selecionada = st.selectbox("Empresa", options=lista_clientes if lista_clientes else ["Selecione o Cliente"])
    
    dados_padrao = clientes_dict.get(empresa_selecionada, {})
    
    col1, col2 = st.columns(2)
    with col1:
        endereco = st.text_input("Endereço", value=str(dados_padrao.get('endereco', '')))
        bairro = st.text_input("Bairro", value=str(dados_padrao.get('bairro', '')))
        solicitante = st.text_input("Solicitante", value=str(dados_padrao.get('solicitante', '')))
        email = st.text_input("E-mail", value=str(dados_padrao.get('email', '')))
    with col2:
        cpm = st.text_input("Número CPM")
        cidade = st.text_input("Cidade", value=str(dados_padrao.get('cidade', '')))
        estado = st.text_input("Estado", value=str(dados_padrao.get('estado', '')))
        departamento = st.text_input("Departamento / Área", value=str(dados_padrao.get('area', '')))
        telefone = st.text_input("Telefone / Fax", value=str(dados_padrao.get('telefone', '')))

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

    servicos_executar = st.text_area("Serviços a executar")
    
    submitted = st.form_submit_button("Gerar PDF Oficial KTSA")

if submitted:
    if os.path.exists(arquivo_excel):
        wb = openpyxl.load_workbook(arquivo_excel)
        
        if 'Frente - Relatório de SC - 1' in wb.sheetnames:
            ws = wb['Frente - Relatório de SC - 1']
        else:
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
        
        # Preenchimento exato nas células mapeadas da planilha oficial KTSA
        set_cell(ws, 'C5', empresa_selecionada)
        set_cell(ws, 'AJ5', cpm)
        set_cell(ws, 'C6', endereco)
        set_cell(ws, 'C7', bairro)
        set_cell(ws, 'AA7', cidade)
        set_cell(ws, 'AV7', estado)
        set_cell(ws, 'C8', solicitante)
        set_cell(ws, 'AJ8', departamento)
        set_cell(ws, 'C9', email)
        set_cell(ws, 'AJ9', telefone)
        set_cell(ws, 'C12', servicos_executar)
        
        # Marcações limpas das caixas de seleção
        set_cell(ws, 'F10', 'X' if s_levantamento else '')
        set_cell(ws, 'U10', 'X' if s_comissionamento else '')
        set_cell(ws, 'AH10', 'X' if s_startup else '')
        set_cell(ws, 'AQ10', 'X' if s_operacao else '')
        
        set_cell(ws, 'F11', 'X' if s_assistencia else '')
        set_cell(ws, 'U11', 'X' if s_contrato else '')
        set_cell(ws, 'AH11', 'X' if s_outro else '')
        set_cell(ws, 'AQ11', 'X' if s_periculosidade else '')
        
        temp_excel = "temp_rsc.xlsx"
        wb.save(temp_excel)
        
        # Conversão para PDF via LibreOffice
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
