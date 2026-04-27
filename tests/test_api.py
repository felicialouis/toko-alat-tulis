def test_halaman_utama(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Sistem Informasi Alat Tulis" in res.data

def test_flow_tambah_barang_via_gui(client):
    # Simulasi isi form tambah barang
    client.post('/tambah', data={
        'nama': 'Penggaris', 'stok': '20', 
        'harga_beli': '1000', 'harga_jual': '2000'
    }, follow_redirects=True)
    
    res = client.get('/')
    assert b"Penggaris" in res.data
    assert b"20" in res.data

def test_flow_jual_barang_via_gui(client):
    # Tambah dulu
    client.post('/tambah', data={
        'nama': 'Pensil', 'stok': '10', 
        'harga_beli': '1000', 'harga_jual': '2000'
    })
    # Jual
    client.post('/jual/1', data={'qty': '3'}, follow_redirects=True)
    
    res = client.get('/')
    assert b"7" in res.data # Sisa stok 10-3
    assert b"3,000" in res.data # Untung (2000-1000) * 3

def test_error_tambah_via_gui(client):
    # Coba tambah tanpa nama
    res = client.post('/tambah', data={
        'nama': '', 'stok': '10', 'harga_beli': '1000', 'harga_jual': '2000'
    }, follow_redirects=True)
    assert b"Nama barang tidak boleh kosong" in res.data

def test_flow_hapus_barang(client):
    client.post('/tambah', data={
        'nama': 'Spidol', 'stok': '5', 'harga_beli': '5000', 'harga_jual': '7000'
    })
    client.get('/hapus/1', follow_redirects=True)
    res = client.get('/')
    assert b"Spidol" not in res.data

def test_flow_update_barang_via_gui(client):
    client.post('/tambah', data={
        'nama': 'Buku', 'stok': '10', 'harga_beli': '2000', 'harga_jual': '5000'
    })
    
    res = client.post('/update/1', data={
        'stok': '50', 
        'harga_beli': '2500', 
        'harga_jual': '6000'
    }, follow_redirects=True)
    
    assert res.status_code == 200
    assert b"50" in res.data
    assert b"Data berhasil diperbarui!" in res.data

def test_flow_update_barang_no_change_gui(client):
    client.post('/tambah', data={
        'nama': 'Buku', 'stok': '10', 'harga_beli': '2000', 'harga_jual': '5000'
    })
    
    res = client.post('/update/1', data={
        'stok': '10', 
        'harga_beli': '2000', 
        'harga_jual': '5000'
    }, follow_redirects=True)
    assert b"Tidak ada perubahan data." in res.data

def test_flow_update_barang_error_negatif_gui(client):
    client.post('/tambah', data={
        'nama': 'Buku', 'stok': '10', 'harga_beli': '2000', 'harga_jual': '5000'
    })
    
    # Kirim stok negatif
    res = client.post('/update/1', data={
        'stok': '-10', 'harga_beli': '2000', 'harga_jual': '5000'
    }, follow_redirects=True)
    assert b"Nilai tidak boleh negatif" in res.data

def test_error_jual_stok_tidak_cukup_gui(client):
    # Tambah barang dengan stok sedikit
    client.post('/tambah', data={
        'nama': 'Buku', 'stok': '5', 'harga_beli': '2000', 'harga_jual': '5000'
    })
    
    # Jual melebihi stok (jual 10)
    res = client.post('/jual/1', data={'qty': '10'}, follow_redirects=True)
    assert b"Stok tidak cukup" in res.data
    
def test_flow_update_barang_id_ngawur_gui(client):
    res = client.post('/update/999', data={
        'stok': '10', 'harga_beli': '1000', 'harga_jual': '2000'
    }, follow_redirects=True)
    
    assert b"Barang tidak ditemukan." in res.data 