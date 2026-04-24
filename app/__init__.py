from flask import Flask
from .storage import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_felicia_123' # Untuk fitur flash message (notifikasi)

    # Inisialisasi database saat aplikasi jalan
    init_db()

    # Daftarkan jalur (routes)
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app