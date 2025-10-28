# simple_streamlit_app.py
import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import io

st.set_page_config(page_title="Simple Generative Poster", layout="centered")

st.title("Web-based Generative Poster")

if st.button("Generate Poster"):
    # 随机生成参数
    seed = random.randint(1, 10000)
    n_layers = random.randint(6, 15)
    styles = ["default", "minimal", "vivid", "noisetouch", "organic", "aquatic"]
    style_preset = random.choice(styles)
    palette_styles = ["pastel", "vivid", "monochrome", "earth", "ocean"]
    palette_style = random.choice(palette_styles)

    # 固定画布大小
    size = (10, 12)

    # 设置随机种子
    random.seed(seed)
    np.random.seed(seed)

    # 创建图形
    fig, ax = plt.subplots(1, 1, figsize=size)
    ax.set_facecolor((0.98, 0.98, 0.97))
    fig.patch.set_facecolor((0.98, 0.98, 0.97))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # 生成调色板
    def random_palette(k=5, style="pastel"):
        palette = []
        if style == "pastel":
            for _ in range(k):
                r = random.random() * 0.5 + 0.5
                g = random.random() * 0.5 + 0.5
                b = random.random() * 0.5 + 0.5
                palette.append((r, g, b))
        elif style == "vivid":
            for _ in range(k):
                r = random.random()
                g = random.random()
                b = random.random()
                palette.append((r, g, b))
        elif style == "monochrome":
            base_hue = random.random()
            for _ in range(k):
                variation = random.random() * 0.3 + 0.4
                palette.append((base_hue * variation, base_hue * variation, base_hue * variation))
        elif style == "earth":
            earth_colors = [(0.6, 0.4, 0.2), (0.8, 0.6, 0.4), (0.4, 0.3, 0.2), (0.7, 0.5, 0.3), (0.9, 0.7, 0.5)]
            palette = random.sample(earth_colors, min(k, len(earth_colors)))
        elif style == "ocean":
            ocean_colors = [(0.2, 0.4, 0.8), (0.3, 0.5, 0.9), (0.1, 0.3, 0.6), (0.4, 0.7, 0.9), (0.2, 0.6, 0.8)]
            palette = random.sample(ocean_colors, min(k, len(ocean_colors)))
        else:
            for _ in range(k):
                palette.append((random.random(), random.random(), random.random()))
        return palette

    # 生成形状的函数
    def generate_blob(center=(0.5, 0.5), radius=0.3, complexity=5, wobble=0.15, points=200):
        angles = np.linspace(0, 2 * math.pi, points)
        radii = np.ones_like(angles) * radius
        for i in range(complexity):
            frequency = random.randint(2, 8)
            amplitude = random.random() * wobble * radius
            phase = random.random() * 2 * math.pi
            radii += amplitude * np.sin(frequency * angles + phase)
        radii = np.maximum(radii, radius * 0.2)
        x = center[0] + radii * np.cos(angles)
        y = center[1] + radii * np.sin(angles)
        return x, y

    palette = random_palette(n_layers + 3, palette_style)

    # 创建图层
    for i in range(n_layers):
        center_x = 0.5 + (random.random() - 0.5) * 0.7
        center_y = 0.5 + (random.random() - 0.5) * 0.7
        radius = random.uniform(0.1, 0.4)
        complexity = random.randint(4, 7)
        wobble = random.uniform(0.1, 0.3)
        alpha = random.uniform(0.3, 0.7)

        x, y = generate_blob(
            center=(center_x, center_y),
            radius=radius,
            complexity=complexity,
            wobble=wobble
        )

        color = random.choice(palette)
        vertices = np.column_stack([x, y])
        polygon = Polygon(vertices, closed=True, facecolor=color, alpha=alpha, edgecolor='none', linewidth=0)
        ax.add_patch(polygon)

    # 添加标题和信息
    title_text = "Generative Poster | Arts & Advanced Big Data"
    ax.text(0.5, 0.02, title_text, transform=ax.transAxes, ha='center', va='bottom', fontsize=10, alpha=0.7, color='#333333')
    info_text = f"Layers: {n_layers} | Style: {style_preset} | Seed: {seed}"
    ax.text(0.5, 0.96, info_text, transform=ax.transAxes, ha='center', va='top', fontsize=9, alpha=0.6, color='#666666')

    plt.tight_layout()

    # 显示海报
    st.pyplot(fig)

    # 提供下载
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    st.download_button(
        label="Download Poster",
        data=buf,
        file_name=f"poster_{seed}.png",
        mime="image/png"
    )

    plt.close(fig)
