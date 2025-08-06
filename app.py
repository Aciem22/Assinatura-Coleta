import streamlit as st
from utils.assinatura import AssinaturaCanvas
from utils.formulario import FormularioRetirada
from utils.gerador_pdf import GeradorPDF

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
            pdf = GeradorPDF(dados, assinatura)
            pdf_stream = pdf.gerar_pdf()
    
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
    
    