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