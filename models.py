import sqlite3
from docxtpl import DocxTemplate
import pandas as pd
import os
import re

class LeadModel:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def get_all_leads(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                # IMPORTANTE: Isso permite acessar por nome da coluna: lead['email']
                conn.row_factory = sqlite3.Row 
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM leads ORDER BY data_registro DESC')
                return cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"Erro no banco: {e}")
            return []

class DocumentService:
    def gerar_lote(self, caminho_excel):
        # Lógica de limpeza e leitura do seu script
        df = pd.read_excel(caminho_excel).fillna('N/A')
        
        # Filtra apenas linhas que têm um modelo definido
        df_limpo = df[df['NOME_DO_MODELO'] != 'N/A']
        
        arquivos_criados = []
        
        for dados in df_limpo.to_dict('records'):
            try:
                # Busca o modelo na pasta static
                template_path = os.path.join('static', 'modelos', 'modelosPadrao', dados['NOME_DO_MODELO'])
                doc = DocxTemplate(template_path)
                
                # O seu 'context' é o próprio dicionário da linha
                doc.render(dados)
                
                # Nome do arquivo (Documento_Cliente.docx)
                nome_formatado = f"{dados['DOCUMENTO']}_{dados['CLIENTE']}.docx".replace(" ", "_")
                caminho_saida = os.path.join('documentos_gerados', nome_formatado)
                
                doc.save(caminho_saida)
                arquivos_criados.append(nome_formatado)
            except Exception as e:
                print(f"Erro no registro {dados.get('CLIENTE')}: {e}")
                
        return arquivos_criados