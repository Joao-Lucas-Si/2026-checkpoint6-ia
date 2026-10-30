# CKP03 — Agente • IA de Assistência à Escrita

**Prompt Engineering & AI • FIAP • 2º Semestre 2026**

**Integrantes:** 
- Gabriel de Paula Santos (RM573195) 
- Joao Lucas Silva Lopes (RM573875) 
- Alan Otalvaro (RM571794) 
- Joao Pedro Ribeiro Santos (RM570562) 
- Joao Pedro Evangelista (RM573899) 
- Enzo Ribeiro (RM569429)
  
---

# Domínio

O domínio escolhido pelo grupo foi **Agente de Inteligência Artificial aplicado à assistência de escrita**.

A proposta do projeto é desenvolver um agente profissional capaz de auxiliar o usuário em diferentes etapas da produção e desenvolvimento de textos.

O agente terá consigo várias tools que permitiram se adaptar para atender da melhor forma o usuário, indo desde escrever arquivos de textos a uma busca inteligente pelas mensagens anteriores do sistema.

## Rags

Mudamos um pouco o funcionamento do rags no projeto, já que nosso dominio é um assitente de escrita, documentos técnicos não eram os mais apropriados para seu funcionamento, então adaptamos o rags para ele ser um auxiliar do agente na manipulação de arquivos, então invés de ser estático, ele é dinamico, conforme o agente modifica os arquivos, o rags acompanha. 
seu principal uso é procurar por trechos ou documentos quando o usuário pedir ou quando o nome do documento a ser modificado ou lido não for informado de modo integral
além disso, optamos por usar markdown como documento invés de pdf devido a ser o principal formado escrito pelo agent, usando MarkdownHeaderTextSplitter como splitter, para termos uma separação lógica dos trechos por titulo invés do método por chunking.

para o rags não começar sem nada, deixamos alguns documentos já prontos, esses foram usados durante o teste do sistema

## ferramentas/tools

dividimos as ferrementas utilizadas pelo agente em categorias, sendo elas: documentos, memoria, auxiliares.

### ferramentas para Documentos

essa categoria abrange as ferramentas que iteragem com os documentos do sistema, podendo ler, escrever e procurar pelos arquivos dentro da pasta documents.
uma regra que é aplicada a todas as ferramentas de documentos é que um documento só pode ser acesso por nome simples, ou seja, sem barras ou extensão de arquivos, essas regras existem para impedir quebra do funcionamento do sistema.

#### Ferramenta de Leitura

permite o agente ler integralmente o conteúdo

#### Ferramenta de escrita

a principal ferramenta do projeto, dá ao agent a possibilidade de escrever arquivos no sistema.
devido a segurança, ela também é bem limitada, só escreve arquivos dentro de uma única pasta e todos os arquivos seguem o formato markdown, além disso, ela segue as regras de nomenclatura para impedir a criação de subpastas e de arquivos de outros tipos

#### Ferramenta de busca

a ferramenta de busca é o rags do projeto, ela tem todos os documentos escritos e já processados pelo embeddings, ela recebe uma consulta e procura pela sessão mais apropriada, retornando o documento de origem, a sessão ou subsessão e o contéudo.
ela é usado pelo agent quando o usuário procura por algum trecho ou não especifica o nome do documento preciso para a tarefa

### Ferramentas de memoria

as ferramentas de memoria são funções focadas na manipulação de contexto, invés do agente sempre ter a memoria das tarefas anteriores, ele chama uma ferramenta de memoria apropriada para o contexto e obtém as mensagens anteriores, só chamando essas ferramentas quando necessário.

#### ferramenta de memoria recente

essa ferramenta é usada quando o agente percebe uma mensagem abigua ou com contexto cortado, ela busca pelas mensagens anteriores mais recentes e retorna elas em par de (pedido do usuário, resposta do agente)

#### ferramenta de memoria por escopo

essa ferramenta obtem todas as mensagens dentro de um escopo, sendo esse escopo atrelacado a um arquivo, então quando o agente precisa saber o historico de modificações de um arquivo, essa tool é chamada.
ela tem um uso bem limitado e o agente é informado que só deve usar quando necessário ou requerido.

### Ferramentas auxiliares

As ferramentas auxiliares são uma adapção do chatbot construido anteriromente, um reaproveitamento do comportamento anteriro.
na Primeira versão, tinhamos uma ia que analisava o pedido do usuário e fazia um de três tarefas, expandir, resumir e brainstorm, cada tarefa tinha seu proprio prompt e comportamento interno.
então modificamos elas para serem uma tool do agente, que quando precisa de uma tarefa especializada, redireciona ela para uma das três ias auxiliares.

#### Ferramenta de Brainstorm

a antiga ia responsável por ajudar a dar ideias ao usuário

#### Ferramenta de resumo

auxiliar de resumo de textos, tem o contexto de uso limitado á resumir textos já existentes, em pedidos do usuário para resumir conteúdos não escritos ainda, ela é despensada.

#### Ferramenta de expansão

ai especializada em expandir textos, dando mais detalhes e aumentando seu escopo.

## Público-alvo

O agente pode ser utilizado principalmente por:

- Estudantes;
- Profissionais;
- Pessoas desenvolvendo projetos;
- Pessoas que precisam organizar ou reduzir textos;
- Usuários que desejam desenvolver conteúdos;
- Pessoas que procuram novas ideias para trabalhos, projetos ou textos.

## Funcionalidades


# ChatOllama

O modelo utilizado é:

```text
gemma4:cloud
```

O modelo é utilizado através do **Ollama Cloud**.

A chave de acesso é configurada através do arquivo `.env`:

```env
OLLAMA_API_KEY=<sua-chave>
```

# Interface

A interface atual do agente funciona através do gradio, criando um aplicativo web que é divido em duas abas.
a primeira aba é a de chat, onde o usuário pode conversar com nosso agente fazendo perguntas ou solicitando ações
e a segunda é a arvore de arquivos, que permite o usuário ver os documentos escritos até agora pelo agente.

# Principais arquivos

| Arquivo | Responsabilidade |
|----------|------------------|
| `main.py` | Inicialização do chatbot |
| `src/agent` | criação do agent do projeto |
| `src/chain.py` | pipeline da ia antiga, usado como auxiliar |
| `src/interface` | configuração da interface gradio |
| `src/rag` | configuração do rags |
| `src/tools` | configuração das tools |
| `assets/prompt/` | Prompts utilizados pelo chatbot |

# Como executar

## 1. Criar o ambiente virtual

```bash
python -m venv .venv
```

## 2. Ativar o ambiente virtual

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 4. Configurar o Ollama Cloud

Crie um arquivo `.env` baseado no `.env.example`:

```env
OLLAMA_API_KEY=<sua-chave>
```

## 5. Configurar o ollama local

devido algums problemas com o ollama cloud para embeds, é preciso tanto ter ele em sua maquina quanto ter a chave do ollama cloud, siga as instruções do [site oficial](https://ollama.com/download) para abaixar o ollama 

após ter o ollama em sua maquina, inicie o servidor e rode com o modelo de embeddings, cada comando em um terminal distinto


```base
ollama serve

ollama pull nomic-embed-text
```

## 5. Executar

com os dois ollamas configurados, rode

```bash
python main.py
```

ou use o gradio em caso de hot reload 

```
gradio main.py
```

# Limitações atuais

- O funcionamento depende da configuração do Ollama Cloud;
- O Rags só consegue acompanhar as modificações feitas pelo agent, quando o usuário modifica um arquivo manualmente ele fica fora do rastreio;
- o visualizar de arquivos esta limitado a arquivos já disponivel quando o projeto é executado, não conseguindo rastrear arquivos criados pelo agent, isso devido a uma limitação interna do gradio, mas ainda é possivel ver as modificações aplicadas arquivos já existentes
- o funcionamento interno do gradio pode ser defeituoso quando algum arquivo dos documentos é deletado, mesmo reininciando o projeto

# Teste e Avaliação

para testar e avaliar o agent, preparamos um arquivo separado chamado iteracoes.md, nele contém três perguntas feitas em iterações de testes, o objetivo da pergunta, e a resposta dada.

além disso, para avaliar o comportamento interno do agent, cada mensagem criada por ele, tem seus pensamentos registrados no arquivo data/logs/logs.txt, assim é possivel saber cada ferramenta usada e como o agente utilizou elas
