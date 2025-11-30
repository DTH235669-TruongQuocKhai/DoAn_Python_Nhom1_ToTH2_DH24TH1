# tab_theloai.py

import tkinter as tk
from tkinter import ttk, messagebox
from db_utility import connect_db, get_all_codes
import pyodbc


# --- Khai báo biến Global cho tab này ---
entry_matl_tl = None
entry_tentl = None
entry_mota_tl = None
tree_tl = None


def setup_theloai_tab(tab, root):
    """Thiết lập giao diện và logic cho tab Thể Loại."""
    global entry_matl_tl, entry_tentl, entry_mota_tl, tree_tl
    
    # ====== Frame nhập thông tin Thể Loại ====== 
    frame_info = tk.Frame(tab) 
    frame_info.pack(pady=15, padx=10, fill="x") 

    tk.Label(frame_info, text="Mã Thể Loại").grid(row=0, column=0, padx=5, pady=5, sticky="w") 
    entry_matl_tl = tk.Entry(frame_info, width=15) 
    entry_matl_tl.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
    
    tk.Label(frame_info, text="Tên Thể Loại").grid(row=0, column=2, padx=5, pady=5, sticky="w") 
    entry_tentl = tk.Entry(frame_info, width=40) 
    entry_tentl.grid(row=0, column=3, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Mô Tả").grid(row=1, column=0, padx=5, pady=5, sticky="w") 
    entry_mota_tl = tk.Entry(frame_info, width=65) 
    entry_mota_tl.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w") 

    # ====== Bảng danh sách Thể Loại ====== 
    lbl_ds = tk.Label(tab, text="Danh sách Thể Loại", font=("Arial", 10, "bold")) 
    lbl_ds.pack(pady=5, anchor="w", padx=10) 
    
    columns = ("matl", "tentl", "mota") 
    tree_tl = ttk.Treeview(tab, columns=columns, show="headings", height=12) 
    
    tree_tl.heading("matl", text="Mã TL")
    tree_tl.heading("tentl", text="Tên Thể Loại")
    tree_tl.heading("mota", text="Mô Tả")

    tree_tl.column("matl", width=100, anchor="center") 
    tree_tl.column("tentl", width=250) 
    tree_tl.column("mota", width=450) 
    
    tree_tl.pack(padx=10, pady=5, fill="both") 
    
    # ====== Chức năng CRUD Thể Loại ====== 
    def clear_input_tl(): 
        entry_matl_tl.config(state='normal')
        entry_matl_tl.delete(0, tk.END) 
        entry_tentl.delete(0, tk.END) 
        entry_mota_tl.delete(0, tk.END)
        
    def load_data_tl(): 
        for i in tree_tl.get_children(): tree_tl.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor() 
        try:
            cur.execute("SELECT MaTheLoai, TenTheLoai, MoTa FROM THELOAI") 
            for row in cur.fetchall(): 
                display_row = list(row)
                if isinstance(display_row[0], str): display_row[0] = display_row[0].strip()
                tree_tl.insert("", tk.END, values=tuple(display_row)) 
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Tải Dữ Liệu TL", f"Không thể tải dữ liệu: {e}")
        finally:
            if conn: conn.close() 

    def them_tl(): 
        matl = entry_matl_tl.get().strip()
        tentl = entry_tentl.get()
        mota = entry_mota_tl.get()
        
        if not matl or not tentl: 
            messagebox.showwarning("Thiếu dữ liệu", "Mã TL và Tên TL không được để trống") 
            return 
        
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try: 
            sql = "INSERT INTO THELOAI (MaTheLoai, TenTheLoai, MoTa) VALUES (?, ?, ?)"
            params = (matl, tentl, mota)
            cur.execute(sql, params) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã thêm Thể Loại mới.")
            load_data_tl() 
            clear_input_tl() 

        except pyodbc.Error as e: 
            messagebox.showerror("Lỗi Thêm TL", str(e)) 
        finally:
            if conn: conn.close() 

    def xoa_tl(): 
        selected = tree_tl.selection() 
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn Thể Loại để xóa") 
            return 
        if not messagebox.askyesno("Xác nhận Xóa", "Việc này có thể gây lỗi khóa ngoại ở bảng Bài Hát. Bạn có chắc chắn muốn xóa?"):
            return

        matl = tree_tl.item(selected)["values"][0] 
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            # Kiểm tra ràng buộc khóa ngoại
            cur.execute("SELECT COUNT(*) FROM BAIHAT WHERE MaTheLoai = ?", (matl,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Cảnh báo", f"Không thể xóa Thể Loại {matl} vì có Bài Hát đang tham chiếu.")
                return

            cur.execute("DELETE FROM THELOAI WHERE MaTheLoai=?", (matl,)) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã xóa Thể Loại.")

        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Xóa TL", str(e))
        finally:
            if conn: conn.close() 
        load_data_tl() 

    def sua_tl(): 
        selected = tree_tl.selection() 
        if not selected: 
            messagebox.showwarning("Chưa chọn", "Hãy chọn Thể Loại để sửa") 
            return 
        values = tree_tl.item(selected)["values"] 
        clear_input_tl()
        entry_matl_tl.insert(0, values[0]) 
        entry_matl_tl.config(state='readonly')
        entry_tentl.insert(0, values[1]) 
        entry_mota_tl.insert(0, values[2])

    def luu_tl(): 
        matl = entry_matl_tl.get().strip() 
        tentl = entry_tentl.get() 
        mota = entry_mota_tl.get()
        
        if not matl or not tentl: 
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin để lưu") 
            return 

        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            sql = "UPDATE THELOAI SET TenTheLoai=?, MoTa=? WHERE MaTheLoai=?"
            params = (tentl, mota, matl)
            cur.execute(sql, params) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin Thể Loại.")
            load_data_tl() 
            clear_input_tl() 
            entry_matl_tl.config(state='normal')
        except pyodbc.Error as e:
            messagebox.showerror("Lỗi Lưu TL", str(e))
        finally:
            if conn: conn.close() 

    # ====== Frame nút Thể Loại ====== 
    frame_btn = tk.Frame(tab) 
    frame_btn.pack(pady=10) 
    
    tk.Button(frame_btn, text="Thêm", width=8, command=them_tl).grid(row=0, column=0, padx=5) 
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_tl).grid(row=0, column=1, padx=5) 
    tk.Button(frame_btn, text="Sửa", width=8, command=sua_tl).grid(row=0, column=2, padx=5) 
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input_tl).grid(row=0, column=3, padx=5) 
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_tl).grid(row=0, column=4, padx=5) 
    tk.Button(frame_btn, text="Thoát", width=8, command=root.quit).grid(row=0, column=5, padx=5) 
    
    load_data_tl()