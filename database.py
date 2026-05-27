import sqlite3


_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL,
    email    TEXT UNIQUE NOT NULL,
    phone    TEXT NOT NULL DEFAULT '',
    company  TEXT NOT NULL DEFAULT '',
    password TEXT NOT NULL,
    created  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS services (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    price       REAL NOT NULL,
    unit        TEXT NOT NULL DEFAULT 'intervention',
    description TEXT NOT NULL DEFAULT '',
    icon        TEXT NOT NULL DEFAULT '🔧',
    popular     INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS interventions (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date    TEXT NOT NULL DEFAULT (datetime('now')),
    status  TEXT NOT NULL DEFAULT 'en attente',
    notes   TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS intervention_items (
    intervention_id INTEGER NOT NULL REFERENCES interventions(id) ON DELETE CASCADE,
    service_id      INTEGER NOT NULL REFERENCES services(id),
    qty             INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (intervention_id, service_id)
);

CREATE TABLE IF NOT EXISTS agences (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL,
    address  TEXT NOT NULL DEFAULT '',
    phone    TEXT NOT NULL DEFAULT '',
    is_siege INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS contacts (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    email   TEXT NOT NULL,
    phone   TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL DEFAULT '',
    message TEXT NOT NULL DEFAULT '',
    date    TEXT NOT NULL DEFAULT (datetime('now')),
    status  TEXT NOT NULL DEFAULT 'nouveau'
);
"""

_SEED_SERVICES = [
    ('Dépannage PC & Mac', 'dépannage', 59.00, 'intervention',
     'Diagnostic complet, suppression de virus, résolution de pannes matérielles et logicielles. Intervention sur site ou à distance.',
     '🔧', 1),
    ('Installation réseau', 'réseau', 149.00, 'forfait',
     'Configuration réseau complet : box, Wi-Fi, switch, câblage Ethernet. Sécurisation et optimisation du débit.',
     '🌐', 1),
    ('Sauvegarde & récupération de données', 'données', 89.00, 'intervention',
     'Mise en place de solutions de sauvegarde automatique. Récupération de données sur disque dur, SSD ou clé USB.',
     '💾', 0),
    ('Maintenance préventive', 'maintenance', 39.00, 'mois',
     'Contrat de maintenance mensuel : mises à jour, nettoyage, monitoring, support prioritaire par téléphone et email.',
     '🛡️', 1),
    ('Installation poste de travail', 'installation', 79.00, 'poste',
     'Installation et configuration complète : OS, drivers, suite bureautique, antivirus, imprimante, comptes email.',
     '🖥️', 0),
    ('Sécurité informatique', 'sécurité', 199.00, 'forfait',
     'Audit de sécurité, installation pare-feu, antivirus pro, VPN, politique de mots de passe, sensibilisation des équipes.',
     '🔒', 1),
    ('Assistance à distance', 'dépannage', 35.00, '30 min',
     'Prise en main à distance pour résoudre rapidement les problèmes courants : configuration, bugs, lenteurs.',
     '📡', 0),
    ('Migration Cloud', 'cloud', 299.00, 'forfait',
     'Migration de vos données et services vers le Cloud (Microsoft 365, Google Workspace, AWS). Formation incluse.',
     '☁️', 0),
    ('Création site web vitrine', 'développement', 890.00, 'projet',
     'Site web professionnel responsive, optimisé SEO. Hébergement et nom de domaine inclus la première année.',
     '🌍', 0),
]

_SEED_AGENCES = [
    ('Siège — Aix-en-Provence', '45 Cours Mirabeau, 13100 Aix-en-Provence', '04 42 00 00 01', 1),
    ('Agence Marseille', '12 Rue de la République, 13001 Marseille', '04 91 00 00 02', 0),
    ('Agence Lyon', '8 Place Bellecour, 69002 Lyon', '04 72 00 00 03', 0),
    ('Agence Paris', '25 Boulevard Haussmann, 75009 Paris', '01 42 00 00 04', 0),
    ('Agence Toulouse', '3 Place du Capitole, 31000 Toulouse', '05 61 00 00 05', 0),
    ('Agence Bordeaux', '18 Cours de l\'Intendance, 33000 Bordeaux', '05 56 00 00 06', 0),
    ('Agence Nantes', '7 Rue Crébillon, 44000 Nantes', '02 40 00 00 07', 0),
    ('Agence Lille', '14 Rue Faidherbe, 59000 Lille', '03 20 00 00 08', 0),
    ('Agence Strasbourg', '5 Place Kléber, 67000 Strasbourg', '03 88 00 00 09', 0),
    ('Agence Nice', '22 Avenue Jean Médecin, 06000 Nice', '04 93 00 00 10', 0),
    ('Agence Montpellier', '9 Place de la Comédie, 34000 Montpellier', '04 67 00 00 11', 0),
    ('Agence Rennes', '11 Rue Le Bastard, 35000 Rennes', '02 99 00 00 12', 0),
    ('Agence Grenoble', '6 Place Victor Hugo, 38000 Grenoble', '04 76 00 00 13', 0),
]


class Database:
    def __init__(self, path: str):
        self._path = path

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_schema(self) -> None:
        with self.get_connection() as conn:
            conn.executescript(_SCHEMA)
            self._migrate(conn)
            self._seed_if_empty(conn)

    def _migrate(self, conn: sqlite3.Connection) -> None:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(contacts)").fetchall()}
        if 'status' not in cols:
            conn.execute("ALTER TABLE contacts ADD COLUMN status TEXT NOT NULL DEFAULT 'nouveau'")

    def _seed_if_empty(self, conn: sqlite3.Connection) -> None:
        if conn.execute("SELECT COUNT(*) FROM services").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO services (name,category,price,unit,description,icon,popular) VALUES (?,?,?,?,?,?,?)",
                _SEED_SERVICES,
            )
        if conn.execute("SELECT COUNT(*) FROM agences").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO agences (name,address,phone,is_siege) VALUES (?,?,?,?)",
                _SEED_AGENCES,
            )
