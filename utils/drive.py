import streamlit as st
from google.ouath2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io 
import datetime
import json

def upload_pdf_google_drive(pdf_bytes, nome_arquivo):
    info = json.loads(st.secrets["gcp"]["service_account"])
    creds = service_account.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/drive"]
    )

    pasta_principal_id = st.secrets["gcp"]["pasta_id"]

    service = build("drive","v3", credentials=creds)

    data_hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    pasta_query = f"mimeType='application/vnd.google-apps.folder' and name='{data_hoje}' and '{pasta_principal_id}' in parents"
    resposta = service.files().list(q=pasta_query, spaces="drive").execute()
    pastas = resposta.get("files",[])

    if pastas:
        pasta_id = pastas[0]["id"]
    else:
        pasta_metadata = {
            "name": data_hoje,
            "mimeType" : "application/vnd.google-apps.folder",
            "parents" : [pasta_principal_id],
        }
        pasta = service.files().create(body=pasta_metadata, fields = "id").execute()
        pasta_id = pasta["id"]

    media = MediaIoBaseUpload(io.BytesIO(pdf_bytes), mimetype="application/pdf")
    file_metadata ={
        "name": nome_arquivo,
        "parents": [pasta_id],
    }

    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    return f"https://drive.google.com/file/d/{file.get('id')}/view"

