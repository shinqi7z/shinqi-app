# streamlit_app.py
import streamlit as st
import requests
import pandas as pd
import json
from PIL import Image
import io
import random

# 页面配置
st.set_page_config(
    page_title="Explore Artworks with MET Museum API",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("🏛️ Explore Artworks with MET Museum API")
st.markdown("""
### Arts & Advanced Big Data - Week 10
**Sungkyunkwan University** | Prof. Jahwan Koo

使用MET Museum的开放API探索世界艺术珍品
""")

# MET Museum API 基础URL
MET_API_BASE = "https://collectionapi.metmuseum.org/public/collection/v1"

class METMuseumExplorer:
    def __init__(self):
        self.session = requests.Session()
    
    def search_artworks(self, query, limit=20):
        """搜索艺术品"""
        try:
            # 搜索API
            search_url = f"{MET_API_BASE}/search"
            params = {
                'q': query,
                'hasImages': True  # 只返回有图片的作品
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                data = response.json()
                object_ids = data.get('objectIDs', [])[:limit]
                
                artworks = []
                for obj_id in object_ids:
                    artwork = self.get_artwork_details(obj_id)
                    if artwork and artwork.get('primaryImage'):
                        artworks.append(artwork)
                
                return artworks
            else:
                st.error(f"搜索失败: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"搜索过程中出现错误: {e}")
            return []
    
    def get_artwork_details(self, object_id):
        """获取艺术品详细信息"""
        try:
            details_url = f"{MET_API_BASE}/objects/{object_id}"
            response = self.session.get(details_url)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None
    
    def get_random_artworks(self, limit=12):
        """获取随机艺术品"""
        try:
            # 获取所有有图片的艺术品ID
            search_url = f"{MET_API_BASE}/search"
            params = {
                'hasImages': True,
                'q': ''  # 空搜索返回所有
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                data = response.json()
                all_ids = data.get('objectIDs', [])
                
                # 随机选择
                random_ids = random.sample(all_ids, min(limit, len(all_ids)))
                
                artworks = []
                for obj_id in random_ids:
                    artwork = self.get_artwork_details(obj_id)
                    if artwork and artwork.get('primaryImage'):
                        artworks.append(artwork)
                
                return artworks
            return []
        except:
            return []

# 侧边栏
st.sidebar.header("🔍 Search Options")

# 搜索选项
search_type = st.sidebar.radio(
    "Search Type",
    ["Keyword Search", "Random Exploration", "By Department"]
)

# 初始化探索器
explorer = METMuseumExplorer()

# 主内容区域
if search_type == "Keyword Search":
    st.subheader("🔍 Search for Artworks")
    
    # 搜索框
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Enter keywords to search:",
            placeholder="e.g., flower, portrait, landscape...",
            value="flower"
        )
    with col2:
        results_limit = st.number_input("Results limit", min_value=5, max_value=50, value=12)
    
    if st.button("Search Artworks", type="primary"):
        if search_query:
            with st.spinner("Searching MET Museum collection..."):
                artworks = explorer.search_artworks(search_query, results_limit)
                
                if artworks:
                    st.success(f"Found {len(artworks)} artworks!")
                    
                    # 显示艺术品网格
                    cols = st.columns(3)
                    for idx, artwork in enumerate(artworks):
                        col = cols[idx % 3]
                        
                        with col:
                            # 显示图片
                            if artwork.get('primaryImage'):
                                try:
                                    response = requests.get(artwork['primaryImage'])
                                    image = Image.open(io.BytesIO(response.content))
                                    st.image(image, use_column_width=True)
                                except:
                                    st.image("https://via.placeholder.com/300x200?text=Image+Not+Available", 
                                            use_column_width=True)
                            
                            # 显示信息
                            title = artwork.get('title', 'Unknown Title')
                            artist = artwork.get('artistDisplayName', 'Unknown Artist')
                            date = artwork.get('objectDate', 'Unknown Date')
                            department = artwork.get('department', 'Unknown Department')
                            
                            st.markdown(f"**{title}**")
                            st.caption(f"**Artist:** {artist}")
                            st.caption(f"**Date:** {date}")
                            st.caption(f"**Department:** {department}")
                            
                            # 显示更多信息的按钮
                            with st.expander("More Details"):
                                st.write(f"**Culture:** {artwork.get('culture', 'N/A')}")
                                st.write(f"**Medium:** {artwork.get('medium', 'N/A')}")
                                st.write(f"**Dimensions:** {artwork.get('dimensions', 'N/A')}")
                                
                                if artwork.get('objectURL'):
                                    st.markdown(f"[View on MET Website]({artwork['objectURL']})")
                            
                            st.markdown("---")
                else:
                    st.warning("No artworks found with images. Try different keywords.")
        else:
            st.warning("Please enter search keywords")

elif search_type == "Random Exploration":
    st.subheader("🎲 Random Art Exploration")
    st.markdown("Discover random artworks from the MET Museum collection")
    
    if st.button("Explore Random Artworks", type="primary"):
        with st.spinner("Fetching random artworks from MET collection..."):
            artworks = explorer.get_random_artworks(12)
            
            if artworks:
                st.success(f"Showing {len(artworks)} random artworks!")
                
                # 显示随机艺术品网格
                cols = st.columns(3)
                for idx, artwork in enumerate(artworks):
                    col = cols[idx % 3]
                    
                    with col:
                        # 显示图片
                        if artwork.get('primaryImage'):
                            try:
                                response = requests.get(artwork['primaryImage'])
                                image = Image.open(io.BytesIO(response.content))
                                st.image(image, use_column_width=True)
                            except:
                                st.image("https://via.placeholder.com/300x200?text=Image+Not+Available", 
                                        use_column_width=True)
                        
                        # 显示信息
                        title = artwork.get('title', 'Unknown Title')[:50] + "..." if len(artwork.get('title', '')) > 50 else artwork.get('title', 'Unknown Title')
                        artist = artwork.get('artistDisplayName', 'Unknown Artist')
                        date = artwork.get('objectDate', 'Unknown Date')
                        
                        st.markdown(f"**{title}**")
                        st.caption(f"**Artist:** {artist}")
                        st.caption(f"**Date:** {date}")
                        
                        st.markdown("---")
            else:
                st.error("Failed to fetch random artworks")

else:  # By Department
    st.subheader("🏛️ Browse by Department")
    
    # MET Museum的主要部门
    departments = {
        "American Decorative Arts": "American Decorative Arts",
        "Ancient Near Eastern Art": "Ancient Near Eastern Art",
        "Arms and Armor": "Arms and Armor",
        "Arts of Africa, Oceania, and the Americas": "Arts of Africa, Oceania, and the Americas",
        "Asian Art": "Asian Art",
        "The Cloisters": "The Cloisters",
        "The Costume Institute": "The Costume Institute",
        "Drawings and Prints": "Drawings and Prints",
        "Egyptian Art": "Egyptian Art",
        "European Paintings": "European Paintings",
        "European Sculpture and Decorative Arts": "European Sculpture and Decorative Arts",
        "Greek and Roman Art": "Greek and Roman Art",
        "Islamic Art": "Islamic Art",
        "The Robert Lehman Collection": "The Robert Lehman Collection",
        "Medieval Art": "Medieval Art",
        "Musical Instruments": "Musical Instruments",
        "Photographs": "Photographs",
        "Modern Art": "Modern Art"
    }
    
    selected_dept = st.selectbox("Select Department:", list(departments.keys()))
    
    if st.button(f"Browse {selected_dept}", type="primary"):
        with st.spinner(f"Searching {selected_dept} collection..."):
            # 使用部门名称搜索
            artworks = explorer.search_artworks(departments[selected_dept], 15)
            
            if artworks:
                st.success(f"Found {len(artworks)} artworks in {selected_dept}!")
                
                # 显示部门艺术品网格
                cols = st.columns(3)
                for idx, artwork in enumerate(artworks):
                    col = cols[idx % 3]
                    
                    with col:
                        # 显示图片
                        if artwork.get('primaryImage'):
                            try:
                                response = requests.get(artwork['primaryImage'])
                                image = Image.open(io.BytesIO(response.content))
                                st.image(image, use_column_width=True)
                            except:
                                st.image("https://via.placeholder.com/300x200?text=Image+Not+Available", 
                                        use_column_width=True)
                        
                        # 显示信息
                        title = artwork.get('title', 'Unknown Title')
                        artist = artwork.get('artistDisplayName', 'Unknown Artist')
                        date = artwork.get('objectDate', 'Unknown Date')
                        
                        st.markdown(f"**{title}**")
                        st.caption(f"**Artist:** {artist}")
                        st.caption(f"**Date:** {date}")
                        
                        st.markdown("---")
            else:
                st.warning(f"No artworks found in {selected_dept}. Try a different department.")

# 特色搜索部分
st.markdown("---")
st.subheader("🚀 Quick Searches")

quick_cols = st.columns(4)

with quick_cols[0]:
    if st.button("🌺 Flowers", use_container_width=True):
        st.session_state.search_query = "flower"
        st.session_state.search_type = "Keyword Search"
        st.rerun()

with quick_cols[1]:
    if st.button("🎭 Portraits", use_container_width=True):
        st.session_state.search_query = "portrait"
        st.session_state.search_type = "Keyword Search"
        st.rerun()

with quick_cols[2]:
    if st.button("🏞️ Landscape", use_container_width=True):
        st.session_state.search_query = "landscape"
        st.session_state.search_type = "Keyword Search"
        st.rerun()

with quick_cols[3]:
    if st.button("⚔️ Armor", use_container_width=True):
        st.session_state.search_query = "armor"
        st.session_state.search_type = "Keyword Search"
        st.rerun()

# API信息部分
with st.sidebar.expander("ℹ️ About MET Museum API"):
    st.markdown("""
    **MET Museum Open Access API**
    
    The Metropolitan Museum of Art provides public access to:
    - 406,000+ high-resolution images
    - Complete artwork metadata
    - Search and browse functionality
    
    All data is available under Creative Commons Zero (CC0).
    
    [Learn More](https://metmuseum.github.io/)
    """)

# 技术信息
with st.sidebar.expander("🔧 Technical Details"):
    st.markdown("""
    **Built with:**
    - Streamlit (Web Framework)
    - MET Museum API (Data Source)
    - Requests (HTTP Client)
    - Pillow (Image Processing)
    
    **API Endpoints Used:**
    - `/search` - Search artworks
    - `/objects/{id}` - Get artwork details
    """)

# 初始化session state
if 'search_query' not in st.session_state:
    st.session_state.search_query = "flower"
if 'search_type' not in st.session_state:
    st.session_state.search_type = "Keyword Search"

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>Arts & Advanced Big Data | Week 10 - Open API Integration</p>
    <p>Sungkyunkwan University | Prof. Jahwan Koo | 2024</p>
    <p>Data provided by The Metropolitan Museum of Art</p>
    </div>
    """,
    unsafe_allow_html=True
)
