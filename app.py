import matplotlib
matplotlib.use('Agg') 

from flask import Flask, render_template, request
from loadWeight_pokemon import fight_v2, get_pokemon_stats, get_pokemon_name
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

pokemon_df = pd.read_csv('filtered_pokemon.csv')
pokemon_df.set_index("#", inplace=True)

@app.route('/searchForID')
def index():
    return render_template('searchForID.html')
    
@app.route('/index')
def choose():
    return render_template('choose_query.html')
@app.route('/searchForName')
def name():
    return render_template('searchForName.html')

@app.route('/NameToID', methods=['POST'])
def resultTest():
    pokemon1_id = int(request.form.get('pokemon1_id'))
    pokemon2_id = int(request.form.get('pokemon2_id'))
    fight_result = fight_v2(pokemon1_id, pokemon2_id)
    
    pokemon1_name = get_pokemon_name(pokemon1_id)
    pokemon2_name = get_pokemon_name(pokemon2_id)
    
    pokemon1_image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon1_id}.png"
    pokemon2_image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon2_id}.png"
    
    pokemon1_stats = get_pokemon_stats(pokemon1_id).tolist()
    pokemon2_stats = get_pokemon_stats(pokemon2_id).tolist()
    
    # 生成横条图
    def create_bar_chart(stats, pokemon_name, filename):
        attributes = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        plt.figure(figsize=(3, 4)) 
        plt.barh(attributes, stats, color='skyblue')
        plt.xlabel('Value')
        plt.xlim(0, 200)
        plt.tight_layout()
        plt.savefig(f'static/{filename}')
        plt.close()

    create_bar_chart(pokemon1_stats, pokemon1_name, 'pokemon1_stats.png')
    create_bar_chart(pokemon2_stats, pokemon2_name, 'pokemon2_stats.png')

    return render_template('result.html', result=fight_result, 
                           pokemon1_image=pokemon1_image, 
                           pokemon2_image=pokemon2_image,
                           pokemon1_name=pokemon1_name,
                           pokemon2_name=pokemon2_name,
                           pokemon1_stats_img='pokemon1_stats.png',
                           pokemon2_stats_img='pokemon2_stats.png')

    
@app.route('/result', methods=['POST'])
def result():
    pokemon1_id = int(request.form['pokemon1'])
    pokemon2_id = int(request.form['pokemon2'])
    fight_result = fight_v2(pokemon1_id, pokemon2_id)
    
    pokemon1_name = get_pokemon_name(pokemon1_id)
    pokemon2_name = get_pokemon_name(pokemon2_id)
    
    pokemon1_image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon1_id}.png"
    pokemon2_image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon2_id}.png"
    
    pokemon1_stats = get_pokemon_stats(pokemon1_id).tolist()
    pokemon2_stats = get_pokemon_stats(pokemon2_id).tolist()
    
    # 生成横条图
    def create_bar_chart(stats, pokemon_name, filename):
        attributes = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        plt.figure(figsize=(3, 4)) 
        plt.barh(attributes, stats, color='skyblue')
        plt.xlabel('Value')
        plt.xlim(0, 200)
        plt.tight_layout()
        plt.savefig(f'static/{filename}')
        plt.close()

    create_bar_chart(pokemon1_stats, pokemon1_name, 'pokemon1_stats.png')
    create_bar_chart(pokemon2_stats, pokemon2_name, 'pokemon2_stats.png')

    return render_template('result.html', result=fight_result, 
                           pokemon1_image=pokemon1_image, 
                           pokemon2_image=pokemon2_image,
                           pokemon1_name=pokemon1_name,
                           pokemon2_name=pokemon2_name,
                           pokemon1_stats_img='pokemon1_stats.png',
                           pokemon2_stats_img='pokemon2_stats.png')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form['name']
        result = pokemon_df[pokemon_df['Name'].str.lower() == name.lower()]
        if not result.empty:
            pokemon_id = result.index[0]
            return render_template('search_result.html', name=name, pokemon_id=pokemon_id)
        else:
            return render_template('search_result.html', name=name, pokemon_id=None)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
