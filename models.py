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
    def __init__(self):
        # Caminho base a partir da raiz do projeto
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.pasta_modelos = os.path.join(self.base_path, 'static', 'modelos', 'modelosPadrao')
        self.pasta_saida = os.path.join(self.base_path, 'documentos_gerados')

    def gerar_lote(self, caminho_excel):
        import pandas as pd
        df = pd.read_excel(caminho_excel).fillna('N/A')
        df_limpo = df[df['NOME_DO_MODELO'] != 'N/A']
        
        arquivos_criados = []
        os.makedirs(self.pasta_saida, exist_ok=True)

        for dados in df_limpo.to_dict('records'):
            try:
                # Monta o caminho completo do template
                template_nome = dados['NOME_DO_MODELO']
                caminho_template = os.path.join(self.base_path, 'static', 'modelos', template_nome)
                # DEBUG: Verifique se este caminho aparece correto no seu terminal
                print(f"--- Tentando abrir: {caminho_template}")
                
                if not os.path.exists(caminho_template):
                    print(f"⚠️ ARQUIVO NÃO ENCONTRADO: {template_nome}")
                    continue

                doc = DocxTemplate(caminho_template)
                doc.render(dados)
                
                # Nome do arquivo de saída
                nome_f = f"{dados['DOCUMENTO']}_{dados['CLIENTE']}.docx".replace(" ", "_")
                caminho_final = os.path.join(self.pasta_saida, nome_f)
                
                doc.save(caminho_final)
                arquivos_criados.append(nome_f)
            except Exception as e:
                print(f"❌ Erro ao processar {dados.get('CLIENTE')}: {e}")
                
        return arquivos_criados
        
    def gerar_unico(self, dados):
        try:
            # 1. Pega o nome do modelo (ex: "CARTA_PROPOSTA.docx")
            template_nome = dados.get('NOME_DO_MODELO')
            caminho_template = os.path.join(self.pasta_modelos, template_nome)
            
            doc = DocxTemplate(caminho_template)
            doc.render(dados)
            
            # 2. Remove a extensão .docx do nome original para criar o nome de saída
            # Ex: "CARTA_PROPOSTA.docx" vira "CARTA_PROPOSTA"
            nome_base = template_nome.replace('.docx', '')
            
            # 3. Opcional: Adicionar um timestamp ou o nome do cliente se existir 
            # para não sobrescrever arquivos caso você gere vários seguidos.
            cliente = dados.get('CLIENTE', '').replace(" ", "_")
            if cliente:
                nome_f = f"{nome_base}_{cliente}.docx"
            else:
                nome_f = f"{nome_base}_GERADO.docx"
                
            caminho_final = os.path.join(self.pasta_saida, nome_f)
            
            doc.save(caminho_final)
            print(f"✅ Arquivo gerado com sucesso: {nome_f}")
            return [nome_f]
            
        except Exception as e:
            print(f"❌ Erro no preenchimento manual: {e}")
            return []
            
    def extrair_campos(self, nome_modelo):
        try:
            caminho = os.path.join(self.pasta_modelos, nome_modelo)
            doc = DocxTemplate(caminho)
            
            # O método get_undeclared_template_variables() é o segredo!
            campos = doc.get_undeclared_template_variables()
            
            # Filtramos para evitar comandos internos do Jinja (como 'if', 'for')
            filtros = ['if', 'else', 'endif', 'for', 'in', 'endfor']
            campos_limpos = [c for c in campos if c not in filtros]
            
            return sorted(campos_limpos)
        except Exception as e:
            print(f"Erro ao extrair campos: {e}")
            return []
    
    def listar_modelos(self):
        try:
            # Lista apenas arquivos que terminam com .docx na pasta correta
            arquivos = [f for f in os.listdir(self.pasta_modelos) if f.endswith('.docx')]
            return sorted(arquivos)
        except Exception as e:
            print(f"Erro ao listar modelos: {e}")
            return []