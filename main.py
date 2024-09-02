import tkinter as tk
from tkinter import ttk

def on_close():
    root.destroy()

def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_move(event):
    x = (event.x_root - root.x)
    y = (event.y_root - root.y)
    root.geometry(f"+{x}+{y}")

def main():
    global root
    root = tk.Tk()
    root.geometry("600x850")
    root.configure(background='#140901')

    # Varsayılan başlık çubuğunu kaldır
    root.overrideredirect(True)

    # Özel başlık çubuğu
    title_bar = tk.Frame(root, bg='#CAFF94', relief='raised', bd=2)
    title_bar.pack(side='top', fill='x')

    # Başlık etiketini ekle
    title_label = tk.Label(title_bar, text="Warden Desktop Wallet", bg='#CAFF94', fg='black')
    title_label.pack(side='left', padx=10)

    # Kapatma butonu
    close_button = ttk.Button(title_bar, text="X", command=on_close)
    close_button.pack(side='right')

    # Taşıma işlevi ekle
    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<B1-Motion>", on_move)
    title_bar.bind("<ButtonRelease-1>", stop_move)

    # Ana içerik alanı
    main_frame = tk.Frame(root, bg='#140901')
    main_frame.pack(expand=True, fill='both')

    # Ana ekran içeriğini yükle
    import mainscreen
    mainscreen.show_main_screen(main_frame)  # Ana ekranı göster

    root.mainloop()

if __name__ == "__main__":
    main()
