import json
import os

# Lokasi file database kita
DATA_PATH = 'data/inventory.json'

def init_db():
    """Memastikan folder dan file data tersedia."""
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'w') as f:
            # Data awal: barang kosong dan penjualan kosong
            json.dump({"barang": [], "penjualan": []}, f)

def load_data():
    """Membaca data dari file JSON."""
    init_db()
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def save_data(data):
    """Menyimpan data ke file JSON."""
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=4)