from fastapi import FastAPI
import jinja2
from fastapi.responses import HTMLResponse
from src.whatwg import html, head, title, body, header, h1, main, p

environment = jinja2.Environment()




def create_page() -> str:
    with html(lang="pt-BR") as page:
        with head():
            title(children=["Not So Lit"])

        with body(class_name="main-body"):
            with header():
                h1(children=["Bem-vindo ao Not So Lit"])

            with main():
                p(children=["Este é um exemplo com componentes filhos."])

    return "<!doctype html>\n" + page.render()


app = FastAPI()


@app.get("/")
def read_root():
    return HTMLResponse(content=create_page(), media_type="text/html")
