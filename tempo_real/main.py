import streamlit as st
from extract import extract_report_tempo_real 
from transform import transform_tempo_real
import os

def main():
    st.title("Tempo Real Analytics – Extração e processamento de relatórios em tempo real 🚀")

    if st.button("Executar Pipeline"):
        st.write("Iniciando extração de dados...")
        extract_report_tempo_real()
        st.write("Transformação em andamento...")
        file_path = transform_tempo_real()
        st.write("Processo concluído com sucesso! ✅")

        # Verifica se o arquivo final_tempo_real.xlsx foi gerado
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                btn = st.download_button(
                    label="📥 Baixar Arquivo Processado",
                    data=file,
                    file_name="final_tempo_real.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("Clique no botão acima para baixar o arquivo! 🎉")
        else:
            st.error("Erro: O arquivo final_tempo_real.xlsx não foi encontrado! 😢")

if __name__ == "__main__":
    main()
