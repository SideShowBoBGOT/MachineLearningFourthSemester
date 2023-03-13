import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# constants
notebook_path = 'main.ipynb'
class_attribute = 'class'
jp_cell = 'jp-Cell'
jp_markdown_cell = 'jp-MarkdownCell'
notebook_path = 'file:///home/choleraplague/university/MachineLearning/Lab1/some.html'

# init driver
options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options)

#parse notebook
driver.get(url=notebook_path)
cells = driver.find_elements(By.CLASS_NAME, jp_cell)
for c in cells:
    class_name = c.get_attribute(class_attribute)
    class_name_parts = class_name.split(' ')
    if jp_markdown_cell in class_name_parts:
        
