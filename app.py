import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO

st.set_page_config(page_title="Gerador RSC KTSA", page_icon="📝")

st.title("📝 Preenchimento Automático RSC - KTSA")

# 1. Upload do seu Template (arquivo .xlsx original com fórmulas)
uploaded_file = st.file_uploader("Suba o arquivo Template da KTSA (.xlsx)", type=["xlsx"])

# 2. Entrada de dados
texto_servico = st.text_area("Descreva o serviço (ou cole a transcrição do áudio):")

if uploaded_file and texto_servico:
    if st.button("Gerar Relatório Final"):
        # Carrega o template
        wb = openpyxl.load_workbook(uploaded_file)
        ws = wb.active # Ajuste para a aba correta se necessário (ex: wb['Relatorio'])

        # --- A MÁGICA DA IA (Simulada aqui) ---
        # No futuro, aqui chamaremos o Gemini para extrair os dados do texto_servico
        dados_extraidos = {
            "cliente": "Nitro Química", # Exemplo extraído
            "cpm": "08.6581.26",
            "descricao": texto_servico
        }

        # Preenche as células do seu Excel original
        ws['B5'] = dados_extraidos['cliente']
        ws['H5'] = dados_extraidos['cpm']
        ws['C12'] = dados_extraidos['descricao']

        # Salva o arquivo em memória para download
        output = BytesIO()
        wb.save(output)
        
        st.success("Relatório processado com sucesso!")
        st.download_button(
            label="Baixar Excel Preenchido",
            data=output.getvalue(),
            file_name="RSC_Preenchido.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.markdown("---")
st.info("💡 Dica: Suba o arquivo que você salvou como template (sem dados antigos).")
