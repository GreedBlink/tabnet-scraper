import pytest
import os
from rich import print as r_print
from tabnet_scraper.tabnet_driver import TabnetDriver
from tabnet_scraper.schema_components import TabnetComponent,TabnetComponents

URL = 'http://tabnet.datasus.gov.br/cgi/dhdat.exe?PAINEL_ONCO/PAINEL_ONCOLOGIABR.def'

def test_tabnet_scraper():


    component = TabnetComponent(
        id='cancer_de_mama_painel_oncologia',
        row=['Município da residência'],
        column=['Sexo'],
        mesure=['Casos'],
        period=['2023'],
        custom_filters = [
            {'name': 'Diagnóstico Detalhado','values': ['C53 - Neoplasia maligna do colo do útero']},
            {'name': 'Sexo','values': ['Feminino']}
        ]
    )
    os.getcwd()
    scraper = TabnetDriver(
        extractions=TabnetComponents(components = [component]),
        download_dir=os.getcwd()+'/data/'
    )
    
    for result in scraper.extract(URL):
        r_print(result)