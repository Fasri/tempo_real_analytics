def extract_report_tempo_real():
    import time
    
    from selenium import webdriver
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    fp = Options()

    fp.add_argument("--headless") # executar sem o browser aparecer
    fp.set_preference("browser.download.folderList", 2)  # 2 indica uma pasta personalizada
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", r"C:\Users\lipea\Documents\contadoria\consolida_contadoria\data_tempo_real")  # Substitua pelo caminho da sua pasta
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")  # Tipo de arquivo XLS

    servico = Service(GeckoDriverManager().install())

    navegador = webdriver.Firefox(options=fp,service=servico)

    navegador.get("https://www.tjpe.jus.br/tjpereports/xhtml/login.xhtml")

    time.sleep(3)

    navegador.find_element('xpath','//*[@id="j_id5:cpf"]').send_keys("06016077402")

    navegador.find_element('xpath','/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/input').send_keys("282309CiLuBi*")

    navegador.find_element('xpath',
                        '/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td/input[1]').click()

    time.sleep(10)
    navegador.find_element('xpath', '/html/body/div/div/div/div/div[9]/div/form/div[2]/div[2]/table/tbody/tr[1]/td[2]/input').send_keys("PJe 1º Grau | Acervo em Tramitação em tempo real d")
    time.sleep(8)
    navegador.find_element('xpath', '//*[@id="relatorioForm:pesquisarButton"]').click()
    time.sleep(8)
    navegador.find_element('xpath', '/html/body/div/div/div/div/div[9]/div/form/table/tbody/tr/td[7]/table/tbody/tr/td/a/img').click()
    time.sleep(8)
    navegador.find_element('xpath', '//*[@id="filtroRelatorioForm:GRUPO"]').send_keys("TODAS")
    time.sleep(4)
    navegador.find_element('xpath', '//*[@id="filtroRelatorioForm:ORGAO"]').send_keys("TODOS")
    time.sleep(4)
    navegador.find_element('xpath', '//*[@id="filtroRelatorioForm:j_id95:0"]').click()
    time.sleep(4)
    navegador.find_element('xpath', '//*[@id="filtroRelatorioForm:j_id102:1"]').click()
    time.sleep(4)

    navegador.find_element('xpath', '//*[@id="filtroRelatorioForm:btnExportarXlsx"]').click()

    time.sleep(80)

    navegador.close()