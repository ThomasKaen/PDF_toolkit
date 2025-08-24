from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog
from ..core.services import PDFService
from ..core.models import MergeOptions, SplitOptions, EncryptOptions, DecryptOptions
import tkinter as tk

svc = PDFService()

class PDFToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Toolkit")
        self.root.geometry("500x300")

        # UI
        tk.Button(root, text="Merge PDFs", command=self.merge_ui).pack(pady=10)
        tk.Button(root, text="Split PDF", command=self.split_ui).pack(pady=10)
       # tk.Button(root, text="Compress PDF", command=self.compress_pdf).pack(pady=10)
        tk.Button(root, text="Add Password", command=self.encrypt_pdf).pack(pady=10)
        tk.Button(root, text="Remove Password", command=self.decrypt_pdf).pack(pady=10)

    def merge_ui(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not files: return
        save = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not save: return
        res = svc.merge(MergeOptions(files=[Path(f) for f in files], output_path=Path(save)))
        messagebox.showinfo("Merge", res.message if res.ok else f"Failed: {res.message}")

    def split_ui(self):
        src = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not src: return
        out_dir = filedialog.askdirectory()
        if not out_dir: return

        def ask_pwd():
            return simpledialog.askstring("Password required", "Enter password:", show="*")

        res = svc.split(SplitOptions(src=Path(src), out_dir=Path(out_dir), get_password=ask_pwd))
        messagebox.showinfo("Split", res.message if res.ok else f"Failed: {res.message}")

    def encrypt_pdf(self):
        src = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not src: return
        pwd = simpledialog.askstring("Add password", "Enter password:", show="*")
        if not pwd: return
        save = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not save: return
        try:
            res = svc.encrypt(EncryptOptions(src=Path(src), output_path=Path(save), password=pwd))
            messagebox.showinfo("Encrypt", res.message if res.ok else f"Failed: {res.message}")
        except Exception as e:
            messagebox.showerror("Encrypt", str(e))

    def decrypt_pdf(self):
        src = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not src: return
        pwd = simpledialog.askstring("Remove password", "Enter current password:", show="*")
        if pwd is None: return
        save = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not save: return
        try:
            res = svc.decrypt(DecryptOptions(src=Path(src), output_path=Path(save), password=pwd))
            messagebox.showinfo("Decrypt", res.message if res.ok else f"Failed: {res.message}")
        except Exception as e:
            messagebox.showerror("Decrypt", str(e))

def main():
    root = tk.Tk()
    app = PDFToolkitApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()