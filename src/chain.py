import sys
from typing import TypeVar, overload

from langchain.chat_models import init_chat_model
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.utils.pydantic import PydanticBaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel
from src.rag import rag_indexar

model = ChatOllama(
    model="gemma4:cloud", base_url="https://ollama.com", temperature=0
)

T = TypeVar("T", bound=BaseModel)

# retriever = rag_indexar()


@overload
def pipeline(
    system: str,
    message: str,
    format: type[T],
    *,
    persona: str = "",
    data: dict = {},
    usar_rag: bool = False,
    user_message: str,
) -> T: ...


@overload
def pipeline(
    system: str,
    message: str,
    *,
    persona: str = "",
    data: dict = {},
    usar_rag: bool = False,
    user_message: str,
) -> str: ...


def pipeline(
    system: str,
    message: str,
    format: type[BaseModel] | None = None,
    *,
    data: dict = {},
    user_message: str,
    usar_rag: bool = False,
    persona: str = "assets/prompt/aux/persona.md",
) -> str | T:
    # return retriever.similarity_search(message)
    base = open("assets/prompt/templates/base.md").read()
    # return base
    prompt = ChatPromptTemplate(
        messages=[
            ("system", base),
            # MessagesPlaceholder("history"),
            (
                "human",
                """
{input}
            """,
            ),
        ]
    )
    llm: Runnable = model
    if format:
        # model.output_schema
        # llm = model.with_structured_output(format)
        model.format = "json"
    else:
        model.format = None

    parser = (
        PydanticOutputParser(pydantic_object=format) if format else StrOutputParser()
    )

    prompt = prompt.partial(
        format_instructions=(
            "siga esse formato para o json: \n"
            + parser.get_format_instructions().replace("{", "\\{{").replace("}", "\\}}")
            if isinstance(parser, PydanticOutputParser)
            else ""
        ),
    )

    chain = prompt | llm | parser

    # print(chain.get_prompts())

    response: str | T = chain.invoke(
        {
            "tipo": "",
            "objetivo": open(
                f"assets/prompt/aux/{system}/{system}-objetivo.md"
            ).read(),
            "regras": open(f"assets/prompt/aux/{system}/{system}-regras.md").read(),
            "persona": open(persona).read(),
            "input": message,
        }
    )

    return response
