import tkinter as tk
from tkinter import messagebox
import bech32
import cosmospy
import mainscreen
import walletaction

def clear_content(root):
    for widget in root.winfo_children():
        widget.destroy()

def generate_warden_wallet():
    try:
        # Cüzdan oluşturuluyor
        wallet = cosmospy.generate_wallet()
        private_key_hex = wallet["private_key"].hex()
        
        # Adresin doğru bir şekilde warden formatına dönüştürülmesi
        warden_address = convert_address(wallet["address"], "warden")
        
        return private_key_hex, warden_address
    except Exception as e:
        # Hata durumunda kullanıcıyı bilgilendirme
        messagebox.showerror("Error", f"Wallet generation failed: {str(e)}")
        return None, None

def convert_address(cosmos_address, new_prefix):
    try:
        # Adres decode edilip yeni prefix ile encode ediliyor
        _, data = bech32.bech32_decode(cosmos_address)
        if data is None:
            raise ValueError("Invalid address format")  # Geçersiz adres
        warden_address = bech32.bech32_encode(new_prefix, data)
        return warden_address
    except Exception as e:
        # Hata durumunda kullanıcıyı bilgilendirme
        messagebox.showerror("Error", f"Address conversion failed: {str(e)}")
        return None

def create_new_wallet(root):
    clear_content(root)
    frame = tk.Frame(root, bg='#140901')
    frame.pack(fill='both', expand=True)

    # Logo ekleniyor
    logo = tk.PhotoImage(file="logo.png")
    logo_label = tk.Label(frame, image=logo, bg='#140901')
    logo_label.image = logo  # Logo görselini saklamak için bu gerekli
    logo_label.pack(pady=(20, 0))

    # Geliştirici bilgisi
    developer_info_label = tk.Label(frame, text="This application is developed by Coinsspor", font=('Arial', 10), bg='#140901', fg='white')
    developer_info_label.pack(pady=(0, 20))

    # Cüzdan oluşturma
    priv_key, warden_address = generate_warden_wallet()

    if not priv_key or not warden_address:
        # Hata oluştuysa işlem durduruluyor
        messagebox.showerror("Error", "Failed to create a new wallet. Please try again.")
        return

    # Global değişkenlere cüzdan bilgilerini ve private key'i aktar
    walletaction.warden_address = warden_address
    walletaction.private_key = priv_key

    # Stil ayarları
    label_style = {'font': ('Arial', 12), 'bg': '#140901', 'fg': 'white', 'anchor': 'center'}
    title_style = {**label_style, 'font': ('Arial', 12, 'bold', 'underline')}

    # Private Key ve Warden Address gösterimi
    tk.Label(frame, text="Private Key:", **{**title_style, 'fg': 'blue'}).pack(fill='x')
    tk.Label(frame, text=priv_key, **label_style).pack(fill='x')

    tk.Label(frame, text="Warden Address:", **{**title_style, 'fg': 'orange'}).pack(fill='x')
    tk.Label(frame, text=warden_address, **label_style).pack(fill='x')

    # Copy Information Butonu
    copy_button = tk.Button(frame, text="Copy Information", bg='#CAFF94', fg='black', font=('Arial', 14, 'bold'), command=lambda: copy_info(root, priv_key, warden_address))
    copy_button.pack(fill='x', pady=10)

    # Back Butonu
    back_button = tk.Button(frame, text="Back", bg='#CAFF94', fg='black', font=('Arial', 14, 'bold'), command=lambda: mainscreen.show_main_screen(root))
    back_button.pack(side='left', fill='x', expand=True, padx=20, pady=20)

    # Next Butonu
    next_button = tk.Button(frame, text="Next", bg='#CAFF94', fg='black', font=('Arial', 14, 'bold'), command=lambda: walletaction.wallet_actions(root, warden_address, priv_key))
    next_button.pack(side='right', fill='x', expand=True, padx=20, pady=20)

def copy_info(root, priv_key, warden_address):
    # Bilgiler panoya kopyalanıyor
    info_text = f"Private Key: {priv_key}\nWarden Address: {warden_address}"
    root.clipboard_clear()
    root.clipboard_append(info_text)
    messagebox.showinfo("Copied", "Wallet information copied to clipboard!")
