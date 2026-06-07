import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from supabase import create_client

load_dotenv()

app = Flask(__name__)

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SECRET_KEY"],
)


def listar_links(busca=""):
    query = supabase.table("links").select("*")

    if busca:
        query = query.ilike("nome", f"%{busca}%")

    response = query.order("categoria").order("nome").execute()
    return response.data


@app.route("/")
def index():
    busca = request.args.get("busca", "")
    links = listar_links(busca)
    return render_template("index.html", links=links, busca=busca)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    supabase.table("links").insert(
        {
            "nome": request.form["nome"],
            "url": request.form["url"],
            "categoria": request.form["categoria"],
        }
    ).execute()
    return redirect("/")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        supabase.table("links").update(
            {
                "nome": request.form["nome"],
                "url": request.form["url"],
                "categoria": request.form["categoria"],
            }
        ).eq("id", id).execute()
        return redirect("/")

    response = supabase.table("links").select("*").eq("id", id).single().execute()
    return render_template("editar.html", link=response.data)


@app.route("/excluir/<int:id>")
def excluir(id):
    supabase.table("links").delete().eq("id", id).execute()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
