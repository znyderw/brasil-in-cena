import json 
import os
import re
import shutil
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = 'dados'
OUTPUT_ROOT = 'site'
OUTPUT_PAGES = os.path.join(OUTPUT_ROOT, 'src', 'assets', 'pages')

def minify_html(html_str):
    return re.sub(r'>\s+<', '><', html_str.strip())

def gerar_site():
    print("🚀 Iniciando Build do Projeto 'Brasil In Cena'...")
    
    assets_src = 'assets'
    assets_dest = os.path.join(OUTPUT_ROOT, 'src', 'assets', 'styles')
    
    if os.path.exists(assets_src):
        if os.path.exists(assets_dest):
            shutil.rmtree(assets_dest)
        os.makedirs(os.path.dirname(assets_dest), exist_ok=True)
        shutil.copytree(assets_src, assets_dest)
    
    os.makedirs(OUTPUT_PAGES, exist_ok=True)
    
    json_path = os.path.join(TEMPLATE_DIR, 'regioes.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            dados_regioes = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar regioes.json: {e}")
        return

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR, encoding='utf-8'))
    
    try:
        template_index = env.get_template('index.html')
        html_index = template_index.render(root_path="./")
        html_index = minify_html(html_index)
        with open(os.path.join(OUTPUT_ROOT, 'index.html'), "w", encoding='utf-8') as f:
            f.write(html_index)
        print("✅ index.html gerado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao gerar index.html: {e}")

    template_regiao = env.get_template('base_regiao.html')
    for slug, info in dados_regioes.items():
        try:
            html_final = template_regiao.render(regiao=info, root_path="../../../")
            html_final = minify_html(html_final)
            
            file_path = os.path.join(OUTPUT_PAGES, f"{slug}.html")
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(html_final)
        except Exception as e:
            print(f"❌ Erro ao gerar página da região {slug}: {e}")

    for page in ['sobre.html', 'contato.html', 'qr.html']:
        try:
            template_page = env.get_template(page)
            html_page = template_page.render(root_path="../../../")
            html_page = minify_html(html_page)
            
            file_path = os.path.join(OUTPUT_PAGES, page)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(html_page)
            print(f"✅ Página [{page}] gerada.")
        except Exception as e:
            print(f"❌ Erro ao gerar página {page}: {e}")

    print(f"\n✨ Build concluído com sucesso em: {OUTPUT_ROOT}")

if __name__ == "__main__":
    gerar_site()
