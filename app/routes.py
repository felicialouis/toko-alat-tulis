from flask import Blueprint, render_template, request, redirect, url_for, flash
from .logic import StationeryManager
from .storage import load_data, save_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    db = load_data()
    manager = StationeryManager(db)
    # Menampilkan halaman utama dengan data barang dan total profit
    return render_template('index.html', 
                           barang=db['barang'], 
                           total_profit=manager.total_pendapatan_bersih())

@main_bp.route('/tambah', methods=['POST'])
def tambah():
    db = load_data()
    manager = StationeryManager(db)
    try:
        # Mengambil data dari form HTML
        manager.tambah_item(
            request.form['nama'],
            request.form['stok'],
            request.form['harga_beli'],
            request.form['harga_jual']
        )
        save_data(db)
        flash("Barang berhasil ditambah!", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('main.index'))

@main_bp.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    db = load_data()
    mgr = StationeryManager(db)
    
    # Ambil data dari form
    stok = request.form.get('stok')
    h_beli = request.form.get('harga_beli')
    h_jual = request.form.get('harga_jual')
    
    try:
        # PINDAHKAN INI KE DALAM TRY
        res = mgr.update_barang(item_id, stok, h_beli, h_jual)
        
        if res == "NO_CHANGE":
            flash("Tidak ada perubahan data.", "info") 
        elif res:
            save_data(db)
            flash("Data berhasil diperbarui!", "success")
        else:
            flash("Barang tidak ditemukan.", "danger")
            
    except ValueError as e:
        flash(str(e), "danger")
        
    return redirect(url_for('main.index'))

@main_bp.route('/jual/<int:item_id>', methods=['POST'])
def jual(item_id):
    db = load_data()
    manager = StationeryManager(db)
    try:
        manager.proses_jual(item_id, request.form['qty'])
        save_data(db)
        flash("Penjualan berhasil!", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('main.index'))

@main_bp.route('/hapus/<int:item_id>')
def hapus(item_id):
    db = load_data()
    manager = StationeryManager(db)
    if manager.hapus_item(item_id):
        save_data(db)
        flash("Barang dihapus!", "warning")
    return redirect(url_for('main.index'))