
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tattoo_secret_key_2024')

# Configure database URI - use SQLite by default if DATABASE_URL is not set
database_url = os.getenv('DATABASE_URL')
if database_url is None or database_url.strip() == '':
    database_url = 'sqlite:///tattoo_finance.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_timeout': 20,
    'max_overflow': 0
}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def get_id(self):
        return str(self.id)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'ingreso', 'gasto', 'mixto'
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    income_percentage = db.Column(db.Integer, default=0)  # Para tipo mixto
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category = db.relationship('Category', backref='transactions')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
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
        
        if username == 'tito' and password == 'titotito':
            user = User.query.filter_by(username='tito').first()
            if not user:
                # Create user if doesn't exist
                user = User(username='tito', password_hash=generate_password_hash('titotito'))
                db.session.add(user)
                db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales inválidas', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/transactions')
@login_required
def transactions():
    categories = Category.query.all()
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(20).all()
    return render_template('transactions.html', categories=categories, recent_transactions=recent_transactions)

@app.route('/api/dashboard_data')
@login_required
def dashboard_data():
    filter_type = request.args.get('filter', 'month')
    
    if filter_type == 'day':
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)
    elif filter_type == 'month':
        start_date = datetime.now().replace(day=1).date()
        end_date = (start_date + timedelta(days=32)).replace(day=1)
    elif filter_type == 'year':
        start_date = datetime.now().replace(month=1, day=1).date()
        end_date = datetime.now().replace(month=12, day=31).date()
    else:
        start_date = datetime.now().replace(month=1, day=1).date()
        end_date = datetime.now().replace(month=12, day=31).date()
    
    transactions = Transaction.query.filter(
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).all()
    
    total_income = 0
    total_expense = 0
    expense_by_category = {}
    
    for transaction in transactions:
        amount = float(transaction.amount)
        
        if transaction.type == 'ingreso':
            total_income += amount
        elif transaction.type == 'gasto':
            total_expense += amount
            category_name = transaction.category.name
            expense_by_category[category_name] = expense_by_category.get(category_name, 0) + amount
        elif transaction.type == 'mixto':
            income_amount = amount * (transaction.income_percentage / 100)
            expense_amount = amount * ((100 - transaction.income_percentage) / 100)
            total_income += income_amount
            total_expense += expense_amount
            category_name = transaction.category.name
            expense_by_category[category_name] = expense_by_category.get(category_name, 0) + expense_amount
    
    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': total_income - total_expense,
        'expense_by_category': expense_by_category
    })

@app.route('/api/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    try:
        data = request.get_json()
        
        transaction = Transaction(
            type=data['type'],
            amount=data['amount'],
            description=data['description'],
            category_id=data['category_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            income_percentage=data.get('income_percentage', 0)
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Transacción agregada exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/add_category', methods=['POST'])
@login_required
def add_category():
    try:
        data = request.get_json()
        
        category = Category(name=data['name'])
        db.session.add(category)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Categoría creada exitosamente', 'category': {'id': category.id, 'name': category.name}})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/get_categories')
@login_required
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])

def init_database():
    """Initialize database with required data"""
    try:
        # Create tables
        db.create_all()
        
        # Create initial categories if they don't exist
        default_categories = [
            'Tatuajes', 'Piercings', 'Productos', 'Servicios', 
            'Alquiler', 'Suministros', 'Marketing', 'Mantenimiento', 'Otros'
        ]
        
        existing_categories = {c.name for c in Category.query.all()}
        new_categories = [Category(name=cat) for cat in default_categories 
                         if cat not in existing_categories]
        
        if new_categories:
            db.session.add_all(new_categories)
        
        # Create admin user if doesn't exist
        if not User.query.filter_by(username='tito').first():
            admin = User(username='tito', password_hash=generate_password_hash('titotito'))
            db.session.add(admin)
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"Database initialization error: {e}")

# Initialize database when app starts
with app.app_context():
    init_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
