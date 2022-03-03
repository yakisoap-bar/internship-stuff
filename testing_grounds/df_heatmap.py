import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv('./df_heatmap.csv', header=None)

    fig= plt.figure(1, figsize=(15, 10))
    ax = fig.add_subplot(111)

    sns.heatmap(df, annot=True, fmt='d', cbar=False, square=True, ax=ax, cmap='Spectral_r')
    plt.text(3, 10.5, 'X', weight='bold')

    plt.savefig('heatmap.png', bbox_inches='tight')


if __name__ == '__main__':
    main()