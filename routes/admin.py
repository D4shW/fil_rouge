from flask import (Blueprint, render_template, request, redirect,
                   url_for, flash, session, current_app, abort)
from config import Config
from repositories import ContactRepository
from repositories.contact_repository import VALID_STATUSES
from repositories.intervention_repository import InterventionRepository

bp = Blueprint('admin', __name__, url_prefix='/admin')


def _contact_repo() -> ContactRepository:
    return ContactRepository(current_app.config['db'])


def _inv_repo() -> InterventionRepository:
    return InterventionRepository(current_app.config['db'])


def _require_admin():
    if not session.get('is_admin'):
        return redirect(url_for('admin.login'))


@bp.route('/')
def index():
    if not session.get('is_admin'):
        return redirect(url_for('admin.login'))
    contacts = _contact_repo().get_all()
    return render_template('admin/contacts.html', contacts=contacts,
                           statuses=VALID_STATUSES)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('is_admin'):
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        if request.form.get('password') == Config.ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin.index'))
        flash("Mot de passe incorrect.", "error")
    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin.login'))


@bp.route('/dashboard')
def dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('admin.login'))
    analytics = _inv_repo().get_sales_analytics()
    return render_template('admin/dashboard.html', analytics=analytics)


@bp.route('/contact/<int:contact_id>/status', methods=['POST'])
def update_status(contact_id):
    if not session.get('is_admin'):
        abort(403)
    status = request.form.get('status', '')
    result = _contact_repo().update_status(contact_id, status)
    if not result:
        flash("Statut invalide ou contact introuvable.", "error")
    return redirect(url_for('admin.index'))
