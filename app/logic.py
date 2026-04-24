class StationeryManager:
    def __init__(self, db_data):
        self.db = db_data
        self.barang = db_data['barang']
        self.penjualan = db_data['penjualan']

    def tambah_item(self, nama, stok, h_beli, h_jual):
        # Validasi input (Ini poin penting untuk Testing!)
        if not nama or str(nama).strip() == "":
            raise ValueError("Nama barang tidak boleh kosong")
        if int(stok) < 0 or int(h_beli) < 0 or int(h_jual) < 0:
            raise ValueError("Stok dan harga tidak boleh negatif")
        if int(h_jual) < int(h_beli):
            raise ValueError("Harga jual tidak boleh lebih rendah dari harga beli")

        new_id = max([b['id'] for b in self.barang], default=0) + 1
        item = {
            "id": new_id,
            "nama": nama.strip(),
            "stok": int(stok),
            "harga_beli": int(h_beli),
            "harga_jual": int(h_jual)
        }
        self.barang.append(item)
        return item

    def hapus_item(self, item_id):
        # CRUD: Delete
        original_count = len(self.barang)
        self.db['barang'] = [b for b in self.barang if b['id'] != item_id]
        self.barang = self.db['barang']
        return len(self.barang) < original_count

    def proses_jual(self, item_id, qty):
        qty = int(qty)
        if qty <= 0:
            raise ValueError("Jumlah penjualan minimal 1")

        for b in self.barang:
            if b['id'] == item_id:
                if b['stok'] < qty:
                    raise ValueError(f"Stok tidak cukup (Sisa: {b['stok']})")
                
                # Kurangi stok
                b['stok'] -= qty
                # Hitung profit bersih (Harga Jual - Harga Beli) * Qty
                untung = (b['harga_jual'] - b['harga_beli']) * qty
                
                self.penjualan.append({
                    "id_barang": item_id,
                    "nama_barang": b['nama'],
                    "jumlah": qty,
                    "profit": untung
                })
                return True
        raise ValueError("Barang tidak ditemukan")

    def total_pendapatan_bersih(self):
        return sum(p['profit'] for p in self.penjualan)