import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
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
        # 1) pick ONE source PDF
        src = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not src:
            return

        # 2) open (and handle encryption if needed)
        try:
            reader = PdfReader(src)
            if getattr(reader, "is_encrypted", False):
                pwd = simpledialog.askstring("Password required", "Please enter your password")
                if not pwd:
                    messagebox.showwarning("Warning", "No password entered")
                    return
                ok = reader.decrypt(pwd)
                if ok == 0:
                    messagebox.showerror("Error", "Wrong password")
                    return
        except Exception as e:
            messagebox.showerror("Error", f"Could not open PDF:\n{e}")
            return

        pages = len(reader.pages)
        if pages == 0:
            messagebox.showerror("Error", "PDF has 0 pages (or could not be read)")
            return

        # 3) choose output folder
        out_dir = filedialog.askdirectory(title="Select output folder for split pages")
        if not out_dir:
            return

        # 4) write one file per page
        base = os.path.splitext(os.path.basename(src))[0]
        written = 0
        try:
            for i in range(pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                out_path = os.path.join(out_dir, f"{base}_page_{i+1}.pdf")
                with open(out_path, "wb") as f:
                    writer.write(f)
                written += 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed while writing pages:\n{e}")
            return

        messagebox.showinfo("Success", f"PDFs split into {written} pages.\nSaved in: {out_dir}")


    def compress_pdf(self):
        messagebox.showinfo("Coming soon", "Compression is a placeholder (uses Ghostscript).")

    def encrypt_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
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
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
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





