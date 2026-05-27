from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from repositories import UserRepository
from services import AuthService

bp = Blueprint('auth', __name__)


def _user_repo() -> UserRepository:
    return UserRepository(current_app.config['db'])


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        repo = _user_repo()
        email = request.form['email'].strip().lower()
        if repo.find_by_email(email):
            flash("Cet email est déjà utilisé.", "error")
            return redirect(url_for('auth.register'))
        user = repo.create(
            name=request.form['name'].strip(),
            email=email,
            password=AuthService.hash_password(request.form['password']),
            phone=request.form.get('phone', ''),
            company=request.form.get('company', ''),
        )
        session['user_id'] = user.id
        session['user_name'] = user.name
        flash(f"Bienvenue, {user.name} !", "success")
        return redirect(url_for('main.index'))
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = AuthService.login(
            request.form['email'],
            request.form['password'],
            _user_repo(),
        )
        if not user:
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('auth.login'))
        session['user_id'] = user.id
        session['user_name'] = user.name
        flash(f"Bon retour, {user.name} !", "success")
        return redirect(url_for('main.index'))
    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('main.index'))
