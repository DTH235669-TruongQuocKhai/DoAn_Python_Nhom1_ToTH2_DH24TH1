# tab_album.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from db_utility import connect_db, get_all_codes
import pyodbc


# --- Khai báo biến Global cho tab này ---
entry_maalb = None
entry_tenalb = None
date_entry_alb = None
entry_hangph = None
tree_alb = None


def setup_album_tab(tab, root):
    """Thiết lập giao diện và logic cho tab Album."""
    global entry_maalb, entry_tenalb, date_entry_alb, entry_hangph, tree_alb
    
    # ====== Frame nhập thông tin Album ====== 
    frame_info = tk.Frame(tab) 
    frame_info.pack(pady=15, padx=10, fill="x") 

    # Hàng 1
    tk.Label(frame_info, text="Mã Album").grid(row=0, column=0, padx=5, pady=5, sticky="w") 
    entry_maalb = tk.Entry(frame_info, width=15) 
    entry_maalb.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
    
    tk.Label(frame_info, text="Tên Album").grid(row=0, column=2, padx=5, pady=5, sticky="w") 
    entry_tenalb = tk.Entry(frame_info, width=40) 
    entry_tenalb.grid(row=0, column=3, padx=5, pady=5, sticky="w") 

    # Hàng 2
    tk.Label(frame_info, text="Ngày PH").grid(row=1, column=0, padx=5, pady=5, sticky="w") 
    date_entry_alb = DateEntry(frame_info, width=12, background="darkblue", 
                              foreground="white", date_pattern="yyyy-mm-dd") 
    date_entry_alb.grid(row=1, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Hãng PH").grid(row=1, column=2, padx=5, pady=5, sticky="w") 
    entry_hangph = tk.Entry(frame_info, width=40) 
    entry_hangph.grid(row=1, column=3, padx=5, pady=5, sticky="w") 

    # ====== Bảng danh sách Album ====== 
    lbl_ds = tk.Label(tab, text="Danh sách Album", font=("Arial", 10, "bold")) 
    lbl_ds.pack(pady=5, anchor="w", padx=10) 
    
    columns = ("maalb", "tenalb", "ngayph", "hangph") 
    tree_alb = ttk.Treeview(tab, columns=columns, show="headings", height=12) 
    
    tree_alb.heading("maalb", text="Mã Album")
    tree_alb.heading("tenalb", text="Tên Album")
    tree_alb.heading("ngayph", text="Ngày PH")
    tree_alb.heading("hangph", text="Hãng PH")

    tree_alb.column("maalb", width=100, anchor="center") 
    tree_alb.column("tenalb", width=250) 
    tree_alb.column("ngayph", width=150, anchor="center") 
    tree_alb.column("hangph", width=250) 
    
    tree_alb.pack(padx=10, pady=5, fill="both") 
    
    # ====== Chức năng CRUD Album ====== 
    def clear_input_alb(): 
        entry_maalb.config(state='normal')
        entry_maalb.delete(0, tk.END) 
        entry_tenalb.delete(0, tk.END) 
        date_entry_alb.set_date(datetime.date.today().strftime('%Y-%m-%d'))
        entry_hangph.delete(0, tk.END)
        
    def load_data_alb(): 
        for i in tree_alb.get_children(): tree_alb.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor() 
        try:
            cur.execute("SELECT MaAlbum, TenAlbum, NgayPhatHanh, HangPhatHanh FROM ALBUM") 
            for row in cur.fetchall(): 
                display_row = list(row)
                if display_row[2]: display_row[2] = display_row[2].strftime('%Y-%m-%d')
                
                if isinstance(display_row[0], str): display_row[0] = display_row[0].strip()
                
                tree_alb.insert("", tk.END, values=tuple(display_row)) 
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Tải Dữ Liệu ALB", f"Không thể tải dữ liệu: {e}")
        finally:
            if conn: conn.close() 

    def them_alb(): 
        maalb = entry_maalb.get().strip()
        tenalb = entry_tenalb.get()
        ngayph = date_entry_alb.get()
        hangph = entry_hangph.get()
        
        if not maalb or not tenalb: 
            messagebox.showwarning("Thiếu dữ liệu", "Mã Album và Tên Album không được để trống") 
            return 
        
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try: 
            sql = "INSERT INTO ALBUM (MaAlbum, TenAlbum, NgayPhatHanh, HangPhatHanh) VALUES (?, ?, ?, ?)"
            params = (maalb, tenalb, ngayph, hangph)
            cur.execute(sql, params) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã thêm Album mới.")
            load_data_alb() 
            clear_input_alb() 
  
        except pyodbc.Error as e: 
            messagebox.showerror("Lỗi Thêm ALB", str(e)) 
        finally:
            if conn: conn.close() 

    def xoa_alb(): 
        selected = tree_alb.selection() 
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn Album để xóa") 
            return 
        if not messagebox.askyesno("Xác nhận Xóa", "Việc này có thể gây lỗi khóa ngoại ở bảng Bài Hát. Bạn có chắc chắn muốn xóa?"):
            return

        maalb = tree_alb.item(selected)["values"][0] 
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            # Kiểm tra ràng buộc khóa ngoại
            cur.execute("SELECT COUNT(*) FROM BAIHAT WHERE MaAlbum = ?", (maalb,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Cảnh báo", f"Không thể xóa Album {maalb} vì có Bài Hát đang tham chiếu.")
                return

            cur.execute("DELETE FROM ALBUM WHERE MaAlbum=?", (maalb,)) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã xóa Album.")
            
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Xóa ALB", str(e))
        finally:
            if conn: conn.close() 
        load_data_alb() 

    def sua_alb(): 
        selected = tree_alb.selection() 
        if not selected: 
            messagebox.showwarning("Chưa chọn", "Hãy chọn Album để sửa") 
            return 
        values = tree_alb.item(selected)["values"] 
        clear_input_alb()
        entry_maalb.insert(0, values[0]) 
        entry_maalb.config(state='readonly')
        entry_tenalb.insert(0, values[1]) 
        if values[2]: date_entry_alb.set_date(values[2])
        entry_hangph.insert(0, values[3])

    def luu_alb(): 
        maalb = entry_maalb.get().strip()
        tenalb = entry_tenalb.get()
        ngayph = date_entry_alb.get()
        hangph = entry_hangph.get()
        
        if not maalb or not tenalb: 
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin để lưu") 
            return 

        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            sql = """
                UPDATE ALBUM SET 
                    TenAlbum=?, NgayPhatHanh=?, HangPhatHanh=?  
                WHERE MaAlbum=?
            """
            params = (tenalb, ngayph, hangph, maalb)
            cur.execute(sql, params) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin Album.")
            load_data_alb() 
            clear_input_alb() 
            entry_maalb.config(state='normal')
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Lưu ALB", str(e))
        finally:
            if conn: conn.close() 

    # ====== Frame nút Album ====== 
    frame_btn = tk.Frame(tab) 
    frame_btn.pack(pady=10) 
    
    tk.Button(frame_btn, text="Thêm", width=8, command=them_alb).grid(row=0, column=0, padx=5) 
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_alb).grid(row=0, column=1, padx=5) 
    tk.Button(frame_btn, text="Sửa", width=8, command=sua_alb).grid(row=0, column=2, padx=5) 
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input_alb).grid(row=0, column=3, padx=5) 
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_alb).grid(row=0, column=4, padx=5) 
    tk.Button(frame_btn, text="Thoát", width=8, command=root.quit).grid(row=0, column=5, padx=5) 
    
    load_data_alb()