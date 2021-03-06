import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

'''
Class 1
Challenge 01: Investigar por que a classe tratamento é tão desbalanceada?
Challenge 02: Plotar as 5 últimas linhas da tabela
Challenge 03: Proporção das classes tratamento
Challenge 04: Quantas tipos de drogas foram investigados
Challenge 05: Procurar na documentação o método query(pandas)
Challenge 06: Renomear as colunas tirando o hífen
Challenge 07: Deixar os gráficos bonitões. (Matplotlib.pyplot)
Challenge 08: Resumo do que você aprendeu com os dados
'''
data = pd.read_csv('dados/dados_experimentos.zip', compression='zip')
def test_filter():
    # print first rows, default 5
    print(data.head())

    # print last rows, default 5
    print(data.tail())

    # print #rows, #columns
    print(data.shape)

    # print unique values for each column
    print(data['tratamento'].unique())
    print(data['tempo'].unique())
    print(data['dose'].unique())
    print(data['droga'].unique())
    print(data['g-0'].unique(), end='\n\n')

    # frequency of each unique value
    print(data['tratamento'].value_counts())
    print(data['dose'].value_counts(), end='\n\n')

    # proportion
    print(data['tratamento'].value_counts(normalize=True))
    print(data['dose'].value_counts(normalize=True))

    # plot bar graph
    print(data['tempo'].value_counts().plot.bar())
    plt.show()

    filtered_data = data[data['g-0'] > 0]
    print(filtered_data.head())

'''
Class 2
Challenge 01: Sort graph
    ax = sns.countplot(x = x,
                       data=data_compound,
                       # value_counts(ascending=True)
                       order = data_compound[x].value_counts().index)
Challenge 02: Change axis name
'''
def test_compound_graph():
    map = {'droga':'composto'}
    data.rename(columns=map, inplace=True)
    # get index of 5 most frequent compounds
    compound_ids = data['composto'].value_counts().index[:5]

    data_compound = data.query('composto in @compound_ids')


    sns.set()
    plt.figure(figsize=(8,6))
    x = 'composto'
    ax = sns.countplot(x = x,
                       data=data_compound,
                       # value_counts(ascending=True)
                       order = data_compound[x].value_counts().index)
    ax.set_title('Top 5 Compounds')
    plt.show()

'''
Challenge 03: Plot graphs side by side
    fig, axes = plt.subplots(1, 2)
    data['g-0'].hist(bins=200, ax=axes[0])
    data['g-19'].hist(bins=200, ax=axes[1])
Challenge 04: Plot graphs with seaborn
Challenge 05: Check stats in describe()
'''
def test_histogram():
    data['g-0'].hist(bins=200)
    data['g-19'].hist(bins=200)
    plt.show()

# g: gene expression
def test_describe_g():
    data.loc[:, 'g-0':'g-771'].describe().T.hist(bins=30)
    plt.show()

# c: cell line
def test_describe_c():
    data.loc[:, 'c-0':'c-99'].describe().T.hist(bins=30)
    plt.show()

'''
Challenge 06: Reflect about graph size and visualization
Challenge 07: Plot other boxplots and histogram
'''
def test_boxplot():
    sns.boxplot(x='g-0', data=data)
    sns.boxplot(y='g-0', x='tratamento', data=data)
    plt.show()

'''
Class 3
Challenge 01: Create frequency table with pandas.groupby()
Challenge 02: Normalize frequency table by columns
Challenge 03: Test other aggfunc
Challenge 04: Explote melt tool
'''
def test_freq_table():
    # freq table 'dose' x 'tempo'
    print(pd.crosstab(data['dose'], data['tempo']))
    # freq table ('dose' x 'tempo') x 'tratamento'
    print(pd.crosstab([data['dose'], data['tempo']], data['tratamento']))
    # freq table ('dose' x 'tempo') x 'tratamento', normalized by 'index'
    print(pd.crosstab([data['dose'], data['tempo']], data['tratamento'], normalized='index'))
    # freq table ('dose' x 'tempo') x 'tratamento', for mean of 'g-0'
    print(pd.crosstab([data['dose'], data['tempo']], data['tratamento'], values=data['g-0'], aggfunc='mean'))

def test_scatterplot():
    # plot graph maping 'g-0' and 'g-3' as coordinates
    sns.scatterplot(x='g-0', y='g-3', data=data)
    # plot graph maping 'g-0' and 'g-8' as coordinates
    sns.scatterplot(x='g-0', y='g-8', data=data)
    # plot graph maping 'g-0' and 'g-8' as coordinates and draw tendency line in red
    sns.lmplot(data=data, x='g-0', y='g-8', line_kws={'color':'red'})
    # plot graph maping 'g-0' and 'g-8' as coordinates, separating for 'tratamento'
    sns.lmplot(data=data, x='g-0', y='g-8', line_kws={'color':'red'}, col='tratamento')
    # plot graph maping 'g-0' and 'g-8' as coordinates, separating for 'tratamento' and 'tempo'
    sns.lmplot(data=data, x='g-0', y='g-8', line_kws={'color':'red'}, col='tratamento', row='tempo')
    plt.show()

def test_correlation_g():
    # # print correlation of all gene expressions
    # print(data.loc[:, 'g-0':'g-771'].corr())

    corr = data.loc[:, 'g-0':'g-50'].corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0,
        square=True, linewidths=.5, cbar_kws={'shrink': .5})

    plt.show()

'''
Challenge 05: Check correlation between 'g-X' and 'c-X'
Challenge 06: Study how heatmap is built
'''
def test_correlation_c():
    # # print correlation of all gene expressions
    # print(data.loc[:, 'c-0':'c-771'].corr())

    corr = data.loc[:, 'c-0':'c-50'].corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0,
        square=True, linewidths=.5, cbar_kws={'shrink': .5})

    plt.show()

'''
Class 4
Challenge 01: Find top 10 actions of moa (sulfix inhibitor, antagonist, agonist, ...)
'''
results = pd.read_csv('dados/dados_resultados.csv')
def test_most_activated_moa():
    print(results['acetylcholine_receptor_agonist'].unique())

    # moa =  mechanism of activation
    # sum moa columns and sort descending order
    # select int64 types to ignore first column (alphanumeric 'id')
    # alternative way dropping 'id': results.drop('id', axis=1).sum().sort_values(ascending=False)
    count_moa = results.select_dtypes('int64').sum().sort_values(ascending=False)
    print(count_moa)

def test_most_active_compound():
    count_compounds = results.select_dtypes('int64').sum(axis=1).sort_values(ascending=False)
    print(count_compounds)

'''
Challenge 02: Create column 'is_control_group' if 'tratamento == com_controle'
Challenge 03: Create different columns to each 'tempo'
Challenge 04: Study dataframe merge types: https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
'''
results['n_moa'] = results.drop('id', axis=1).sum(axis=1)
results['is_moa_active'] = (results['n_moa'] != 0)
# merge results 'id', 'n_moa' and 'is_moa_active' into data
# use 'id' as a reference
merged_data = pd.merge(data, results[['id', 'n_moa', 'is_moa_active']], on='id')
def test_control_group_activations():
    print(merged_data.query('tratamento == "com_controle"')['is_moa_active'].unique())

def test_compound_inactive():
    print(merged_data.query('tratamento == "com_droga"')['is_moa_active'].value_counts())

'''
Challenge 05: Do further analisys, considering 'tempo' and 'dose'
Challenge 06: Find if there is any compound that activate any moa with a certain configuration
              but doesn't activate it with another configuration
Challenge 07: Find if there is any compound that activate a moa with a certain configuration
              and activate other moas with a different configuration
'''
def test_boxplot_main_compound():
    main_compound = merged_data['droga'].value_counts().index[:5]
    sns.boxplot(data = merged_data.query('droga in @main_compound'), y='g-0', x='droga', hue='is_moa_active')
    plt.show()

'''
Class 5
Initial machine learning problem:
Classify based on 'is_moa_active'
'''
x = merged_data.select_dtypes('float64')
y = merged_data['is_moa_active']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=376) # use 'stratify=y' split proportionaly to y
def test_machine_learning_regression():
    regression_model = LogisticRegression(max_iter=1000)
    regression_model.fit(x_train, y_train)
    print(regression_model.score(x_test, y_test))

    dummy_model = DummyClassifier('most_frequent')
    dummy_model.fit(x_train, y_train)
    prediction = dummy_model.predict(x_test)
    print(accuracy_score(y_test, prediction))

def test_machine_learning_decition_tree():
    test=[]
    train=[]
    for i in range(1,15):
        tree_model = DecisionTreeClassifier(max_depth=i)
        tree_model.fit(x_train, y_train)
        test.append(tree_model.score(x_test, y_test))
        train.append(tree_model.score(x_train, y_train))

    print(test, train)

'''
    # print decision tree
    from sklearn import tree

    fig, ax = plt.subplots(figsize=(15, 10), facecolor='k')
    tree.plot_tree(tree_model,
                   ax=ax,
                   fontsize=10,
                   rounded=True,
                   filled=True,
                   feature_names=x_train.columns,
                   class_names=['Not Activated', 'Activated'])
    plt.show()
'''

'''
Challenge 01: Try different models or other parameters
Challenge 02: Study Sklearn documentation
Challenge 03: Choosing the right estimator
Challenge 04: Try different questions restricting numbers of moa activated
Challenge 05: Choose the most used drug to try to predict if tested drug is control group or real drug
'''
def test_machine_learning_random_forest():
    x = merged_data.drop(['id', 'n_moa', 'is_moa_active', 'droga'], axis=1)
    x = pd.get_dummies(x, columns=['tratamento', 'dose', 'tempo'])
    y = merged_data['is_moa_active']

    random_forest_model = RandomForestClassifier()
    random_forest_model.fit(x_train, y_train)
    print(random_forest_model.score(x_test, y_test))


if __name__ == "__main__":
    test_machine_learning_random_forest()