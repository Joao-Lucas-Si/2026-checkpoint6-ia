import json
import os
from typing import TypedDict
from langchain_core.tools import tool

# from langchain_cores.tools import tool
from pydantic import BaseModel, Field

from src.db import Database
from src.rag import atualizar_rag, rag_indexar
from src.chain import pipeline


def obter_caminho_documento(nome: str):
    return f"data/documents/{nome}.md"

def validar_arquivo(nome: str):
    if nome.endswith(".md"):
        return "nome invalido com acordo com as regras de nomenclatura, extensão de arquivo não é permitida"

    if "/" in nome or "\\" in nome:
        return "nome invalido com acordo com as regras de nomenclatura, barras (/) não podem ser incluidas"

    return None
@tool
def tool_ler(nome: str):
    """\
    use essa tool para ler os documentos que foram escritos usando "tool_escrever".
    sempre que o usuário pedir sobreescrita de algum documento, chame essa ferramenta e depois use a tool_escrever para modificar o documento.
    caso o documento informado não exista, uma resposta será dada.
    o nome deve seguir a mesma nomenclatura de "tool_escrever", ou seja, sem barras e sem extensão de arquivo
    """
    valido = validar_arquivo(nome)
        
    if valido:
        return valido
    caminho = obter_caminho_documento(nome)
    if not os.path.exists(caminho):
        return "documento não existe"

    with open(caminho, "r", encoding="utf-8") as doc:
        return doc.read()


class EscritaParam(BaseModel):
    nome: str = Field(description="o nome do documento")
    conteudo: str = Field(description="o conteúdo do documento")


@tool()
def tool_escrever(param):
    """\
    use essa ferramenta para escrever documentos para o usuário quando for requerido, informando o nome do documento e seu conteúdo.
    o nome do documento deve ser um nome simples sem extensão de arquivo como .md, .pdf ou .docx, além de não poder incluir barras.
    caso essa politica de nomenclatura não foi seguida, uma resposta informando que o documento não foi escrito será informado.
    o contéudo deve ser escrito seguindo o formanto markdown
    
    Args:
        nome: o nome do document
        conteudo: o conteudo do documento
        
    """
    parm = EscritaParam(**json.loads(param))
    nome = parm.nome
    conteudo = parm.conteudo

    valido = validar_arquivo(nome)
    
    if valido:
        return valido
    
    with open(obter_caminho_documento(nome), "w", encoding="utf-8") as doc:
        doc.write(conteudo)
        
    atualizar_rag(f"{nome}.md")
    return "documento escrito com sucesso"


@tool
def tool_buscar(query: str):
    """\
    Use esta tool quando o usuário perguntar
    sobre qualquer informação que pode estar nos
    documentos, mas não foi especificado qual seria o nome.
    ele buscará o documento e o trecho que conter o texto mais similar a query enviada.
    serão enviados multiplas possibilidades, 
    leve em consideração as que mais parecem condizer com o que o usuário disse.
    a busca é limitada à apenas pegar trechos correspondentes a consulta feita, sendo assim,
    em tarefas que precisem saber o conteúdo integral do documento, use a busca para achar o documento procurado,
    e depois use a tool_ler para saber o conteúdo na integra.
    em tarefas voltados a achar algum seção ou trecho dos documentos. é obrigatorio a menção do documento(use o nome do arquivo), da seção e da subsção(se houver) onde o trecho foi encontrado
    """
    retriever = rag_indexar()
    
    return retriever.invoke(query)


def tool_ai_auxiliar(tipo, prompt):
    resposta = pipeline(
        tipo,
        prompt.replace("{", "\\{{"),
        user_message=prompt.replace("{", "\\{{"),
    )
    # print(expansao)
    return resposta


@tool
def tool_historico_recente():
    """
    Use essa ferramenta para obter o historico recente de mensagens com o usuário.
    ela deve ser usada com prioridade em relação as outras ferramentas de histórico em contextos de historico mais vagas, quando o usuário não especifica qual contexto você deve seguir.
    em mensagens que sejam pedidos para refazer algo, sempre use esse tool.
    em pedidos diretos, que sejam apenas informados uma tarefa simples a ser feita com todo o contexto disponivel, não chame essa ferramenta e nenhuma outra de historico.
    """
    quantidade: int = 3
    # é possivel informar a quantidade de itens passados que devem ser buscados, mas é opcional, o número de itens do historico a ser informado como quantidade se referem sempre a duplas de mensagens, conténdo o pedido do usuário e a resposta do chatbot, ou seja, 3 itens sempre é equivalente a 6 mensagens.
    
    return Database.get_singleton().mensagens[-(quantidade * 2):]
    


@tool
def tool_historico_arquivo(documento: str):
    """
    Use essa ferramenta para obter todo o historico referente a um arquivo.
    historico de arquivo, aqui é usado para se referir a toda mensagem que foi necessário ler um documento ou escrever um documento, sempre retorna o pedido do usuário e sua resposta equivalente.
    deve ser usado em pedidos muito especificos ou quando diretamente referindo, como dizer qual é o historico de alterações de um arquivo, nunca opte por si mesmo a usar essa tool.
    em pedidos diretos, que sejam apenas informados uma tarefa simples a ser feita com todo o contexto disponivel, não chame essa ferramenta e nenhuma outra de historico.
    o documento deve ser informado seguindo as regras de nomenclatura gerais, ou seja, sem barras e sem extensão de arquivo
    """
    valido = validar_arquivo(documento)
        
    if valido:
        return valido
    return [m for m in Database.get_singleton().mensagens if documento in m["arquivos"]]

@tool
def tool_resumo(prompt: str):
    """
    Use essa tool para chamar uma ia especializada em resumo de textos.
    informe dentro do prompt toda a informação necessária para a ia auxiliar, como qual texto a ser resumido, a forma como deve ser resumido, informações que devem ser mantidas, etc.
    caso seja especificado pelo usuário resumo focado em uma sessão especifica, apenas mande a parte necessária para o resumo junto ao contexto geral presente no documento, depois junto o resultado com o restante
    """
    return tool_ai_auxiliar("resumo", prompt)


@tool
def tool_brainstorm(prompt: str):
    """
    Use essa tool para chamar uma ia especializada em brainstorm e formação de ideias.
    Na maioria das vezes essa ferramenta deve ser usada em conversas diretas com o usuario
    """
    return tool_ai_auxiliar("brainstorm", prompt)


@tool
def tool_expansao(prompt: str):
    """
    Use essa tool para chamar uma ia auxiliar especializada em expandir o escopo de textos.
    expanção/expandir aqui se refere ao qualquer tarefa que se resuma em peguar um texto e acrescentar informações a ela, seja informação nova ou detalhadamento de informações já presentes.
    considere como sinonimos de expansão: detalhar, expandir, melhorar, incrementar, etc.
    informe dentro do prompt toda a informação necessária para a ia auxiliar, como qual texto expandido, a forma como deve ser expandido, informações extras a serem adicionadas, etc.
    caso seja especificado pelo usuário expansão focada em uma sessão especifica, apenas mande a parte necessária para a expansão junto ao contexto geral presente no documento, depois junto o resultado com o restante
    não use essa ferramentas para tarefas referentes a criação de novos textos do zero.
    """
    return tool_ai_auxiliar("expansao", prompt)


tools = [tool_escrever, tool_ler, tool_expansao, tool_brainstorm, tool_resumo, tool_buscar, tool_historico_recente, tool_historico_arquivo]
