from flask import Flask, render_template, request, redirect, url_for, session
from models import LeadModel

app = Flask(__name__)
app.secret_key = 'chave_secreta_marra_stack' # Necessário para usar sessões

lead_service = LeadModel()

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

if __name__ == '__main__':
    app.run(debug=True)