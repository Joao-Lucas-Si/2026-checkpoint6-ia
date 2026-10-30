import os
import time
from typing import Literal, TypedDict, Union

import gradio as gr

from src.db import Database
from src.agent import (
    FinalAgentResponse,
    PensamentoAgentResponse,
    WriteAgentResponse,
    gerar_resposta_agent,
)
from src.tools import obter_caminho_documento


class NavigationState(TypedDict):
    tipo: Literal["chat", "documento"]
    caminho: str | None


def obter_docs():
    docs = [
        i.replace(".md", "") for i in os.listdir("data/documents") if i.endswith(".md")
    ]
    return docs


def criar_gradio():
    db = Database.get_singleton()

    with gr.Blocks() as demo:
        docs = gr.State(obter_docs())

        Database.read()
        initial: NavigationState = {
            "tipo": "chat",
            "caminho": docs.value[0] if len(docs.value) > 0 else None,
        }
        route = gr.State(initial)

        # current = gr.Column()

        def responder(pergunta: str, historico: list):
            start_time = time.time()
            segments: list[Union[str, gr.FileData, gr.Component]] = ["pensando"]
            response = gr.ChatMessage(
                content=segments,
                metadata={
                    "status": "pending",
                },
            )
            yield response
            try:
                resposta = gerar_resposta_agent(pergunta)

                for i in resposta:
                    if isinstance(i, WriteAgentResponse):
                        segments.append(gr.FileData(path=i.file))
                        # yield response
                        # docs.change(lambda : obter_docs(), outputs=[docs])
                    # elif isinstance(i, PensamentoAgentResponse):
                    #     # pensamento_conteudo.value += i.pensamento
                    #     final += i.pensamento
                    elif isinstance(i, FinalAgentResponse):
                        # pen
                        segments[0] = i.conteudo
                    yield response
                response.metadata["status"] = "done"
                yield response
            except Exception as e:
                segments[0] = str(e)
                yield response
            response.metadata["duration"] = time.time() - start_time
            yield response

        with gr.Row():
            with gr.Column(scale=1):
                with gr.Tab("chats", scale=1):
                    gr.ChatInterface(
                        fn=responder,
                        title="🤖 Agente de escrita — CKP03",
                        description="Agente com RAG + manipulação de documentos + ais auxliares. Powered by Ollama.",
                        # inputs=gr.Textbox(label="Pergunta", placeholder="Digite aqui..."),
                        # outputs=gr.Textbox(label="Resposta"),
                        # title="Assistente escrita",
                        # description="Seu agente de escrita",
                        chatbot=gr.Chatbot(
                            [
                                {
                                    "content": [
                                        m["conteudo"],
                                        *[
                                            gr.FileData(path=obter_caminho_documento(a))
                                            for a in m["arquivos"]
                                            if m["role"] == "chat"
                                        ],
                                    ],
                                    "role": (
                                        "user"
                                        if m["role"] == "usuario"
                                        else "assistant"
                                    ),
                                }
                                for m in db.mensagens
                            ]
                        ),
                        # examples=[
                        #     "Faça sua pergunta"
                        # ]
                    )
                with gr.Tab("documentos", scale=1) as documentos:
                    documentos.select()
                    with gr.Row():

                        @gr.render(docs)
                        def listar_docs(x):
                            with gr.Column(scale=1):
                                for file in docs.value:
                                    gr.Button(file).click(
                                        lambda x, y=file: {
                                            "tipo": "documento",
                                            "caminho": y.replace(".md", ""),
                                        },
                                        route,
                                        route,
                                    )

                        @gr.render(route)
                        def current(current: NavigationState):
                            if current["caminho"]:
                                gr.Markdown(
                                    open(
                                        obter_caminho_documento(current["caminho"])
                                    ).read(),
                                    scale=9,
                                )

        return demo
