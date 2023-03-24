from flask import Flask, render_template, request
from pente import analyse_capteur, liste_tests
import os
from pathlib import Path

app = Flask(__name__)
basedir = Path(__file__).resolve().parent
data_folder = basedir / "test_finaux"

@app.route('/')
def index():
    tests_list = liste_tests()
    return render_template('index.html', liste_tests=tests_list)

@app.route('/analyse')
def analyse():
    test_name = request.args.get('test_name', '')
    resultats = analyse_capteur(test_name)
    return render_template('analyse.html', resultats=resultats)

@app.route('/historique')
def historique():
    return render_template('historique.html')

if __name__ == '__main__':
    app.run(debug=True)
