from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
import io

class GeradorPDF:
    def __init__(self, dados, assinatura_array):
        self.dados = dados
        self.assinatura = Image.fromarray(assinatura_array.astype("uint8"))

    def gerar_pdf(self):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        c.setFont("Helvetica", 12)
        c.drawString(50, 800, "📄 Comprovante de Retirada")
        c.drawString(50, 770, f"Transportadora: {self.dados['transportadora']}")
        c.drawString(50, 750, f"Motorista: {self.dados['motorista']}")
        c.drawString(50, 730, f"CPF:{self.dados['cpf']}")
        c.drawString(50, 710, f"Número do Pedido: {self.dados['pedido']}")
        c.drawString(50, 690, f"Data da Retirada: {self.dados['data'].strftime('%d/%m/%Y')}")

        assinatura_path = "assinatura_temp.png"
        self.assinatura.save(assinatura_path)
        c.drawImage(assinatura_path, 50, 620, width=200, height=60)
        c.drawString(50, 600, "Assinatura")

        c.save()
        buffer.seek(0)
        return buffer
