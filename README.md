# ⬡ NOVATECH — Réseau d'assistance informatique

Plateforme web pour un réseau de **13 agences d'assistance informatique** en France, avec siège à Aix-en-Provence. Backend **Flask** (Python), frontend HTML/CSS/JS.

## Lancement

```bash
pip install flask
python app.py
```

Ouvrir **http://localhost:5000**

## Structure du projet

```
├── app.py                      # Backend Flask complet
├── instance/
│   └── store.json              # BDD JSON (auto-générée)
├── static/
│   ├── css/style.css           # Design system
│   └── js/main.js              # Interactions front
├── templates/
│   ├── base.html               # Layout (navbar, footer)
│   ├── index.html              # Accueil (hero, stats, services, CTA)
│   ├── services.html           # Catalogue avec filtres par catégorie
│   ├── service.html            # Fiche service détaillée
│   ├── agences.html            # Liste des 13 agences
│   ├── cart.html               # Panier / devis
│   ├── interventions.html      # Suivi des demandes client
│   ├── login.html              # Connexion
│   ├── register.html           # Inscription
│   ├── contact.html            # Formulaire de contact
│   └── 404.html                # Erreur 404
└── README.md
```

## Fonctionnalités

- **Catalogue de 9 services IT** : dépannage, réseau, sécurité, cloud, maintenance, développement...
- **Filtrage par catégorie** : dépannage, réseau, sécurité, cloud, données, installation, développement, maintenance
- **Panier / devis** : ajout de services, calcul du total, notes complémentaires
- **Demandes d'intervention** : soumission et suivi côté client
- **Authentification** : inscription, connexion, sessions
- **Formulaire de contact** : sauvegardé en base
- **13 agences** : siège Aix-en-Provence + 12 agences nationales
- **API REST complète** : CRUD services, interventions, agences, contacts
- **Responsive** : mobile-first, menu burger, grilles adaptatives

## API REST

Base URL : `http://localhost:5000/api/v1`

| Méthode  | Endpoint              | Description             |
|----------|-----------------------|-------------------------|
| GET      | /services             | Lister les services     |
| GET      | /services?category=x  | Filtrer par catégorie   |
| GET      | /services/<id>        | Détail d'un service     |
| POST     | /services             | Créer un service        |
| PUT      | /services/<id>        | Modifier un service     |
| DELETE   | /services/<id>        | Supprimer un service    |
| GET      | /interventions        | Lister les interventions|
| GET      | /agences              | Lister les agences      |
| GET      | /contacts             | Lister les contacts     |

### Exemple — créer un service

```bash
curl -X POST http://localhost:5000/api/v1/services \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Formation cybersécurité",
    "price": 450,
    "unit": "session",
    "category": "sécurité",
    "description": "Formation de 3h pour sensibiliser vos équipes.",
    "icon": "🎓"
  }'
```
