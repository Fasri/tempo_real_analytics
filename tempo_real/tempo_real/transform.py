def transform_tempo_real():

    import pandas as pd
    import glob
    import shutil
    import os
    from datetime import datetime

    # Encontrar o arquivo mais recente na pasta
    list_of_files = glob.glob('consolida_contadoria/data_tempo_real/*.xlsx')
    file_path = max(list_of_files, key=os.path.getctime)

    # Carregar a planilha e excluir a primeira linha
    df = pd.read_excel(file_path)

    # Verificar o número de colunas no DataFrame
    num_colunas = df.shape[1]
    print(f"Número de colunas no DataFrame: {num_colunas}")

    #selecionar colunas 

    df_selected = df[['unidade_judiciaria', 'npu', 'data_entrada_tarefa_atual', 'dias_aguardando_tarefa', 
                    'prioridade', 'lista_prioridades', 'contadoria']]

   


    # Renomear as colunas e reorganizar a ordem
    novas = ['vara', 'processo', 'data', 'dias', 'prioridade', 'lista_prioridades', 'nucleo']
    df_selected.columns = novas[:len(df_selected.columns)]
    df_selected = df_selected[['nucleo','processo', 'vara', 'data', 'dias', 'prioridade', 'lista_prioridades']]

    
    # Função para determinar a prioridade
    def determinar_prioridade(lista_prioridades):
        if pd.isna(lista_prioridades):
            return "Sem prioridade"
        prioridades = lista_prioridades.split(';')
        super_prioridades = ["Pessoa idosa (80+)", "Doença terminal", "Pessoa com deficiência", "Deficiente físico"]
        for prioridade in prioridades:
            if prioridade.strip() in super_prioridades:
                return "Super prioridade"
        return "Prioridade Legal"

    # Criar a nova coluna 'prioridades'
    df_selected['prioridades'] = df_selected['lista_prioridades'].apply(determinar_prioridade)

    df_selected = df_selected.drop(columns=['prioridade','lista_prioridades'])

    df_selected = df_selected.drop_duplicates(subset=['processo', 'data'])

    
    df_selected = df_selected[["nucleo","processo","vara","data","prioridades","dias"]] # Reorganizar as colunas
    df_selected =df_selected.fillna("") # Preencher as celulas vazias com vazio

    # Retirar tudo depois da virgula da coluna dias
    df_selected["dias"] = df_selected["dias"].str.split(",").str[0]

    # Função para tratar a coluna de data
    def formatar_data(data):
        if pd.isna(data):
            return None
        primeira_data = data.split(',')[0].strip().replace("'","")
        data_formatada = pd.to_datetime(primeira_data, format='%d/%m/%Y %H:%M:%S', errors='coerce')
        if data_formatada is pd.NaT:
            return None
        return data_formatada.strftime('%d/%m/%Y')

    # Aplicar a função de formatação de data
    df_selected['data'] = df_selected['data'].apply(formatar_data)

    # Criar um dicionário com as substituições para Contadoria de Cálculos Judiciais
    substituicoes_ccj = {
        '1ª CONTADORIA DE CÁLCULOS JUDICIAIS': '1ª CCJ',
        '2ª CONTADORIA DE CÁLCULOS JUDICIAIS': '2ª CCJ',
        '3ª CONTADORIA DE CÁLCULOS JUDICIAIS': '3ª CCJ',
        '4ª CONTADORIA DE CÁLCULOS JUDICIAIS': '4ª CCJ',
        '5ª CONTADORIA DE CÁLCULOS JUDICIAIS': '5ª CCJ',
        '6ª CONTADORIA DE CÁLCULOS JUDICIAIS': '6ª CCJ'
    }

    # Criar um dicionário com as substituições para Contadoria de Custas
    substituicoes_cc = {
        '1ª CONTADORIA DE CUSTAS': '1ª CC',
        '2ª CONTADORIA DE CUSTAS': '2ª CC',
        '3ª CONTADORIA DE CUSTAS': '3ª CC',
        '4ª CONTADORIA DE CUSTAS': '4ª CC',
        '5ª CONTADORIA DE CUSTAS': '5ª CC',
        '6ª CONTADORIA DE CUSTAS': '6ª CC',
        '7ª CONTADORIA DE CUSTAS': '7ª CC'
    }

    # Combinar os dois dicionários
    todas_substituicoes = {**substituicoes_ccj, **substituicoes_cc}

    # Fazer as substituições
    df_selected['nucleo'] = df_selected['nucleo'].replace(todas_substituicoes)

    # Verificar o resultado
    print("\nValores únicos na coluna Núcleo após as substituições:")
    print(df_selected['nucleo'].unique())

    # Obter os núcleos únicos
    nucleos = sorted(df_selected['nucleo'].unique())

    # Calcular a quantidade de processos por núcleo
    quantidade_processos = df_selected['nucleo'].value_counts().reset_index()
    quantidade_processos.columns = ['nucleo', 'quantidade']
    quantidade_processos['data'] = datetime.now().strftime('%d/%m/%Y')
    quantidade_processos = quantidade_processos[['data', 'nucleo','quantidade']]

    # CONSOLIDADO
    consolidado = df_selected

    # Criar um arquivo Excel com várias abas
    divided_file_path = 'final_tempo_real.xlsx'
    destination_folder = r'data_transform'  # Caminho de destino
    destination_path = f"{destination_folder}\\{divided_file_path}"

   
    # Caminhos dos arquivos finais
    file_path_xlsx = 'Consolidado.xlsx'
    file_path_csv = 'Consolidado.csv'
    destination_xlsx = 'data_transform/Consolidado.xlsx'
    destination_csv = 'data_transform/Consolidado.csv'

    # Certifique-se de que o diretório de destino existe
    os.makedirs(os.path.dirname(destination_xlsx), exist_ok=True)
 
    # Criar e salvar o arquivo Excel
    with pd.ExcelWriter(file_path_xlsx) as writer:
        consolidado.to_excel(writer, sheet_name='CONSOLIDADO', index=False)

    # Salvar o arquivo CSV
    consolidado.to_csv(file_path_csv, index=False, encoding='utf-8')

    # Mover os arquivos para o destino
    shutil.move(file_path_xlsx, destination_xlsx)
    shutil.move(file_path_csv, destination_csv)

    print(f'Arquivos copiados para {destination_xlsx} e {destination_csv}') 


   
    with pd.ExcelWriter(divided_file_path) as writer:
        for nucleo in nucleos:
            # Filtra o DataFrame para o núcleo específico
            df_nucleo = df_selected[df_selected['nucleo'] == nucleo]
            df_nucleo = df_nucleo.sort_values(by='dias')  # Ordenar pela data em ordem crescente

            # Definir um nome padrão se 'nucleo' estiver vazio
            nome_planilha = nucleo if nucleo else "Sem_Nucleo"
            
            # Salva o DataFrame no Excel com o nome da planilha adequado
            df_nucleo.to_excel(writer, sheet_name=nome_planilha, index=False)
    
        # Adicionar a aba 'quantidade'
        quantidade_processos.to_excel(writer, sheet_name='QUANTIDADE', index=False)
        consolidado.to_excel(writer, sheet_name='CONSOLIDADO', index=False)
    # excluir a planilha principal 
    os.remove(file_path)
    #shutil.move(file_path, '/home/felipe/acompamhamento_contadoria/acompamhamento_contadoria/data_backup/' + os.path.basename(file_path))
    # Mover a planilha dividida para a pasta data_transform

    shutil.move(divided_file_path,destination_path)

    # Mensagem de sucesso
    print(f"A tabela modificada foi salva como {divided_file_path}")