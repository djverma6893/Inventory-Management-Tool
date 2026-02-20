from database_mongodb_api import DatabaseManager

db = DatabaseManager()

print(db.fetch_all_records())