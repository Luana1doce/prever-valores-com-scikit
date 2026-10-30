
from flask import Flask, render_template, request
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            meses = [int(m) for m in request.form.getlist("mes")]
            valores = [float(v) for v in request.form.getlist("valor")]

            # CORREÇÃO: o modelo usa a posição na sequência (1, 2, 3 ... 10)
            # em vez do número do mês, que volta para 1 depois do 12
            x = [[i + 1] for i in range(len(valores))]
            y = valores

            modelo = LinearRegression()
            modelo.fit(x, y)

            proxima_posicao = len(valores) + 1
            previsao = modelo.predict([[proxima_posicao]])[0]

            # o mês digitado só serve para mostrar na tela (depois do 12 vem o 1)
            proximo_mes = meses[-1] % 12 + 1

            return render_template("main.html", previsao=previsao, proximo_mes=proximo_mes)
        except ValueError:
            return render_template("main.html", erro="Confira os campos: use apenas números.")

    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)