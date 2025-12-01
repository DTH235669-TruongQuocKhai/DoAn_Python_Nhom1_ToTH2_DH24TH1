# db_utility.py

import pyodbc
from tkinter import messagebox, filedialog
import datetime
from openpyxl import Workbook
import os

# ===================== CẤU HÌNH KẾT NỐI DATABASE (SQL Server) =====================
def connect_db():
    """Kết nối đến SQL Server bằng pyodbc."""
    server = 'DESKTOP-69RCC7P' 
    database = 'QLBH_DA_TEST' 
    username = 'sa' 
    password = '123' 
    driver = '{ODBC Driver 17 for SQL Server}' 

    connection_string = (
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Lỗi Kết Nối Database: {sqlstate}") 
        return None

# ====== Hàm canh giữa cửa sổ ====== 
def center_window(win, w=900, h=650): 
    ws = win.winfo_screenwidth() 
    hs = win.winfo_screenheight() 
    x = (ws // 2) - (w // 2) 
    y = (hs // 2) - (h // 2) 
    win.geometry(f'{w}x{h}+{x}+{y}') 

# ====== Chức năng hỗ trợ lấy dữ liệu cho Combobox ======
def get_all_codes(table_name, code_column):
    """Lấy danh sách mã (Ca Sĩ, Thể Loại, Album) từ DB"""
    conn = connect_db()
    if not conn: return []
    cur = conn.cursor()
    codes = []
    try:
        cur.execute(f"SELECT {code_column} FROM {table_name}")
        codes = [row[0].strip() for row in cur.fetchall()]
    except Exception as e:
        print(f"Lỗi khi lấy mã {code_column} từ {table_name}: {e}")
    finally:
        if conn: conn.close()
    return codes

# ====== Hàm hỗ trợ Xuất Excel ======
def export_to_excel(title, headings, data):
    """Xuất dữ liệu từ Treeview ra file Excel (.xlsx)."""
    try:
        # Mở hộp thoại lưu file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title=f"Lưu danh sách {title} vào Excel",
            initialfile=f"DanhSach{title}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        if not file_path:
            return  # Người dùng hủy

        wb = Workbook()
        ws = wb.active
        ws.title = title
        
        # Ghi tiêu đề cột (headings)
        ws.append(headings)
        
        # Ghi dữ liệu
        for row in data:
            ws.append(row)
        
        # Tự động điều chỉnh độ rộng cột (tùy chọn)
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter # Lấy tên cột, ví dụ 'A'
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column].width = adjusted_width

        wb.save(file_path)
        messagebox.showinfo("Thành công", f"Đã xuất thành công danh sách {title} ra:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Lỗi Xuất Excel", f"Lỗi: {e}")