import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

class DatabaseClient:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL not set in .env")
        self.engine = create_engine(db_url)

    def execute_query(self, query: str, params: dict = None):
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            if query.strip().upper().startswith("SELECT"):
                rows = result.fetchall()
                if rows:
                    keys = result.keys()
                    return [dict(zip(keys, row)) for row in rows]
                return []
            conn.commit()
            return result.rowcount

    def get_user_by_email(self, email: str):
        rows = self.execute_query("SELECT * FROM users WHERE email = :email", {"email": email})
        return rows[0] if rows else None

    def get_business_by_name(self, name: str):
        rows = self.execute_query("SELECT * FROM businesses WHERE name = :name", {"name": name})
        return rows[0] if rows else None

    def get_resource_by_name(self, name: str):
        rows = self.execute_query("SELECT * FROM resources WHERE name = :name", {"name": name})
        return rows[0] if rows else None

    def get_reservation_by_resource_and_date(self, resource_id: int, date: str):
        rows = self.execute_query(
            "SELECT * FROM reservations WHERE resource_id = :resource_id AND reservation_date = :date",
            {"resource_id": resource_id, "date": date}
        )
        return rows[0] if rows else None

