import json 
import os
import re
from jinja2 import Environment, FileSystemLoader
def minify_html(html_str):
    return html_str.strip()
def fix_lazy_images(html_str):
    return html_str
def gerar_site():
    print("Iniciando Build Site...")
    json_path = os.path.join('dados', 'regioes.json')
    template_dir = 'dados'
    output_dir_pages = 'site/src/assets/pages'
    output_dir_root = 'site'
    os.makedirs(output_dir_pages, exist_ok=True)
    with open(json_path, 'r', encoding='utf-8') as f:
        dados_regioes = json.load(f)
    env = Environment(loader=FileSystemLoader(template_dir, encoding='utf-8'))
    template_index = env.get_template('index.html')
    html_index = template_index.render(root_path="")
    html_index = minify_html(fix_lazy_images(html_index))
    with open(os.path.join(output_dir_root, 'index.html'), "w", encoding='utf-8') as f:
        f.write(html_index)
    print("✅ Página Home [index.html] gerada com sucesso!")
    template_regiao = env.get_template('base_regiao.html')
    for slug, info in dados_regioes.items():
        html_final = template_regiao.render(regiao=info, root_path="../../../")
        html_final = fix_lazy_images(html_final)
        html_final = minify_html(html_final)
        file_path = os.path.join(output_dir_pages, f"{slug}.html")
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(html_final)
        print(f"✅ Página otimizada [{info.get('nome', slug)}] gerada com sucesso!")
    for page in ['sobre.html', 'contato.html']:
        template_page = env.get_template(page)
        html_page = template_page.render(root_path="../../../")
        html_page = minify_html(fix_lazy_images(html_page))
        file_path = os.path.join(output_dir_pages, page)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(html_page)
        print(f"✅ Página [{page}] gerada com sucesso!")
    print(f"Processo concluído no diretório: {output_dir_root}")
if __name__ == "__main__":
    gerar_site()
