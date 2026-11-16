
from app import app
from extensions import db
from models import Profile, Skill, Education, Experience, Project


def seed_data():
    with app.app_context():

        try:
            # ==================================
            # 1. PROFILE
            # ==================================

            profile = Profile.query.first()

            if not profile:
                profile = Profile(
                    full_name="Mohamad Budi Wibowo",
                    headline="Mahasiswa Informatika",
                    about=(
                        "Saya adalah mahasiswa Informatika yang "
                        "tertarik pada teknologi, pemrograman, "
                        "jaringan komputer, dan pengembangan solusi digital."
                    ),
                    location="Yogyakarta"
                )
                db.session.add(profile)
                print("Profil berhasil ditambahkan.")
            else:
                print("Profil sudah tersedia, dilewati.")

            # ==================================
            # 2. SKILLS
            # ==================================

            skills = [
                ("Python", "Programming", "Dasar"),
                ("HTML", "Web Development", "Dasar"),
                ("CSS", "Web Development", "Dasar"),
                ("JavaScript", "Web Development", "Dasar"),
                ("SQL", "Database", "Dasar"),
                ("Networking", "Networking", "Dasar"),
                ("MikroTik", "Networking", "Dasar"),
                ("UI/UX Design", "Design", "Dasar")
            ]

            for name, category, level in skills:
                exists = Skill.query.filter_by(name=name).first()

                if not exists:
                    db.session.add(
                        Skill(
                            name=name,
                            category=category,
                            level=level
                        )
                    )
                    print(f"Skill ditambahkan: {name}")

            # ==================================
            # 3. EDUCATION
            # ==================================

            educations = [
                {
                    "institution": "SMK NU Pace",
                    "degree": "SMK",
                    "major": "Teknik Komputer dan Jaringan",
                    "start_year": None,
                    "end_year": "2025",
                    "description": (
                        "Mempelajari jaringan komputer, "
                        "perangkat keras, dan teknologi informasi."
                    )
                },
                {
                    "institution": "Universitas Nahdlatul Ulama Yogyakarta",
                    "degree": "S1",
                    "major": "Informatika",
                    "start_year": "2025",
                    "end_year": "Sekarang",
                    "description": (
                        "Mempelajari pemrograman, basis data, "
                        "statistika, dan pengembangan teknologi digital."
                    )
                }
            ]

            for item in educations:
                exists = Education.query.filter_by(
                    institution=item["institution"],
                    major=item["major"]
                ).first()

                if not exists:
                    db.session.add(Education(**item))
                    print(
                        f"Pendidikan ditambahkan: "
                        f"{item['institution']}"
                    )

            # ==================================
            # 4. EXPERIENCES
            # ==================================

            experiences = [
                {
                    "organization": "IPNU",
                    "position": "Ketua",
                    "experience_type": "Organisasi",
                    "start_period": "2024",
                    "end_period": "2024",
                    "description": (
                        "Memiliki pengalaman memimpin organisasi "
                        "dan mengoordinasikan kegiatan anggota."
                    )
                },
                {
                    "organization": "Makesta",
                    "position": "Ketua Pelaksana",
                    "experience_type": "Kepanitiaan",
                    "start_period": "2023",
                    "end_period": "2023",
                    "description": (
                        "Bertanggung jawab mengoordinasikan "
                        "persiapan dan pelaksanaan kegiatan Makesta."
                    )
                }
            ]

            for item in experiences:
                exists = Experience.query.filter_by(
                    organization=item["organization"],
                    position=item["position"]
                ).first()

                if not exists:
                    db.session.add(Experience(**item))
                    print(
                        f"Pengalaman ditambahkan: "
                        f"{item['organization']}"
                    )

            # ==================================
            # 5. PROJECTS
            # ==================================

            projects = [
                {
                    "title": "Pengembangan Laboratorium Komputer",
                    "description": (
                        "Pengalaman praktik kerja lapangan dalam "
                        "mempersiapkan ruang kelas menjadi laboratorium "
                        "komputer, termasuk penataan perangkat "
                        "dan instalasi dasar."
                    ),
                    "technologies": "Networking, Hardware, Mikrotik",
                    "is_featured": True
                },
                {
                    "title": "Website Portofolio Pribadi",
                    "description": (
                        "Pengembangan website portofolio pribadi "
                        "menggunakan Flask dan PostgreSQL sebagai "
                        "media untuk menampilkan profil, keahlian, "
                        "pendidikan, organisasi, dan proyek."
                    ),
                    "technologies": "Python, Flask, PostgreSQL, HTML, CSS, JavaScript",
                    "is_featured": True
                }
            ]

            for item in projects:
                exists = Project.query.filter_by(
                    title=item["title"]
                ).first()

                if not exists:
                    db.session.add(Project(**item))
                    print(
                        f"Proyek ditambahkan: {item['title']}"
                    )

            # ==================================
            # SIMPAN DATA
            # ==================================

            db.session.commit()

            print("\n================================")
            print("DATA PORTOFOLIO BERHASIL DISIMPAN")
            print("================================")

            print("Profil:", Profile.query.count())
            print("Skills:", Skill.query.count())
            print("Pendidikan:", Education.query.count())
            print("Pengalaman:", Experience.query.count())
            print("Proyek:", Project.query.count())

        except Exception as error:
            db.session.rollback()
            print("GAGAL MENYIMPAN DATA!")
            print("Detail:", error)
            raise


if __name__ == "__main__":
    seed_data()
