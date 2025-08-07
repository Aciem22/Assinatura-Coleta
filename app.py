import streamlit as st
from utils.assinatura import AssinaturaCanvas
from utils.formulario import FormularioRetirada
from utils.gerador_pdf import GeradorPDF
from utils.drive import upload_pdf_google_drive
import io

st.set_page_config(page_title="Coleta Transportadora", layout="centered")
st.title("📦 Confirmação de Retirada de Pedido")

if "dados_formulario" not in st.session_state:

    form = FormularioRetirada()
    dados = form.exibir_formulario()

    if dados:
        st.session_state["dados_formulario"] = dados
        st.rerun()

else:
    dados = st.session_state["dados_formulario"]
    st.success("✅ Dados do formulário recebidos. Agora colete a assinatura.")

    assinatura = AssinaturaCanvas().capturar_assinatura()

    if assinatura is not None:
            if st.button("📄 Gerar PDF e Enviar para o Google Drive"):
                pdf = GeradorPDF(dados, assinatura)
                pdf_stream = pdf.gerar_pdf()

                # 👉 Upload para o Google Drive
                link_drive = upload_pdf_google_drive(
                    pdf_bytes=pdf_stream, 
                    nome_arquivo=f"comprovante_{dados['pedido']}.pdf"
                )

                st.success("✅ PDF gerado e enviado para o Google Drive com sucesso!")
                st.markdown(f"[📂 Ver no Google Drive]({link_drive})", unsafe_allow_html=True)

    
                st.download_button(
                    label="⬇ Baixar Comprovante",
                    data=pdf_stream,
                    file_name=f"comprovante_{dados['pedido']}.pdf",
                    mime="application/pdf"
                    )

    else:
        st.warning("✍️ Por favor, assine no campo acima.")

        
    if st.button("🔄 Nova Retirada"):
        st.session_state.clear()
        st.rerun()
    
    
