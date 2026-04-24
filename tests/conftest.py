import pytest
import os
import json
from app import create_app
from app import storage

@pytest.fixture
def client():
    # Setup: Pakai file database khusus testing
    test_db = 'data/test_inventory.json'
    storage.DATA_PATH = test_db
    
    # Isi dengan data kosong awal
    with open(test_db, 'w') as f:
        json.dump({"barang": [], "penjualan": []}, f)
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client
    
    # Teardown: Hapus file database testing setelah selesai
    if os.path.exists(test_db):
        os.remove(test_db)