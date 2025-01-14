import os

from unidecode import unidecode
from typing import List
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

from .schema_components import TabnetComponents

class TabnetDriver:

    def __init__(self, extractions: TabnetComponents, download_dir:str):


        

# Configurar o ChromeOptions
        options = Options()
        prefs = {
            "download.default_directory": download_dir,  # Diretório de download
            "download.prompt_for_download": False,       # Evitar pop-ups de download
            "download.directory_upgrade": True,         # Atualizar o diretório automaticamente
            "safebrowsing.enabled": True                # Desabilitar proteção para arquivos perigosos
        }
        options.add_experimental_option("prefs", prefs)

        self.download_dir=download_dir
        self.extractions = extractions
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

    @staticmethod
    def select_options(item:str, component: list, driver):
        helpers = {
            'row': 'L',
            'column': 'C',
            'incremet': 'I'
        }
        
    
        item_html_element = Select(driver.find_element(by=By.ID, value=helpers.get(item)) )
        

        lower_components = [unidecode(comp).lower() for comp in component]
        items_to_click = [option for option in item_html_element.options if unidecode(option.text).lower() in lower_components]
    
        
        item_html_element.deselect_all
        for to_select in items_to_click:
            item_html_element.select_by_value(to_select.get_property('value'))
    
        return None 

    @staticmethod
    def select_custom_filters(extraction_filters:List[dict], driver):
        options = driver.find_element(by=By.CLASS_NAME, value='opcoes')
        filters = options.find_elements(by=By.CLASS_NAME, value='titulo_select')
    
        for ft in extraction_filters:
            print(f'Filtrando filtro: {ft["name"]}')
            for custom_filter in filters:
                page_filter = unidecode(custom_filter.find_element(by=By.TAG_NAME, value='label').text)
                if page_filter == unidecode(ft['name']):
            #if aux == 'Diagnostico Detalhado':
                    custom_filter.find_element(by=By.TAG_NAME, value='img').click()
                    select_custom_filter_options = Select(custom_filter.find_element(by=By.CLASS_NAME, value='fundo_select_tabnet'))
                    select_custom_filter_options.deselect_all()
            
                    for filter_value in ft['values']:
                        select_custom_filter_options.select_by_visible_text(filter_value)


        
    
    def extract(self, url:str):

        self.driver.get(url)
        
        self.current_page = self.driver.current_window_handle
        
        for index, component in enumerate(self.extractions.components):
            #row
            self.select_options(item='row', component=component.row,driver= self.driver)
            #col
            self.select_options(item='column', component=component.column,driver=self.driver)
            #mesure
            self.select_options(item='incremet', component=component.mesure,driver=self.driver)
            #custom filters
            self.select_custom_filters(component.custom_filters, self.driver)


            self.driver.find_element(by=By.NAME, value='button1').click()

            tabs = self.driver.window_handles
            for tab in tabs:
                if(tab!=self.current_page):
                    self.driver.switch_to.window(tab)
                    
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT, 'SALVA COMO CSV')))    
            download_button = self.driver.find_element(by=By.LINK_TEXT,value='SALVA COMO CSV')
            download_button.click()
            file_name = download_button.get_attribute('href')           

            print(file_name)
            downloaded_file = os.path.join(self.download_dir, file_name)
            new_name = os.path.join(self.download_dir, component.id+'.csv')

            if os.path.exists(downloaded_file):
                os.rename(downloaded_file, new_name)

            yield {
                "id": component.id,
                "index": index,
                "row": component.row,
                "column": component.column,
                "measure": component.mesure,
                "filters": component.custom_filters,
                "status": True,
                "file_name": file_name
             }
            self.driver.switch_to.window(self.current_page)
            
#        self.driver.quit()
        
    