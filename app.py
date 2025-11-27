import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-for-session'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload Config
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelo da db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False) 
    role = db.Column(db.String(20), nullable=False) 

class ServiceOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='Pending') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='my_orders')
    messages = db.relationship('ChatMessage', backref='order', cascade="all, delete-orphan")

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True) # Content can be empty if just sending a file
    attachment = db.Column(db.String(200), nullable=True) # New Attachment field for chat
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_id = db.Column(db.Integer, db.ForeignKey('service_order.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender = db.relationship('User')

@login_manager.user_loader
def load_user(user_id):
    # Solves the issue where resetting DB keeps browser cookie active but invalid
    try:
        return User.query.get(int(user_id))
    except:
        return None

def create_initial_data():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='tech').first():
            print("Criando usuários padrão...")
            tech = User(username='tech', password='tech123', role='admin')
            db.session.add(tech)
            user = User(username='user', password='user123', role='user')
            db.session.add(user)
            db.session.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    if current_user.role == 'admin':
        orders = ServiceOrder.query.order_by(ServiceOrder.created_at.desc()).all()
    else:
        orders = ServiceOrder.query.filter_by(owner_id=current_user.id).order_by(ServiceOrder.created_at.desc()).all()
            
    return render_template('dashboard.html', orders=orders)

@app.route('/create_order', methods=['POST'])
@login_required
def create_order():
    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')
    file = request.files.get('file')
    
    if not title or not description:
        flash('Título e Descrição são obrigatórios.', 'warning')
        return redirect(url_for('dashboard'))

    filename = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    new_order = ServiceOrder(
        title=title,
        category=category,
        description=description,
        attachment=filename,
        owner_id=current_user.id 
    )
    db.session.add(new_order)
    db.session.commit()
    flash('Ticket criado com sucesso.', 'success')

    return redirect(url_for('dashboard'))

@app.route('/add_message/<int:order_id>', methods=['POST'])
@login_required
def add_message(order_id):
    content = request.form.get('content')
    file = request.files.get('chat_file')

    if not content and not file:
        return redirect(url_for('dashboard'))

    filename = None
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    msg = ChatMessage(
        content=content if content else "", 
        attachment=filename,
        order_id=order_id, 
        sender_id=current_user.id
    )
    db.session.add(msg)
    db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/update_status/<int:order_id>', methods=['POST'])
@login_required
def update_status(order_id):
    if current_user.role != 'admin':
        flash("Permissão negada.", "danger")
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
    if current_user.role != 'admin':
        abort(403)
    order = ServiceOrder.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    create_initial_data()