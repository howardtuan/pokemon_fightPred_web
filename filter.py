import pandas as pd

# 处理 pokemon.csv
pokemon_df = pd.read_csv('pokemon.csv')
pokemon_df.set_index("#", inplace=True)

# 处理 NaN 值，确保 'Name' 列中没有 NaN，并将所有值转换为字符串
pokemon_df['Name'] = pokemon_df['Name'].fillna('').astype(str)

# 记录包含 'Mega' 的宝可梦数量
pokemon_df['Mega_Count'] = pokemon_df['Name'].str.contains('Mega').cumsum() - pokemon_df['Name'].str.contains('Mega')

# 记录包含 'Mega' 的宝可梦编号
megaList = pokemon_df[pokemon_df['Name'].str.contains('Mega')].index.tolist()

# 保存中间结果
pokemon_df.to_csv('with_mega_counts.csv', index=True, index_label='#')

# 读取对战数据
combats_df = pd.read_csv('combats.csv')

# 移除包含 Mega 宝可梦的对战记录
combats_df = combats_df[~combats_df['First_pokemon'].isin(megaList)]
combats_df = combats_df[~combats_df['Second_pokemon'].isin(megaList)]

# 使用累积 Mega 数量调整 ID
def adjust_id(id, mega_counts):
    return id - mega_counts.get(id, 0)

# 应用调整函数
combats_df['First_pokemon'] = combats_df['First_pokemon'].apply(adjust_id, mega_counts=pokemon_df['Mega_Count'].to_dict())
combats_df['Second_pokemon'] = combats_df['Second_pokemon'].apply(adjust_id, mega_counts=pokemon_df['Mega_Count'].to_dict())
combats_df['Winner'] = combats_df['Winner'].apply(adjust_id, mega_counts=pokemon_df['Mega_Count'].to_dict())

# 移除包含 NaN 的行
combats_df.dropna(inplace=True)
combats_df = combats_df.astype(int)  # 将 ID 转换回整数

# 保存处理后的对战数据
combats_df.to_csv('filtered_combat.csv', index=False)

# 更新并保存 pokemon.csv，移除 Mega 角色
pokemon_df = pd.read_csv('with_mega_counts.csv')
pokemon_df.set_index("#", inplace=True)

# 处理 NaN 值，确保 'Name' 列中没有 NaN，并将所有值转换为字符串
pokemon_df['Name'] = pokemon_df['Name'].fillna('').astype(str)

# 移除包含 Mega 角色
pokemon_df = pokemon_df[~pokemon_df['Name'].str.contains('Mega')]

# 重置索引以生成新的 ID
pokemon_df.reset_index(drop=True, inplace=True)
pokemon_df.index += 1  # ID 从 1 开始

# 保存处理后的宝可梦数据
pokemon_df.to_csv('filtered_pokemon.csv', index=True, index_label='#')
