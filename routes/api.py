from flask import Blueprint, request, jsonify, current_app
from repositories import (ServiceRepository, InterventionRepository,
                           AgenceRepository, ContactRepository)

bp = Blueprint('api', __name__, url_prefix='/api/v1')


def _svc_repo() -> ServiceRepository:
    return ServiceRepository(current_app.config['db'])


def _inv_repo() -> InterventionRepository:
    return InterventionRepository(current_app.config['db'])


def _agc_repo() -> AgenceRepository:
    return AgenceRepository(current_app.config['db'])


def _cnt_repo() -> ContactRepository:
    return ContactRepository(current_app.config['db'])


@bp.route('/services', methods=['GET'])
def api_services():
    repo = _svc_repo()
    category = request.args.get('category')
    items = repo.get_by_category(category) if category else repo.get_all()
    return jsonify({'count': len(items), 'services': [s.to_dict() for s in items]})


@bp.route('/services/<int:sid>', methods=['GET'])
def api_service(sid):
    service = _svc_repo().get_by_id(sid)
    if not service:
        return jsonify({'error': 'Service introuvable'}), 404
    return jsonify(service.to_dict())


@bp.route('/services', methods=['POST'])
def api_create_service():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Données invalides'}), 400
    service = _svc_repo().create(
        name=data['name'],
        category=data.get('category', 'autre'),
        price=float(data.get('price', 0)),
        unit=data.get('unit', 'intervention'),
        description=data.get('description', ''),
        icon=data.get('icon', '🔧'),
        popular=bool(data.get('popular', False)),
    )
    return jsonify(service.to_dict()), 201


@bp.route('/services/<int:sid>', methods=['PUT'])
def api_update_service(sid):
    data = request.get_json() or {}
    service = _svc_repo().update(sid, **data)
    if not service:
        return jsonify({'error': 'Service introuvable'}), 404
    return jsonify(service.to_dict())


@bp.route('/services/<int:sid>', methods=['DELETE'])
def api_delete_service(sid):
    _svc_repo().delete(sid)
    return jsonify({'message': 'Service supprimé'})


@bp.route('/interventions', methods=['GET'])
def api_interventions():
    items = _inv_repo().get_all()
    return jsonify({'count': len(items), 'interventions': [i.to_dict() for i in items]})


@bp.route('/agences', methods=['GET'])
def api_agences():
    items = _agc_repo().get_all()
    return jsonify({'count': len(items), 'agences': [a.to_dict() for a in items]})


@bp.route('/contacts', methods=['GET'])
def api_contacts():
    items = _cnt_repo().get_all()
    return jsonify({'count': len(items), 'contacts': [c.to_dict() for c in items]})
