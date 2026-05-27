"""Peuple la base de données avec des données fictives de démonstration."""
import hashlib
import random
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / 'instance' / 'store.db'


def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def random_date(days_back: int = 180) -> str:
    delta = timedelta(days=random.randint(0, days_back),
                      hours=random.randint(8, 18),
                      minutes=random.randint(0, 59))
    return (datetime.now() - delta).strftime('%Y-%m-%d %H:%M:%S')


USERS = [
    ('Alice Martin',    'alice.martin@email.fr',    '06 11 22 33 44', 'Martin SARL'),
    ('Baptiste Dupont', 'baptiste.dupont@email.fr', '06 22 33 44 55', ''),
    ('Clara Leroy',     'clara.leroy@email.fr',     '06 33 44 55 66', 'Leroy & Associés'),
    ('David Bernard',   'david.bernard@email.fr',   '06 44 55 66 77', 'BTP Bernard'),
    ('Émilie Thomas',   'emilie.thomas@email.fr',   '06 55 66 77 88', ''),
    ('François Petit',  'f.petit@email.fr',         '06 66 77 88 99', 'Petit Conseil'),
    ('Gabrielle Roux',  'gabrielle.roux@email.fr',  '06 77 88 99 00', 'Cabinet Roux'),
]

INTERVENTION_STATUSES = ['en attente', 'en cours', 'terminé', 'annulé']

INTERVENTION_NOTES = [
    'PC très lent, possibles virus.',
    'Réseau instable depuis la mise à jour du routeur.',
    'Récupération urgente de données suite à panne disque.',
    'Contrat mensuel — renouvellement automatique.',
    'Nouveau collaborateur à intégrer.',
    'Audit demandé par la direction suite à incident.',
    'Support rapide pour configuration email.',
    'Migration de nos fichiers vers Microsoft 365.',
    'Site vitrine pour lancement de produit en mars.',
    'Panne totale, PC ne démarre plus.',
    'Installation de 3 nouveaux postes en open space.',
    'Mise en place VPN pour télétravail.',
    '',
]

CONTACTS = [
    ('Marc Fontaine',   'marc.fontaine@gmail.com',    '06 10 20 30 40',
     'Demande de devis',      'Bonjour, je souhaite un devis pour la maintenance de 5 postes.', 'nouveau'),
    ('Sophie Mercier',  'sophie.mercier@orange.fr',   '06 20 30 40 50',
     'Problème réseau',       'Mon réseau Wi-Fi ne fonctionne plus depuis hier matin.', 'en cours'),
    ('Jean-Paul Vidal', 'jp.vidal@entreprise.com',    '06 30 40 50 60',
     'Migration cloud',       'Nous envisageons de migrer vers Google Workspace, pouvez-vous nous accompagner ?', 'traité'),
    ('Nathalie Simon',  'nathalie.simon@free.fr',     '06 40 50 60 70',
     'Récupération données',  'J\'ai effacé par erreur des fichiers importants. Est-il possible de les récupérer ?', 'traité'),
    ('Pierre Lambert',  'p.lambert@pme.fr',           '06 50 60 70 80',
     'Devis site web',        'Nous souhaitons créer un site vitrine pour notre cabinet comptable.', 'nouveau'),
    ('Isabelle Girard', 'i.girard@hotmail.com',       '',
     'Virus détecté',         'Mon antivirus signale une menace, je ne sais pas quoi faire.', 'fermé'),
    ('Thomas Richard',  'thomas.richard@sfr.fr',      '06 60 70 80 90',
     'Installation poste',    'Besoin d\'installer et configurer 2 nouveaux ordinateurs pour des stagiaires.', 'en cours'),
    ('Camille Dubois',  'camille.dubois@gmail.com',   '06 70 80 90 01',
     'Contrat maintenance',   'Quelles sont vos offres de maintenance mensuelle pour une TPE de 4 personnes ?', 'nouveau'),
    ('Arnaud Moreau',   'arnaud.moreau@yahoo.fr',     '06 80 90 01 12',
     'Assistance urgente',    'Panne informatique totale ce matin, nous ne pouvons plus travailler.', 'traité'),
    ('Lucie Garnier',   'lucie.garnier@laposte.net',  '06 90 01 12 23',
     'Sécurité réseau',       'Nous avons eu un incident de sécurité la semaine dernière, besoin d\'un audit.', 'en cours'),
    ('Éric Blanchard',  'eric.blanchard@pme.fr',      '',
     'Renseignement VPN',     'Nous passons au télétravail, comment mettre en place un VPN sécurisé ?', 'fermé'),
    ('Martine Chevalier','m.chevalier@gmail.com',     '07 01 12 23 34',
     'Création site',         'Bonjour, budget autour de 1000€ pour un site vitrine. Est-ce possible ?', 'nouveau'),
]


def seed(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON")

    # ── Récupère les IDs des services existants ──────────────────────────────
    service_ids = [r[0] for r in conn.execute("SELECT id FROM services ORDER BY id").fetchall()]
    if not service_ids:
        print("ERREUR : la table services est vide. Lancez l'application une fois pour initialiser le schéma.")
        sys.exit(1)

    # ── Utilisateurs ─────────────────────────────────────────────────────────
    existing_emails = {r[0] for r in conn.execute("SELECT email FROM users").fetchall()}
    user_ids = []
    for name, email, phone, company in USERS:
        if email in existing_emails:
            uid = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()[0]
        else:
            cur = conn.execute(
                "INSERT INTO users (name, email, phone, company, password, created) VALUES (?,?,?,?,?,?)",
                (name, email, phone, company, hash_pw('Password1!'), random_date(365)),
            )
            uid = cur.lastrowid
        user_ids.append(uid)
    print(f"  {len(user_ids)} utilisateurs prêts.")

    # ── Interventions ─────────────────────────────────────────────────────────
    existing_count = conn.execute("SELECT COUNT(*) FROM interventions").fetchone()[0]
    if existing_count == 0:
        weights = [2, 3, 4, 1]  # en attente, en cours, terminé, annulé
        for _ in range(28):
            user_id = random.choice(user_ids)
            status   = random.choices(INTERVENTION_STATUSES, weights=weights)[0]
            notes    = random.choice(INTERVENTION_NOTES)
            date     = random_date(180)
            cur = conn.execute(
                "INSERT INTO interventions (user_id, status, notes, date) VALUES (?,?,?,?)",
                (user_id, status, notes, date),
            )
            interv_id = cur.lastrowid
            # 1 à 3 services par intervention, sans doublon
            nb_services = random.randint(1, 3)
            chosen = random.sample(service_ids, min(nb_services, len(service_ids)))
            for svc_id in chosen:
                qty = random.randint(1, 4)
                conn.execute(
                    "INSERT INTO intervention_items (intervention_id, service_id, qty) VALUES (?,?,?)",
                    (interv_id, svc_id, qty),
                )
        print(f"  28 interventions créées.")
    else:
        print(f"  {existing_count} interventions déjà présentes — ignorées.")

    # ── Contacts ──────────────────────────────────────────────────────────────
    existing_contact_count = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    if existing_contact_count == 0:
        for name, email, phone, subject, message, status in CONTACTS:
            conn.execute(
                "INSERT INTO contacts (name, email, phone, subject, message, status, date) VALUES (?,?,?,?,?,?,?)",
                (name, email, phone, subject, message, status, random_date(90)),
            )
        print(f"  {len(CONTACTS)} contacts créés.")
    else:
        print(f"  {existing_contact_count} contacts déjà présents — ignorés.")


if __name__ == '__main__':
    if not DB_PATH.exists():
        print(f"Base introuvable : {DB_PATH}")
        print("Lancez d'abord l'application pour initialiser la base, puis relancez ce script.")
        sys.exit(1)

    with sqlite3.connect(DB_PATH) as conn:
        seed(conn)

    print("\nDonnées fictives insérées avec succès.")
    print("Mot de passe de tous les comptes utilisateurs : Password1!")
