import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
import random
import calendar
import database as db

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="🌾 Liz Farm Enterprise - Complete Management",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DATABASE INIT
# ============================================
db.init_db()
if '_db_loaded' not in st.session_state:
    db.load_all()
    st.session_state._db_loaded = True

def save(session_key, edited_df):
    """Persist an edited DataFrame back to SQLite and update session_state."""
    st.session_state[session_key] = edited_df
    db.save_table(session_key, edited_df)

# ============================================
# CREATIVE FARM CSS — ANIMATED BACKGROUND
# ============================================
st.markdown("""
<style>
/* ─── SOFT GRADIENT BACKGROUND ─── */
.stApp {
    background: linear-gradient(160deg, #fef9ef 0%, #fdf5e6 30%, #fff8e1 60%, #fef9ef 100%);
    background-attachment: fixed;
}
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    background:
        radial-gradient(ellipse 800px 600px at 20% 20%, rgba(255,243,224,0.5) 0%, transparent 70%),
        radial-gradient(ellipse 600px 500px at 80% 80%, rgba(255,224,178,0.4) 0%, transparent 70%),
        radial-gradient(ellipse 400px 400px at 50% 50%, rgba(255,236,179,0.3) 0%, transparent 70%);
}

/* Floating particles */
.farm-particles {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.farm-particles span {
    position: absolute;
    display: block;
    font-size: 1.5em;
    animation: floatUp linear infinite;
    opacity: 0.35;
    filter: blur(0.5px);
}
.farm-particles span:nth-child(1) { left: 3%; animation-duration: 18s; animation-delay: 0s; font-size: 1em; }
.farm-particles span:nth-child(2) { left: 12%; animation-duration: 22s; animation-delay: 3s; font-size: 1.4em; }
.farm-particles span:nth-child(3) { left: 25%; animation-duration: 16s; animation-delay: 1s; font-size: 0.9em; }
.farm-particles span:nth-child(4) { left: 38%; animation-duration: 25s; animation-delay: 5s; font-size: 1.6em; }
.farm-particles span:nth-child(5) { left: 52%; animation-duration: 20s; animation-delay: 2s; font-size: 1.1em; }
.farm-particles span:nth-child(6) { left: 65%; animation-duration: 19s; animation-delay: 4s; font-size: 1.3em; }
.farm-particles span:nth-child(7) { left: 78%; animation-duration: 24s; animation-delay: 0.5s; font-size: 0.8em; }
.farm-particles span:nth-child(8) { left: 88%; animation-duration: 17s; animation-delay: 6s; font-size: 1.5em; }
.farm-particles span:nth-child(9) { left: 32%; animation-duration: 21s; animation-delay: 3.5s; font-size: 1em; }
.farm-particles span:nth-child(10) { left: 72%; animation-duration: 15s; animation-delay: 7s; font-size: 1.2em; }
@keyframes floatUp {
    0%   { transform: translateY(110vh) rotate(0deg) scale(0.8); opacity: 0; }
    10%  { opacity: 0.5; }
    50%  { opacity: 0.3; }
    90%  { opacity: 0.15; }
    100% { transform: translateY(-10vh) rotate(360deg) scale(1.1); opacity: 0; }
}

/* Walking chicken */
.walking-chicken {
    position: fixed;
    bottom: 12px;
    font-size: 1.8em;
    z-index: 1;
    animation: walkAcross 25s linear infinite;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.15));
}
@keyframes walkAcross {
    0%   { left: -5%; transform: scaleX(1); }
    49%  { left: 105%; transform: scaleX(1); }
    50%  { left: 105%; transform: scaleX(-1); }
    99%  { left: -5%; transform: scaleX(-1); }
    100% { left: -5%; transform: scaleX(1); }
}

/* Swaying tree */
.swaying-tree {
    position: fixed;
    bottom: 15px;
    right: 25px;
    font-size: 2.5em;
    z-index: 1;
    animation: swayTree 5s ease-in-out infinite;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));
    transform-origin: bottom center;
}
@keyframes swayTree {
    0%, 100% { transform: rotate(-2deg); }
    50% { transform: rotate(2deg); }
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.5); border-radius: 10px; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #FFB74D, #FF9800, #E65100); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #FF9800, #F57C00, #E65100); }

/* ─── BUTTONS ─── */
.stButton > button {
    background: linear-gradient(135deg, #E65100 0%, #F57C00 50%, #FFB74D 100%);
    color: white;
    font-weight: 600;
    border-radius: 50px;
    padding: 0.65rem 2rem;
    border: none;
    transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 4px 15px rgba(230, 81, 0, 0.2);
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(230, 81, 0, 0.3);
    background: linear-gradient(135deg, #BF360C 0%, #E65100 50%, #F57C00 100%);
}

/* ─── SECTION HEADERS ─── */
.section-header {
    background: linear-gradient(135deg, #E65100 0%, #F57C00 50%, #FFB74D 100%);
    padding: 20px 30px;
    border-radius: 20px;
    color: white;
    margin: 35px 0 25px 0;
    font-size: 1.3em;
    font-weight: 600;
    box-shadow: 0 4px 20px rgba(230, 81, 0, 0.15);
    position: relative;
    overflow: hidden;
    animation: slideIn 0.5s ease;
    letter-spacing: 0.3px;
}
.section-header::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.08) 50%, transparent 100%);
    animation: headerShine 4s ease-in-out infinite;
}
@keyframes headerShine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
.section-header::after {
    content: "";
    position: absolute;
    right: 25px;
    top: 50%;
    transform: translateY(-50%);
    width: 8px; height: 8px;
    background: rgba(255,255,255,0.3);
    border-radius: 50%;
}
@keyframes slideIn {
    from { transform: translateY(-10px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* ─── ALERT BOXES ─── */
.info-box {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 20px 24px; border-radius: 16px;
    border-left: 5px solid #42A5F5;
    margin: 12px 0;
    box-shadow: 0 2px 12px rgba(66, 165, 245, 0.1);
    transition: all 0.3s ease;
    color: #1565C0;
}
.info-box:hover { transform: translateX(4px); box-shadow: 0 4px 20px rgba(66, 165, 245, 0.15); }

.success-box {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    padding: 20px 24px; border-radius: 16px;
    border-left: 5px solid #FFB74D;
    margin: 12px 0;
    box-shadow: 0 2px 12px rgba(255, 183, 77, 0.1);
    transition: all 0.3s ease;
    color: #2E7D32;
}
.success-box:hover { transform: translateX(4px); }

.warning-box {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    padding: 20px 24px; border-radius: 16px;
    border-left: 5px solid #FFB74D;
    margin: 12px 0;
    box-shadow: 0 2px 12px rgba(255, 183, 77, 0.1);
    color: #E65100;
}

/* ─── DASHBOARD CARDS ─── */
.dashboard-card {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(16px);
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.04), 0 0 0 1px rgba(255,255,255,0.5) inset;
    margin: 12px 0;
    transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
    border-top: 4px solid #FFB74D;
    position: relative;
}
.dashboard-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.08), 0 0 0 1px rgba(255,255,255,0.5) inset;
}

/* ─── FARM HEADER ─── */
.farm-header {
    background: linear-gradient(135deg, #BF360C 0%, #E65100 30%, #F57C00 60%, #FF9800 100%);
    padding: 50px 40px 55px;
    border-radius: 24px;
    color: white;
    text-align: center;
    margin-bottom: 35px;
    box-shadow: 0 8px 40px rgba(191, 54, 12, 0.2);
    position: relative;
    overflow: hidden;
}
.farm-header::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.1) 0%, transparent 60%);
}
.farm-header::after {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #FFD700, #FF9800, #FFD700);
}
.farm-header-glow {
    position: absolute;
    bottom: 3px; left: 0; right: 0;
    height: 20px;
    background: linear-gradient(0deg, rgba(255,215,0,0.08), transparent);
}
.liz-brand {
    font-family: Georgia, serif;
    font-size: 1.6em;
    color: #FFD700;
    text-shadow: 0 1px 10px rgba(255, 215, 0, 0.3);
    display: inline-block;
    margin-top: 8px;
}

/* ─── METRIC CARDS ─── */
.metric-card {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(16px);
    padding: 24px 18px;
    border-radius: 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.04), 0 0 0 1px rgba(255,255,255,0.5) inset;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
    position: relative;
    overflow: hidden;
    animation: cardAppear 0.5s ease backwards;
}
@keyframes cardAppear {
    from { transform: translateY(15px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
.metric-card:nth-child(1) { animation-delay: 0.05s; }
.metric-card:nth-child(2) { animation-delay: 0.1s; }
.metric-card:nth-child(3) { animation-delay: 0.15s; }
.metric-card:nth-child(4) { animation-delay: 0.2s; }
.metric-card:nth-child(5) { animation-delay: 0.25s; }
.metric-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 36px rgba(0,0,0,0.08);
}
.metric-card::after {
    content: attr(data-emoji);
    position: absolute;
    top: -8px; right: -8px;
    font-size: 2.5em;
    opacity: 0.06;
    transform: rotate(12deg);
    transition: all 0.3s ease;
}
.metric-card:hover::after {
    opacity: 0.12;
    transform: rotate(0deg) scale(1.1);
}

.glow-green { border-top: 4px solid #FFB74D; }
.glow-orange { border-top: 4px solid #FFB74D; }
.glow-blue { border-top: 4px solid #64B5F6; }
.glow-red { border-top: 4px solid #EF5350; }
.glow-purple { border-top: 4px solid #BA68C8; }
.glow-gold { border-top: 4px solid #FFD54F; }

/* ─── BIG NUMBERS ─── */
.big-number {
    font-size: 2.6em; font-weight: 800;
    background: linear-gradient(135deg, #E65100, #FFB74D);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15;
}
.big-number-orange {
    font-size: 2.6em; font-weight: 800;
    background: linear-gradient(135deg, #E65100, #FFB74D);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15;
}
.big-number-blue {
    font-size: 2.6em; font-weight: 800;
    background: linear-gradient(135deg, #1565C0, #64B5F6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15;
}
.big-number-gold {
    font-size: 2.6em; font-weight: 800;
    background: linear-gradient(135deg, #F57F17, #FFD54F);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15;
}
.big-number-red {
    font-size: 2.6em; font-weight: 800;
    background: linear-gradient(135deg, #C62828, #EF9A9A);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15;
}
.sub-label { font-size: 0.9em; color: #9E9E9E; font-weight: 500; margin-top: 4px; letter-spacing: 0.3px; }

/* ─── FOOTER ─── */
.farm-footer {
    text-align: center;
    padding: 40px;
    background: linear-gradient(135deg, #E65100 0%, #F57C00 50%, #FFB74D 100%);
    border-radius: 24px;
    color: white;
    margin-top: 50px;
    box-shadow: 0 4px 24px rgba(46, 125, 50, 0.15);
    position: relative;
    overflow: hidden;
}
.farm-footer::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,215,0,0.3), transparent);
}

/* ─── TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.5);
    backdrop-filter: blur(8px);
    padding: 8px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.3);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 10px 20px;
    background: transparent;
    transition: all 0.25s ease;
    font-weight: 500;
    color: #666;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 152, 0, 0.08);
    color: #333;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #E65100 !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    font-weight: 600;
}

/* ─── PROGRESS BARS ─── */
.stProgress > div > div {
    background: linear-gradient(90deg, #FF9800, #FFD54F);
    border-radius: 8px;
}

/* ─── EMPLOYEE CARDS ─── */
.employee-card {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(12px);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    border-left: 4px solid #FFB74D;
    margin: 10px 0;
    transition: all 0.3s ease;
}
.employee-card:hover {
    transform: translateX(6px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #BF360C 0%, #E65100 30%, #F57C00 60%, #FF9800 100%);
}
[data-testid="stSidebar"] .stRadio > div { gap: 4px; }
[data-testid="stSidebar"] [data-baseweb="radio"] {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 6px 14px;
    transition: all 0.25s ease;
    border: 1px solid rgba(255,255,255,0.04);
}
[data-testid="stSidebar"] [data-baseweb="radio"]:hover {
    background: rgba(255,255,255,0.12);
}
[data-testid="stSidebar"] [aria-checked="true"] {
    background: rgba(255,255,255,0.2) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: rgba(255,255,255,0.85) !important;
}

/* ─── SIDEBAR FARM SCENE ─── */
.sidebar-farm-scene {
    position: relative;
    height: 110px;
    margin: 8px 0 16px;
    background: linear-gradient(180deg, rgba(135,206,235,0.2) 0%, rgba(255,152,0,0.15) 60%, rgba(230,81,0,0.25) 100%);
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}
.sidebar-sun {
    position: absolute;
    top: 8px; right: 12px;
    font-size: 1.8em;
    animation: sidebarSun 5s ease-in-out infinite;
}
@keyframes sidebarSun {
    0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.8; }
    50% { transform: scale(1.05) rotate(10deg); opacity: 1; }
}
.sidebar-cloud {
    position: absolute;
    top: 6px;
    font-size: 1.2em;
    opacity: 0.6;
    animation: sidebarCloud 15s linear infinite;
}
@keyframes sidebarCloud {
    0% { left: -30px; }
    100% { left: 110%; }
}
.sidebar-tree-left {
    position: absolute;
    bottom: 5px; left: 10px;
    font-size: 1.8em;
    animation: sidebarSway 4s ease-in-out infinite;
}
.sidebar-tree-right {
    position: absolute;
    bottom: 5px; right: 10px;
    font-size: 1.6em;
    animation: sidebarSway 4.5s ease-in-out infinite reverse;
}
@keyframes sidebarSway {
    0%, 100% { transform: rotate(-3deg); }
    50% { transform: rotate(3deg); }
}
.sidebar-chicken {
    position: absolute;
    bottom: 8px;
    font-size: 1.1em;
    animation: sidebarChicken 10s ease-in-out infinite;
}
@keyframes sidebarChicken {
    0%, 100% { left: 25%; transform: scaleX(1); }
    45% { left: 60%; transform: scaleX(1); }
    50% { left: 60%; transform: scaleX(-1); }
    95% { left: 25%; transform: scaleX(-1); }
}
.sidebar-grass {
    position: absolute;
    bottom: 0;
    font-size: 0.7em;
    opacity: 0.4;
    letter-spacing: 2px;
}

/* ─── TOAST ─── */
.stToast {
    background: rgba(255,255,255,0.92) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 12px !important;
    border-left: 4px solid #FFB74D !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important;
}

/* ─── WIDER CONTENT ─── */
.block-container {
    max-width: 1200px;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}
</style>

<!-- Floating farm particles -->
<div class="farm-particles">
    <span>\U0001f33e</span><span>\U0001f343</span><span>\U0001f338</span><span>\U0001f33f</span>
    <span>\U0001f342</span><span>\U0001f33e</span><span>\U0001f33b</span><span>\U0001f343</span>
    <span>\U0001f338</span><span>\U0001f33f</span>
</div>

<!-- Walking chicken at bottom -->
<div class="walking-chicken">\U0001f414</div>

<!-- Swaying tree -->
<div class="swaying-tree">\U0001f333</div>
""", unsafe_allow_html=True)


# HELPER FUNCTIONS
# ============================================

def format_kes(amount):
    return f"KES {amount:,.0f}"

def ordered_editor(session_key, df, **kwargs):
    """Display a data editor with canonical column ordering."""
    ordered = db.order_columns(session_key, df)
    return st.data_editor(ordered, **kwargs)

def create_gauge(value, title, max_val, color="#2E7D32"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title={'text': title, 'font': {'size': 14, 'color': '#333'}},
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': '#333'},
            'bar': {'color': color}, 'bgcolor': "white",
            'steps': [
                {'range': [0, max_val * 0.5], 'color': '#e8f5e9'},
                {'range': [max_val * 0.5, max_val * 0.8], 'color': '#fff3e0'},
                {'range': [max_val * 0.8, max_val], 'color': '#ffebee'}],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_val * 0.9}
        }
    ))
    fig.update_layout(height=220, margin=dict(t=50, b=10, l=20, r=20))
    return fig

def createMiniDonut(values, labels, colors, title=""):
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.6,
        marker_colors=colors, textinfo='percent', textfont=dict(size=12)
    )])
    fig.update_layout(
        showlegend=True, height=280,
        margin=dict(t=30, b=10, l=10, r=10),
        title=dict(text=title, font=dict(size=14, color='#333'), x=0.5),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=10)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


# ============================================
# SIDEBAR NAVIGATION
# ============================================
with st.sidebar:
    # Animated farm scene
    st.markdown("""
    <div class="sidebar-farm-scene">
        <div class="sidebar-sun">☀️</div>
        <div class="sidebar-cloud">☁️</div>
        <div class="sidebar-tree-left">🌲</div>
        <div class="sidebar-tree-right">🌳</div>
        <div class="sidebar-chicken">🐔</div>
        <div class="sidebar-grass">🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding: 15px; background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); border-radius: 20px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.15);">
        <span style="font-size: 2.5em;">🌾</span>
        <br>
        <span style="color: #FFD700; font-size: 1.2em; font-weight: bold; font-family: Georgia, serif;">Liz Farm</span>
        <br>
        <span style="color: rgba(255,255,255,0.7); font-size: 0.8em;">Enterprise Manager</span>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "🐔 Livestock", "🍊 Orange Orchard", "🛒 Cereal Shop",
         "🥚 Eggs", "👤 Employees", "🐾 Pets & Feeding", "📋 Tasks",
         "🌤️ Weather", "💰 Finance", "📦 Feed Inventory", "📊 Reports",
         "💾 Backup & Restore"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8em;">
        <p>📍 Kenya | Est. 2020</p>
        <p>👨‍🌾 Owner: Liz</p>
        <p>📅 {datetime.now().strftime('%B %d, %Y')}</p>
        <p>💾 SQLite Database</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# PAGE: DASHBOARD
# ============================================
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="farm-header">
        <div class="farm-header-glow"></div>
        <h1 style="margin:0; font-size: 2.8em; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
            🌾 Liz Farm Enterprise 🌾
        </h1>
        <p style="font-size: 1.3em; opacity: 0.95; margin-top: 10px; text-shadow: 0 1px 5px rgba(0,0,0,0.1);">
            Complete Farm Management Dashboard
        </p>
        <span class="liz-brand">✨ Where Nature Meets Nurturing ✨</span>
        <br><br>
        <span style="font-size: 0.9em; opacity: 0.7;">🍊 Orange Orchard · 🐔 Poultry Farm · 🛒 Cereal Shop · 🐾 Pet Care</span>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    total_eggs_30 = st.session_state.egg_data['Total Eggs'].sum()
    total_egg_revenue = st.session_state.egg_sales_data['Total Revenue (KES)'].sum()
    total_orange_revenue = st.session_state.orange_harvest_data['Total Revenue (KES)'].sum()
    total_cereal_revenue = st.session_state.cereal_data['Total Revenue (KES)'].sum()
    total_cereal_profit = st.session_state.cereal_data['Profit/Loss (KES)'].sum()
    total_income = st.session_state.finance_data[st.session_state.finance_data['Type'] == 'Income']['Amount (KES)'].sum()
    total_expense = st.session_state.finance_data[st.session_state.finance_data['Type'] == 'Expense']['Amount (KES)'].sum()
    net_profit = total_income - total_expense
    total_livestock = st.session_state.inventory_data['Total'].sum()
    total_pet_feed_cost = st.session_state.pet_feed_data['Total Cost (KES)'].sum()
    total_employee_cost = st.session_state.payments_data['Amount (KES)'].sum()

    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class="metric-card glow-green" data-emoji="🥚">
            <div style="font-size:2.5em;">🥚</div>
            <div class="big-number">{total_eggs_30:,}</div>
            <div class="sub-label">Eggs (30 days)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card glow-gold" data-emoji="💰">
            <div style="font-size:2.5em;">💰</div>
            <div class="big-number-gold">{format_kes(total_income)}</div>
            <div class="sub-label">Total Income</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        profit_color = "glow-green" if net_profit > 0 else "glow-red"
        num_class = "big-number" if net_profit > 0 else "big-number-red"
        st.markdown(f"""
        <div class="metric-card {profit_color}" data-emoji="📈">
            <div style="font-size:2.5em;">{'📈' if net_profit > 0 else '📉'}</div>
            <div class="{num_class}">{format_kes(net_profit)}</div>
            <div class="sub-label">Net Profit</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card glow-orange" data-emoji="🐔">
            <div style="font-size:2.5em;">🐔</div>
            <div class="big-number-orange">{int(total_livestock)}</div>
            <div class="sub-label">Total Livestock</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="metric-card glow-blue" data-emoji="🌳">
            <div style="font-size:2.5em;">🌳</div>
            <div class="big-number-blue">{st.session_state.farm_overview['orange_trees']}</div>
            <div class="sub-label">Orange Trees</div>
        </div>
        """, unsafe_allow_html=True)

    # Revenue Breakdown
    st.markdown('<div class="section-header">💵 Revenue Breakdown</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="dashboard-card glow-green">
            <h3 style="margin:0; color: #333;">🥚 Egg Revenue</h3>
            <div class="big-number" style="font-size: 1.8em;">{format_kes(total_egg_revenue)}</div>
            <p style="color: #888;">{len(st.session_state.egg_sales_data)} sales recorded</p>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(createMiniDonut(
            [total_egg_revenue, total_orange_revenue, total_cereal_revenue],
            ['Eggs', 'Oranges', 'Cereals'], ['#4CAF50', '#FF9800', '#2196F3'], "Revenue Mix"
        ), use_container_width=True)
    with col2:
        st.markdown(f"""
        <div class="dashboard-card glow-orange">
            <h3 style="margin:0; color: #333;">🍊 Orange Revenue</h3>
            <div class="big-number-orange" style="font-size: 1.8em;">{format_kes(total_orange_revenue)}</div>
            <p style="color: #888;">{st.session_state.orange_harvest_data['Quantity (kg)'].sum()} kg harvested</p>
        </div>
        """, unsafe_allow_html=True)
        fig = px.bar(x=st.session_state.orange_harvest_data['Date'],
                     y=st.session_state.orange_harvest_data['Total Revenue (KES)'],
                     color=st.session_state.orange_harvest_data['Buyer'],
                     color_discrete_sequence=['#FF9800', '#FFB74D'], title="Orange Sales Trend")
        fig.update_layout(height=250, margin=dict(t=40, b=30), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        st.markdown(f"""
        <div class="dashboard-card glow-blue">
            <h3 style="margin:0; color: #333;">🛒 Cereal Revenue</h3>
            <div class="big-number-blue" style="font-size: 1.8em;">{format_kes(total_cereal_revenue)}</div>
            <p style="color: #888;">Profit: {format_kes(total_cereal_profit)}</p>
        </div>
        """, unsafe_allow_html=True)
        cereal_by_type = st.session_state.cereal_data.groupby('Cereal Type')['Profit/Loss (KES)'].sum().reset_index()
        fig = px.pie(cereal_by_type, values='Profit/Loss (KES)', names='Cereal Type',
                     color_discrete_sequence=px.colors.qualitative.Set2, title="Profit by Cereal Type")
        fig.update_layout(height=250, margin=dict(t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # Expenses
    st.markdown('<div class="section-header">💸 Expense Overview</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        expense_by_cat = st.session_state.finance_data[st.session_state.finance_data['Type'] == 'Expense'].groupby('Category')['Amount (KES)'].sum().reset_index()
        fig = px.bar(expense_by_cat, x='Category', y='Amount (KES)', color='Category',
                     color_discrete_sequence=px.colors.qualitative.Pastel, text_auto='.2s')
        fig.update_layout(height=350, margin=dict(t=20, b=30), showlegend=False,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        feed_cost = st.session_state.feed_data['Quantity (kg)'].sum() * st.session_state.feed_data['Cost per kg (KES)'].mean()
        profit_pct = (net_profit / total_income * 100) if total_income > 0 else 0
        st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="margin:0 0 15px 0;">📊 Expense Summary</h3>
            <p>💰 <strong>Total Income:</strong> {format_kes(total_income)}</p>
            <p>💸 <strong>Total Expenses:</strong> {format_kes(total_expense)}</p>
            <p>👷 <strong>Employee Costs:</strong> {format_kes(total_employee_cost)}</p>
            <p>🐾 <strong>Pet Feeding:</strong> {format_kes(total_pet_feed_cost)}</p>
            <p>📦 <strong>Feed Costs:</strong> {format_kes(feed_cost)}</p>
            <p>📈 <strong>Profit Margin:</strong> {profit_pct:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # Livestock + Weather
    st.markdown('<div class="section-header">🐔 Farm Activity & Conditions</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        inv = st.session_state.inventory_data
        fig = px.bar(inv, x='Category', y=['Male', 'Female'], barmode='group',
                     color_discrete_sequence=['#42A5F5', '#EF5350'], title="Livestock Distribution")
        fig.update_layout(height=300, margin=dict(t=40, b=30), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        weather = st.session_state.weather_data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weather['Date'], y=weather['Temperature (C)'],
                                 mode='lines+markers', name='Temperature',
                                 line=dict(color='#FF6F00', width=3), marker=dict(size=10)))
        fig.add_trace(go.Scatter(x=weather['Date'], y=weather['Humidity (%)'],
                                 mode='lines+markers', name='Humidity',
                                 line=dict(color='#2196F3', width=3, dash='dot'),
                                 marker=dict(size=10), yaxis='y2'))
        fig.update_layout(height=300, margin=dict(t=40, b=30),
                          yaxis=dict(title='Temperature (°C)', side='left'),
                          yaxis2=dict(title='Humidity (%)', side='right', overlaying='y'),
                          title="Weather Trends (7 days)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # Tasks
    st.markdown('<div class="section-header">📋 Today\'s Tasks</div>', unsafe_allow_html=True)
    tasks_df = st.session_state.tasks_data
    done = len(tasks_df[tasks_df['Status'] == '✅ Done'])
    total = len(tasks_df)
    progress = done / total if total > 0 else 0
    st.progress(progress)
    st.markdown(f"**{done}/{total} tasks completed** ({progress*100:.0f}%)")
    col1, col2, col3 = st.columns(3)
    for idx, (_, task) in enumerate(tasks_df.iterrows()):
        col = [col1, col2, col3][idx % 3]
        with col:
            priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(task['Priority'], '⚪')
            st.markdown(f"""
            <div class="dashboard-card" style="padding: 15px; margin: 5px 0;">
                {task['Status']} {priority_emoji} <strong>{task['Task']}</strong>
                <br><small style="color: #888;">👤 {task['Assigned To']} | 📁 {task['Category']}</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="farm-footer">
        <h3 style="margin:0;">🌾 Liz Farm Enterprise 🌾</h3>
        <p style="opacity: 0.9;">Nurturing Nature, Growing Prosperity</p>
        <p style="opacity: 0.7; font-size: 0.85em;">© 2026 Liz Farm Enterprise | All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# PAGE: LIVESTOCK
# ============================================
elif page == "🐔 Livestock":
    st.markdown('<div class="section-header">🐔 Livestock Inventory & Management</div>', unsafe_allow_html=True)
    inv = st.session_state.inventory_data
    total_male = inv['Male'].sum()
    total_female = inv['Female'].sum()
    total_all = inv['Total'].sum()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card glow-blue" data-emoji="♂️"><div style="font-size:2em;">♂️</div><div class="big-number-blue">{total_male}</div><div class="sub-label">Male</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card glow-red" data-emoji="♀️"><div style="font-size:2em;">♀️</div><div class="big-number-red">{total_female}</div><div class="sub-label">Female</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card glow-green" data-emoji="🐾"><div style="font-size:2em;">🐾</div><div class="big-number">{total_all}</div><div class="sub-label">Total</div></div>""", unsafe_allow_html=True)
    with c4:
        healthy = len(inv[inv['Health Status'].str.contains('Excellent')])
        st.markdown(f"""<div class="metric-card glow-gold" data-emoji="💚"><div style="font-size:2em;">💚</div><div class="big-number-gold">{healthy}/{len(inv)}</div><div class="sub-label">Healthy</div></div>""", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.pie(inv, values='Total', names='Category', color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        for _, row in inv.iterrows():
            st.markdown(f"""<div class="employee-card"><strong>{row['Category']}</strong><br>♂️ {row['Male']} | ♀️ {row['Female']} | Total: <strong>{row['Total']}</strong><br><small>📍 {row['Location']} | {row['Health Status']}</small></div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("##### ✏️ Edit Livestock Inventory")
    st.markdown("""<div class="info-box">💡 <strong>Tip:</strong> Edit Male/Female counts below. The <strong>Total</strong> column auto-calculates as Male + Female.</div>""", unsafe_allow_html=True)
    edited = ordered_editor('inventory_data', inv, use_container_width=True, num_rows="dynamic")
    if not edited.equals(inv):
        # Auto-calculate Total = Male + Female
        edited['Total'] = edited['Male'] + edited['Female']
        save('inventory_data', edited)
        # Update the displayed totals
        total_male_new = edited['Male'].sum()
        total_female_new = edited['Female'].sum()
        total_all_new = edited['Total'].sum()
        st.success(f"✅ Saved! ♂️ {total_male_new} male + ♀️ {total_female_new} female = 🐾 **{total_all_new} total animals**")
        st.rerun()


# ============================================
# PAGE: ORANGE ORCHARD
# ============================================
elif page == "🍊 Orange Orchard":
    st.markdown('<div class="section-header">🍊 Orange Orchard Management</div>', unsafe_allow_html=True)
    orchard = st.session_state.orchard_data
    harvest = st.session_state.orange_harvest_data
    total_harvest_kg = harvest['Quantity (kg)'].sum()
    total_orange_rev = harvest['Total Revenue (KES)'].sum()
    grade_a = harvest['Grade A (kg)'].sum()
    grade_b = harvest['Grade B (kg)'].sum()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card glow-orange" data-emoji="🍊"><div style="font-size:2em;">🍊</div><div class="big-number-orange">{st.session_state.farm_overview['orange_trees']}</div><div class="sub-label">Total Trees</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card glow-green" data-emoji="⚖️"><div style="font-size:2em;">⚖️</div><div class="big-number">{total_harvest_kg:,}</div><div class="sub-label">Total Harvest (kg)</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card glow-gold" data-emoji="💰"><div style="font-size:2em;">💰</div><div class="big-number-gold">{format_kes(total_orange_rev)}</div><div class="sub-label">Total Revenue</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card glow-blue" data-emoji="⭐"><div style="font-size:2em;">⭐</div><div class="big-number-blue">{grade_a}</div><div class="sub-label">Grade A (kg)</div></div>""", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🌳 Orchard Overview", "📦 Harvest Log", "📈 Revenue Analytics"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(orchard, x='Tree ID', y='Harvest (kg)', color='Quality', color_discrete_map={'Grade A': '#FF9800', 'Grade B': '#FFB74D'}, title="Harvest per Tree")
            fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            _orch = orchard.copy()
            _orch['Harvest (kg)'] = pd.to_numeric(_orch['Harvest (kg)'], errors='coerce').fillna(0)
            _orch['Age (years)'] = pd.to_numeric(_orch['Age (years)'], errors='coerce').fillna(0)
            fig = px.scatter(_orch, x='Age (years)', y='Harvest (kg)', size='Harvest (kg)', color='Quality', hover_data={'Tree ID': True, 'Age (years)': False, 'Harvest (kg)': False}, title="Age vs Harvest")
            fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("##### ✏️ Edit Orchard Data")
        edited = ordered_editor('orchard_data', orchard, use_container_width=True, num_rows="dynamic")
        if not edited.equals(orchard):
            save('orchard_data', edited)
            st.toast("✅ Orchard data saved!", icon="💾")
    with tab2:
        st.markdown("##### 📦 Harvest History")
        edited = ordered_editor('orange_harvest_data', harvest, use_container_width=True, num_rows="dynamic")
        if not edited.equals(harvest):
            save('orange_harvest_data', edited)
            st.toast("✅ Harvest log saved!", icon="💾")
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(harvest, x='Date', y='Total Revenue (KES)', markers=True, title="Revenue Trend")
            fig.update_traces(line_color='#FF9800', line_width=3)
            fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.plotly_chart(createMiniDonut([int(grade_a), int(grade_b)], [f'Grade A ({int(grade_a)} kg)', f'Grade B ({int(grade_b)} kg)'], ['#FF9800', '#FFE0B2'], "Quality Distribution"), use_container_width=True)
        st.markdown(f"**Payment Status:** {len(harvest[harvest['Payment Received'] == '✅ Yes'])}/{len(harvest)} received")


# ============================================
# PAGE: CEREAL SHOP
# ============================================
elif page == "🛒 Cereal Shop":
    st.markdown('<div class="section-header">🛒 Cereal Shop Management</div>', unsafe_allow_html=True)
    cereal = st.session_state.cereal_data
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card glow-blue" data-emoji="📊"><div style="font-size:2em;">📊</div><div class="big-number-blue">{len(cereal)}</div><div class="sub-label">Transactions</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card glow-gold" data-emoji="💰"><div style="font-size:2em;">💰</div><div class="big-number-gold">{format_kes(cereal['Total Revenue (KES)'].sum())}</div><div class="sub-label">Total Revenue</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card glow-orange" data-emoji="💸"><div style="font-size:2em;">💸</div><div class="big-number-orange">{format_kes(cereal['Total Cost (KES)'].sum())}</div><div class="sub-label">Total Cost</div></div>""", unsafe_allow_html=True)
    with c4:
        profit = cereal['Profit/Loss (KES)'].sum()
        st.markdown(f"""<div class="metric-card glow-green" data-emoji="📈"><div style="font-size:2em;">📈</div><div class="big-number">{format_kes(profit)}</div><div class="sub-label">Net Profit</div></div>""", unsafe_allow_html=True)
    cereal_inv = st.session_state.cereal_inv_data
    cereal_daily = st.session_state.cereal_daily_data
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "📈 Daily Sales", "📦 Inventory", "✏️ Sales Editor"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            cereal_profit = cereal.groupby('Cereal Type')['Profit/Loss (KES)'].sum().reset_index()
            fig = px.bar(cereal_profit, x='Cereal Type', y='Profit/Loss (KES)', color='Cereal Type', color_discrete_sequence=px.colors.qualitative.Set2, title="Profit by Cereal Type")
            fig.update_layout(height=350, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            retail_rev = cereal[cereal['Customer Type'] == 'Retail']['Total Revenue (KES)'].sum()
            wholesale_rev = cereal[cereal['Customer Type'] == 'Wholesale']['Total Revenue (KES)'].sum()
            st.plotly_chart(createMiniDonut([retail_rev, wholesale_rev], ['Retail', 'Wholesale'], ['#2196F3', '#64B5F6'], "Revenue by Customer Type"), use_container_width=True)
        fig = px.line(cereal, x='Date', y='Total Revenue (KES)', color='Cereal Type', title="Sales Trend by Cereal")
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown('##### 📈 Daily Sales Summary')
        total_rev = cereal_daily['Total Revenue (KES)'].sum()
        total_profit = cereal_daily['Profit (KES)'].sum()
        total_kg = cereal_daily['Kg Sold'].sum()
        total_cust = cereal_daily['Customers'].sum()
        dc1, dc2, dc3, dc4 = st.columns(4)
        with dc1:
            st.markdown(f"""<div class="metric-card glow-gold" data-emoji="💰"><div style="font-size:2em;">💰</div><div class="big-number-gold">{format_kes(total_rev)}</div><div class="sub-label">Total Revenue</div></div>""", unsafe_allow_html=True)
        with dc2:
            st.markdown(f"""<div class="metric-card glow-green" data-emoji="📈"><div style="font-size:2em;">📈</div><div class="big-number">{format_kes(total_profit)}</div><div class="sub-label">Total Profit</div></div>""", unsafe_allow_html=True)
        with dc3:
            st.markdown(f"""<div class="metric-card glow-blue" data-emoji="⚖️"><div style="font-size:2em;">⚖️</div><div class="big-number-blue">{total_kg:,} kg</div><div class="sub-label">Total Kg Sold</div></div>""", unsafe_allow_html=True)
        with dc4:
            st.markdown(f"""<div class="metric-card glow-orange" data-emoji="👥"><div style="font-size:2em;">👥</div><div class="big-number-orange">{total_cust:,}</div><div class="sub-label">Customers Served</div></div>""", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(cereal_daily, x='Date', y='Total Revenue (KES)', markers=True, title='Daily Revenue Trend')
            fig.update_traces(line_color='#FFB74D', line_width=3)
            fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=cereal_daily['Date'], y=cereal_daily['Profit (KES)'], mode='lines+markers', name='Profit', line=dict(color='#66BB6A', width=3), fill='tozeroy', fillcolor='rgba(102,187,106,0.1)'))
            fig.update_layout(title='Daily Profit Trend', height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(createMiniDonut([cereal_daily['Cash Sales (KES)'].sum(), cereal_daily['M-Pesa Sales (KES)'].sum(), cereal_daily['Bank Sales (KES)'].sum()], ['Cash', 'M-Pesa', 'Bank'], ['#4CAF50', '#2196F3', '#FF9800'], 'Sales by Payment Method'), use_container_width=True)
        with col2:
            fig = px.bar(cereal_daily.head(14), x='Date', y='Kg Sold', color='Sold By', color_discrete_sequence=['#66BB6A', '#FFB74D'], title='Daily Kg Sold (Last 14 days)')
            fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('##### ✏️ Edit Daily Sales')
        edited_daily = ordered_editor('cereal_daily_data', cereal_daily, use_container_width=True, num_rows='dynamic')
        if not edited_daily.equals(cereal_daily):
            save('cereal_daily_data', edited_daily)
            st.toast('✅ Daily sales saved!', icon='💾')

    with tab3:
        st.markdown('##### 📦 Cereal Shop Inventory')
        total_stock = cereal_inv['Stock (kg)'].sum()
        total_value = (cereal_inv['Stock (kg)'] * cereal_inv['Buying Price (KES/kg)']).sum()
        low_items = len(cereal_inv[cereal_inv['Stock (kg)'] <= cereal_inv['Min Stock (kg)']])
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            st.markdown(f"""<div class="metric-card glow-green" data-emoji="📦"><div style="font-size:2em;">📦</div><div class="big-number">{total_stock:,} kg</div><div class="sub-label">Total Stock</div></div>""", unsafe_allow_html=True)
        with ic2:
            st.markdown(f"""<div class="metric-card glow-gold" data-emoji="💰"><div style="font-size:2em;">💰</div><div class="big-number-gold">{format_kes(total_value)}</div><div class="sub-label">Stock Value</div></div>""", unsafe_allow_html=True)
        with ic3:
            st.markdown(f"""<div class="metric-card glow-red" data-emoji="⚠️"><div style="font-size:2em;">⚠️</div><div class="big-number-red">{low_items}</div><div class="sub-label">Low Stock Items</div></div>""", unsafe_allow_html=True)
        if low_items > 0:
            st.markdown("""<div class="warning-box">⚠️ <strong>Low Stock Alert!</strong> Some items are below minimum levels.</div>""", unsafe_allow_html=True)
            for _, item in cereal_inv[cereal_inv['Stock (kg)'] <= cereal_inv['Min Stock (kg)']].iterrows():
                st.markdown(f"**{item['Cereal Type']}**: {item['Stock (kg)']}kg (min: {item['Min Stock (kg)']}kg)")
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=cereal_inv['Cereal Type'].tolist(), y=cereal_inv['Stock (kg)'].tolist(),
                marker_color=['#f44336' if s <= m else '#4CAF50' for s, m in zip(cereal_inv['Stock (kg)'], cereal_inv['Min Stock (kg)'])],
                name='Current Stock'))
            fig.add_trace(go.Scatter(x=cereal_inv['Cereal Type'].tolist(), y=cereal_inv['Min Stock (kg)'].tolist(),
                mode='markers+lines', marker=dict(color='red', size=10, symbol='x'), name='Min Level'))
            fig.add_trace(go.Scatter(x=cereal_inv['Cereal Type'].tolist(), y=cereal_inv['Max Stock (kg)'].tolist(),
                mode='markers+lines', marker=dict(color='green', size=10, symbol='diamond'), name='Max Level'))
            fig.update_layout(title="Stock Levels vs Min/Max", height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.plotly_chart(createMiniDonut(cereal_inv['Stock (kg)'].tolist(), cereal_inv['Cereal Type'].tolist(),
                px.colors.qualitative.Set2[:len(cereal_inv)], "Stock Distribution"), use_container_width=True)
        st.markdown("##### ✏️ Edit Inventory")
        edited_inv = ordered_editor('cereal_inv_data', cereal_inv, use_container_width=True, num_rows="dynamic")
        if not edited_inv.equals(cereal_inv):
            save('cereal_inv_data', edited_inv)
            st.toast("✅ Inventory saved!", icon="💾")

    with tab4:
        st.markdown("##### ✏️ Edit Sales Transactions")
        edited = ordered_editor('cereal_data', cereal, use_container_width=True, num_rows="dynamic")
        if not edited.equals(cereal):
            save('cereal_data', edited)
            st.toast("✅ Cereal sales saved!", icon="💾")


# ============================================
# PAGE: EGGS
# ============================================
elif page == "🥚 Eggs":
    st.markdown('<div class="section-header">🥚 Egg Production & Sales</div>', unsafe_allow_html=True)
    eggs = st.session_state.egg_data
    sales = st.session_state.egg_sales_data
    total_eggs = eggs['Total Eggs'].sum()
    total_sellable = eggs['Sellable'].sum()
    total_revenue = sales['Total Revenue (KES)'].sum()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card glow-green" data-emoji="🥚"><div style="font-size:2em;">🥚</div><div class="big-number">{total_eggs:,}</div><div class="sub-label">Total Eggs</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card glow-blue" data-emoji="✅"><div style="font-size:2em;">✅</div><div class="big-number-blue">{total_sellable:,}</div><div class="sub-label">Sellable</div></div>""", unsafe_allow_html=True)
    with c3:
        cracked = eggs['Cracked'].sum()
        st.markdown(f"""<div class="metric-card glow-red" data-emoji="💔"><div style="font-size:2em;">💔</div><div class="big-number-red">{cracked}</div><div class="sub-label">Cracked</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card glow-gold" data-emoji="💰"><div style="font-size:2em;">💰</div><div class="big-number-gold">{format_kes(total_revenue)}</div><div class="sub-label">Revenue</div></div>""", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📈 Production Trends", "💰 Sales Log", "📋 Production Data"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(eggs.head(14), x='Date', y='Total Eggs', color='Quality', color_discrete_map={'Grade A': '#4CAF50', 'Grade B': '#FF9800'}, title="Daily Egg Production")
            fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=eggs['Date'], y=eggs['Sellable'], mode='lines+markers', name='Sellable', line=dict(color='#4CAF50', width=2)))
            fig.add_trace(go.Scatter(x=eggs['Date'], y=eggs['Cracked'], mode='lines+markers', name='Cracked', line=dict(color='#f44336', width=2)))
            fig.update_layout(title="Sellable vs Cracked Trend", height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        quality_counts = eggs['Quality'].value_counts().reset_index()
        quality_counts.columns = ['Quality', 'Count']
        st.plotly_chart(createMiniDonut(quality_counts['Count'].tolist(), quality_counts['Quality'].tolist(), ['#4CAF50', '#FF9800'], "Quality Distribution"), use_container_width=True)
    with tab2:
        edited = ordered_editor('egg_sales_data', sales, use_container_width=True, num_rows="dynamic")
        if not edited.equals(sales):
            save('egg_sales_data', edited)
            st.toast("✅ Egg sales saved!", icon="💾")
    with tab3:
        edited = ordered_editor('egg_data', eggs, use_container_width=True, num_rows="dynamic")
        if not edited.equals(eggs):
            save('egg_data', edited)
            st.toast("✅ Egg production saved!", icon="💾")


# ============================================
# PAGE: EMPLOYEES
# ============================================
elif page == "👤 Employees":
    st.markdown('<div class="section-header">👤 Employee Management</div>', unsafe_allow_html=True)
    emp = st.session_state.employee_data
    payments = st.session_state.payments_data
    for _, row in emp.iterrows():
        monthly_payments = payments[payments['Employee'] == row['Employee Name']]
        total_paid = monthly_payments['Amount (KES)'].sum()
        st.markdown(f"""<div class="employee-card"><div style="display: flex; justify-content: space-between; align-items: center;"><div><h3 style="margin:0;">👤 {row['Employee Name']}</h3><p style="color: #888; margin: 5px 0;">💼 {row['Role']} | 📍 {row['Work Location']} | {row['Status']}</p></div><div style="text-align: right;"><div style="font-size: 1.5em; font-weight: bold; color: #2E7D32;">{format_kes(row['Salary (KES/month)'])}/mo</div><div style="color: #888; font-size: 0.85em;">Total paid: {format_kes(total_paid)}</div></div></div><p style="color: #666; margin: 5px 0;">📱 {row['Phone']} | 📅 Since {row['Start Date']} | 💳 {row['Payment Method']}</p><p style="color: #555;"><em>{row['Notes']}</em></p></div>""", unsafe_allow_html=True)
    st.markdown("---")
    tab1, tab2 = st.tabs(["💰 Payment History", "📊 Analytics"])
    with tab1:
        edited = ordered_editor('payments_data', payments, use_container_width=True, num_rows="dynamic")
        if not edited.equals(payments):
            save('payments_data', edited)
            st.toast("✅ Payment data saved!", icon="💾")
    with tab2:
        fig = px.bar(payments, x='Month', y='Amount (KES)', color='Employee', barmode='group', color_discrete_sequence=['#4CAF50', '#2196F3'], title="Monthly Salary Payments")
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.metric("💰 Total Salary Paid (6 months)", format_kes(payments['Amount (KES)'].sum()))


# ============================================
# PAGE: PETS & FEEDING
# ============================================
elif page == "🐾 Pets & Feeding":
    st.markdown('<div class="section-header">🐾 Pet Management & Feeding Program</div>', unsafe_allow_html=True)
    pets = st.session_state.pet_feed_data
    cat_menu = st.session_state.cat_menu_data
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Feeding Log", "🐱 Cat Menu", "📝 Mortality Tracker", "📊 Cost Analysis"])
    with tab1:
        st.markdown("##### 🍽️ Feeding Schedule & Log")
        st.metric("💰 Total Pet Feeding Cost", format_kes(pets['Total Cost (KES)'].sum()))
        col1, col2 = st.columns(2)
        with col1:
            pet_summary = pets.groupby('Pet Type')['Total Cost (KES)'].sum().reset_index()
            fig = px.pie(pet_summary, values='Total Cost (KES)', names='Pet Type', color_discrete_sequence=['#FF9800', '#4CAF50'], hole=0.4, title="Cost by Pet Type")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(pets, x='Food Type', y='Total Cost (KES)', color='Pet Type', title="Cost by Food Type")
            fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        edited = ordered_editor('pet_feed_data', pets, use_container_width=True, num_rows="dynamic")
        if not edited.equals(pets):
            save('pet_feed_data', edited)
            st.toast("✅ Pet feeding data saved!", icon="💾")
    with tab2:
        st.markdown("##### 🐱 Cat Meal Menu")
        st.markdown("""<div class="info-box">🐱 <strong>Cat Feeding Program</strong> - 7 cats fed daily with balanced nutrition<br>🕐 Schedule: Breakfast (6AM), Lunch (12PM), Dinner (6PM), Treat (9PM)</div>""", unsafe_allow_html=True)
        edited = ordered_editor('cat_menu_data', cat_menu, use_container_width=True, num_rows="dynamic")
        if not edited.equals(cat_menu):
            save('cat_menu_data', edited)
            st.toast("✅ Cat menu saved!", icon="💾")
    with tab3:
        st.markdown("##### 💀 Mortality Tracker")
        st.markdown("""<div class="success-box">🎉 <strong>Great news!</strong> No livestock losses recorded. All animals are healthy.</div>""", unsafe_allow_html=True)
        mort = st.session_state.mortality_data
        edited = ordered_editor('mortality_data', mort, use_container_width=True, num_rows="dynamic")
        if not edited.equals(mort):
            save('mortality_data', edited)
            st.toast("✅ Mortality data saved!", icon="💾")
    with tab4:
        daily_cost = pets.groupby('Date')['Total Cost (KES)'].sum().reset_index()
        fig = px.area(daily_cost, x='Date', y='Total Cost (KES)', color_discrete_sequence=['#FF9800'], title="Daily Pet Feeding Cost")
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)


# ============================================
# PAGE: TASKS
# ============================================
elif page == "📋 Tasks":
    st.markdown('<div class="section-header">📋 Task Management</div>', unsafe_allow_html=True)
    tasks = st.session_state.tasks_data
    done_count = len(tasks[tasks['Status'] == '✅ Done'])
    total_count = len(tasks)
    st.progress(done_count / total_count if total_count > 0 else 0)
    st.markdown(f"**Progress:** {done_count}/{total_count} tasks completed ({done_count/total_count*100:.0f}%)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 High Priority", len(tasks[tasks['Priority'] == 'High']))
    with col2:
        st.metric("🟡 Medium Priority", len(tasks[tasks['Priority'] == 'Medium']))
    with col3:
        st.metric("🟢 Low Priority", len(tasks[tasks['Priority'] == 'Low']))
    st.markdown("---")
    for cat in tasks['Category'].unique():
        cat_tasks = tasks[tasks['Category'] == cat]
        cat_emoji = {'Poultry': '🐔', 'Orchard': '🍊', 'Shop': '🛒', 'Health': '💊', 'Maintenance': '🔧', 'Pets': '🐾'}.get(cat, '📋')
        st.markdown(f"##### {cat_emoji} {cat} Tasks")
        for _, task in cat_tasks.iterrows():
            priority_color = {'High': '#f44336', 'Medium': '#FF9800', 'Low': '#4CAF50'}.get(task['Priority'], '#888')
            st.markdown(f"""<div class="dashboard-card" style="padding: 15px; border-left: 4px solid {priority_color};">{task['Status']} <strong>{task['Task']}</strong><br><small style="color: #888;">👤 {task['Assigned To']} | 🔴 Priority: {task['Priority']}</small></div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("##### ✏️ Edit Tasks")
    edited = ordered_editor('tasks_data', tasks, use_container_width=True, num_rows="dynamic")
    if not edited.equals(tasks):
        save('tasks_data', edited)
        st.toast("✅ Tasks saved!", icon="💾")


# ============================================
# PAGE: WEATHER
# ============================================
elif page == "🌤️ Weather":
    st.markdown('<div class="section-header">🌤️ Weather Monitoring</div>', unsafe_allow_html=True)
    weather = st.session_state.weather_data
    latest = weather.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card glow-orange" data-emoji="🌡️"><div style="font-size:2.5em;">🌡️</div><div class="big-number-orange">{latest['Temperature (C)']}°C</div><div class="sub-label">Temperature</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card glow-blue" data-emoji="💧"><div style="font-size:2.5em;">💧</div><div class="big-number-blue">{latest['Humidity (%)']}%</div><div class="sub-label">Humidity</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card glow-green" data-emoji="🌧️"><div style="font-size:2.5em;">🌧️</div><div class="big-number">{latest['Rainfall (mm)']}mm</div><div class="sub-label">Rainfall</div></div>""", unsafe_allow_html=True)
    with c4:
        weather_text = latest['Weather'].split(' ')[-1] if ' ' in str(latest['Weather']) else str(latest['Weather'])
        st.markdown(f"""<div class="metric-card glow-gold" data-emoji="🌤️"><div style="font-size:2.5em;">🌤️</div><div class="big-number-gold" style="font-size: 1.5em;">{weather_text}</div><div class="sub-label">Conditions</div></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weather['Date'], y=weather['Temperature (C)'], fill='tozeroy', name='Temperature', line=dict(color='#FF6F00', width=3)))
        fig.update_layout(title="Temperature Trend (7 days)", height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=weather['Date'], y=weather['Rainfall (mm)'], marker_color='#2196F3', name='Rainfall'))
        fig.update_layout(title="Rainfall (7 days)", height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    edited = ordered_editor('weather_data', weather, use_container_width=True, num_rows="dynamic")
    if not edited.equals(weather):
        save('weather_data', edited)
        st.toast("✅ Weather data saved!", icon="💾")


# ============================================
# PAGE: FINANCE
# ============================================
elif page == "💰 Finance":
    st.markdown('<div class="section-header">💰 Farm Financial Overview</div>', unsafe_allow_html=True)
    fin = st.session_state.finance_data
    total_income = fin[fin['Type'] == 'Income']['Amount (KES)'].sum()
    total_expense = fin[fin['Type'] == 'Expense']['Amount (KES)'].sum()
    net = total_income - total_expense
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card glow-green" data-emoji="💰"><div style="font-size:2em;">💰</div><div class="big-number">{format_kes(total_income)}</div><div class="sub-label">Total Income</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card glow-red" data-emoji="💸"><div style="font-size:2em;">💸</div><div class="big-number-red">{format_kes(total_expense)}</div><div class="sub-label">Total Expenses</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card glow-gold" data-emoji="{'📈' if net > 0 else '📉'}"><div style="font-size:2em;">{'📈' if net > 0 else '📉'}</div><div class="big-number-gold">{format_kes(net)}</div><div class="sub-label">Net Profit</div></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        type_summary = fin.groupby('Type')['Amount (KES)'].sum().reset_index()
        fig = px.pie(type_summary, values='Amount (KES)', names='Type', color_discrete_map={'Income': '#4CAF50', 'Expense': '#f44336'}, hole=0.5, title="Income vs Expenses")
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cat_summary = fin.groupby(['Category', 'Type'])['Amount (KES)'].sum().reset_index()
        fig = px.bar(cat_summary, x='Category', y='Amount (KES)', color='Type', barmode='group', color_discrete_map={'Income': '#4CAF50', 'Expense': '#f44336'}, title="By Category")
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    payment_methods = fin['Payment Method'].unique().tolist()
    st.plotly_chart(createMiniDonut([fin[fin['Payment Method'] == m]['Amount (KES)'].sum() for m in payment_methods], payment_methods, ['#4CAF50', '#FF9800', '#2196F3'], "Payment Methods"), use_container_width=True)
    st.markdown("##### ✏️ Edit Financial Records")
    edited = ordered_editor('finance_data', fin, use_container_width=True, num_rows="dynamic")
    if not edited.equals(fin):
        save('finance_data', edited)
        st.toast("✅ Finance data saved!", icon="💾")


# ============================================
# PAGE: FEED INVENTORY
# ============================================
elif page == "📦 Feed Inventory":
    st.markdown('<div class="section-header">📦 Feed & Supply Inventory</div>', unsafe_allow_html=True)
    feed = st.session_state.feed_data
    total_value = (feed['Quantity (kg)'] * feed['Cost per kg (KES)']).sum()
    low_stock = feed[feed['Quantity (kg)'] <= feed['Reorder Level (kg)']]
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card glow-green" data-emoji="📦"><div style="font-size:2em;">📦</div><div class="big-number">{len(feed)}</div><div class="sub-label">Feed Types</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card glow-gold" data-emoji="💰"><div style="font-size:2em;">💰</div><div class="big-number-gold">{format_kes(total_value)}</div><div class="sub-label">Total Value</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card glow-red" data-emoji="⚠️"><div style="font-size:2em;">⚠️</div><div class="big-number-red">{len(low_stock)}</div><div class="sub-label">Low Stock</div></div>""", unsafe_allow_html=True)
    if len(low_stock) > 0:
        st.markdown("""<div class="warning-box">⚠️ <strong>Low Stock Alert!</strong> The following items need to be reordered.</div>""", unsafe_allow_html=True)
        for _, item in low_stock.iterrows():
            st.markdown(f"**{item['Feed Type']}**: {item['Quantity (kg)']}kg remaining (reorder at {item['Reorder Level (kg)']}kg)")
    col1, col2 = st.columns(2)
    with col1:
        reorder_warning = feed['Quantity (kg)'].values <= feed['Reorder Level (kg)'].values
        fig = go.Figure()
        fig.add_trace(go.Bar(x=feed['Feed Type'].tolist(), y=feed['Quantity (kg)'].tolist(), marker_color=['#f44336' if w else '#4CAF50' for w in reorder_warning], name='Stock'))
        fig.add_trace(go.Scatter(x=feed['Feed Type'].tolist(), y=feed['Reorder Level (kg)'].tolist(), mode='markers+lines', marker=dict(color='red', size=12, symbol='x'), name='Reorder Level'))
        fig.update_layout(title="Stock vs Reorder Level", height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.plotly_chart(createMiniDonut(feed['Quantity (kg)'].tolist(), feed['Feed Type'].tolist(), px.colors.qualitative.Set2[:len(feed)], "Inventory Distribution"), use_container_width=True)
    edited = ordered_editor('feed_data', feed, use_container_width=True, num_rows="dynamic")
    if not edited.equals(feed):
        save('feed_data', edited)
        st.toast("✅ Feed inventory saved!", icon="💾")


# ============================================
# PAGE: REPORTS
# ============================================
elif page == "📊 Reports":
    st.markdown('<div class="section-header">📊 Comprehensive Farm Reports</div>', unsafe_allow_html=True)
    st.markdown("##### 📥 Export Data (Formatted Excel)")
    col1, col2, col3 = st.columns(3)
    export_keys = [
        'inventory_data', 'orchard_data', 'orange_harvest_data',
        'cereal_data', 'cereal_inv_data', 'cereal_daily_data',
        'egg_data', 'egg_sales_data',
        'employee_data', 'payments_data',
        'pet_feed_data', 'cat_menu_data',
        'finance_data', 'feed_data',
        'tasks_data', 'weather_data', 'chick_data',
    ]
    for idx, key in enumerate(export_keys):
        df = st.session_state[key]
        display_name = db.SHEET_NAMES.get(key, key)
        col = [col1, col2, col3][idx % 3]
        with col:
            excel_bytes, filename = db.export_excel(key, df)
            st.download_button(
                label=f"📥 {display_name} ({len(df)} rows)",
                data=excel_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
    st.markdown("---")
    st.markdown("##### 📊 Complete Financial Summary")
    fin = st.session_state.finance_data
    income = fin[fin['Type'] == 'Income']['Amount (KES)'].sum()
    expense = fin[fin['Type'] == 'Expense']['Amount (KES)'].sum()
    profit = income - expense
    st.markdown(f"""
    <div class="dashboard-card">
        <h2 style="margin: 0 0 20px 0;">🌾 Liz Farm Enterprise - Financial Report</h2>
        <p style="color: #888;">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        <p style="color: #888;">💾 Data source: SQLite database (liz_farm.db)</p>
        <hr>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 10px; font-weight: bold;">💰 Total Income</td><td style="padding: 10px; text-align: right; color: #4CAF50; font-weight: bold; font-size: 1.2em;">{format_kes(income)}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">💸 Total Expenses</td><td style="padding: 10px; text-align: right; color: #f44336; font-weight: bold; font-size: 1.2em;">{format_kes(expense)}</td></tr>
            <tr style="background: rgba(0,0,0,0.03);"><td style="padding: 10px; font-weight: bold; font-size: 1.1em;">📈 Net Profit</td><td style="padding: 10px; text-align: right; color: {'#4CAF50' if profit > 0 else '#f44336'}; font-weight: bold; font-size: 1.3em;">{format_kes(profit)}</td></tr>
        </table>
        <hr>
        <h3>🐔 Livestock: <strong>{st.session_state.inventory_data['Total'].sum()}</strong> animals</h3>
        <h3>🌳 Orange Trees: <strong>{st.session_state.farm_overview['orange_trees']}</strong> ({st.session_state.farm_overview['fruiting_trees']} fruiting)</h3>
        <h3>🥚 Eggs (30 days): <strong>{st.session_state.egg_data['Total Eggs'].sum():,}</strong></h3>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# PAGE: BACKUP & RESTORE
# ============================================
elif page == "💾 Backup & Restore":
    import io, shutil
    st.markdown('<div class="section-header">💾 Backup & Restore Database</div>', unsafe_allow_html=True)
    info = db.backup_info()
    st.markdown("##### 📊 Current Database Status")
    if info['exists']:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="metric-card glow-green" data-emoji="💾"><div style="font-size:2em;">💾</div><div class="big-number" style="font-size:1.8em;">{info['size_mb']} MB</div><div class="sub-label">Database Size</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="metric-card glow-blue" data-emoji="📋"><div style="font-size:2em;">📋</div><div class="big-number-blue" style="font-size:1.8em;">{info['tables']}</div><div class="sub-label">Tables</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="metric-card glow-orange" data-emoji="📊"><div style="font-size:2em;">📊</div><div class="big-number-orange" style="font-size:1.8em;">{info['total_rows']:,}</div><div class="sub-label">Total Rows</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="metric-card glow-gold" data-emoji="🕐"><div style="font-size:2em;">🕐</div><div class="big-number-gold" style="font-size:1.2em;">{info['modified']}</div><div class="sub-label">Last Modified</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="info-box">📍 <strong>Path:</strong> <code>{info['path']}</code></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="warning-box">⚠️ <strong>No database found!</strong> Run the app once to create it.</div>""", unsafe_allow_html=True)
    st.markdown("---")
    if info['exists']:
        st.markdown("##### 📋 Table Breakdown")
        stats = db.get_table_stats()
        cols = st.columns(3)
        for idx, s in enumerate(stats):
            with cols[idx % 3]:
                st.markdown(f"""<div class="dashboard-card" style="padding: 12px; margin: 5px 0;"><strong>📋 {s['table']}</strong><span style="float: right; color: #2E7D32; font-weight: bold;">{s['rows']} rows</span></div>""", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="section-header" style="font-size: 1.1em; padding: 14px 20px; margin-top: 0;">📥 Export Backup</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="info-box">Download a complete copy of your farm database.<ul><li>📁 Keep periodic backups</li><li>🔄 Transfer data to another computer</li><li>🛡️ Safety before major changes</li></ul></div>""", unsafe_allow_html=True)
        if info['exists']:
            db_bytes = db.backup_database()
            if db_bytes:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"liz_farm_backup_{timestamp}.db"
                st.download_button(label=f"📥 Download Backup ({info['size_mb']} MB)", data=db_bytes, file_name=filename, mime="application/octet-stream", type="primary", use_container_width=True)
                st.success(f"✅ Ready to download: `{filename}`")
    with col2:
        st.markdown("""<div class="section-header" style="font-size: 1.1em; padding: 14px 20px; margin-top: 0;">📤 Restore from Backup</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="warning-box">⚠️ <strong>Warning:</strong> Restoring will <strong>replace</strong> all current data!<ul><li>📦 A backup of the current DB is saved automatically</li><li>🔍 The uploaded file is validated before restoring</li><li>🔄 The app will reload with the restored data</li></ul></div>""", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload a .db backup file", type=['db'], help="Select a previously exported liz_farm_backup_*.db file")
        if uploaded is not None:
            file_bytes = uploaded.read()
            st.info(f"📄 Uploaded: `{uploaded.name}` ({len(file_bytes):,} bytes)")
            if st.button("🔄 Restore This Backup", type="primary", use_container_width=True):
                with st.spinner("Restoring database..."):
                    success, message = db.restore_database(file_bytes)
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                    db.load_all()
                    st.session_state._db_loaded = True
                    st.info("🔄 Data reloaded. Navigate to any page to see the restored data.")
                else:
                    st.error(f"❌ {message}")
    st.markdown("---")
    st.markdown("##### ⚡ Quick Actions")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("🔄 Reload All Data from DB", use_container_width=True):
            db.load_all()
            st.session_state._db_loaded = True
            st.toast("✅ All data reloaded from database!", icon="🔄")
            st.rerun()
    with q2:
        if st.button("📊 Refresh Stats", use_container_width=True):
            st.rerun()
    with q3:
        if st.button("🗑️ Reset Database (Fresh Start)", use_container_width=True):
            st.warning("⚠️ This will delete all data and create a fresh database with sample data.")
            if st.button("✅ Yes, Reset Everything", type="primary"):
                import os as _os
                if _os.path.exists(db.DB_PATH):
                    _os.remove(db.DB_PATH)
                db.init_db()
                db.load_all()
                st.session_state._db_loaded = True
                st.success("✅ Database reset with fresh sample data!")
                st.balloons()
                st.rerun()


# ============================================
# GLOBAL FOOTER
# ============================================
if page not in ("🏠 Dashboard", "💾 Backup & Restore"):
    st.markdown("""
    <div class="farm-footer" style="margin-top: 40px;">
        <h3 style="margin:0;">🌾 Liz Farm Enterprise 🌾</h3>
        <p style="opacity: 0.9;">Nurturing Nature, Growing Prosperity</p>
        <p style="opacity: 0.7; font-size: 0.85em;">© 2026 Liz Farm Enterprise | All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)
