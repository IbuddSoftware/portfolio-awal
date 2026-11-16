"""Model tabel untuk data portofolio."""

from datetime import datetime, timezone

from extensions import db


def current_time():
    return datetime.now(timezone.utc)


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    headline = db.Column(db.String(180))
    about = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    location = db.Column(db.String(150))
    photo_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    instagram_url = db.Column(db.String(255))
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=current_time,
        onupdate=current_time,
    )


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(80))
    level = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, nullable=False, default=0)


class Education(db.Model):
    __tablename__ = "education"

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(100))
    major = db.Column(db.String(100))
    start_year = db.Column(db.String(30))
    end_year = db.Column(db.String(30))
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, nullable=False, default=0)


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(120))
    experience_type = db.Column(
        db.String(50), nullable=False, default="Organisasi"
    )
    start_period = db.Column(db.String(50))
    end_period = db.Column(db.String(50))
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, nullable=False, default=0)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.Text)
    project_url = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, nullable=False, default=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(
        db.DateTime(timezone=True), default=current_time
    )

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=current_time
    )
