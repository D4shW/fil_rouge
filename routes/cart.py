from functools import wraps
from flask import (Blueprint, render_template, request, redirect,
                   url_for, flash, session, current_app)
from repositories import ServiceRepository, InterventionRepository

bp = Blueprint('cart', __name__)


def _login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def _service_repo() -> ServiceRepository:
    return ServiceRepository(current_app.config['db'])


def _intervention_repo() -> InterventionRepository:
    return InterventionRepository(current_app.config['db'])


@bp.route('/panier')
def cart():
    cart_items = session.get('cart', [])
    repo = _service_repo()
    items = []
    total = 0.0
    for ci in cart_items:
        service = repo.get_by_id(ci['service_id'])
        if service:
            subtotal = service.price * ci['qty']
            total += subtotal
            items.append({'service': service, 'qty': ci['qty'], 'subtotal': subtotal})
    return render_template('cart.html', items=items, total=total)


@bp.route('/panier/add/<int:service_id>', methods=['POST'])
def add_to_cart(service_id):
    cart = session.get('cart', [])
    existing = next((c for c in cart if c['service_id'] == service_id), None)
    if existing:
        existing['qty'] += 1
    else:
        cart.append({'service_id': service_id, 'qty': 1})
    session['cart'] = cart
    flash("Service ajouté au devis !", "success")
    return redirect(request.referrer or url_for('main.services'))


@bp.route('/panier/remove/<int:service_id>', methods=['POST'])
def remove_from_cart(service_id):
    cart = [c for c in session.get('cart', []) if c['service_id'] != service_id]
    session['cart'] = cart
    flash("Service retiré du devis.", "success")
    return redirect(url_for('cart.cart'))


@bp.route('/demande-intervention', methods=['POST'])
@_login_required
def request_intervention():
    cart = session.get('cart', [])
    if not cart:
        flash("Votre panier est vide.", "warning")
        return redirect(url_for('cart.cart'))
    interv = _intervention_repo().create(
        user_id=session['user_id'],
        cart=cart,
        notes=request.form.get('notes', ''),
    )
    session.pop('cart', None)
    flash(
        f"Demande d'intervention #{interv.id} enregistrée ! Notre équipe vous contactera sous 24h.",
        "success",
    )
    return redirect(url_for('main.index'))


@bp.route('/mes-interventions')
@_login_required
def my_interventions():
    interventions = _intervention_repo().get_by_user(session['user_id'])
    return render_template('interventions.html', interventions=interventions)
