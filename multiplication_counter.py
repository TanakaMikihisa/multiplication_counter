import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.font_manager as fm

def setup_japanese_font():
    """日本語フォントを設定する"""
    japanese_fonts = [
        'Hiragino Sans',
        'Hiragino Kaku Gothic ProN',
        'Arial Unicode MS',
        'Yu Gothic',
        'Meiryo',
        'Noto Sans CJK JP',
        'AppleGothic'
    ]
    
    for font_name in japanese_fonts:
        try:
            font_path = fm.findfont(fm.FontProperties(family=font_name))
            plt.rcParams['font.family'] = font_name
            print(f'日本語フォントを設定しました: {font_name}')
            return True
        except:
            continue
    
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Arial Unicode MS', 'Yu Gothic', 'Meiryo']
    print('デフォルトの日本語フォント設定を使用します')
    return False

setup_japanese_font()


def count_unique_multiplication_results(n, m):
    """
    n×mの掛け算表で、異なる答えの数をカウントする関数
    
    Args:
        n: 最初の数の範囲（1からnまで）
        m: 2番目の数の範囲（1からmまで）
    
    Returns:
        unique_results: ユニークな答えのセット
        count: ユニークな答えの数
        result_matrix: n×mの掛け算結果の行列
        is_new_matrix: 各マスが新しい答えかどうかを示すブール行列
    """
    result_matrix = np.zeros((n, m), dtype=np.int32)
    is_new_matrix = np.zeros((n, m), dtype=np.bool_)
    seen_results = set()
    
    for i in range(1, n + 1):
        j_range = np.arange(i, m + 1, dtype=np.int32)
        results = i * j_range
        
        for idx, j in enumerate(j_range):
            result = results[idx]
            result_matrix[i - 1, j - 1] = result
            
            if j <= n:
                result_matrix[j - 1, i - 1] = result
            
            if result not in seen_results:
                is_new_matrix[i - 1, j - 1] = True
                seen_results.add(result)
    
    return seen_results, len(seen_results), result_matrix, is_new_matrix


def visualize_multiplication_table(n, m, save_path='multiplication_table.png'):
    """
    n×mの掛け算表を視覚化し、新しい答えのマスを赤色で表示する
    
    Args:
        n: 最初の数の範囲（1からnまで）
        m: 2番目の数の範囲（1からmまで）
        save_path: 保存する画像のパス
    """
    unique_results, count, result_matrix, is_new_matrix = count_unique_multiplication_results(n, m)
    
    CELL_SIZE_PIXELS = 50
    DPI = 300
    CELL_SIZE_INCHES = CELL_SIZE_PIXELS / DPI
    
    cell_area_width = m * CELL_SIZE_INCHES
    cell_area_height = n * CELL_SIZE_INCHES
    
    title_height = 0.8
    legend_width = 1.5
    
    width_inches = cell_area_width + legend_width
    height_inches = cell_area_height + title_height
    
    fig, ax = plt.subplots(figsize=(width_inches, height_inches), dpi=DPI)
    
    top_margin = title_height / height_inches
    fig.subplots_adjust(
        left=0,
        bottom=0,
        right=cell_area_width / width_inches,
        top=1.0 - top_margin
    )
    
    for i in range(n):
        y_pos = n - 1 - i
        is_new_row = is_new_matrix[i]
        
        for j in range(m):
            x_pos = j
            color = 'red' if is_new_row[j] else 'white'
            
            rect = patches.Rectangle(
                (x_pos, y_pos), 1, 1,
                linewidth=1,
                edgecolor='black',
                facecolor=color,
                alpha=0.7
            )
            ax.add_patch(rect)
    
    ax.set_xlim(0, m)
    ax.set_ylim(0, n)
    ax.set_aspect('equal')
    ax.axis('off')
    
    title = f'{n}×{m}の掛け算表（答えの数: {count}個）'
    fig.suptitle(title, fontsize=16, fontweight='bold', y=1.0 - (title_height / height_inches / 2))
    
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.7, label='新しい答え'),
        Patch(facecolor='white', alpha=0.7, label='既に出現した答え')
    ]
    legend = ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1.0))
    
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight', pad_inches=0.1)
    print(f'画像を保存しました: {save_path}')
    print(f'ユニークな答えの数: {count}個')
    
    plt.show()
    
    return count, unique_results


if __name__ == '__main__':
    n = 100
    m = 100
    
    smaller = min(n, m)
    larger = max(n, m)
    save_path = f'multiplication_table_{smaller}×{larger}.png'
    
    count, unique_results = visualize_multiplication_table(n, m, save_path)
    
    print(f'\n{n}×{m}の掛け算表で見つかったユニークな答え:')
    print(sorted(unique_results))

