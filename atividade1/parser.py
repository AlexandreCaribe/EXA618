import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def extrair_dados_pagina(url):
    """Extrai título e primeira imagem de uma página HTML"""
    try:
        page = urllib.request.urlopen(url, timeout=5)
        html = str(page.read().decode('utf-8'))
        soup = BeautifulSoup(html, 'lxml')
        
        titulo = soup.title.string if soup.title else "Sem título"
        primeira_imagem = None
        for img in soup.find_all('img'):
            src = img.attrs.get("src")
            if src:
                # Converte URLs relativas para absolutas
                primeira_imagem = urljoin(url, src)
                break
        
        return {
            'url': url,
            'titulo': titulo,
            'imagem': primeira_imagem
        }
    except Exception as e:
        print(f"Erro ao acessar {url}: {str(e)}")
        return None

def gerar_html_agregado(dados_lista):
    """Gera um arquivo HTML com todos os dados agregados"""
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agregado de Alunos - EXA618</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        .card-content {
            padding: 15px;
        }
        .card h2 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 18px;
        }
        .card a {
            color: #0066cc;
            text-decoration: none;
            word-break: break-all;
            font-size: 12px;
        }
        .card a:hover {
            text-decoration: underline;
        }
        .sem-imagem {
            width: 100%;
            height: 200px;
            background-color: #ddd;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
        }
        .total {
            text-align: center;
            margin-top: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>Agregado de Estudantes - EXA618 Atividade 1</h1>
    <div class="container">
"""
    
    for dados in dados_lista:
        if dados:
            html_content += f"""        <div class="card">
"""
            if dados['imagem']:
                html_content += f"""            <img src="{dados['imagem']}" alt="{dados['titulo']}">
"""
            else:
                html_content += f"""            <div class="sem-imagem">Sem Imagem</div>
"""
            html_content += f"""            <div class="card-content">
                <h2>{dados['titulo']}</h2>
                <a href="{dados['url']}" target="_blank">Acessar página</a>
            </div>
        </div>
"""
    
    html_content += f"""    </div>
    <div class="total">
        <p>Total de estudantes: {len([d for d in dados_lista if d])}</p>
    </div>
</body>
</html>
"""
    return html_content

script_dir = os.path.dirname(os.path.abspath(__file__))
seeds_file = os.path.join(script_dir, 'seeds.txt')

urls = []
try:
    with open(seeds_file, 'r') as f:
        urls = [linha.strip() for linha in f.readlines() if linha.strip()]
except FileNotFoundError:
    print(f"Arquivo {seeds_file} não encontrado!")
    exit(1)

print(f"Processando {len(urls)} URLs...")

# Extrai dados de todas as páginas
dados_lista = []
for i, url in enumerate(urls, 1):
    print(f"[{i}/{len(urls)}] Processando: {url}")
    dados = extrair_dados_pagina(url)
    dados_lista.append(dados)

# Gera o arquivo HTML
html_final = gerar_html_agregado(dados_lista)
output_file = os.path.join(script_dir, 'resultado.html')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_final)

print(f"\n✓ Arquivo HTML gerado com sucesso: {output_file}")
print(f"Total de páginas processadas com sucesso: {len([d for d in dados_lista if d])}")
