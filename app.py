import os

from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from models import LeadModel
from models import DocumentService


app = Flask(__name__)
app.secret_key = "marra_secret_key" # Para exibir mensagens de feedback

lead_service = LeadModel()
doc_service = DocumentService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('user_email')
    try:
        lead_service.save_lead(email)
        return render_template('sucesso.html', email=email)
    except:
        return render_template('erro.html', email=email)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        senha_digitada = request.form.get('senha')
        if senha_digitada == "marra123":
            session['admin_logado'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('login_admin.html', erro="Senha Incorreta!")
    
    return render_template('login_admin.html')

@app.route('/admin/painel')
def admin_panel():
    # Verificação de segurança: se não houver sessão, volta pro login
    if not session.get('admin_logado'):
        return redirect(url_for('admin_login'))
        
    leads = lead_service.get_all_leads()
    return render_template('admin.html', leads=leads)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logado', None)
    return redirect(url_for('home'))

@app.route('/docs/gerar', methods=['GET', 'POST'])
def view_gerador_docs():
    if request.method == 'POST':
        file = request.files.get('planilha')
        if file:
            # Salva temporariamente
            temp_path = os.path.join('uploads', file.filename)
            file.save(temp_path)
            
            # Chama o Model para processar
            arquivos_criados = doc_service.gerar_lote(temp_path)
            
            return render_template('docs_resultado.html', arquivos=arquivos_criados)
            
    return render_template('docs_home.html')

@app.route('/docs/testar', methods=['POST'])
def testar_gerador():
    file = request.files.get('planilha')
    if file:
        # Salva o Excel na pasta uploads
        caminho_temp = os.path.join('uploads', file.filename)
        file.save(caminho_temp)
        
        # Executa a automação
        resultado = doc_service.gerar_lote(caminho_temp)
        
        return f"✅ Sucesso! {len(resultado)} documentos gerados na pasta /documentos_gerados"
    return "❌ Nenhum arquivo enviado.", 400  
    
    
@app.route('/dashboard/docs')
def docs_dashboard():
    # Rota para exibir a interface de upload
    return render_template('docs/gerador.html')

@app.route('/docs/processar', methods=['POST'])
def processar_docs():
    if 'planilha' not in request.files:
        flash("Nenhum arquivo enviado!", "erro")
        return redirect(url_for('docs_dashboard'))
    
    file = request.files['planilha']
    
    if file.filename == '':
        flash("Selecione um arquivo .xlsx", "erro")
        return redirect(url_for('docs_dashboard'))

    # Salva e Processa
    temp_path = os.path.join('uploads', file.filename)
    file.save(temp_path)
    
    resultado = doc_service.gerar_lote(temp_path)
    print(f"DEBUG: Lista de arquivos gerados: {resultado}")
    
    flash(f"Sucesso! {len(resultado)} documentos gerados.", "sucesso")
    return render_template('docs/resultado.html', arquivos=resultado)

@app.route('/docs/processar_manual', methods=['POST'])
def processar_manual():
    # Pega todos os campos digitados e transforma em dicionário
    dados_digitados = request.form.to_dict()
    
    # Criamos uma lista com esse único dicionário para reaproveitar sua lógica de lote
    # Mas vamos criar uma função específica no Model para um arquivo só
    resultado = doc_service.gerar_unico(dados_digitados)
    
    return render_template('docs/resultado.html', arquivos=resultado)

@app.route('/docs/get_campos/<nome_modelo>')
def get_campos(nome_modelo):
    campos = doc_service.extrair_campos(nome_modelo)
    return {"campos": campos}

@app.route('/docs/manual', strict_slashes=False)
def docs_manual():
    # Esta é a versão automatizada que busca os arquivos na pasta
    lista_modelos = doc_service.listar_modelos()
    return render_template('docs/formulario.html', modelos=lista_modelos)

@app.route('/download/<filename>')
def download_file(filename):
    # Rota para baixar o arquivo gerado
    return send_from_directory('documentos_gerados', filename, as_attachment=True)   




if __name__ == '__main__':
    app.run(debug=True)