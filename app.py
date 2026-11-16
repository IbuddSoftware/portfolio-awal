
import secrets
from pathlib import Path
from functools import wraps

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort
)

from sqlalchemy import text
from werkzeug.security import check_password_hash

from config import Config
from extensions import db

from models import (
    Profile,
    Skill,
    Education,
    Experience,
    Project,
    Admin
)


# =====================================
# KONFIGURASI APLIKASI
# =====================================

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

app.config.from_object(Config)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False
)

db.init_app(app)


# =====================================
# DEKORATOR PERLINDUNGAN ADMIN
# =====================================

def admin_required(view_function):

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        admin_id = session.get("admin_id")

        if not admin_id:
            return redirect(url_for("admin_login"))

        admin = db.session.get(Admin, admin_id)

        if not admin:
            session.clear()
            return redirect(url_for("admin_login"))

        return view_function(*args, **kwargs)

    return wrapped_view


# =====================================
# TOKEN PERLINDUNGAN FORMULIR (CSRF)
# =====================================

@app.context_processor
def inject_csrf_token():

    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)

    return {
        "csrf_token": session["csrf_token"]
    }


def validate_csrf():

    submitted_token = request.form.get("csrf_token", "")
    saved_token = session.get("csrf_token", "")

    return bool(saved_token) and secrets.compare_digest(
        submitted_token,
        saved_token
    )


# =====================================
# HALAMAN UTAMA PORTOFOLIO
# =====================================

@app.route("/")
def home():

    profile = Profile.query.first()

    skills = Skill.query.order_by(
        Skill.sort_order.asc(),
        Skill.id.asc()
    ).all()

    education = Education.query.order_by(
        Education.sort_order.asc(),
        Education.id.asc()
    ).all()

    experiences = Experience.query.order_by(
        Experience.sort_order.asc(),
        Experience.id.asc()
    ).all()

    projects = Project.query.order_by(
        Project.is_featured.desc(),
        Project.sort_order.asc(),
        Project.id.desc()
    ).all()

    return render_template(
        "index.html",
        profile=profile,
        skills=skills,
        education=education,
        experiences=experiences,
        projects=projects
    )


# =====================================
# LOGIN ADMIN
# =====================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if session.get("admin_id"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = Admin.query.filter_by(
            username=username
        ).first()

        if admin and check_password_hash(
            admin.password_hash,
            password
        ):

            session.clear()
            session["admin_id"] = admin.id

            flash(
                "Login berhasil. Selamat datang!",
                "success"
            )

            return redirect(url_for("admin_dashboard"))

        flash(
            "Username atau password salah.",
            "error"
        )

    return render_template("admin/login.html")


# =====================================
# DASHBOARD ADMIN
# =====================================

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():

    admin = db.session.get(
        Admin,
        session["admin_id"]
    )

    total_skills = Skill.query.count()
    total_education = Education.query.count()
    total_experiences = Experience.query.count()
    total_projects = Project.query.count()

    return render_template(
        "admin/dashboard.html",
        admin=admin,
        total_skills=total_skills,
        total_education=total_education,
        total_experiences=total_experiences,
        total_projects=total_projects
    )


# =====================================
# DAFTAR PROYEK
# =====================================

@app.route("/admin/projects")
@admin_required
def admin_projects():

    projects = Project.query.order_by(
        Project.sort_order.asc(),
        Project.id.desc()
    ).all()

    return render_template(
        "admin/projects.html",
        projects=projects
    )


# =====================================
# TAMBAH PROYEK
# =====================================

@app.route("/admin/projects/new", methods=["GET", "POST"])
@admin_required
def admin_project_new():

    if request.method == "POST":

        if not validate_csrf():
            abort(400, description="Token formulir tidak valid.")

        title = request.form.get("title", "").strip()

        if not title:
            flash("Judul proyek wajib diisi.", "error")
            return redirect(url_for("admin_project_new"))

        try:

            project = Project(
                title=title,
                description=request.form.get(
                    "description", ""
                ).strip(),
                technologies=request.form.get(
                    "technologies", ""
                ).strip(),
                project_url=request.form.get(
                    "project_url", ""
                ).strip(),
                image_url=request.form.get(
                    "image_url", ""
                ).strip(),
                is_featured=request.form.get(
                    "is_featured"
                ) == "on",
                sort_order=int(
                    request.form.get("sort_order") or 0
                )
            )

            db.session.add(project)
            db.session.commit()

            flash(
                "Proyek berhasil ditambahkan.",
                "success"
            )

            return redirect(url_for("admin_projects"))

        except (ValueError, Exception):
            db.session.rollback()

            flash(
                "Gagal menyimpan proyek. Periksa kembali data.",
                "error"
            )

    return render_template(
        "admin/project_form.html",
        project=None,
        page_title="Tambah Proyek"
    )


# =====================================
# EDIT PROYEK
# =====================================

@app.route(
    "/admin/projects/<int:project_id>/edit",
    methods=["GET", "POST"]
)
@admin_required
def admin_project_edit(project_id):

    project = db.session.get(Project, project_id)

    if not project:
        abort(404)

    if request.method == "POST":

        if not validate_csrf():
            abort(400, description="Token formulir tidak valid.")

        title = request.form.get("title", "").strip()

        if not title:
            flash("Judul proyek wajib diisi.", "error")

            return redirect(
                url_for(
                    "admin_project_edit",
                    project_id=project.id
                )
            )

        try:

            project.title = title

            project.description = request.form.get(
                "description", ""
            ).strip()

            project.technologies = request.form.get(
                "technologies", ""
            ).strip()

            project.project_url = request.form.get(
                "project_url", ""
            ).strip()

            project.image_url = request.form.get(
                "image_url", ""
            ).strip()

            project.is_featured = (
                request.form.get("is_featured") == "on"
            )

            project.sort_order = int(
                request.form.get("sort_order") or 0
            )

            db.session.commit()

            flash(
                "Proyek berhasil diperbarui.",
                "success"
            )

            return redirect(url_for("admin_projects"))

        except (ValueError, Exception):

            db.session.rollback()

            flash(
                "Gagal memperbarui proyek. Periksa kembali data.",
                "error"
            )

    return render_template(
        "admin/project_form.html",
        project=project,
        page_title="Edit Proyek"
    )


# =====================================
# HAPUS PROYEK
# =====================================

@app.route(
    "/admin/projects/<int:project_id>/delete",
    methods=["POST"]
)
@admin_required
def admin_project_delete(project_id):

    if not validate_csrf():
        abort(400, description="Token formulir tidak valid.")

    project = db.session.get(Project, project_id)

    if not project:
        abort(404)

    try:

        db.session.delete(project)
        db.session.commit()

        flash(
            "Proyek berhasil dihapus.",
            "success"
        )

    except Exception:

        db.session.rollback()

        flash(
            "Gagal menghapus proyek.",
            "error"
        )

    return redirect(url_for("admin_projects"))


# =====================================
# DAFTAR SKILLS
# =====================================

@app.route("/admin/skills")
@admin_required
def admin_skills():

    skills = Skill.query.order_by(
        Skill.sort_order.asc(),
        Skill.id.asc()
    ).all()

    return render_template(
        "admin/skills.html",
        skills=skills
    )


# =====================================
# TAMBAH SKILL
# =====================================

@app.route("/admin/skills/new", methods=["GET", "POST"])
@admin_required
def admin_skill_new():

    if request.method == "POST":

        if not validate_csrf():
            abort(400, description="Token formulir tidak valid.")

        name = request.form.get("name", "").strip()

        if not name:
            flash("Nama keahlian wajib diisi.", "error")
            return redirect(url_for("admin_skill_new"))

        try:
            skill = Skill(
                name=name,
                category=request.form.get("category", "").strip(),
                level=request.form.get("level", "").strip(),
                sort_order=int(request.form.get("sort_order") or 0)
            )

            db.session.add(skill)
            db.session.commit()

            flash("Keahlian berhasil ditambahkan.", "success")
            return redirect(url_for("admin_skills"))

        except Exception:
            db.session.rollback()
            flash("Gagal menambahkan keahlian.", "error")

    return render_template(
        "admin/skill_form.html",
        skill=None,
        page_title="Tambah Keahlian"
    )


# =====================================
# EDIT SKILL
# =====================================

@app.route("/admin/skills/<int:skill_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_skill_edit(skill_id):

    skill = db.session.get(Skill, skill_id)

    if not skill:
        abort(404)

    if request.method == "POST":

        if not validate_csrf():
            abort(400, description="Token formulir tidak valid.")

        name = request.form.get("name", "").strip()

        if not name:
            flash("Nama keahlian wajib diisi.", "error")
            return redirect(
                url_for("admin_skill_edit", skill_id=skill.id)
            )

        try:
            skill.name = name
            skill.category = request.form.get("category", "").strip()
            skill.level = request.form.get("level", "").strip()
            skill.sort_order = int(request.form.get("sort_order") or 0)

            db.session.commit()

            flash("Keahlian berhasil diperbarui.", "success")
            return redirect(url_for("admin_skills"))

        except Exception:
            db.session.rollback()
            flash("Gagal memperbarui keahlian.", "error")

    return render_template(
        "admin/skill_form.html",
        skill=skill,
        page_title="Edit Keahlian"
    )


# =====================================
# HAPUS SKILL
# =====================================

@app.route("/admin/skills/<int:skill_id>/delete", methods=["POST"])
@admin_required
def admin_skill_delete(skill_id):

    if not validate_csrf():
        abort(400, description="Token formulir tidak valid.")

    skill = db.session.get(Skill, skill_id)

    if not skill:
        abort(404)

    try:
        db.session.delete(skill)
        db.session.commit()

        flash("Keahlian berhasil dihapus.", "success")

    except Exception:
        db.session.rollback()
        flash("Gagal menghapus keahlian.", "error")

    return redirect(url_for("admin_skills"))


# =====================================
# DAFTAR PENGALAMAN
# =====================================

@app.route("/admin/experiences")
@admin_required
def admin_experiences():

    experiences = Experience.query.order_by(
        Experience.sort_order.asc(),
        Experience.id.asc()
    ).all()

    return render_template(
        "admin/experiences.html",
        experiences=experiences
    )


# =====================================
# TAMBAH PENGALAMAN
# =====================================

@app.route("/admin/experiences/new", methods=["GET", "POST"])
@admin_required
def admin_experience_new():

    if request.method == "POST":

        if not validate_csrf():
            abort(400, description="Token formulir tidak valid.")

        organization = request.form.get("organization", "").strip()

        if not organization:
            flash("Nama organisasi atau tempat pengalaman wajib diisi.", "error")
            return redirect(url_for("admin_experience_new"))

        try:
            experience = Experience(
                organization=organization,
                position=request.form.get("position", "").strip(),
                experience_type=request.form.get(
                    "experience_type", "Organisasi"
                ).strip(),
                start_period=request.form.get("start_period", "").strip(),
                end_period=request.form.get("end_period", "").strip(),
                description=request.form.get("description", "").strip(),
                sort_order=int(request.form.get("sort_order") or 0)
            )

            db.session.add(experience)
            db.session.commit()

            flash("Pengalaman berhasil ditambahkan.", "success")
            return redirect(url_for("admin_experiences"))

        except Exception:
            db.session.rollback()
            flash("Gagal menambahkan pengalaman. Periksa kembali data.", "error")

    return render_template(
        "admin/experience_form.html",
        experience=None,
        page_title="Tambah Pengalaman"
    )


# =====================================
# EDIT PENGALAMAN
# =====================================

@app.route(
    "/admin/experiences/<int:experience_id>/edit",
    methods=["GET", "POST"]
)
@admin_required
def admin_experience_edit(experience_id):

    experience = db.session.get(Experience, experience_id)

    if not experience:
        abort(404)

    if request.method == "POST":

        if not validate_csrf():
            abort(400, description="Token formulir tidak valid.")

        organization = request.form.get("organization", "").strip()

        if not organization:
            flash("Nama organisasi atau tempat pengalaman wajib diisi.", "error")
            return redirect(
                url_for(
                    "admin_experience_edit",
                    experience_id=experience.id
                )
            )

        try:
            experience.organization = organization
            experience.position = request.form.get("position", "").strip()
            experience.experience_type = request.form.get(
                "experience_type", "Organisasi"
            ).strip()
            experience.start_period = request.form.get(
                "start_period", ""
            ).strip()
            experience.end_period = request.form.get(
                "end_period", ""
            ).strip()
            experience.description = request.form.get(
                "description", ""
            ).strip()
            experience.sort_order = int(
                request.form.get("sort_order") or 0
            )

            db.session.commit()

            flash("Pengalaman berhasil diperbarui.", "success")
            return redirect(url_for("admin_experiences"))

        except Exception:
            db.session.rollback()
            flash("Gagal memperbarui pengalaman. Periksa kembali data.", "error")

    return render_template(
        "admin/experience_form.html",
        experience=experience,
        page_title="Edit Pengalaman"
    )


# =====================================
# HAPUS PENGALAMAN
# =====================================

@app.route(
    "/admin/experiences/<int:experience_id>/delete",
    methods=["POST"]
)
@admin_required
def admin_experience_delete(experience_id):

    if not validate_csrf():
        abort(400, description="Token formulir tidak valid.")

    experience = db.session.get(Experience, experience_id)

    if not experience:
        abort(404)

    try:
        db.session.delete(experience)
        db.session.commit()

        flash("Pengalaman berhasil dihapus.", "success")

    except Exception:
        db.session.rollback()
        flash("Gagal menghapus pengalaman.", "error")

    return redirect(url_for("admin_experiences"))


# =====================================
# KELOLA PROFILE
# =====================================

@app.route("/admin/profile", methods=["GET", "POST"])
@admin_required
def admin_profile():

    profile = Profile.query.first()

    if request.method == "POST":

        if not validate_csrf():
            abort(400, description="Token formulir tidak valid.")

        full_name = request.form.get("full_name", "").strip()

        if not full_name:
            flash("Nama lengkap wajib diisi.", "error")
            return redirect(url_for("admin_profile"))

        try:
            if profile is None:
                profile = Profile(full_name=full_name)
                db.session.add(profile)

            profile.full_name = full_name
            profile.headline = request.form.get("headline", "").strip()
            profile.about = request.form.get("about", "").strip()
            profile.email = request.form.get("email", "").strip()
            profile.phone = request.form.get("phone", "").strip()
            profile.location = request.form.get("location", "").strip()
            profile.photo_url = request.form.get("photo_url", "").strip()
            profile.github_url = request.form.get("github_url", "").strip()
            profile.linkedin_url = request.form.get("linkedin_url", "").strip()
            profile.instagram_url = request.form.get("instagram_url", "").strip()

            db.session.commit()

            flash("Profil berhasil diperbarui.", "success")
            return redirect(url_for("admin_profile"))

        except Exception:
            db.session.rollback()
            flash("Gagal menyimpan profil. Periksa kembali data.", "error")

    return render_template(
        "admin/profile_form.html",
        profile=profile
    )


# =====================================
# LOGOUT ADMIN
# =====================================


@app.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():

    if not validate_csrf():
        abort(400, description="Token formulir tidak valid.")

    session.clear()

    flash("Berhasil logout.", "success")

    return redirect(url_for("admin_login"))


# =====================================
# PEMERIKSAAN APLIKASI
# =====================================

@app.route("/health")
def health():

    try:

        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "success",
            "message": "Aplikasi dan database berjalan."
        }), 200

    except Exception:

        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": "Koneksi database gagal."
        }), 500


# =====================================
# MENJALANKAN APLIKASI
# =====================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
