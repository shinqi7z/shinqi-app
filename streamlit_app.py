# streamlit_app.py
import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import io
from PIL import Image
import pandas as pd
import base64

# 页面配置
st.set_page_config(
    page_title="Web-based Generative Poster",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("🎨 Web-based Generative Poster")
st.markdown("""
### Arts & Advanced Big Data - Week 9
**Sungkyunkwan University** | Prof. Jahwan Koo

基于现代软件开发流程的生成式艺术Web应用：
**Colab → GitHub → Streamlit Cloud → Web Service**
""")

# 生成式海报核心类
class WebGenerativePoster:
    def __init__(self):
        self.fig = None
        self.ax = None
        
    def random_palette(self, k=5, style="pastel"):
        """生成随机调色板"""
        palette = []
        
        if style == "pastel":
            # 柔和色调
            for _ in range(k):
                r = random.random() * 0.5 + 0.5
                g = random.random() * 0.5 + 0.5
                b = random.random() * 0.5 + 0.5
                palette.append((r, g, b))
        elif style == "vivid":
            # 鲜艳色调
            for _ in range(k):
                r = random.random()
                g = random.random()
                b = random.random()
                palette.append((r, g, b))
        elif style == "monochrome":
            # 单色调
            base_hue = random.random()
            for _ in range(k):
                variation = random.random() * 0.3 + 0.4
                palette.append((base_hue * variation, base_hue * variation, base_hue * variation))
        elif style == "earth":
            # 大地色调
            earth_colors = [
                (0.6, 0.4, 0.2),   # 棕色
                (0.8, 0.6, 0.4),   # 米色
                (0.4, 0.3, 0.2),   # 深棕
                (0.7, 0.5, 0.3),   # 陶土色
                (0.9, 0.7, 0.5)    # 沙色
            ]
            palette = random.sample(earth_colors, min(k, len(earth_colors)))
        elif style == "ocean":
            # 海洋色调
            ocean_colors = [
                (0.2, 0.4, 0.8),   # 蓝色
                (0.3, 0.5, 0.9),   # 天蓝
                (0.1, 0.3, 0.6),   # 深蓝
                (0.4, 0.7, 0.9),   # 浅蓝
                (0.2, 0.6, 0.8)    # 青蓝
            ]
            palette = random.sample(ocean_colors, min(k, len(ocean_colors)))
        else:
            # 默认随机颜色
            for _ in range(k):
                palette.append((random.random(), random.random(), random.random()))
                
        return palette

    def generate_blob(self, center=(0.5, 0.5), radius=0.3, complexity=5, wobble=0.15, points=200):
        """生成有机形状"""
        angles = np.linspace(0, 2 * math.pi, points)
        radii = np.ones_like(angles) * radius
        
        # 添加多个正弦波创造有机形状
        for i in range(complexity):
            frequency = random.randint(2, 8)
            amplitude = random.random() * wobble * radius
            phase = random.random() * 2 * math.pi
            radii += amplitude * np.sin(frequency * angles + phase)
        
        radii = np.maximum(radii, radius * 0.2)
        
        x = center[0] + radii * np.cos(angles)
        y = center[1] + radii * np.sin(angles)
        
        return x, y

    def create_poster(self, seed=None, n_layers=8, size=(10, 12),
                     wobble_range=(0.1, 0.3), radius_range=(0.1, 0.4),
                     palette_style="pastel", style_preset="default",
                     background_color=(0.98, 0.98, 0.97), title=True):
        """创建生成式海报"""
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # 应用风格预设
        if style_preset == "minimal":
            n_layers = max(4, n_layers - 2)
            wobble_range = (0.05, 0.15)
            radius_range = (0.08, 0.25)
            palette_style = "monochrome"
            background_color = (0.95, 0.95, 0.95)
        elif style_preset == "vivid":
            n_layers = n_layers + 2
            wobble_range = (0.2, 0.4)
            radius_range = (0.15, 0.45)
            palette_style = "vivid"
        elif style_preset == "noisetouch":
            wobble_range = (0.25, 0.5)
            radius_range = (0.05, 0.35)
            palette_style = "pastel"
        elif style_preset == "organic":
            wobble_range = (0.3, 0.6)
            radius_range = (0.08, 0.3)
            palette_style = "earth"
        elif style_preset == "aquatic":
            wobble_range = (0.15, 0.35)
            radius_range = (0.12, 0.4)
            palette_style = "ocean"
        
        # 创建图形
        self.fig, self.ax = plt.subplots(1, 1, figsize=size)
        self.ax.set_facecolor(background_color)
        self.fig.patch.set_facecolor(background_color)
        
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        
        # 生成调色板
        palette = self.random_palette(n_layers + 3, palette_style)
        
        # 创建图层
        for i in range(n_layers):
            center_x = 0.5 + (random.random() - 0.5) * 0.7
            center_y = 0.5 + (random.random() - 0.5) * 0.7
            
            radius = random.uniform(radius_range[0], radius_range[1])
            complexity = random.randint(4, 7)
            wobble = random.uniform(wobble_range[0], wobble_range[1])
            alpha = random.uniform(0.3, 0.7)
            
            x, y = self.generate_blob(
                center=(center_x, center_y),
                radius=radius,
                complexity=complexity,
                wobble=wobble
            )
            
            color = random.choice(palette)
            
            vertices = np.column_stack([x, y])
            polygon = Polygon(
                vertices,
                closed=True,
                facecolor=color,
                alpha=alpha,
                edgecolor='none',
                linewidth=0
            )
            self.ax.add_patch(polygon)
        
        # 添加标题和信息
        if title:
            title_text = "Generative Poster | Arts & Advanced Big Data"
            self.ax.text(0.5, 0.02, title_text,
                        transform=self.ax.transAxes,
                        ha='center', va='bottom',
                        fontsize=10, alpha=0.7, color='#333333')
            
            info_text = f"Layers: {n_layers} | Style: {style_preset} | Seed: {seed if seed else 'Random'}"
            self.ax.text(0.5, 0.96, info_text,
                        transform=self.ax.transAxes,
                        ha='center', va='top',
                        fontsize=9, alpha=0.6, color='#666666')
        
        plt.tight_layout()
        return self.fig

# 侧边栏 - 控制面板
st.sidebar.header("🎛️ Control Panel")

# 基础参数
st.sidebar.subheader("Basic Parameters")
seed = st.sidebar.number_input("Random Seed", value=42, help="Use the same seed to reproduce results")
n_layers = st.sidebar.slider("Number of Layers", 3, 25, 10, help="More layers create more complex designs")

# 风格选择
st.sidebar.subheader("Style Settings")
style_preset = st.sidebar.selectbox(
    "Art Style Preset",
    ["default", "minimal", "vivid", "noisetouch", "organic", "aquatic"],
    index=0,
    help="Choose different artistic style presets"
)

palette_style = st.sidebar.selectbox(
    "Color Palette",
    ["pastel", "vivid", "monochrome", "earth", "ocean"],
    index=0,
    help="Choose color palette style"
)

# 高级参数
st.sidebar.subheader("Advanced Parameters")
with st.sidebar.expander("Shape Controls"):
    col1, col2 = st.columns(2)
    with col1:
        wobble_min = st.slider("Min Wobble", 0.01, 0.5, 0.1, 0.01)
        radius_min = st.slider("Min Radius", 0.05, 0.3, 0.1, 0.01)
    with col2:
        wobble_max = st.slider("Max Wobble", 0.1, 1.0, 0.3, 0.01)
        radius_max = st.slider("Max Radius", 0.1, 0.6, 0.4, 0.01)

with st.sidebar.expander("Canvas Settings"):
    canvas_width = st.slider("Canvas Width", 6, 16, 10)
    canvas_height = st.slider("Canvas Height", 8, 20, 12)
    show_title = st.checkbox("Show Title & Info", value=True)

# 确保参数有效性
if wobble_min > wobble_max:
    wobble_min, wobble_max = wobble_max, wobble_min
if radius_min > radius_max:
    radius_min, radius_max = radius_max, radius_min

# 主内容区域
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎨 Poster Generator")
    
    # 生成按钮
    if st.button("✨ Generate New Poster", type="primary", use_container_width=True):
        with st.spinner("Creating your generative poster..."):
            # 创建海报
            generator = WebGenerativePoster()
            fig = generator.create_poster(
                seed=seed if seed != 0 else None,
                n_layers=n_layers,
                size=(canvas_width, canvas_height),
                wobble_range=(wobble_min, wobble_max),
                radius_range=(radius_min, radius_max),
                palette_style=palette_style,
                style_preset=style_preset,
                title=show_title
            )
            
            # 显示海报
            st.pyplot(fig)
            
            # 保存到session state
            st.session_state.current_fig = fig
            st.session_state.generator = generator
            
            plt.close(fig)

    # 显示当前海报（如果存在）
    if 'current_fig' in st.session_state:
        st.pyplot(st.session_state.current_fig)

with col2:
    st.subheader("📥 Export Options")
    
    if 'current_fig' in st.session_state:
        # 创建下载缓冲区
        buf = io.BytesIO()
        st.session_state.current_fig.savefig(
            buf, 
            format="png", 
            dpi=300, 
            bbox_inches='tight',
            facecolor=st.session_state.current_fig.get_facecolor(),
            edgecolor='none'
        )
        buf.seek(0)
        
        # 下载按钮
        st.download_button(
            label="📥 Download PNG (300 DPI)",
            data=buf,
            file_name=f"generative_poster_seed_{seed}.png",
            mime="image/png",
            use_container_width=True
        )
        
        # 预览小图
        st.image(buf, caption="Preview", use_column_width=True)
        
        # 参数摘要
        st.subheader("📊 Parameters Summary")
        st.json({
            "seed": seed if seed != 0 else "Random",
            "layers": n_layers,
            "style": style_preset,
            "palette": palette_style,
            "wobble_range": [wobble_min, wobble_max],
            "radius_range": [radius_min, radius_max],
            "canvas_size": [canvas_width, canvas_height]
        })

# 快速示例部分
st.markdown("---")
st.subheader("🚀 Quick Examples")

example_cols = st.columns(4)

with example_cols[0]:
    if st.button("Minimal Style", use_container_width=True):
        st.session_state.seed = 123
        st.session_state.n_layers = 6
        st.session_state.style_preset = "minimal"
        st.rerun()

with example_cols[1]:
    if st.button("Vivid Explosion", use_container_width=True):
        st.session_state.seed = 456
        st.session_state.n_layers = 15
        st.session_state.style_preset = "vivid"
        st.rerun()

with example_cols[2]:
    if st.button("Organic Forms", use_container_width=True):
        st.session_state.seed = 789
        st.session_state.n_layers = 12
        st.session_state.style_preset = "organic"
        st.rerun()

with example_cols[3]:
    if st.button("Random Creation", use_container_width=True):
        st.session_state.seed = random.randint(1, 10000)
        st.session_state.n_layers = random.randint(8, 18)
        st.session_state.style_preset = random.choice(["default", "vivid", "noisetouch", "organic"])
        st.rerun()

# 使用说明
with st.expander("📖 How to Use & Technical Details"):
    st.markdown("""
    ## 🎯 How to Use This Web App
    
    ### Basic Workflow:
    1. **Adjust Parameters**: Use the control panel on the left to customize your poster
    2. **Generate**: Click the "Generate New Poster" button to create your design
    3. **Download**: Save your favorite creations as high-quality PNG files
    
    ### Parameter Guide:
    
    - **Random Seed**: Same seed = same design (perfect for reproducibility)
    - **Layers**: More layers = more complex, overlapping shapes
    - **Art Styles**:
        - **Default**: Balanced organic shapes
        - **Minimal**: Clean, monochromatic aesthetic
        - **Vivid**: Bright, high-contrast colors
        - **NoiseTouch**: High randomness, organic feel
        - **Organic**: Earth tones, natural forms
        - **Aquatic**: Ocean-inspired blue palette
    
    - **Shape Controls**:
        - **Wobble**: Controls how irregular the shapes are
        - **Radius**: Controls the size of the shapes
    
    ### Technical Background:
    
    This web application demonstrates the modern software development workflow:
    
    ```
    Colab (Development) → GitHub (Version Control) → Streamlit Cloud (Deployment) → Web Service
    ```
    
    **Technologies Used:**
    - Python + Matplotlib (Generative Art)
    - Streamlit (Web Framework)
    - NumPy (Mathematical Operations)
    - Streamlit Cloud (Hosting Platform)
    
    **Algorithm Details:**
    - Organic shapes are created using trigonometric functions with multiple sine waves
    - Randomness is controlled through seed values for reproducibility
    - Color palettes are algorithmically generated based on selected styles
    
    ### Educational Context:
    
    This project is based on the "Coding with Prompt" methodology from:
    - **Course**: Arts and Advanced Big Data
    - **University**: Sungkyunkwan University
    - **Professor**: Jahwan Koo
    - **Week 9**: Web-based Generative Poster
    """)

# 开发流程展示
st.markdown("---")
st.subheader("🔄 Modern Development Workflow")

workflow_cols = st.columns(4)

with workflow_cols[0]:
    st.markdown("""
    ### 1. Sandbox Development
    🏗️ **Google Colab**
    - Code prototyping
    - AI-assisted coding
    - Rapid iteration
    """)

with workflow_cols[1]:
    st.markdown("""
    ### 2. Version Control
    📚 **GitHub Repository**
    - Code management
    - Collaboration
    - Version history
    """)

with workflow_cols[2]:
    st.markdown("""
    ### 3. Cloud Deployment
    ☁️ **Streamlit Cloud**
    - Automatic deployment
    - Web service hosting
    - Scalable infrastructure
    """)

with workflow_cols[3]:
    st.markdown("""
    ### 4. Web Service
    🌐 **Browser Access**
    - User-friendly interface
    - Real-time generation
    - Global accessibility
    """)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>Arts & Advanced Big Data | Week 9 - Web-based Generative Poster</p>
    <p>Sungkyunkwan University | Prof. Jahwan Koo | 2024</p>
    <p>Built with Streamlit • Deployed on Streamlit Cloud</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 初始化session state
if 'seed' not in st.session_state:
    st.session_state.seed = 42
if 'n_layers' not in st.session_state:
    st.session_state.n_layers = 10
if 'style_preset' not in st.session_state:
    st.session_state.style_preset = "default"
