# tab_baihat.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
# Import các hàm DB chung
from db_utility import connect_db, get_all_codes
import pyodbc

# --- Khai báo biến Global cho tab này (Cần thiết cho các hàm CRUD và Refresh) ---
entry_mabh = None
entry_tenbh = None
entry_thoiluong = None
date_entry_bh = None
cbb_macasi = None
cbb_matl = None
cbb_maalbum = None
tree_bh = None


def refresh_foreign_key_comboboxes():
    """Cập nhật giá trị Combobox MaCaSi, MaTheLoai, MaAlbum.
    Hàm này có thể được gọi từ các tab khác (Album, Ca Sĩ, Thể Loại) và nút Làm Mới.
    """
    global cbb_macasi, cbb_matl, cbb_maalbum
    # Chỉ cập nhật nếu các Combobox đã được khởi tạo
    if cbb_macasi is not None:
        cbb_macasi['values'] = get_all_codes('CASI', 'MaCaSi')
    if cbb_matl is not None:
        cbb_matl['values'] = get_all_codes('THELOAI', 'MaTheLoai')
    if cbb_maalbum is not None:
        cbb_maalbum['values'] = get_all_codes('ALBUM', 'MaAlbum')

def setup_baihat_tab(tab, root):
    """Thiết lập giao diện và logic cho tab Bài Hát."""
    global entry_mabh, entry_tenbh, entry_thoiluong, date_entry_bh, cbb_macasi, cbb_matl, cbb_maalbum, tree_bh
    
    # ====== Frame nhập thông tin Bài Hát ====== 
    frame_info = tk.Frame(tab) 
    frame_info.pack(pady=5, padx=10, fill="x") 

    # Hàng 1
    tk.Label(frame_info, text="Mã BH").grid(row=0, column=0, padx=5, pady=5, sticky="w") 
    entry_mabh = tk.Entry(frame_info, width=15) 
    entry_mabh.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
    
    tk.Label(frame_info, text="Tên Bài Hát").grid(row=0, column=2, padx=5, pady=5, sticky="w") 
    entry_tenbh = tk.Entry(frame_info, width=40) 
    entry_tenbh.grid(row=0, column=3, padx=5, pady=5, sticky="w") 

    # Hàng 2
    tk.Label(frame_info, text="Thời Lượng (HH:MM:SS)").grid(row=1, column=0, padx=5, pady=5, sticky="w") 
    entry_thoiluong = tk.Entry(frame_info, width=15) 
    entry_thoiluong.grid(row=1, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Ngày PH").grid(row=1, column=2, padx=5, pady=5, sticky="w") 
    date_entry_bh = DateEntry(frame_info, width=12, background="darkblue", 
                              foreground="white", date_pattern="yyyy-mm-dd") 
    date_entry_bh.grid(row=1, column=3, padx=5, pady=5, sticky="w") 

    # Hàng 3 (Dùng Combobox để chọn Mã từ các bảng khác)
    tk.Label(frame_info, text="Mã Ca Sĩ").grid(row=2, column=0, padx=5, pady=5, sticky="w") 
    cbb_macasi = ttk.Combobox(frame_info, width=13) 
    cbb_macasi['values'] = get_all_codes('CASI', 'MaCaSi')
    cbb_macasi.grid(row=2, column=1, padx=5, pady=5, sticky="w") 
    
    tk.Label(frame_info, text="Mã Thể Loại").grid(row=2, column=2, padx=5, pady=5, sticky="w") 
    cbb_matl = ttk.Combobox(frame_info, width=13)
    cbb_matl['values'] = get_all_codes('THELOAI', 'MaTheLoai')
    cbb_matl.grid(row=2, column=3, padx=5, pady=5, sticky="w") 
    
    tk.Label(frame_info, text="Mã Album").grid(row=2, column=4, padx=5, pady=5, sticky="w") 
    cbb_maalbum = ttk.Combobox(frame_info, width=13)
    cbb_maalbum['values'] = get_all_codes('ALBUM', 'MaAlbum')
    cbb_maalbum.grid(row=2, column=5, padx=5, pady=5, sticky="w")

    # ====== Bảng danh sách bài hát ====== 
    lbl_ds = tk.Label(tab, text="Danh sách bài hát", font=("Arial", 10, "bold")) 
    lbl_ds.pack(pady=5, anchor="w", padx=10) 
    
    columns = ("mabh", "tenbh", "thoiluong", "ngayph", "macasi", "matl", "maalbum") 
    tree_bh = ttk.Treeview(tab, columns=columns, show="headings", height=12) 
    
    tree_bh.heading("mabh", text="Mã BH")
    tree_bh.heading("tenbh", text="Tên Bài Hát")
    tree_bh.heading("thoiluong", text="Thời Lượng")
    tree_bh.heading("ngayph", text="Ngày PH")
    tree_bh.heading("macasi", text="Mã Ca Sĩ")
    tree_bh.heading("matl", text="Mã Thể Loại")
    tree_bh.heading("maalbum", text="Mã Album")

    tree_bh.column("mabh", width=70, anchor="center") 
    tree_bh.column("tenbh", width=200) 
    tree_bh.column("thoiluong", width=90, anchor="center") 
    tree_bh.column("ngayph", width=90, anchor="center") 
    tree_bh.column("macasi", width=80, anchor="center") 
    tree_bh.column("matl", width=80, anchor="center") 
    tree_bh.column("maalbum", width=80, anchor="center") 
    
    tree_bh.pack(padx=10, pady=5, fill="both") 

    # ====== Chức năng CRUD Bài Hát ====== 
    def clear_input_bh(): 
        entry_mabh.config(state='normal')
        entry_mabh.delete(0, tk.END) 
        entry_tenbh.delete(0, tk.END) 
        entry_thoiluong.delete(0, tk.END) 
        date_entry_bh.set_date(datetime.date.today().strftime('%Y-%m-%d'))
        cbb_macasi.set("") 
        cbb_matl.set("")
        cbb_maalbum.set("")

    def load_data_bh(): 
        for i in tree_bh.get_children(): tree_bh.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor() 
        try:
            cur.execute("SELECT MaBaiHat, TenBaiHat, ThoiLuong, NgayPhatHanh, MaCaSi, MaTheLoai, MaAlbum FROM BAIHAT") 
            for row in cur.fetchall(): 
                display_row = list(row)
                if display_row[3]: display_row[3] = display_row[3].strftime('%Y-%m-%d')
                
                # Định dạng Thời Lượng
                if isinstance(display_row[2], (datetime.timedelta, datetime.time)):
                    if isinstance(display_row[2], datetime.timedelta):
                        total_seconds = int(display_row[2].total_seconds())
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        seconds = total_seconds % 60
                        display_row[2] = f"{hours:02}:{minutes:02}:{seconds:02}"
                    else:
                        display_row[2] = display_row[2].strftime('%H:%M:%S')

                for i in [0, 4, 5, 6]: # strip các cột char
                    if isinstance(display_row[i], str):
                        display_row[i] = display_row[i].strip()
                
                tree_bh.insert("", tk.END, values=tuple(display_row)) 
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Tải Dữ Liệu BH", f"Không thể tải dữ liệu: {e}")
        finally:
            if conn: conn.close() 

    # HÀM update_comboboxes() CŨ ĐÃ BỊ XÓA VÀ THAY BẰNG refresh_foreign_key_comboboxes() Ở ĐẦU FILE

    def them_bh(): 
        mabh = entry_mabh.get().strip() 
        tenbh = entry_tenbh.get() 
        thoiluong = entry_thoiluong.get() 
        ngayph = date_entry_bh.get() 
        macasi = cbb_macasi.get().strip()
        matl = cbb_matl.get().strip()
        maalbum = cbb_maalbum.get().strip()
        
        if not mabh or not tenbh or not macasi or not matl: 
            messagebox.showwarning("Thiếu dữ liệu", "Mã BH, Tên BH, Mã Ca Sĩ và Mã Thể Loại không được để trống") 
            return 
        if not thoiluong: thoiluong = '00:00:00'
        
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try: 
            sql = "INSERT INTO BAIHAT (MaBaiHat, TenBaiHat, ThoiLuong, NgayPhatHanh, MaCaSi, MaTheLoai, MaAlbum) VALUES (?, ?, ?, ?, ?, ?, ?)"
            params = (mabh, tenbh, thoiluong, ngayph, macasi, matl, maalbum)
            cur.execute(sql, params) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã thêm bài hát mới.")
            load_data_bh() 
            clear_input_bh() 
            refresh_foreign_key_comboboxes() # GỌI HÀM LÀM MỚI MỚI
        except pyodbc.Error as e: 
            messagebox.showerror("Lỗi Thêm BH", str(e)) 
        finally:
            if conn: conn.close() 

    def xoa_bh(): 
        selected = tree_bh.selection() 
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn bài hát để xóa") 
            return 
        if not messagebox.askyesno("Xác nhận Xóa", "Bạn có chắc chắn muốn xóa bài hát này?"):
            return

        mabh = tree_bh.item(selected)["values"][0] 
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            cur.execute("DELETE FROM BAIHAT WHERE MaBaiHat=?", (mabh,)) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã xóa bài hát.")
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Xóa BH", str(e))
        finally:
            if conn: conn.close() 
        load_data_bh() 

    def sua_bh(): 
        selected = tree_bh.selection() 
        if not selected: 
            messagebox.showwarning("Chưa chọn", "Hãy chọn bài hát để sửa") 
            return 
        values = tree_bh.item(selected)["values"] 
        clear_input_bh()
        entry_mabh.insert(0, values[0]) 
        entry_mabh.config(state='readonly')
        entry_tenbh.insert(0, values[1]) 
        entry_thoiluong.insert(0, values[2]) 
        if values[3]: date_entry_bh.set_date(values[3])
        cbb_macasi.set(values[4]) 
        cbb_matl.set(values[5]) 
        cbb_maalbum.set(values[6]) 

    def luu_bh(): 
        mabh = entry_mabh.get().strip() 
        tenbh = entry_tenbh.get() 
        thoiluong = entry_thoiluong.get() 
        ngayph = date_entry_bh.get() 
        macasi = cbb_macasi.get().strip()
        matl = cbb_matl.get().strip()
        maalbum = cbb_maalbum.get().strip()
        
        if not mabh or not tenbh or not macasi or not matl: 
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin để lưu") 
            return 
        if not thoiluong: thoiluong = '00:00:00'

        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            sql = """
                UPDATE BAIHAT SET 
                    TenBaiHat=?, ThoiLuong=?, NgayPhatHanh=?, MaCaSi=?, MaTheLoai=?, MaAlbum=?  
                WHERE MaBaiHat=?
            """
            params = (tenbh, thoiluong, ngayph, macasi, matl, maalbum, mabh)
            cur.execute(sql, params) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin bài hát.")
            load_data_bh() 
            clear_input_bh() 
            entry_mabh.config(state='normal')
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Lưu BH", str(e))
        finally:
            if conn: conn.close() 

    # ====== Frame nút Bài Hát ====== 
    frame_btn = tk.Frame(tab) 
    frame_btn.pack(pady=10) 
    
    tk.Button(frame_btn, text="Thêm", width=8, command=them_bh).grid(row=0, column=0, padx=5) 
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_bh).grid(row=0, column=1, padx=5) 
    tk.Button(frame_btn, text="Sửa", width=8, command=sua_bh).grid(row=0, column=2, padx=5) 
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input_bh).grid(row=0, column=3, padx=5) 
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_bh).grid(row=0, column=4, padx=5) 
    
    # Nút Làm Mới Combobox MỚI
    tk.Button(frame_btn, text="Làm Mới ", width=12, command=refresh_foreign_key_comboboxes).grid(row=0, column=5, padx=5) 
    
    tk.Button(frame_btn, text="Thoát", width=8, command=root.quit).grid(row=0, column=6, padx=5) 
    
    load_data_bh()