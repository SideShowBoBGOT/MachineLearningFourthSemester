import os
import string
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


# constants
notebook_path = 'main.ipynb'
class_attribute = 'class'
jp_cell = 'jp-Cell'
jp_markdown_cell = 'jp-MarkdownCell'
jp_code_cell = 'jp-CodeCell'
jp_rendered_markdown = 'jp-RenderedMarkdown'
notebook_path = 'file:///home/choleraplague/university/MachineLearning/Lab1/some.html'

#tags
h1 = 'h1'
h2 = 'h2'
h3 = 'h3'
p = 'p'
png = '.png'
tag = 'tag'
inner_text = 'inner_text'

# init driver
options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options)

def get_random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


#parse notebook
index = 1
tree = []
driver.get(url=notebook_path)
html_cells = driver.find_elements(By.CLASS_NAME, jp_cell)
for c in html_cells:
    class_name = c.get_attribute(class_attribute)
    class_name_parts = class_name.split(' ')
    if jp_markdown_cell in class_name_parts:
        rendered = c.find_element(By.CLASS_NAME, jp_rendered_markdown)
        heading = rendered.find_element(By.XPATH, '*')
        tag_attr = heading.tag_name
        if tag_attr == h1:
            tree.append(
                {'text': heading.text, 'children': []})
        elif tag_attr == h2:
            tree[-1]['children'].append(
                {'text': heading.text, 'children': []})
        elif tag_attr == h3 or tag_attr == p:
            tree[-1]['children'][-1]['children'].append(heading.text)
    elif jp_code_cell in class_name_parts:
        name = str(index) + png
        index += 1
        c.screenshot(name)
        tree[-1]['children'][-1]['children'].append(name)


from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import paragraphs


document = Document()
for section in document.sections:
    section.left_margin = Inches(0.98)
    section.right_margin = Inches(0.59)
    section.top_margin = Inches(0.49)
    section.bottom_margin = Inches(0.59)

paragraph_format = document.styles['Normal'].paragraph_format
paragraph_format.line_spacing = 1.5
paragraph_format.first_line_indent = Inches(0.492)

for head_one in tree:
    heading_one = document.add_heading(' '.join(head_one['text'].split(' ')[1:]), 1)
    heading_one.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    for head_two in head_one['children']:
        heading_two = document.add_heading(' '.join(head_two['text'].split(' ')[1:]), 2)
        heading_two.is_linked_to_previous = True
        ex_text = document.add_paragraph()
        ex_text.text = head_two['children'][0]
        picture_para = document.add_paragraph()
        picture_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        picture_run = picture_para.add_run()
        picture_run.add_picture(head_two['children'][1])
        picture_para.add_run('\n' + head_two['children'][2])



# para = document.add_paragraph()
# picture_run = para.add_run()
# picture_run.add_picture('index.png')
# para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
# para.add_run('\nImage Text')
# para = document.add_heading('3 Виконання', 1)
# para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


document.save('test.docx')
    
    


        


        
