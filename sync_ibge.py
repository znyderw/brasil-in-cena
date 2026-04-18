import os
import json
import requests
import unicodedata
import random
JSON_PATH = os.path.join('dados', 'regioes.json')
UNSPLASH_TOKEN = os.getenv('UNSPLASH_ACCESS_TOKEN', '')
COLORS_MAP = {
    "Norte": "#2F855A",
    "Nordeste": "#DD6B20",
    "Centro-Oeste": "#D69E2E",
    "Sudeste": "#6B46C1",
    "Sul": "#2B6CB0"
}
def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    return value.lower().replace(' ', '-')
def get_unsplash_image(query):
    if not UNSPLASH_TOKEN:
        defaults = [
            "https://images.unsplash.com/photo-1548405021-399cc11b22e1?q=80&w=2940&auto=format&fit=crop", 
            "https://images.unsplash.com/photo-1581452684877-6262b9a7b93a?q=80&w=2940&auto=format&fit=crop", 
            "https://images.unsplash.com/photo-1588661621379-91ee0b938550?q=80&w=2940&auto=format&fit=crop", 
            "https://images.unsplash.com/photo-1622268710574-1234cb30e1cc?q=80&w=2851&auto=format&fit=crop", 
            "https://images.unsplash.com/photo-1516086749007-df0bc3c8b417?q=80&w=2940&auto=format&fit=crop"  
        ]
        return random.choice(defaults)
    url = 'https://api.unsplash.com/photos/random'
    headers = {"Authorization": f"Client-ID {UNSPLASH_TOKEN}"}
    params = {"query": f"{query} Brasil", "orientation": "landscape"}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["urls"]["regular"]
    except Exception as e:
        print(f"Erro ao buscar Unsplash: {e}")
    return "https://images.unsplash.com/photo-1588661621379-91ee0b938550?q=80&w=2940&auto=format&fit=crop"
def generate_skeleton(slug, region_name):
    print(f"Gerando esqueleto novo para: {region_name}")
    bg_image = get_unsplash_image(region_name)
    cor_tema = COLORS_MAP.get(region_name, "#3182ce")
    return {
        "id": slug,
        "nome": f"Região {region_name}",
        "slug": slug,
        "cor_tema": cor_tema,
        "icone": "fa-solid fa-map-location-dot",
        "imagem_card": bg_image,
        "imagem_card_alt": region_name,
        "descricao_card": f"Descubra as ricas tradições da Região {region_name}.",
        "estados": [],
        "hero": {
            "titulo_prefixo": "Conheça também a",
            "titulo_destaque": f"Região {region_name}",
            "descricao": "Conteúdo editorial em construção. Em breve mais novidades sobre essa rica região.",
            "banner_url": bg_image
        },
        "galeria": [],
        "exibir_galeria": False,
        "video": {},
        "historia": {
            "titulo_prefixo": "Histórias da",
            "titulo_destaque": f"Região {region_name}",
            "paragrafos": []
        },
        "geografia": {
            "titulo_prefixo": "Geografia da",
            "titulo_destaque": f"Região {region_name}",
            "secoes": []
        },
        "cultura": {
            "titulo_prefixo": "Cultura da",
            "titulo_destaque": f"Região {region_name}",
            "paragrafos": []
        },
        "culinaria": {
            "pratos_tipicos": {"subtitulo": "Pratos Típicos", "itens": []},
            "doces_tipicos": {"subtitulo": "Doces Típicos", "itens": []},
            "bebidas_tipicas": {"subtitulo": "Bebidas Típicas", "itens": []}
        },
        "dashboard": {
            "clima": "Em levantamento",
            "qtd_estados": 0,
            "destaque": "Uma das maravilhas do Brasil"
        }
    }
def main():
    print("Iniciando Pipeline de Dados do IBGE...")
    dataset = {}
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'id' in data and data['id'] == 'sul':
                dataset['sul'] = data
            else:
                dataset = data
        except Exception as e:
            print(f"Erro ao ler {JSON_PATH}: {e}. Iniciando dataset vazio.")
    res_regioes = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/regioes')
    regioes_ibge = res_regioes.json()
    for reg_api in regioes_ibge:
        reg_id = reg_api['id']
        nome_ibge = reg_api['nome']
        sigla = reg_api['sigla']
        slug = slugify(nome_ibge)
        if slug not in dataset:
            dataset[slug] = generate_skeleton(slug, nome_ibge)
        else:
            if "cor_tema" not in dataset[slug]:
                 dataset[slug]["cor_tema"] = COLORS_MAP.get(nome_ibge, "#3182ce")
        res_estados = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/regioes/{reg_id}/estados')
        estados_ibge = res_estados.json()
        nomes_estados = sorted([est['nome'] for est in estados_ibge])
        dataset[slug]['ibge_id'] = reg_id
        dataset[slug]['ibge_nome'] = nome_ibge
        dataset[slug]['sigla'] = sigla
        dataset[slug]['estados'] = nomes_estados
        if 'dashboard' not in dataset[slug]:
            dataset[slug]['dashboard'] = {'clima': 'Consulte API de clima futuramente', 'destaque': ''}
        dataset[slug]['dashboard']['qtd_estados'] = len(nomes_estados)
        galeria_real = dataset[slug].get('galeria', [])
        dataset[slug]['exibir_galeria'] = True if len(galeria_real) >= 3 else False
        print(f"[{nome_ibge}] - Upserting metadata: {len(nomes_estados)} estados mapeados. Galeria imersiva: {dataset[slug]['exibir_galeria']}")
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"Pipeline sincronizado com sucesso. Dados persistidos em {JSON_PATH}.")
if __name__ == '__main__':
    main()
