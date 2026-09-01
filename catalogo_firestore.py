# ============================================================
#  CATÁLOGO DE PRODUTOS — Firebase Firestore (Python)
#  Banco de Dados Não Relacional — FATEC Cotia
# ============================================================
#
#  INSTALAÇÃO:
#    pip install firebase-admin
#
#  CONFIGURAÇÃO:
#    1. Firebase Console → Configurações do projeto → Contas de serviço
#    2. Clique em "Gerar nova chave privada" → baixe o arquivo JSON
#    3. Coloque o arquivo JSON na mesma pasta que este script
#    4. Atualize a variável CREDENCIAL_JSON abaixo
#
# ============================================================

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# ── Configuração ─────────────────────────────────────────────
CREDENCIAL_JSON = "serviceAccountKey.json"  # <- nome do seu arquivo baixado

# ── Conectar ao Firestore ─────────────────────────────────────
cred = credentials.Certificate(CREDENCIAL_JSON)
firebase_admin.initialize_app(cred)
db = firestore.client()

COLECAO = "produtos"  # nome da coleção no Firestore


# ============================================================
#  CRUD — Funções principais
# ============================================================

def criar_produto(nome, preco, categoria, estoque, descricao=""):
    """CREATE — Adiciona um novo documento na coleção 'produtos'"""
    produto = {
        "nome": nome,
        "preco": preco,
        "categoria": categoria,
        "estoque": estoque,
        "descricao": descricao,
        "criado_em": datetime.now().isoformat()
    }
    # O Firestore gera o ID automaticamente (sem schema fixo!)
    ref = db.collection(COLECAO).add(produto)
    print(f"✅ Produto criado! ID: {ref[1].id}")
    return ref[1].id


def listar_produtos(categoria=None):
    """READ — Busca todos os documentos da coleção"""
    query = db.collection(COLECAO)

    # Filtro opcional por categoria
    if categoria:
        query = query.where("categoria", "==", categoria)

    docs = query.stream()
    produtos = []
    print(f"\n{'─'*55}")
    print(f"{'ID':<22} {'Nome':<20} {'Preço':>8}  {'Estoque':>7}")
    print(f"{'─'*55}")
    for doc in docs:
        p = doc.to_dict()
        p["id"] = doc.id
        produtos.append(p)
        print(f"{doc.id:<22} {p['nome']:<20} R${p['preco']:>7.2f}  {p['estoque']:>7}")
    print(f"{'─'*55}")
    print(f"Total: {len(produtos)} produto(s)\n")
    return produtos


def buscar_produto(produto_id):
    """READ — Busca um único documento pelo ID"""
    doc = db.collection(COLECAO).document(produto_id).get()
    if doc.exists:
        p = doc.to_dict()
        print(f"\n📦 Produto encontrado:")
        for chave, valor in p.items():
            print(f"   {chave}: {valor}")
        return p
    else:
        print(f"❌ Produto '{produto_id}' não encontrado.")
        return None


def atualizar_produto(produto_id, **campos):
    """UPDATE — Atualiza campos específicos de um documento"""
    campos["atualizado_em"] = datetime.now().isoformat()
    db.collection(COLECAO).document(produto_id).update(campos)
    print(f"✅ Produto '{produto_id}' atualizado: {campos}")


def deletar_produto(produto_id):
    """DELETE — Remove um documento da coleção"""
    db.collection(COLECAO).document(produto_id).delete()
    print(f"🗑️  Produto '{produto_id}' removido.")


# ============================================================
#  DEMONSTRAÇÃO — executa ao rodar o script
# ============================================================

if __name__ == "__main__":

    print("\n🔥 CATÁLOGO DE PRODUTOS — Firebase Firestore")
    print("=" * 55)

    # CREATE — inserindo produtos
    print("\n[1] Criando produtos...")
    id1 = criar_produto("Notebook Gamer", 4299.99, "Eletrônicos", 5,  "Intel i7, 16GB RAM")
    id2 = criar_produto("Camiseta Polo",    89.90, "Roupas",       30, "Algodão premium")
    id3 = criar_produto("Café Gourmet",     38.50, "Alimentos",   100, "Torração média")

    # READ — listando todos
    print("\n[2] Listando todos os produtos...")
    listar_produtos()

    # READ — filtrando por categoria
    print("\n[3] Filtrando por categoria 'Eletrônicos'...")
    listar_produtos(categoria="Eletrônicos")

    # READ — buscando por ID
    print("\n[4] Buscando produto pelo ID...")
    buscar_produto(id1)

    # UPDATE — atualizando estoque
    print("\n[5] Atualizando estoque do Notebook...")
    atualizar_produto(id1, estoque=3, preco=3999.99)
    buscar_produto(id1)

    # DELETE — removendo um produto
    print("\n[6] Removendo o produto de café...")
    deletar_produto(id3)

    # READ — listagem final
    print("\n[7] Listagem final após exclusão:")
    listar_produtos()

    print("\n✅ Demonstração concluída!")
