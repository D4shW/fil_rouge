"""
╔═══════════════════════════════════════════════════╗
║   NOVATECH — Réseau d'assistance informatique     ║
║   Backend Flask                                    ║
╚═══════════════════════════════════════════════════╝
"""
import os
import json
import hashlib
import secrets
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify, abort
)

# ─── App Configuration ───────────────────────────────────
_instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
app = Flask(__name__, instance_path=_instance_path)
app.secret_key = secrets.token_hex(32)
app.config['DATABASE'] = os.path.join(app.instance_path, 'store.json')

os.makedirs(app.instance_path, exist_ok=True)


# ─── JSON "Database" Layer ────────────────────────────────
def _load_db():
    db_path = app.config['DATABASE']
    if not os.path.exists(db_path):
        default = {
            "users": [],
            "services": _seed_services(),
            "interventions": [],
            "contacts": [],
            "agences": _seed_agences(),
            "next_id": {"user": 2, "service": 10, "intervention": 1, "contact": 1}
        }
        _save_db(default)
        return default
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_db(db):
    db_path = app.config['DATABASE']
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, default=str, ensure_ascii=False)


def _seed_services():
    return [
        {
            "id": 1, "name": "Dépannage PC & Mac",
            "category": "dépannage",
            "price": 59.00, "unit": "intervention",
            "description": "Diagnostic complet, suppression de virus, résolution de pannes matérielles et logicielles. Intervention sur site ou à distance.",
            "icon": "🔧", "popular": True
        },
        {
            "id": 2, "name": "Installation réseau",
            "category": "réseau",
            "price": 149.00, "unit": "forfait",
            "description": "Configuration réseau complet : box, Wi-Fi, switch, câblage Ethernet. Sécurisation et optimisation du débit.",
            "icon": "🌐", "popular": True
        },
        {
            "id": 3, "name": "Sauvegarde & récupération de données",
            "category": "données",
            "price": 89.00, "unit": "intervention",
            "description": "Mise en place de solutions de sauvegarde automatique. Récupération de données sur disque dur, SSD ou clé USB.",
            "icon": "💾", "popular": False
        },
        {
            "id": 4, "name": "Maintenance préventive",
            "category": "maintenance",
            "price": 39.00, "unit": "mois",
            "description": "Contrat de maintenance mensuel : mises à jour, nettoyage, monitoring, support prioritaire par téléphone et email.",
            "icon": "🛡️", "popular": True
        },
        {
            "id": 5, "name": "Installation poste de travail",
            "category": "installation",
            "price": 79.00, "unit": "poste",
            "description": "Installation et configuration complète : OS, drivers, suite bureautique, antivirus, imprimante, comptes email.",
            "icon": "🖥️", "popular": False
        },
        {
            "id": 6, "name": "Sécurité informatique",
            "category": "sécurité",
            "price": 199.00, "unit": "forfait",
            "description": "Audit de sécurité, installation pare-feu, antivirus pro, VPN, politique de mots de passe, sensibilisation des équipes.",
            "icon": "🔒", "popular": True
        },
        {
            "id": 7, "name": "Assistance à distance",
            "category": "dépannage",
            "price": 35.00, "unit": "30 min",
            "description": "Prise en main à distance pour résoudre rapidement les problèmes courants : configuration, bugs, lenteurs.",
            "icon": "📡", "popular": False
        },
        {
            "id": 8, "name": "Migration Cloud",
            "category": "cloud",
            "price": 299.00, "unit": "forfait",
            "description": "Migration de vos données et services vers le Cloud (Microsoft 365, Google Workspace, AWS). Formation incluse.",
            "icon": "☁️", "popular": False
        },
        {
            "id": 9, "name": "Création site web vitrine",
            "category": "développement",
            "price": 890.00, "unit": "projet",
            "description": "Site web professionnel responsive, optimisé SEO. Hébergement et nom de domaine inclus la première année.",
            "icon": "🌍", "popular": False
        },
    ]


def _seed_agences():
    return [
        {"id": 1, "name": "Siège — Aix-en-Provence", "address": "45 Cours Mirabeau, 13100 Aix-en-Provence", "phone": "04 42 00 00 01", "is_siege": True},
        {"id": 2, "name": "Agence Marseille", "address": "12 Rue de la République, 13001 Marseille", "phone": "04 91 00 00 02", "is_siege": False},
        {"id": 3, "name": "Agence Lyon", "address": "8 Place Bellecour, 69002 Lyon", "phone": "04 72 00 00 03", "is_siege": False},
        {"id": 4, "name": "Agence Paris", "address": "25 Boulevard Haussmann, 75009 Paris", "phone": "01 42 00 00 04", "is_siege": False},
        {"id": 5, "name": "Agence Toulouse", "address": "3 Place du Capitole, 31000 Toulouse", "phone": "05 61 00 00 05", "is_siege": False},
        {"id": 6, "name": "Agence Bordeaux", "address": "18 Cours de l'Intendance, 33000 Bordeaux", "phone": "05 56 00 00 06", "is_siege": False},
        {"id": 7, "name": "Agence Nantes", "address": "7 Rue Crébillon, 44000 Nantes", "phone": "02 40 00 00 07", "is_siege": False},
        {"id": 8, "name": "Agence Lille", "address": "14 Rue Faidherbe, 59000 Lille", "phone": "03 20 00 00 08", "is_siege": False},
        {"id": 9, "name": "Agence Strasbourg", "address": "5 Place Kléber, 67000 Strasbourg", "phone": "03 88 00 00 09", "is_siege": False},
        {"id": 10, "name": "Agence Nice", "address": "22 Avenue Jean Médecin, 06000 Nice", "phone": "04 93 00 00 10", "is_siege": False},
        {"id": 11, "name": "Agence Montpellier", "address": "9 Place de la Comédie, 34000 Montpellier", "phone": "04 67 00 00 11", "is_siege": False},
        {"id": 12, "name": "Agence Rennes", "address": "11 Rue Le Bastard, 35000 Rennes", "phone": "02 99 00 00 12", "is_siege": False},
        {"id": 13, "name": "Agence Grenoble", "address": "6 Place Victor Hugo, 38000 Grenoble", "phone": "04 76 00 00 13", "is_siege": False},
    ]


def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ─── Auth Decorator ───────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════
#  PAGE ROUTES
# ═══════════════════════════════════════════════════════════

@app.route('/')
def index():
    db = _load_db()
    popular = [s for s in db['services'] if s.get('popular')]
    return render_template('index.html', services=popular, agences=db['agences'])


@app.route('/services')
def services():
    db = _load_db()
    category = request.args.get('category', 'all')
    if category != 'all':
        items = [s for s in db['services'] if s['category'] == category]
    else:
        items = db['services']
    categories = sorted(set(s['category'] for s in db['services']))
    return render_template('services.html', services=items,
                           categories=categories, current_cat=category)


@app.route('/service/<int:service_id>')
def service_detail(service_id):
    db = _load_db()
    service = next((s for s in db['services'] if s['id'] == service_id), None)
    if not service:
        abort(404)
    return render_template('service.html', service=service)


@app.route('/agences')
def agences():
    db = _load_db()
    return render_template('agences.html', agences=db['agences'])


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        db = _load_db()
        msg = {
            "id": db['next_id']['contact'],
            "name": request.form['name'],
            "email": request.form['email'],
            "phone": request.form.get('phone', ''),
            "subject": request.form.get('subject', ''),
            "message": request.form['message'],
            "date": datetime.now().isoformat()
        }
        db['contacts'].append(msg)
        db['next_id']['contact'] += 1
        _save_db(db)
        flash("Message envoyé avec succès ! Nous reviendrons vers vous sous 24h.", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')


# ═══════════════════════════════════════════════════════════
#  AUTHENTICATION
# ═══════════════════════════════════════════════════════════

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = _load_db()
        email = request.form['email'].strip().lower()
        if any(u['email'] == email for u in db['users']):
            flash("Cet email est déjà utilisé.", "error")
            return redirect(url_for('register'))
        user = {
            "id": db['next_id']['user'],
            "name": request.form['name'].strip(),
            "email": email,
            "phone": request.form.get('phone', ''),
            "company": request.form.get('company', ''),
            "password": _hash_password(request.form['password']),
            "created": datetime.now().isoformat()
        }
        db['users'].append(user)
        db['next_id']['user'] += 1
        _save_db(db)
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        flash(f"Bienvenue, {user['name']} !", "success")
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = _load_db()
        email = request.form['email'].strip().lower()
        pw_hash = _hash_password(request.form['password'])
        user = next((u for u in db['users']
                      if u['email'] == email and u['password'] == pw_hash), None)
        if not user:
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('login'))
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        flash(f"Bon retour, {user['name']} !", "success")
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('index'))


# ═══════════════════════════════════════════════════════════
#  PANIER DE SERVICES (session)
# ═══════════════════════════════════════════════════════════

@app.route('/panier')
def cart():
    cart_items = session.get('cart', [])
    db = _load_db()
    items = []
    total = 0
    for ci in cart_items:
        service = next((s for s in db['services'] if s['id'] == ci['service_id']), None)
        if service:
            subtotal = service['price'] * ci['qty']
            total += subtotal
            items.append({**service, 'qty': ci['qty'], 'subtotal': subtotal})
    return render_template('cart.html', items=items, total=total)


@app.route('/panier/add/<int:service_id>', methods=['POST'])
def add_to_cart(service_id):
    cart = session.get('cart', [])
    existing = next((c for c in cart if c['service_id'] == service_id), None)
    if existing:
        existing['qty'] += 1
    else:
        cart.append({'service_id': service_id, 'qty': 1})
    session['cart'] = cart
    flash("Service ajouté au devis !", "success")
    return redirect(request.referrer or url_for('services'))


@app.route('/panier/remove/<int:service_id>', methods=['POST'])
def remove_from_cart(service_id):
    cart = session.get('cart', [])
    cart = [c for c in cart if c['service_id'] != service_id]
    session['cart'] = cart
    flash("Service retiré du devis.", "success")
    return redirect(url_for('cart'))


@app.route('/demande-intervention', methods=['POST'])
@login_required
def request_intervention():
    cart = session.get('cart', [])
    if not cart:
        flash("Votre panier est vide.", "warning")
        return redirect(url_for('cart'))
    db = _load_db()
    intervention = {
        "id": db['next_id']['intervention'],
        "user_id": session['user_id'],
        "services": cart,
        "date": datetime.now().isoformat(),
        "status": "en attente",
        "notes": request.form.get('notes', '')
    }
    db['interventions'].append(intervention)
    db['next_id']['intervention'] += 1
    _save_db(db)
    session.pop('cart', None)
    flash(f"Demande d'intervention #{intervention['id']} enregistrée ! Notre équipe vous contactera sous 24h.", "success")
    return redirect(url_for('index'))


@app.route('/mes-interventions')
@login_required
def my_interventions():
    db = _load_db()
    user_interventions = [i for i in db['interventions'] if i['user_id'] == session['user_id']]
    # Enrichir avec les noms de services
    for interv in user_interventions:
        interv['service_details'] = []
        for item in interv['services']:
            svc = next((s for s in db['services'] if s['id'] == item['service_id']), None)
            if svc:
                interv['service_details'].append({**svc, 'qty': item['qty']})
    return render_template('interventions.html', interventions=user_interventions)


# ═══════════════════════════════════════════════════════════
#  REST API  —  /api/v1/...
# ═══════════════════════════════════════════════════════════

@app.route('/api/v1/services', methods=['GET'])
def api_services():
    db = _load_db()
    category = request.args.get('category')
    services = db['services']
    if category:
        services = [s for s in services if s['category'] == category]
    return jsonify({"count": len(services), "services": services})


@app.route('/api/v1/services/<int:sid>', methods=['GET'])
def api_service(sid):
    db = _load_db()
    s = next((s for s in db['services'] if s['id'] == sid), None)
    if not s:
        return jsonify({"error": "Service introuvable"}), 404
    return jsonify(s)


@app.route('/api/v1/services', methods=['POST'])
def api_create_service():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Données invalides"}), 400
    db = _load_db()
    service = {
        "id": db['next_id']['service'],
        "name": data['name'],
        "price": float(data.get('price', 0)),
        "unit": data.get('unit', 'intervention'),
        "category": data.get('category', 'autre'),
        "description": data.get('description', ''),
        "icon": data.get('icon', '🔧'),
        "popular": data.get('popular', False)
    }
    db['services'].append(service)
    db['next_id']['service'] += 1
    _save_db(db)
    return jsonify(service), 201


@app.route('/api/v1/services/<int:sid>', methods=['PUT'])
def api_update_service(sid):
    data = request.get_json()
    db = _load_db()
    service = next((s for s in db['services'] if s['id'] == sid), None)
    if not service:
        return jsonify({"error": "Service introuvable"}), 404
    for key in ['name', 'price', 'unit', 'category', 'description', 'icon', 'popular']:
        if key in data:
            service[key] = data[key]
    _save_db(db)
    return jsonify(service)


@app.route('/api/v1/services/<int:sid>', methods=['DELETE'])
def api_delete_service(sid):
    db = _load_db()
    db['services'] = [s for s in db['services'] if s['id'] != sid]
    _save_db(db)
    return jsonify({"message": "Service supprimé"}), 200


@app.route('/api/v1/interventions', methods=['GET'])
def api_interventions():
    db = _load_db()
    return jsonify({"count": len(db['interventions']), "interventions": db['interventions']})


@app.route('/api/v1/agences', methods=['GET'])
def api_agences():
    db = _load_db()
    return jsonify({"count": len(db['agences']), "agences": db['agences']})


@app.route('/api/v1/contacts', methods=['GET'])
def api_contacts():
    db = _load_db()
    return jsonify({"count": len(db['contacts']), "contacts": db['contacts']})


# ─── Error Handlers ──────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# ─── Template Helpers ─────────────────────────────────────
@app.context_processor
def inject_globals():
    cart = session.get('cart', [])
    return {'cart_count': sum(c['qty'] for c in cart)}


# ─── Run ──────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)