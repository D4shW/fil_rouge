from typing import List
from database import Database
from models import Intervention, InterventionItem
from .base_repository import BaseRepository


class InterventionRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    def get_by_user(self, user_id: int) -> List[Intervention]:
        with self._db.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM interventions WHERE user_id = ? ORDER BY date DESC",
                (user_id,),
            ).fetchall()
            interventions = [Intervention.from_row(r) for r in rows]
            for interv in interventions:
                interv.items = self._load_items(conn, interv.id)
        return interventions

    def get_all(self) -> List[Intervention]:
        with self._db.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM interventions ORDER BY date DESC"
            ).fetchall()
            interventions = [Intervention.from_row(r) for r in rows]
            for interv in interventions:
                interv.items = self._load_items(conn, interv.id)
        return interventions

    def create(self, user_id: int, cart: list, notes: str) -> Intervention:
        with self._db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO interventions (user_id, notes) VALUES (?,?)",
                (user_id, notes),
            )
            interv_id = cursor.lastrowid
            conn.executemany(
                "INSERT INTO intervention_items (intervention_id, service_id, qty) VALUES (?,?,?)",
                [(interv_id, item['service_id'], item['qty']) for item in cart],
            )
            row = conn.execute(
                "SELECT * FROM interventions WHERE id = ?", (interv_id,)
            ).fetchone()
            interv = Intervention.from_row(row)
            interv.items = self._load_items(conn, interv_id)
        return interv

    def get_sales_analytics(self) -> dict:
        with self._db.get_connection() as conn:
            revenue_row = conn.execute(
                """SELECT SUM(ii.qty * s.price) as total_revenue
                   FROM intervention_items ii
                   JOIN services s ON ii.service_id = s.id"""
            ).fetchone()
            total_revenue = revenue_row['total_revenue'] if revenue_row and revenue_row['total_revenue'] else 0.0

            status_rows = conn.execute(
                """SELECT status, COUNT(*) as count
                   FROM interventions
                   GROUP BY status"""
            ).fetchall()
            status_distribution = {row['status']: row['count'] for row in status_rows}

            category_rows = conn.execute(
                """SELECT s.category, SUM(ii.qty) as sold_qty, SUM(ii.qty * s.price) as revenue
                   FROM intervention_items ii
                   JOIN services s ON s.id = ii.service_id
                   GROUP BY s.category"""
            ).fetchall()
            category_sales = [dict(row) for row in category_rows]

        return {
            'total_revenue': total_revenue,
            'status_distribution': status_distribution,
            'category_sales': category_sales,
        }

    def _load_items(self, conn, interv_id: int) -> List[InterventionItem]:
        rows = conn.execute(
            """SELECT ii.service_id, ii.qty,
                      s.name AS service_name, s.icon AS service_icon,
                      s.price AS service_price, s.unit AS service_unit
               FROM intervention_items ii
               JOIN services s ON s.id = ii.service_id
               WHERE ii.intervention_id = ?""",
            (interv_id,),
        ).fetchall()
        return [
            InterventionItem(
                service_id=r['service_id'],
                qty=r['qty'],
                service_name=r['service_name'],
                service_icon=r['service_icon'],
                service_price=r['service_price'],
                service_unit=r['service_unit'],
            )
            for r in rows
        ]
