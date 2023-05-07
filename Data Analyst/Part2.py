import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def create_folder():
    try:
        os.makedirs('Diagrams')
    except FileExistsError:
        pass


def check_len_phrase(line: str) -> str:
    """
    Function checks string length and replaces 'space' with '\n' if length > 15
    """
    if len(line) < 16:
        return line
    else:
        return line.replace(' ', '\n')


def diagram(area_name: str, x: list, y: list, name: list, col: list, cluster: list):
    """
    The function plots a scatterplot for unique area
    :param area_name: Name of the area for title
    :param x: Points X coordinates
    :param y: Points Y coordinates
    :param name: Points names
    :param col: Colors for every point
    :param cluster: Numbers of clusters
    """
    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot()
    ax.set_xlabel('Ось Х')
    ax.set_ylabel('Ось У')
    ax.set_title('Area - ' + area_name, loc='center', size=20)
    # Footer
    ax.text(15, -1.5, "Made by: Sokolov Ilya", ha="center", size=20, alpha=0.6)

    # Place points, form legend by color and cluster name
    l, r = 0, 0
    while r < len(x):
        while col[l] == col[r] and r < len(x):
            r += 1
            if r == len(x):     # out of index
                break
        plt.scatter(x[l:r], y[l:r], c=col[l:r], edgecolors='black', marker='o', s=150, alpha=0.5, label=cluster[l])
        l = r
        r += 1

    # Place the names of the points
    for idx in range(len(x)):
        plt.text(x[idx], y[idx] - 0.5, check_len_phrase(name[idx]), fontsize=10,
                 horizontalalignment='center', verticalalignment='center')

    # add legend title
    ax.legend(title='Кластеры')

    # Graphic borders
    plt.xlim(0, 16)
    plt.ylim(0, 16)

    # hide axes and borders
    plt.axis('off')

    # auto safe picture
    wrong_symbols = {'\\', '/', ':', '*', '?', '"', '<', '>', '|', '+'}
    correct_name = ''
    for g in range(len(area_name)):
        if area_name[g] not in wrong_symbols:
            correct_name += area_name[g]
    plt.savefig(f'Diagrams\\{correct_name}.png')

    '''
    # just to watch
    plt.show()
    '''


create_folder()
data = pd.read_excel('result.xlsx')
i = 1
j = 1
while i < len(data) - 1:
    area_data_x = []
    area_data_y = []
    point_keyword = []
    color = []
    cluster_name = []
    while data.loc[i, 'area'] == data.loc[j, 'area'] and j < len(data) - 1:
        area_data_x.append(data.loc[j, 'x'])
        area_data_y.append(data.loc[j, 'y'])
        point_keyword.append(data.loc[j, 'keyword'])
        color.append(data.loc[j, 'color'])
        cluster_name.append(data.loc[j, 'cluster_name'])
        j += 1
    if j == len(data) - 1:
        area_data_x.append(data.loc[j, 'x'])
        area_data_y.append(data.loc[j, 'y'])
        point_keyword.append(data.loc[j, 'keyword'])
        color.append(data.loc[j, 'color'])
        cluster_name.append(data.loc[j, 'cluster_name'])
    # Send data to rendering
    diagram(data.loc[i, 'area'], area_data_x, area_data_y, point_keyword, color, cluster_name)
    i = j
