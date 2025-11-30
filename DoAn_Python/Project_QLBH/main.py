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
root.title("Hệ thống Quản lý Âm nhạc Đa Tab") 
center_window(root, 900, 650) # Hàm này được gọi từ db_utility
root.resizable(False, False) 
 
lbl_title = tk.Label(root, text="HỆ THỐNG QUẢN LÝ ÂM NHẠC", font=("Arial", 16, "bold")) 
lbl_title.pack(pady=10) 

# Khởi tạo Notebook (Giao diện đa tab)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, fill="both", expand=True)

# Khai báo các frame cho từng tab
tab_bh = ttk.Frame(notebook)
tab_cs = ttk.Frame(notebook)
tab_tl = ttk.Frame(notebook)
tab_ab = ttk.Frame(notebook)

notebook.add(tab_bh, text='🎵 Bài Hát')
notebook.add(tab_cs, text='🎤 Ca Sĩ')
notebook.add(tab_tl, text='🎭 Thể Loại')
notebook.add(tab_ab, text='💿 Album')

# Gọi hàm setup_tab cho từng tab (Truyền root vào để các tab có thể gọi root.quit)
setup_baihat_tab(tab_bh, root)
setup_casi_tab(tab_cs, root)
setup_theloai_tab(tab_tl, root)
setup_album_tab(tab_ab, root)

root.mainloop()