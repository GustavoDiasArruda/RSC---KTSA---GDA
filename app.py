# Preenchimento Verso (Linha por Linha nas pautas)
        nome_aba_verso = 'Verso - Relatório de SC - 2'
        if nome_aba_verso in wb.sheetnames:
            ws_verso = wb[nome_aba_verso]
            
            linhas = relatorio_executados.split('\n')
            linha_inicial = 6  # Ajuste se a linha inicial no seu Excel for diferente
            
            for i, texto in enumerate(linhas):
                row_idx = linha_inicial + i
                
                # Limpa as duas colunas primeiro para evitar lixo anterior
                set_cell(ws_verso, f'A{row_idx}', '')
                set_cell(ws_verso, f'B{row_idx}', '')
                
                # Se a linha começar com código padrão (ex: 6.0, 6.3) seguido de espaço ou hífen
                texto_limpo = texto.strip()
                if texto_limpo.startswith("6.") and (" - " in texto_limpo or len(texto_limpo.split()[0]) <= 5):
                    partes = texto_limpo.split(" - ", 1)
                    codigo = partes[0].strip()
                    descricao = partes[1].strip() if len(partes) > 1 else ""
                    
                    set_cell(ws_verso, f'A{row_idx}', codigo)
                    set_cell(ws_verso, f'B{row_idx}', descricao)
                else:
                    # Se não tem código (ex: datas ou continuações), joga direto na coluna B alinhado na pauta
                    set_cell(ws_verso, f'B{row_idx}', texto_limpo)
