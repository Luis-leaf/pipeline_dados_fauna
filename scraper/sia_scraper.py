import pprint
import time
from pathlib import Path

from fauna_db import FaunaDb
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select


class SiaScraper:
    def __init__(self):
        self.logger = self.setup_logging()
        self.driver: WebDriver = self.config_webdriver()
        self.dict_fauna: dict = {}
        self.base_dados = FaunaDb()

    def setup_logging(self):
        import logging

        log_dir = Path(__file__).resolve().parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "scraper.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_file, encoding="utf-8"),
            ],
        )
        return logging.getLogger("sia_scraper")

    def config_webdriver(self, list_options: tuple | None = None) -> WebDriver:
        options = Options()

        if list_options:
            for op in list_options:
                options.add_argument(f"--{op}")

            driver = webdriver.Chrome(options=options)
            self.logger.info("opções do navegador configuradas")
            return driver

        return webdriver.Chrome()

    def access_search_page(self):
        self.driver.get("https://celepar7.pr.gov.br/sia/licenciamento/consulta/con_licenca.asp")

        time.sleep(2)

    def search_city(self):
        city_select = self.driver.find_element(By.ID, "cb_municipio")
        select = Select(city_select)

        for options in select.options:
            if options.text == "-- selecione --":
                continue

            text = options.text
            select.select_by_visible_text(text)
            self.search()

    def search(self):
        button_search = self.driver.find_element(By.CLASS_NAME, "form_botao")
        button_search.click()
        time.sleep(3)
        self.capture_info()

    def capture_info(self):
        try:
            next_page = 0
            while next_page == 0:
                result_div = self.driver.find_element(By.ID, "conteudo_ajax")
                div_table = result_div.find_element(By.ID, "conteudo_corpo")
                table = div_table.find_element(By.ID, "list_tabela")
                table_rows = table.find_elements(By.XPATH, ".//tr[td]")
                time.sleep(3)

                for row in table_rows:
                    list_info = []
                    columns = row.find_elements(By.TAG_NAME, "td")
                    list_info = [column.text for column in columns if column.text]
                    # self.logger.info("colunas capturadas: %s", len(list_info))
                    self.process_info(list_info)

                try:
                    next_button = self.driver.find_element(
                        By.XPATH, "//a[contains(@href,'Proximo()')]"
                    )
                    next_button.click()
                    time.sleep(3)

                except Exception:
                    next_page = 1

        except Exception:
            pass

    def process_info(self, info: list):
        self.dict_fauna = {}
        if info[6].lower() not in (
            "salvamento, resgate e destinação de fauna",
            "monitoramento de fauna",
            "levantamento de fauna",
        ):
            self.logger.info("Não é AA de fauna %s", info[6].lower())
            return

        if self.base_dados.exists_by_protocolo(info[3]):
            self.logger.info(f"já esta salvo no banco, protocolo: {info[3]}")
            return

        if len(info) == 12:
            self.dict_fauna = {
                "regional": info[0],
                "municipio": info[1],
                "tipo": info[2],
                "protocolo": info[3],
                "formulario": info[4],
                "numero_licenca": info[5],
                "atividade": info[6],
                "emissao": info[7],
                "vencimento": info[8],
                "empreendedor": info[9],
                "empreendimento": info[10],
                "bacia_hidrografica": info[11],
            }
            pprint.pp(self.dict_fauna)
            id_aa = self.base_dados.insert_dict_fauna(self.dict_fauna)
            self.logger.info(f"AA inserida no banco com sucesso: ID {id_aa}")
        return

    def main(self):
        self.access_search_page()
        self.search_city()


if __name__ == "__main__":
    scraper = SiaScraper()
    scraper.main()
