"""Buat tabel database yang didefinisikan di models.py."""

from app import app
from extensions import db


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        print("Database berhasil disiapkan.")
        print("Daftar tabel:")
        for table_name in sorted(db.metadata.tables):
            print(f"- {table_name}")
        print(f"Total tabel: {len(db.metadata.tables)}")
