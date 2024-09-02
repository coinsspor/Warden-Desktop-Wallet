import tkinter as tk
import newwallet
from login_prvtkey import login_screen  # login_prvtkey.py dosyasından fonksiyonu import ediyoruz

def clear_content(root):
    for widget in root.winfo_children():
        widget.destroy()

def show_main_screen(root):
    clear_content(root)
    app_info_label = tk.Label(root, text="Warden Desktop Wallet v1.0", font=('Arial', 20), bg='#140901', fg='white')
    app_info_label.pack()

    logo = tk.PhotoImage(file="logo.png")
    logo_label = tk.Label(root, image=logo, bg='#140901')
    logo_label.image = logo  # referansı korumak için
    logo_label.pack(pady=(20, 10))

    # Slogan görüntüsünü ekleyin
    slogan = tk.PhotoImage(file="slogan.png")
    slogan_label = tk.Label(root, image=slogan, bg='#140901')
    slogan_label.image = slogan  # Referansı tutmak için
    slogan_label.pack(pady=(10, 20))

    developer_info_label = tk.Label(root, text="This application is developed by Coinsspor", font=('Arial', 10), bg='#140901', fg='white')
    developer_info_label.pack()

    frame = tk.Frame(root, bg='#140901')
    frame.pack(fill='both', expand=True)

    create_wallet_button = tk.Button(frame, text="Create a New Wallet", bg='#CAFF94', fg='black', font=('Arial', 14, 'bold'), command=lambda: newwallet.create_new_wallet(root))
    create_wallet_button.pack(fill='x', expand=True, padx=20, pady=(50, 10))

    login_private_key_button = tk.Button(frame, text="Login in With a private key", bg='#CAFF94', fg='black', font=('Arial', 14, 'bold'), command=lambda: login_screen(root))
    login_private_key_button.pack(fill='x', expand=True, padx=20, pady=(10, 50))
