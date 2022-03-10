import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    # import heatmaps
    df_full = pd.read_csv('./df_heatmap.csv', header=None)
    df_4point = pd.read_csv('./df_4point.csv', header=None)
    df_8point = pd.read_csv('./df_8point.csv', header=None)

    # plot heatmaps
    for i, heatmap in enumerate([df_full, df_4point, df_8point]):
        y, x = heatmap.shape
        # if y < 18 and x < 6:
        #     heatmap = heatmap.to_numpy().repeat(18//y, axis=0).repeat(6//x, axis=1)

        fig= plt.figure(i, figsize=(6, 18))
        ax = fig.add_subplot(111)

        sns.heatmap(heatmap, annot=True, fmt='d', cbar=False, ax=ax, cmap='Spectral_r')
        plt.text(x/2, y/1.9 if y < 18 else 10.5, 'X', weight='bold')

        plt.savefig(f'heatmap_{i}.png', bbox_inches='tight')


if __name__ == '__main__':
    main()