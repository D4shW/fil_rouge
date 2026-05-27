from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from repositories import ServiceRepository, AgenceRepository, ContactRepository

bp = Blueprint('main', __name__)


def _service_repo() -> ServiceRepository:
    return ServiceRepository(current_app.config['db'])


def _agence_repo() -> AgenceRepository:
    return AgenceRepository(current_app.config['db'])


def _contact_repo() -> ContactRepository:
    return ContactRepository(current_app.config['db'])


@bp.route('/')
def index():
    popular = _service_repo().get_popular()
    agences = _agence_repo().get_all()
    return render_template('index.html', services=popular, agences=agences)


@bp.route('/services')
def services():
    repo = _service_repo()
    category = request.args.get('category', 'all')
    items = repo.get_by_category(category) if category != 'all' else repo.get_all()
    categories = repo.get_categories()
    return render_template('services.html', services=items,
                           categories=categories, current_cat=category)


@bp.route('/service/<int:service_id>')
def service_detail(service_id):
    service = _service_repo().get_by_id(service_id)
    if not service:
        abort(404)
    return render_template('service.html', service=service)


@bp.route('/agences')
def agences():
    return render_template('agences.html', agences=_agence_repo().get_all())


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        _contact_repo().create(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form.get('phone', ''),
            subject=request.form.get('subject', ''),
            message=request.form['message'],
        )
        flash("Message envoyé avec succès ! Nous reviendrons vers vous sous 24h.", "success")
        return redirect(url_for('main.contact'))
    return render_template('contact.html')
