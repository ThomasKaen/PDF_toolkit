from reportlab.pdfgen import canvas

for i in range(1, 4):
    c = canvas.Canvas(f"test_file_{i}.pdf")
    c.drawString(100, 750, f"Hello World. This is test pdf #{i}")
    c.save()