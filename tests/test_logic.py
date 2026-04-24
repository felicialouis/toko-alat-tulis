import pytest
from app.logic import StationeryManager

@pytest.fixture
def db():
    return {
        "barang": [
            {"id": 1, "nama": "Buku", "stok": 10, "harga_beli": 2000, "harga_jual": 5000}
        ],
        "penjualan": []
    }

# --- KATEGORI 1: PENGUJIAN VALIDASI INPUT (CRITICAL) ---

def test_tambah_item_nama_hanya_spasi(db):
    mgr = StationeryManager(db)
    with pytest.raises(ValueError, match="Nama barang tidak boleh kosong"):
        mgr.tambah_item("   ", 10, 2000, 5000)

def test_tambah_item_harga_jual_sama_dengan_beli(db):
    # Kritis: Bisnis tidak untung tapi secara teknis diperbolehkan? 
    # Logika kita di logic.py melarang rugi, tapi mari tes batas (sama dengan)
    mgr = StationeryManager(db)
    item = mgr.tambah_item("Pensil", 10, 2000, 2000)
    assert item['harga_jual'] == item['harga_beli']

def test_tambah_item_input_bukan_angka(db):
    mgr = StationeryManager(db)
    with pytest.raises(ValueError):
        mgr.tambah_item("Pulpen", "sepuluh", "seribu", "dua ribu")

def test_tambah_item_stok_nol(db):
    # Menambah barang baru tapi stok 0 (Valid tapi kritis untuk dicek)
    mgr = StationeryManager(db)
    item = mgr.tambah_item("Spidol", 0, 1000, 2000)
    assert item['stok'] == 0

# --- KATEGORI 2: PENGUJIAN LOGIKA STOK & PENJUALAN ---

def test_jual_tepat_seluruh_stok(db):
    mgr = StationeryManager(db)
    # Stok ada 10, beli 10. Harus sisa 0.
    mgr.proses_jual(1, 10)
    assert db['barang'][0]['stok'] == 0

def test_jual_melebihi_stok_ekstrem(db):
    mgr = StationeryManager(db)
    with pytest.raises(ValueError, match="Stok tidak cukup"):
        mgr.proses_jual(1, 999999)

def test_jual_item_id_tidak_terdaftar(db):
    mgr = StationeryManager(db)
    with pytest.raises(ValueError, match="Barang tidak ditemukan"):
        mgr.proses_jual(99, 1)

def test_jual_jumlah_negatif(db):
    mgr = StationeryManager(db)
    with pytest.raises(ValueError, match="Jumlah penjualan minimal 1"):
        mgr.proses_jual(1, -5)

# --- KATEGORI 3: PENGUJIAN INTEGRITAS DATA & PROFIT ---

def test_profit_setelah_beberapa_transaksi(db):
    mgr = StationeryManager(db)
    # Transaksi 1: Buku (5000-2000) * 2 = 6000
    mgr.proses_jual(1, 2)
    # Tambah barang baru
    mgr.tambah_item("Pen", 10, 1000, 1500)
    # Transaksi 2: Pen (1500-1000) * 4 = 2000
    mgr.proses_jual(2, 4)
    assert mgr.total_pendapatan_bersih() == 8000

def test_profit_barang_dengan_harga_modal_nol(db):
    # Kasus barang hibah/bonus yang dijual (Profit 100%)
    mgr = StationeryManager(db)
    mgr.tambah_item("Bonus", 5, 0, 1000)
    mgr.proses_jual(2, 5)
    assert mgr.total_pendapatan_bersih() == 5000

def test_hapus_barang_tengah_daftar(db):
    mgr = StationeryManager(db)
    mgr.tambah_item("A", 1, 1, 2)
    mgr.tambah_item("B", 1, 1, 2) # ID 3
    mgr.hapus_item(2) # Hapus barang ID 2 (A)
    assert len(db['barang']) == 2
    assert db['barang'][1]['nama'] == "B"

def test_hapus_id_tidak_ada(db):
    mgr = StationeryManager(db)
    hasil = mgr.hapus_item(999)
    assert hasil is False

def test_auto_increment_id_setelah_penghapusan(db):
    mgr = StationeryManager(db)
    mgr.tambah_item("Barang A", 1, 1, 2) # ID 2
    mgr.hapus_item(2)
    mgr.tambah_item("Barang B", 1, 1, 2) # Harus ID 2 atau ID 3? Logika kita ID max + 1.
    assert db['barang'][-1]['id'] == 2

def test_jual_dengan_jumlah_string_angka(db):
    # User kadang kirim string dari form "5" bukan integer 5
    mgr = StationeryManager(db)
    mgr.proses_jual(1, "5")
    assert db['barang'][0]['stok'] == 5

def test_total_pendapatan_saat_kosong(db):
    mgr = StationeryManager(db)
    assert mgr.total_pendapatan_bersih() == 0