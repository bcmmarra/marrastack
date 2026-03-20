import sqlite3

class LeadModel:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def get_all_leads(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                # IMPORTANTE: Isso permite acessar por nome da coluna: lead['email']
                conn.row_factory = sqlite3.Row 
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM leads ORDER BY data_registro DESC')
                return cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"Erro no banco: {e}")
            return []