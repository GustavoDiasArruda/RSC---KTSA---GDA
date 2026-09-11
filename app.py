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
    
    st.subheader("3. Descrição dos Serviços Executados (Relatório de Campo)")
    relatorio_executados = st.text_area(
        "Escreva detalhadamente o que foi feito no dia:",
        placeholder="Digite aqui o passo a passo dos serviços executados em campo...",
        height=150
    )
    
    submitted = st.form_submit_button("Gerar PDF Oficial KTSA")

if submitted:
    if os.path.exists(arquivo_excel):
        wb = openpyxl.load_workbook(arquivo_excel)
        
        # Aba da frente / dados gerais
        if 'Frente - Relatório de SC - 1' in wb.sheetnames:
            ws_frente = wb['Frente - Relatório de SC - 1']
        else:
            ws_frente = wb.active
            
        def set_cell(sheet, cell_coord, value):
            try:
                sheet[cell_coord] = value
            except AttributeError:
                for merged_range in sheet.merged_cells.ranges:
                    if cell_coord in merged_range:
                        top_left_cell = merged_range.start_cell
                        sheet[top_left_cell.coordinate] = value
                        break
        
        # Preenchimento dos dados da primeira parte
        set_cell(ws_frente, 'G5', empresa_selecionada)
        set_cell(ws_frente, 'AL5', cpm)
        set_cell(ws_frente, 'G6', endereco)
        set_cell(ws_frente, 'G7', bairro)
        set_cell(ws_frente, 'Z7', cidade)
        set_cell(ws_frente, 'AV7', estado)
        set_cell(ws_frente, 'G8', solicitante)
        set_cell(ws_frente, 'AL8', departamento)
        set_cell(ws_frente, 'G9', email)
        set_cell(ws_frente, 'AL9', telefone)
        set_cell(ws_frente, 'G12', servicos_executar)
        
        # Caixas de seleção
        set_cell(ws_frente, 'E10', '◼' if s_levantamento else '☐')
        set_cell(ws_frente, 'T10', '◼' if s_comissionamento else '☐')
        set_cell(ws_frente, 'AG10', '◼' if s_startup else '☐')
        set_cell(ws_frente, 'AP10', '◼' if s_operacao else '☐')
        
        set_cell(ws_frente, 'E11', '◼' if s_assistencia else '☐')
        set_cell(ws_frente, 'T11', '◼' if s_contrato else '☐')
        set_cell(ws_frente, 'AG11', '◼' if s_outro else '☐')
        set_cell(ws_frente, 'AP11', '◼' if s_periculosidade else '☐')
        
        # --- SEGUNDA PÁGINA (RELATÓRIO DE SERVIÇOS EXECUTADOS) ---
        # Verifique se o nome da aba da segunda página no seu excel é exatamente esse ou ajuste abaixo:
        nome_aba_verso = 'Verso - Relatório de SC - 2' # Caso seja diferente, me avise o nome exato da aba no Excel
        if nome_aba_verso in wb.sheetnames:
            ws_verso = wb[nome_aba_verso]
            # Aqui definimos a célula de destino do relatório (por padrão vamos jogar na célula onde começa o bloco de texto, ex: 'A5' ou 'B5' dependendo do seu modelo)
            # Vamos ajustar a célula exata conforme o seu layout da segunda página:
            set_cell(ws_verso, 'A5', relatorio_executados)
        
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
                label="📥 Baixar PDF Oficial KTSA",
                data=pdf_bytes,
                file_name="RSC_Oficial.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Erro ao converter o arquivo para PDF.")
    else:
        st.error("Arquivo modelo Excel não encontrado no repositório.")
