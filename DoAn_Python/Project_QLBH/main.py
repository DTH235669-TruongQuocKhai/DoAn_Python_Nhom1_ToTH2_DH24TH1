# main.py

import tkinter as tk 
from tkinter import ttk, messagebox
# Import các hàm tiện ích
from db_utility import center_window
# Import các hàm setup từ từng tab
from tab_baihat import setup_baihat_tab
from tab_casi import setup_casi_tab
from tab_theloai import setup_theloai_tab
from tab_album import setup_album_tab

# ===================== HÀM CHÍNH: KHỞI TẠO GIAO DIỆN =====================

root = tk.Tk() 
root.title("Hệ thống Quản lý Bài hát") 
center_window(root, 900, 650) 
root.resizable(False, False) 
 
lbl_title = tk.Label(root, text="HỆ THỐNG QUẢN LÝ BÀI HÁT", font=("Arial", 16, "bold")) 
lbl_title.pack(pady=10) 

# Khởi tạo Notebook (Giao diện đa tab)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, fill="both", expand=True)

# Khai báo các frame cho từng tab
tab_bh = ttk.Frame(notebook)
tab_cs = ttk.Frame(notebook)
tab_tl = ttk.Frame(notebook)
tab_ab = ttk.Frame(notebook)

# Gán tab vào Notebook theo thứ tự Index 0, 1, 2, 3
notebook.add(tab_bh, text='🎵 Bài Hát')  # Index 0
notebook.add(tab_cs, text='🎤 Ca Sĩ')  # Index 1
notebook.add(tab_tl, text='🎭 Thể Loại')  # Index 2
notebook.add(tab_ab, text='💿 Album')  # Index 3

# ===================== THÊM CHỨC NĂNG MENU =====================

def switch_tab(index):
    """Chuyển sang tab tương ứng theo index."""
    notebook.select(index)

# 1. Tạo Menu Bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# 2. Tạo Menu "Menu" (hoặc "File")
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=file_menu)

# 3. Thêm các lệnh chuyển tab vào Menu
file_menu.add_command(label="🎵 Bài Hát", command=lambda: switch_tab(0))
file_menu.add_command(label="🎤 Ca Sĩ", command=lambda: switch_tab(1))
file_menu.add_command(label="🎭 Thể Loại", command=lambda: switch_tab(2))
file_menu.add_command(label="💿 Album", command=lambda: switch_tab(3))

# Thêm đường phân cách và nút Thoát
file_menu.add_separator()
file_menu.add_command(label="Thoát", command=root.quit)

# ===================== GỌI HÀM SETUP CHO TỪNG TAB =====================

setup_baihat_tab(tab_bh, root)
setup_casi_tab(tab_cs, root)
setup_theloai_tab(tab_tl, root)
setup_album_tab(tab_ab, root)

root.mainloop()