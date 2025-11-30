# tab_casi.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from db_utility import connect_db, get_all_codes
import pyodbc

# --- Khai báo biến Global cho tab này ---
entry_macs = None
entry_tencs = None
date_entry_cs = None
entry_quoctich = None
gender_var_cs = None
entry_mota_cs = None
tree_cs = None

def setup_casi_tab(tab, root):
    """Thiết lập giao diện và logic cho tab Ca Sĩ."""
    global entry_macs, entry_tencs, date_entry_cs, entry_quoctich, gender_var_cs, entry_mota_cs, tree_cs
    
    # ====== Frame nhập thông tin Ca Sĩ ====== 
    frame_info = tk.Frame(tab) 
    frame_info.pack(pady=5, padx=10, fill="x") 

    # Hàng 1
    tk.Label(frame_info, text="Mã Ca Sĩ").grid(row=0, column=0, padx=5, pady=5, sticky="w") 
    entry_macs = tk.Entry(frame_info, width=15) 
    entry_macs.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
    
    tk.Label(frame_info, text="Tên Ca Sĩ").grid(row=0, column=2, padx=5, pady=5, sticky="w") 
    entry_tencs = tk.Entry(frame_info, width=40) 
    entry_tencs.grid(row=0, column=3, padx=5, pady=5, sticky="w") 

    # Hàng 2
    tk.Label(frame_info, text="Ngày Sinh").grid(row=1, column=0, padx=5, pady=5, sticky="w") 
    date_entry_cs = DateEntry(frame_info, width=12, background="darkblue", 
                              foreground="white", date_pattern="yyyy-mm-dd") 
    date_entry_cs.grid(row=1, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Quốc Tịch").grid(row=1, column=2, padx=5, pady=5, sticky="w") 
    entry_quoctich = tk.Entry(frame_info, width=15) 
    entry_quoctich.grid(row=1, column=3, padx=5, pady=5, sticky="w") 

    # Hàng 3
    tk.Label(frame_info, text="Giới Tính").grid(row=2, column=0, padx=5, pady=5, sticky="w") 
    gender_var_cs = tk.StringVar(value="Nam") 
    tk.Radiobutton(frame_info, text="Nam", variable=gender_var_cs, value="Nam").grid(row=2, column=1, padx=5, sticky="w") 
    tk.Radiobutton(frame_info, text="Nữ", variable=gender_var_cs, value="Nữ").grid(row=2, column=1, padx=60, sticky="w") 

    tk.Label(frame_info, text="Mô Tả").grid(row=2, column=2, padx=5, pady=5, sticky="w") 
    entry_mota_cs = tk.Entry(frame_info, width=40) 
    entry_mota_cs.grid(row=2, column=3, padx=5, pady=5, sticky="w") 

    # ====== Bảng danh sách Ca Sĩ ====== 
    lbl_ds = tk.Label(tab, text="Danh sách Ca Sĩ", font=("Arial", 10, "bold")) 
    lbl_ds.pack(pady=5, anchor="w", padx=10) 
    
    columns = ("macasi", "tencasi", "ngaysinh", "quoctich", "gioitinh", "mota") 
    tree_cs = ttk.Treeview(tab, columns=columns, show="headings", height=12) 
    
    tree_cs.heading("macasi", text="Mã CS")
    tree_cs.heading("tencasi", text="Tên Ca Sĩ")
    tree_cs.heading("ngaysinh", text="Ngày Sinh")
    tree_cs.heading("quoctich", text="Quốc Tịch")
    tree_cs.heading("gioitinh", text="Giới Tính")
    tree_cs.heading("mota", text="Mô Tả")

    tree_cs.column("macasi", width=70, anchor="center") 
    tree_cs.column("tencasi", width=150) 
    tree_cs.column("ngaysinh", width=100, anchor="center") 
    tree_cs.column("quoctich", width=100) 
    tree_cs.column("gioitinh", width=80, anchor="center") 
    tree_cs.column("mota", width=250) 
    
    tree_cs.pack(padx=10, pady=5, fill="both") 
    
    # ====== Chức năng CRUD Ca Sĩ ====== 
    def clear_input_cs(): 
        entry_macs.config(state='normal')
        entry_macs.delete(0, tk.END) 
        entry_tencs.delete(0, tk.END) 
        date_entry_cs.set_date(datetime.date.today().strftime('%Y-%m-%d'))
        entry_quoctich.delete(0, tk.END)
        gender_var_cs.set("Nam")
        entry_mota_cs.delete(0, tk.END)
        
    def load_data_cs(): 
        for i in tree_cs.get_children(): tree_cs.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor() 
        try:
            cur.execute("SELECT MaCaSi, TenCaSi, NgaySinh, QuocTich, GioiTinh, MoTa FROM CASI") 
            for row in cur.fetchall(): 
                display_row = list(row)
                if display_row[2]: display_row[2] = display_row[2].strftime('%Y-%m-%d') # NgaySinh
                
                for i in [0, 3, 4]: # strip các cột char
                    if isinstance(display_row[i], str):
                        display_row[i] = display_row[i].strip()
                        
                tree_cs.insert("", tk.END, values=tuple(display_row)) 
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Tải Dữ Liệu CS", f"Không thể tải dữ liệu: {e}")
        finally:
            if conn: conn.close() 

    def them_cs(): 
        macs = entry_macs.get().strip() 
        tencs = entry_tencs.get() 
        ngaysinh = date_entry_cs.get() 
        quoctich = entry_quoctich.get()
        gioitinh = gender_var_cs.get()
        mota = entry_mota_cs.get()
        
        if not macs or not tencs: 
            messagebox.showwarning("Thiếu dữ liệu", "Mã Ca Sĩ và Tên Ca Sĩ không được để trống") 
            return 
        
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try: 
            sql = "INSERT INTO CASI (MaCaSi, TenCaSi, NgaySinh, QuocTich, GioiTinh, MoTa) VALUES (?, ?, ?, ?, ?, ?)"
            params = (macs, tencs, ngaysinh, quoctich, gioitinh, mota)
            cur.execute(sql, params) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã thêm Ca Sĩ mới.")
            load_data_cs() 
            clear_input_cs() 

        except pyodbc.Error as e: 
            messagebox.showerror("Lỗi Thêm CS", str(e)) 
        finally:
            if conn: conn.close() 

    def xoa_cs(): 
        selected = tree_cs.selection() 
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn Ca Sĩ để xóa") 
            return 
        if not messagebox.askyesno("Xác nhận Xóa", "Việc này sẽ xóa Ca Sĩ và có thể gây lỗi khóa ngoại ở bảng Bài Hát. Bạn có chắc chắn muốn xóa?"):
            return

        macs = tree_cs.item(selected)["values"][0] 
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            # Kiểm tra ràng buộc khóa ngoại (nên làm trong DB, nhưng kiểm tra trước để báo lỗi thân thiện hơn)
            cur.execute("SELECT COUNT(*) FROM BAIHAT WHERE MaCaSi = ?", (macs,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Cảnh báo", f"Không thể xóa Ca Sĩ {macs} vì có Bài Hát đang tham chiếu.")
                return
                
            cur.execute("DELETE FROM CASI WHERE MaCaSi=?", (macs,)) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã xóa Ca Sĩ.")

        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Xóa CS", str(e))
        finally:
            if conn: conn.close() 
        load_data_cs() 

    def sua_cs(): 
        selected = tree_cs.selection() 
        if not selected: 
            messagebox.showwarning("Chưa chọn", "Hãy chọn Ca Sĩ để sửa") 
            return 
        values = tree_cs.item(selected)["values"] 
        clear_input_cs()
        entry_macs.insert(0, values[0]) 
        entry_macs.config(state='readonly')
        entry_tencs.insert(0, values[1]) 
        if values[2]: date_entry_cs.set_date(values[2])
        entry_quoctich.insert(0, values[3])
        gender_var_cs.set(values[4])
        entry_mota_cs.insert(0, values[5])

    def luu_cs(): 
        macs = entry_macs.get().strip() 
        tencs = entry_tencs.get() 
        ngaysinh = date_entry_cs.get() 
        quoctich = entry_quoctich.get()
        gioitinh = gender_var_cs.get()
        mota = entry_mota_cs.get()
        
        if not macs or not tencs: 
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin để lưu") 
            return 

        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            sql = """
                UPDATE CASI SET 
                    TenCaSi=?, NgaySinh=?, QuocTich=?, GioiTinh=?, MoTa=?  
                WHERE MaCaSi=?
            """
            params = (tencs, ngaysinh, quoctich, gioitinh, mota, macs)
            cur.execute(sql, params) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin Ca Sĩ.")
            load_data_cs() 
            clear_input_cs() 
            entry_macs.config(state='normal')
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Lưu CS", str(e))
        finally:
            if conn: conn.close() 

    # ====== Frame nút Ca Sĩ ====== 
    frame_btn = tk.Frame(tab) 
    frame_btn.pack(pady=10) 
    
    tk.Button(frame_btn, text="Thêm", width=8, command=them_cs).grid(row=0, column=0, padx=5) 
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_cs).grid(row=0, column=1, padx=5) 
    tk.Button(frame_btn, text="Sửa", width=8, command=sua_cs).grid(row=0, column=2, padx=5) 
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input_cs).grid(row=0, column=3, padx=5) 
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_cs).grid(row=0, column=4, padx=5) 
    tk.Button(frame_btn, text="Thoát", width=8, command=root.quit).grid(row=0, column=5, padx=5) 
    
    load_data_cs()