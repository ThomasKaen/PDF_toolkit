import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter


class PDFToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Toolkit")
        self.root.geometry("500x300")

        # UI
        tk.Button(root, text="Merge PDFs", command=self.merge_pdfs).pack(pady=10)
        tk.Button(root, text="Split PDF", command=self.split_pdf).pack(pady=10)
        tk.Button(root, text="Compress PDF", command=self.compress_pdf).pack(pady=10)
        tk.Button(root, text="Add Password", command=self.encrypt_pdf).pack(pady=10)
        tk.Button(root, text="Remove Password", command=self.decrypt_pdf).pack(pady=10)

    def merge_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not files:
            return
        writer = PdfWriter()
        for f in files:
            reader = PdfReader(f)
            for page in reader.pages:
                writer.add_page(page)
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if save_path:
            with open(save_path, "wb") as out:
                writer.write(out)
            messagebox.showinfo("Success", "PDF merged successfully!")

    def split_pdf(self):
        file = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not file:
            return
        reader = PdfReader(file)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.addPage(page)
            out_name =f"page_{i+1}.pdf"
            with open(out_name, "wb") as out:
                writer.write(out)
        messagebox.showinfo("Success", "PDF split into individual pages!")

    def compress_pdf(self):
        messagebox.showinfo("Coming soon", "Compression is a placeholder (uses Ghostscript).")

    def encrypt_pdf(self):
        file = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not file:
            return
        reader = PdfReader(file)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        password = "1234" # could later ask user
        writer.encrypt(password)
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if save_path:
            with open(save_path, "wb") as out:
                writer.write(out)
            messagebox.showinfo("Success", f"PDF encrypted with password '{password}'!")

    def decrypt_pdf(self):
        file = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not file:
            return
        password = "1234" # could ask user later
        reader = PdfReader(file)
        if reader.is_encrypted:
            reader.decrypt(password)
        writer = PdfWriter()
        for page in reader.pages:
            writer.addPage(page)
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if save_path:
            with open(save_path, "wb") as out:
                writer.write(out)
            messagebox.showinfo("Success", "Password removed")

def main():
    root = tk.Tk()
    app = PDFToolkitApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()





