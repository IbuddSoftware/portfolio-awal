
from getpass import getpass

from app import app
from extensions import db
from models import Admin
from werkzeug.security import generate_password_hash


with app.app_context():
    username = input("Masukkan username admin: ").strip()

    if not username:
        print("Username tidak boleh kosong.")
        raise SystemExit

    if Admin.query.filter_by(username=username).first():
        print("Username sudah digunakan.")
        raise SystemExit

    password = getpass("Masukkan password admin: ")
    confirmation = getpass("Ulangi password: ")

    if len(password) < 8:
        print("Password minimal 8 karakter.")
        raise SystemExit

    if password != confirmation:
        print("Password tidak sama.")
        raise SystemExit

    admin = Admin(
        username=username,
        password_hash=generate_password_hash(password)
    )

    db.session.add(admin)
    db.session.commit()

    print("Akun admin berhasil dibuat.")
