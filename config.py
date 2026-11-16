"""Konfigurasi aplikasi dan koneksi PostgreSQL."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine import make_url


BASE_DIR = Path(__file__).resolve().parent

# Pada komputer lokal, konfigurasi dibaca dari .env.
# Environment variable dari hosting tetap diprioritaskan.
load_dotenv(BASE_DIR / ".env", override=False)


def get_database_url() -> str:
    """Ambil dan validasi URL PostgreSQL dari environment."""
    database_url = os.getenv("DATABASE_URL", "").strip()
    database_url = database_url.strip('"').strip("'")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL tidak ditemukan. Buat file .env "
            "atau atur environment variable DATABASE_URL."
        )

    # Gunakan driver psycopg 3.
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://", "postgresql+psycopg://", 1
        )
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )

    try:
        parsed_url = make_url(database_url)
    except Exception as error:
        raise RuntimeError(
            "Format DATABASE_URL tidak valid. Salin kembali "
            "Connection String dari dashboard Neon."
        ) from error

    if parsed_url.drivername not in {
        "postgresql+psycopg",
        "postgresql",
        "postgres",
    }:
        raise RuntimeError("DATABASE_URL harus menggunakan PostgreSQL.")

    if not parsed_url.host or not parsed_url.database or not parsed_url.username:
        raise RuntimeError(
            "DATABASE_URL belum lengkap: host, database, atau username tidak ada."
        )

    return database_url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.getenv("COOKIE_SECURE", "false").lower() == "true"
    )
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY tidak ditemukan. "
            "Tambahkan SECRET_KEY ke file .env."
        )

    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 3,
        "max_overflow": 2,
    }

    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
