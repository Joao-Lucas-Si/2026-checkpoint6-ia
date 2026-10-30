import os
import sys

import dotenv

from src.tools import tool_ler
dotenv.load_dotenv()

from src.db import Database
from src.rag import atualizar_rag, rag_indexar
from src.interface import criar_gradio
from src.agent import gerar_resposta_agent
# from src.evaluate import avaliar
from time import sleep

from rich.console import Console
from rich.progress import Progress

from rich.theme import Theme
import gradio as gr
# from io import StringIO

gr.set_static_paths(paths=["data/documents/"])
if __name__ == "__main__":
    Database.read()
    demo = criar_gradio()
    rag_indexar()
    
    demo.launch(share=True)

# def main():
#     console = Console(theme=Theme({
#         "background_color": "#191A1B",
#         "info": "dim cyan",
#         "warning": "magenta",
#         "danger": "bold red"
# }), )
    
#     if len(sys.argv) == 2:
#         screen = sys.argv[1]
#         if screen == "-rot":
#             context_rot(console)
#         elif screen == "-ragas":
#             avaliar()
#             ...
#         elif screen == "-chunk":
#             ...
#     else:
#         HistoruScreen().draw(console)

