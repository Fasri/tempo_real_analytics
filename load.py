def load_tempo_real():
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import pandas as pd

    # Autenticação
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'consolida_contadoria/credentials.json'  # Caminho para o seu arquivo credentials.json

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "consolida_contadoria/credentials.json", SCOPES
        )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # ID da planilha do Google Sheets
    SPREADSHEET_ID = '1-hXLDTxGmDlPgbr_jIq73o49divD75c1jJ6Tbsw61iU'


    # Leitura do arquivo XLS local, incluindo todas as abas
    file_path = 'data_transform/final_tempo_real.xlsx'
    sheets = pd.read_excel(file_path, sheet_name=None)  # Lê todas as abas


    for sheet_name, df in sheets.items():
        # Convertendo DataFrame para lista de listas
        df = df.fillna("")
        values = [df.columns.values.tolist()] + df.values.tolist()
    
        # Preparação dos dados
        body = {
            'values': values
        }         
        
        # Limpeza do conteúdo existente e atualização com novos dados
        range_name = f'{sheet_name}!A1:J6000'  # Define o range para cada aba
        service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW', body=body).execute()

        print(f'{result.get("updatedCells")} células atualizadas na aba {sheet_name}.')