import os
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import keras
from keras import layers
pokemon_df = pd.read_csv('pokemon_withoutMEGA.csv') 
pokemon_df= pokemon_df.set_index("#") 
combats_df = pd.read_csv('filtered_combat.csv')  
pokemon_df["Type 2"].fillna('empty',inplace=True)
pokemon_df['Type 1'] = pokemon_df['Type 1'].astype('category')  
pokemon_df['Type 2'] = pokemon_df['Type 2'].astype('category')  
pokemon_df['Legendary'] = pokemon_df['Legendary'].astype('int') 
df_type1_one_hot = pd.get_dummies(pokemon_df['Type 1'])
df_type2_one_hot = pd.get_dummies(pokemon_df['Type 2'])  
combine_df_one_hot = df_type1_one_hot.add(df_type2_one_hot, fill_value=0).astype('int64')
pd.options.display.max_columns = 30
pokemon_df = pokemon_df.join(combine_df_one_hot)
dict(enumerate(pokemon_df['Type 2'].cat.categories))
pokemon_df['Type 1'] = pokemon_df['Type 1'].cat.codes 
pokemon_df['Type 2'] = pokemon_df['Type 2'].cat.codes
pokemon_df.head() 
pokemon_df.drop('Name', axis='columns', inplace=True) 
combats_df['Winner'] = combats_df.apply(lambda x: 0 if x.Winner == x.First_pokemon else 1, axis='columns')
data_num = combats_df.shape[0]
indexes = np.random.permutation(data_num)
train_indexes = indexes[:int(data_num *0.6)]
val_indexes = indexes[int(data_num *0.6):int(data_num *0.8)]
test_indexes = indexes[int(data_num *0.8):]
train_data = combats_df.loc[train_indexes]
val_data = combats_df.loc[val_indexes]
test_data = combats_df.loc[test_indexes]
pokemon_df['Type 1'] = pokemon_df['Type 1'] / 19
pokemon_df['Type 2'] = pokemon_df['Type 2'] / 19
mean = pokemon_df.loc[:, 'HP':'Generation'].mean() 
std = pokemon_df.loc[:, 'HP':'Generation'].std() 
pokemon_df.loc[:,'HP':'Generation'] = (pokemon_df.loc[:,'HP':'Generation']-mean)/std
x_train_index = np.array(train_data.drop('Winner', axis='columns'))
x_val_index = np.array(val_data.drop('Winner', axis='columns'))
x_test_index = np.array(test_data.drop('Winner', axis='columns'))
y_train = np.array(train_data['Winner'])
y_val = np.array(val_data['Winner'])
y_test = np.array(test_data['Winner'])
pokemon_data_normal = np.array(pokemon_df.loc[:, :'Legendary'])
x_train_normal = pokemon_data_normal[x_train_index -1].reshape((-1, 20))
x_val_normal = pokemon_data_normal[x_val_index -1].reshape((-1, 20))
x_test_normal = pokemon_data_normal[x_test_index -1].reshape((-1, 20))
pokemon_data_one_hot = np.array(pokemon_df.loc[:, 'HP':])
x_train_one_hot = pokemon_data_one_hot[x_train_index -1].reshape((-1, 54))
x_val_one_hot = pokemon_data_one_hot[x_val_index -1].reshape((-1, 54))
x_test_one_hot = pokemon_data_one_hot[x_test_index -1].reshape((-1, 54))
pokemon_df = pd.read_csv('pokemon_withoutMEGA.csv')
pokemon_df.set_index('#', inplace=True)
def get_pokemon_stats(index):
    pokemon_stats = pokemon_df.loc[index, ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]
    return pokemon_stats

def get_pokemon_name(index):
    name = pokemon_df.loc[index, 'Name']
    return name
def plot_pokemon_stats(index):
    stats = get_pokemon_stats(index)
    name = get_pokemon_name(index)
    plt.figure(figsize=(10, 6))
    stats.plot(kind='bar')
    plt.title(f'{name}')
    plt.ylabel('Value')
    plt.xlabel('Attribute')
    plt.ylim(0, 200)
    plt.xticks(rotation=45)
    plt.show()

def fight_v2(a, b):
    a_index = a - 1
    b_index = b - 1

    a_data_one_hot = pokemon_data_one_hot[a_index].reshape(1, -1)
    b_data_one_hot = pokemon_data_one_hot[b_index].reshape(1, -1)
    input_data_one_hot = np.concatenate([a_data_one_hot, b_data_one_hot], axis=1)

    def create_model_2():
        inputs = keras.Input(shape=(54, ))  
        x = keras.layers.Dense(64, activation='relu')(inputs)
        x = keras.layers.Dropout(0.3)(x)
        x = keras.layers.Dense(128, activation='relu')(x)
        x = keras.layers.Dropout(0.3)(x)
        x = keras.layers.Dense(64, activation='relu')(x)
        x = keras.layers.Dropout(0.3)(x)
        x = keras.layers.Dense(32, activation='relu')(x)
        x = keras.layers.Dropout(0.3)(x)
        outputs = keras.layers.Dense(1, activation='sigmoid')(x)
        model = keras.Model(inputs, outputs)
        return model

    test_model_2 = create_model_2()
    test_model_2.load_weights('lab3-logs/models/Best-model-2.keras')
    prediction_2 = test_model_2.predict(input_data_one_hot)
    a_name = get_pokemon_name(a)
    b_name = get_pokemon_name(b)
    winner = a_name if prediction_2[0] < 0.5 else b_name

    print(f"Model 2 Pred result: {winner}")
    return f"Winner:{winner}"