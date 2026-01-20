import streamlit as st

def apply_custom_style():
        # --- PREMIUM DESIGN INJECTION ---
    st.markdown("""
        <style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* Global App Style */
.stApp {
    background-color: #f8f9fa;
    font-family: 'Inter', sans-serif;
}

/* Headers */
h1, h2, h3 {
    color: #1e3a8a !important; /* Deep Blue */
    font-weight: 700;
}

/* Hero Section */
.hero-container {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.hero-title {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}
.hero-subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
}

/* Metric Cards */
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #e5e7eb;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.metric-label {
    font-size: 0.875rem;
    color: #6b7280 !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #111827 !important;
    margin: 0.5rem 0;
}
.metric-delta {
    font-size: 0.875rem;
    color: #10b981 !important;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

/* Info Box */
.info-box {
    background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid #3b82f6;
    color: #1e3a8a;
    margin: 1rem 0;
}
.info-box h4 {
    color: #1e40af !important;
    margin-bottom: 0.5rem;
}
.info-box ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}
.info-box li {
    color: #1e3a8a !important;
    margin: 0.25rem 0;
}

/* Alerts */
.custom-alert {
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.alert-success { 
    background-color: #ecfdf5; 
    color: #065f46 !important; 
    border: 1px solid #a7f3d0; 
}
.alert-success h4 {
    color: #065f46 !important;
}
.alert-warning { 
    background-color: #fffbeb; 
    color: #92400e !important; 
    border: 1px solid #fde68a; 
}
.alert-warning h4 {
    color: #92400e !important;
}
.alert-error { 
    background-color: #fef2f2; 
    color: #991b1b !important; 
    border: 1px solid #fecaca; 
}
.alert-error h4 {
    color: #991b1b !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: white;
    padding: 0.5rem;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #f3f4f6;
    border-radius: 8px;
    color: #374151 !important;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
    color: white !important;
    border: none !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2) !important;
}
/* Navigation Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 {
    color: #111827 !important;
    font-size: 1.1rem !important;
}

section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] li, 
section[data-testid="stSidebar"] span {
    color: #374151 !important;
    font-size: 0.95rem !important;
}

/* DataFrames */
.dataframe {
    border-radius: 8px;
    overflow: hidden;
}

/* Expanders - CORRECTION COMPLÈTE */
.streamlit-expanderHeader {
    background-color: white !important;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    font-weight: 600;
    color: #1e3a8a !important;
}

.streamlit-expanderContent {
    background-color: #ffffff !important;
}

/* Tous les textes dans l'app sur fond blanc */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em {
    color: #111827 !important;
}

/* Labels des inputs */
label, .stSelectbox label, .stTextInput label, .stRadio label {
    color: #374151 !important;
    font-weight: 600;
}

/* Texte des selectbox */
.stSelectbox div[data-baseweb="select"] {
    color: #111827 !important;
}

/* Texte des radio buttons */
.stRadio label p {
    color: #374151 !important;
}

/* Markdown général */
.stMarkdown {
    color: #111827 !important;
}

/* Caption */
.caption {
    color: #6b7280 !important;
}

/* Section Headers */
.section-header {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    padding: 1rem 1.5rem;
    border-radius: 8px;
    border-left: 4px solid #3b82f6;
    margin: 1.5rem 0 1rem 0;
}
.section-header h3 {
    margin: 0;
    color: #1e3a8a !important;
}

/* Correction spécifique pour les expanders */
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] strong {
    color: #111827 !important;
}

div[data-testid="stExpander"] h3 {
    color: #1e3a8a !important;
    background-color: #f0f9ff;
    padding: 0.5rem;
    border-radius: 6px;
}

/* Metrics Streamlit natifs */
[data-testid="stMetricValue"] {
    color: #111827 !important;
}

[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
}

[data-testid="stMetricDelta"] {
    color: #10b981 !important;
}
/* Correction Planning par Département - Expanders */
div[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
}

div[data-testid="stExpander"] summary {
    background-color: #f8f9fa !important;
    color: #1e3a8a !important;
    font-weight: 600;
}

div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] strong,
div[data-testid="stExpander"] div {
    color: #111827 !important;
    background-color: transparent !important;
}

div[data-testid="stExpander"] h3 {
    color: #1e3a8a !important;
    background-color: #f0f9ff !important;
    padding: 0.5rem;
    border-radius: 6px;
}

/* Markdown dans expanders */
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
    color: #111827 !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    color: white !important;
    border: none !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2) !important;
}
        /* Sections principales - Cards avec background */
        .main > div > div > div[data-testid="stVerticalBlock"] > div:has(h2) {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            margin: 2rem 0;
            border: 1px solid #e5e7eb;
        }
        
        /* Headers de sections - Style Hero mini */
        .stat-section-header {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }
        
        .stat-section-header h2 {
            color: white !important;
            margin: 0;
            font-size: 1.75rem;
        }
        
        /* Groupes de metrics - Cards groupées */
        .metric-group {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 2rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            border: 2px solid #e2e8f0;
        }
        
        /* Metrics individuels - Cards blanches sur fond gris */
        [data-testid="metric-container"] {
            background: white !important;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.08);
            border: 2px solid #f1f5f9;
            transition: all 0.3s;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.15);
            border-color: #3b82f6;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            color: #1e3a8a !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.875rem !important;
            color: #64748b !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        
        /* Sous-sections avec background coloré */
        .subsection-card {
            background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
            padding: 2rem;
            border-radius: 12px;
            border-left: 6px solid #3b82f6;
            margin: 2rem 0;
            box-shadow: 0 4px 15px -3px rgba(59, 130, 246, 0.2);
        }
        
        .subsection-card h3 {
            color: #1e40af !important;
            margin-top: 0 !important;
            font-size: 1.5rem !important;
        }
        
        /* DataFrames - Card distincte */
        [data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            border: 2px solid #f1f5f9;
            margin: 2rem 0;
        }
        
        [data-testid="stDataFrame"] thead tr th {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 0.875rem;
            letter-spacing: 0.05em;
            padding: 1.25rem !important;
            border: none !important;
        }
        
        [data-testid="stDataFrame"] tbody tr {
            border-bottom: 1px solid #f1f5f9;
        }
        
        [data-testid="stDataFrame"] tbody tr:nth-child(even) {
            background-color: #f8fafc;
        }
        
        [data-testid="stDataFrame"] tbody tr:hover {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
            transform: scale(1.01);
        }
        
        /* Graphiques Plotly - Card forte */
        .js-plotly-plot {
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            background: white;
            padding: 1.5rem;
            border: 2px solid #f1f5f9;
            margin: 1.5rem 0;
        }
        
        /* Séparateurs visuels forts */
        hr {
            border: none;
            height: 4px;
            background: linear-gradient(90deg, transparent, #3b82f6, transparent);
            margin: 3rem 0;
            border-radius: 2px;
        }
        
        /* Progress bar - Plus visible */
        .stProgress > div {
            background-color: #e2e8f0 !important;
            border-radius: 12px;
            height: 28px !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .stProgress > div > div {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
        }
        
        /* Score badge - Plus imposant */
        .score-display {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.15);
            border: 3px solid;
            margin: 2rem 0;
        }
        
        .score-display.green {
            border-color: #10b981;
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        }
        
        .score-display.orange {
            border-color: #f59e0b;
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        }
        
        .score-display.red {
            border-color: #ef4444;
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        }
        
        .score-value {
            font-size: 4rem !important;
            font-weight: 900 !important;
            margin: 1rem 0;
        }
        
        /* Alertes - Cards colorées fortes */
        .stSuccess, .stWarning, .stError, .stInfo {
            border-radius: 12px !important;
            padding: 1.5rem !important;
            border-left: 6px solid !important;
            box-shadow: 0 6px 20px -5px rgba(0, 0, 0, 0.15) !important;
            font-weight: 600 !important;
            margin: 1.5rem 0 !important;
        }
        
        /* Filters section - Card distincte */
        .filter-section {
            background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px solid #fde68a;
            margin: 1.5rem 0;
        }
        
        /* Colonnes avec espacement */
        [data-testid="column"] {
            padding: 0.5rem;
        }
        
        /* Tabs - Style plus marqué */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 1rem;
            border-radius: 12px;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: white;
            border-radius: 10px;
            color: #64748b;
            font-weight: 700;
            padding: 1rem 2rem;
            border: 2px solid #e2e8f0;
            transition: all 0.3s;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            border-color: #3b82f6;
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            color: white !important;
            border-color: #1e3a8a !important;
            box-shadow: 0 8px 20px -5px rgba(30, 58, 138, 0.4);
        }
 /* Hero Section pour titre département */
        .dept-hero {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        /* Metrics Cards - Même style que page principale */
        [data-testid="metric-container"] {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #111827;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.875rem;
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Expanders - Même style que Planning par Département */
        div[data-testid="stExpander"] {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        div[data-testid="stExpander"] summary {
            background-color: #f8f9fa;
            color: #1e3a8a;
            font-weight: 600;
            padding: 1rem;
        }
        
        div[data-testid="stExpander"] summary:hover {
            background-color: #e5e7eb;
        }
        
        div[data-testid="stExpander"] p,
        div[data-testid="stExpander"] span,
        div[data-testid="stExpander"] strong,
        div[data-testid="stExpander"] div {
            color: #111827 !important;
        }
        
        div[data-testid="stExpander"] h5 {
            color: #1e3a8a !important;
            background-color: #f0f9ff;
            padding: 0.5rem;
            border-radius: 6px;
        }
        
        /* DataFrames - Style uniforme */
        [data-testid="stDataFrame"] {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stDataFrame"] thead tr th {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 1rem !important;
        }
        
        [data-testid="stDataFrame"] tbody tr:nth-child(even) {
            background-color: #f9fafb;
        }
        
        [data-testid="stDataFrame"] tbody tr:hover {
            background-color: #f0f9ff !important;
        }
        
        /* Graphiques Plotly */
        .js-plotly-plot {
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            background: white;
            padding: 1rem;
        }
        
        /* Search input */
        .stTextInput > div > div {
            border-radius: 8px;
            border: 2px solid #e5e7eb;
        }
        
        .stTextInput > div > div:focus-within {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Info/Warning/Success boxes */
        .stInfo {
            background-color: #dbeafe;
            color: #1e40af;
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            padding: 1rem;
        }
        
        .stWarning {
            background-color: #fef3c7;
            color: #92400e;
            border-left: 4px solid #f59e0b;
            border-radius: 8px;
            padding: 1rem;
        }
        
        .stSuccess {
            background-color: #d1fae5;
            color: #065f46;
            border-left: 4px solid #10b981;
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Séparateurs */
        hr {
            border: none;
            border-top: 2px solid #e5e7eb;
            margin: 2rem 0;
        }
        .js-plotly-plot {
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    background: white;
    padding: 1rem;
    min-height: 400px !important; /* Force une hauteur minimale */
}

.js-plotly-plot .plotly {
    min-height: 400px !important;
}

.js-plotly-plot .main-svg {
    min-height: 350px !important;
}

/* Container des graphiques */
[data-testid="stPlotlyChart"] {
    min-height: 400px !important;
}

[data-testid="stPlotlyChart"] > div {
    min-height: 400px !important;
}

/* Correction spécifique pour les graphiques dans les colonnes */
[data-testid="column"] .js-plotly-plot {
    min-height: 350px !important;
}

/* Pour les graphiques en pleine largeur */
.stPlotlyChart {
    min-height: 450px !important;
}
        /* Radio buttons - Style horizontal premium */
        .stRadio > div {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
        }
        
        .stRadio [role="radiogroup"] {
            gap: 1rem;
        }
        
        .stRadio label {
            background: white;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: 2px solid #e5e7eb;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .stRadio label:hover {
            border-color: #3b82f6;
            background-color: #f0f9ff;
        }
        
        .stRadio input:checked + div {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            border-color: #1e3a8a;
        }
        
        /* Search inputs - Style groupé */
        .stTextInput > div > div {
            border-radius: 8px;
            border: 2px solid #e5e7eb;
            transition: all 0.3s;
        }
        
        .stTextInput > div > div:focus-within {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Info boxes pour profil utilisateur */
        .stInfo {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            padding: 1rem;
            color: #1e40af;
            font-weight: 600;
        }
        
        /* Containers pour examens/surveillances */
        .exam-item-container {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: all 0.2s;
        }
        
        .exam-item-container:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Dates dans planning */
        .stMarkdown h3 {
            color: #1e3a8a !important;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            font-size: 1.25rem !important;
        }
        
        /* Metrics dans colonnes - Style cohérent */
        [data-testid="metric-container"] {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #111827;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.875rem;
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Graphiques Plotly - Hauteur fixe */
        .js-plotly-plot {
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            background: white;
            padding: 1rem;
            min-height: 400px !important;
        }
        
        [data-testid="stPlotlyChart"] {
            min-height: 400px !important;
        }
        
        /* Success/Warning boxes */
        .stSuccess {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border-left: 4px solid #10b981;
            border-radius: 8px;
            padding: 1rem;
            color: #065f46;
            font-weight: 600;
        }
        
        .stWarning {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 4px solid #f59e0b;
            border-radius: 8px;
            padding: 1rem;
            color: #92400e;
            font-weight: 600;
        }
        
        /* Captions - Plus lisible */
        .caption {
            color: #6b7280 !important;
            font-size: 0.875rem;
        }
        
        /* Containers pour détails examens */
        [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }
        
        /* Download button - Style vert */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
            color: white !important;
            border: none !important;
        }
        
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Séparateurs */
        hr {
            border: none;
            border-top: 2px solid #e5e7eb;
            margin: 2rem 0;
        }
        
        /* Selectbox */
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 2px solid #e5e7eb;
            transition: all 0.3s;
        }
        
        .stSelectbox > div > div:focus-within {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
</style>
    """, unsafe_allow_html=True)
