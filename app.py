import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-for-session'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelo da db

class User(UserMixin, db.Model):
    """
    Representa um usuário do sistema.
    Role 'user': Cliente/Usuário Comum (Abre chamados).
    Role 'admin': Técnico/Admin (Resolve chamados).
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False) 
    role = db.Column(db.String(20), nullable=False) 

class ServiceOrder(db.Model):
    """
    Representa uma ordem de serviço ou ticket.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ticket relacionada ao criador
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='my_orders')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_initial_data():
    """Cria o DB e usuários padrão se não existirem."""
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='tech').first():
            print("Criando usuários padrão...")
            
            # TÉCNICO (Admin): Pode ver tudo e mudar status
            tech = User(username='tech', password='tech123', role='admin')
            db.session.add(tech)
            
            # USUÁRIO (Cliente): Pode apenas criar tickets
            user = User(username='user', password='user123', role='user')
            db.session.add(user)
            
            db.session.commit()
            print("Usuários criados com sucesso:")
            print(" - Técnico (Admin): tech / tech123")
            print(" - Usuário (Cliente): user / user123")

# ROTAS 

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # Logica do login
        if user and user.password == password:
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """
    Lógica do Dashboard:
    - Admin (tech) vê TODOS os tickets.
    - User vê APENAS os seus tickets.
    """
    if current_user.role == 'admin':
        orders = ServiceOrder.query.order_by(ServiceOrder.created_at.desc()).all()
    else:
        # O user ve somente (owner_id == current_user.id)
        orders = ServiceOrder.query.filter_by(owner_id=current_user.id).order_by(ServiceOrder.created_at.desc()).all()
            
    return render_template('dashboard.html', orders=orders)

@app.route('/create_order', methods=['POST'])
@login_required
def create_order():
    """
    Qualquer um pode criar, mas o ticket fica vinculado a quem criou.
    """
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title or not description:
        flash('Título e Descrição são obrigatórios.', 'warning')
        return redirect(url_for('dashboard'))

    # setado ao login automaticamente
    new_order = ServiceOrder(
        title=title, 
        description=description,
        owner_id=current_user.id 
    )
    db.session.add(new_order)
    db.session.commit()
    flash('Ticket criado com sucesso.', 'success')

    return redirect(url_for('dashboard'))

@app.route('/update_status/<int:order_id>', methods=['POST'])
@login_required
def update_status(order_id):
    """
    APENAS Admins (Tech) podem mudar o status.
    """
    if current_user.role != 'admin':
        flash("Permissão negada: Apenas técnicos podem mudar o status.", "danger")
        return redirect(url_for('dashboard'))

    order = ServiceOrder.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['Pending', 'In Progress', 'Completed']:
        order.status = new_status
        db.session.commit()
        flash('Status atualizado.', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/delete_order/<int:order_id>')
@login_required
def delete_order(order_id):
    """
    APENAS Admins podem deletar.
    """
    if current_user.role != 'admin':
        abort(403)
        
    order = ServiceOrder.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Ticket excluído.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    create_initial_data()
    app.run(debug=True)