import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.sample_tools import init

def upload_to_drive(folder_path):
    # Reutiliza a autenticação que você já configurou para o Blogger
    # Adicione o escopo do Drive na sua configuração original
    scope = ['https://www.googleapis.com/auth/drive.file']
    
    # Inicializa o serviço do Drive
    # (Pode usar o sample_tools como você já faz no projeto)
    service, _ = init(
        ["--noauth_local_webserver"], "drive", "v3", __doc__, __file__,
        scope=scope
    )

    # 1. Cria a pasta no Drive (ou busca se já existir)
    file_metadata = {
        'name': 'Blog_Archive_2026',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder.get('id')

    # 2. Faz o upload de cada .docx
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            print(f"Subindo {filename} para o Drive...")
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            media = MediaFileUpload(
                os.path.join(folder_path, filename),
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"Sucesso! Todos os arquivos estão na pasta ID: {folder_id}")
    return folder_id

upload_to_drive("docao_2026-04-07")