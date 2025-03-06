from extract import extract_report_tempo_real
from transform import transform_tempo_real
from load import load_tempo_real

def main():
    extract_report_tempo_real()
    transform_tempo_real()
    #load_tempo_real()

if __name__ == "__main__":
    main()  

