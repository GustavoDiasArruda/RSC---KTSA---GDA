import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configuração da sua chave API do Google (pegue no Google AI Studio)
genai.configure(api_key="SUA_CHAVE_API_AQUI")

def processar_relatorio(texto_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Você é um assistente da KTSA. Analise o relato de campo abaixo e extraia:
    Cliente, Data, Numero_CPM, Tecnico, Descricao_Servico, Horas_Totais.
    Formate a resposta estritamente como um JSON.
    Relato: {texto_input}
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- Interface ---
st.title("🤖 KTSA Inteligente: Relatório Automático")
entrada = st.text_area("Descreva o que foi feito (pode ser bagunçado):")

if st.button("Organizar Relatório"):
    resultado_json = processar_relatorio(entrada)
    st.json(resultado_json) # Exibe o que a IA entendeu
    # Aqui você adicionaria o código para salvar no Excel (biblioteca openpyxl)
