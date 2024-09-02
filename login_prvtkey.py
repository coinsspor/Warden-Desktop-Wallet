import tkinter as tk
from tkinter import PhotoImage, messagebox
import bech32
import ecdsa
import hashlib
import mainscreen
import walletaction

def clear_content(root):
    # Mevcut içerikleri temizler
    for widget in root.winfo_children():
        widget.destroy()

def paste_text(entry_widget, root):
    try:
        # Clipboard'tan metin alıp Entry widget'ına yapıştırır
        text = root.clipboard_get()
        entry_widget.insert(tk.END, text)
    except tk.TclError:
        pass  # Clipboard boşsa hata mesajı gösterme

def create_context_menu(root, entry_widget):
    # Sağ tıklama menüsü oluşturur
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Paste", command=lambda: paste_text(entry_widget, root))
    
    # Menüyü yapılandırır
    def show_menu(event):
        menu.post(event.x_root, event.y_root)
    
    entry_widget.bind("<Button-3>", show_menu)  # Sağ tıklama ile menüyü göster

def login_screen(root):
    clear_content(root)

    # Logo ve metin ekleme
    logo_image = PhotoImage(file="logo.png")
    logo_label = tk.Label(root, image=logo_image, bg='#140901')
    logo_label.image = logo_image  # Görsel referansı korumak için bu gerekli
    logo_label.pack(pady=(20, 0))

    title_label = tk.Label(root, text="Please enter your private key", font=("Arial", 14))
    title_label.pack(pady=(10, 20))

    # Özel anahtar için metin kutusu
    prvt_key_entry = tk.Entry(root, font=("Arial", 14), width=50)
    prvt_key_entry.pack(pady=(0, 20))
    prvt_key_entry.bind("<Control-v>", lambda event: paste_text(prvt_key_entry, root))  # Ctrl+V ile yapıştırma işlevini ekle
    create_context_menu(root, prvt_key_entry)  # Sağ tıklama menüsü ekleme

    # Yapıştırma butonu
    paste_button = tk.Button(root, text="Paste", font=("Arial", 10), bg='lightblue', command=lambda: paste_text(prvt_key_entry, root))
    paste_button.pack(pady=(5, 20))

    # Butonlar
    next_button = tk.Button(root, text="Next", font=("Arial", 12), bg='#CAFF94', fg='black', command=lambda: process_private_key(prvt_key_entry.get(), root))
    next_button.pack(fill='x', expand=True, pady=(10, 2))

    back_button = tk.Button(root, text="Back", font=("Arial", 12), bg='#CAFF94', fg='black', command=lambda: mainscreen.show_main_screen(root))
    back_button.pack(fill='x', expand=True, pady=(2, 10))

def process_private_key(private_key_hex, root):
    try:
        # Eğer private key "0x" ile başlıyorsa, bu kısmı kaldır
        if private_key_hex.startswith("0x"):
            private_key_hex = private_key_hex[2:]

        # Warden adresini hesaplama
        warden_address = get_warden_address_from_private_key(private_key_hex)
        if warden_address:
            # walletaction.py'daki wallet_actions fonksiyonunu çağırarak adres bilgilerini göster
            walletaction.wallet_actions(root, warden_address, private_key_hex)
        else:
            messagebox.showerror("Error", "Invalid private key. Please check and try again.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def get_warden_address_from_private_key(private_key_hex):
    try:
        # Hex formatındaki özel anahtarı bytes'a çevirme
        priv_key_bytes = bytes.fromhex(private_key_hex)

        # Özel anahtarın geçerli olup olmadığını kontrol etme
        if len(priv_key_bytes) != 32:
            messagebox.showerror("Error", "Invalid private key length.")
            return None

        # Kamu anahtarını üretme
        sk = ecdsa.SigningKey.from_string(priv_key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        # Sıkıştırılmış public key oluşturma: İlk byte 0x02 veya 0x03 (ilk bit'e bağlı olarak)
        prefix = b'\x02' if vk.pubkey.point.y() % 2 == 0 else b'\x03'
        pub_key_bytes = prefix + vk.to_string()[:32]  # Sıkıştırılmış anahtar

        # Kamu anahtarından adres üretimi
        sha256_bpk = hashlib.sha256(pub_key_bytes).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()

        # Warden adresi oluşturma
        warden_address = bech32.bech32_encode('warden', bech32.convertbits(ripemd160_bpk, 8, 5))
        return warden_address

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate warden address: {str(e)}")
        return None
