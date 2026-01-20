import streamlit as st
import plotly.express as px
import sys
import os

# Add src path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import Database
from src.analytics import Analytics
from src.scheduler import ExamScheduler

# Page Config
st.set_page_config(
    page_title="ExamOptimizer Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Connect Resources
@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_analytics(_db):
    return Analytics(_db)

@st.cache_resource
def get_scheduler(_db):
    return ExamScheduler(_db)

def main():
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
            color: #1e3a8a; /* Deep Blue */
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
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #111827;
            margin: 0.5rem 0;
        }
        .metric-delta {
            font-size: 0.875rem;
            color: #10b981; /* Green for success/info */
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        /* Navigation Sidebar */
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
        
        /* Alerts */
        .custom-alert {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .alert-success { background-color: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
        .alert-warning { background-color: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
        
        </style>
    """, unsafe_allow_html=True)
    
    # --- HERO SECTION ---
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">🎓 ExamOptimizer Pro</div>
            <div class="hero-subtitle">Plateforme Intelligente de Gestion des Examens Universitaires</div>
        </div>
    """, unsafe_allow_html=True)

    db = get_database()
    analytics = get_analytics(db)
    
    # --- SIDEBAR (Empty for clean look) ---
    with st.sidebar:
        pass
    
    
    st.markdown("### 📊 Tableau de Bord")
    
    try:
        kpis = analytics.get_dashboard_kpis()
        
        # --- METRICS ROW 1 ---
        col1, col2, col3, col4 = st.columns(4)
        
        def display_card(col, label, value, delta, icon):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{icon} {label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-delta">
                        <span>{delta}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        display_card(col1, "Étudiants", f"{kpis.get('total_etudiants', 0):,}", "Inscrits actifs", "👨‍🎓")
        display_card(col2, "Professeurs", f"{kpis.get('total_professeurs', 0):,}", "Enseignants", "👨‍🏫")
        display_card(col3, "Modules", f"{kpis.get('total_modules', 0):,}", "Matières", "📚")
        display_card(col4, "Examens", f"{kpis.get('examens_planifies', 0):,}", "Planifiés", "📝")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- METRICS ROW 2 (Infrastructure) ---
        col5, col6, col7, col8 = st.columns(4)
        
        display_card(col5, "Départements", kpis.get('total_departements', 0), "Unités pédagogiques", "🏛️")
        display_card(col6, "Formations", kpis.get('total_formations', 0), "Parcours", "🎯")
        display_card(col7, "Salles", kpis.get('total_salles', 0), "Capacité " + str(kpis.get('capacite_totale', 0)), "🏫")
        display_card(col8, "Inscriptions", f"{kpis.get('total_inscriptions', 0):,}", "Total cursus", "📋")

        st.markdown("---")
        
        # --- CHARTS SECTION ---
        col_chart1, col_chart2 = st.columns(2)
        
        dept_stats = analytics.get_department_stats()
        
        if not dept_stats.empty:
            with col_chart1:
                st.markdown("##### 👥 Étudiants par Département")
                fig_students = px.bar(
                    dept_stats, x='departement', y='nb_etudiants',
                    color='nb_etudiants', color_continuous_scale='Blues',
                    template='plotly_white'
                )
                fig_students.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig_students, use_container_width=True)
            
            with col_chart2:
                st.markdown("##### 🎓 Professeurs par Département")
                fig_profs = px.bar(
                    dept_stats, x='departement', y='nb_professeurs',
                    color='nb_professeurs', color_continuous_scale='Greens',
                    template='plotly_white'
                )
                fig_profs.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig_profs, use_container_width=True)

        # --- CONFLICTS SECTION ---
        st.markdown("### 🛡️ Centre de Contrôle")
        
        conflict_summary = analytics.get_conflict_summary()
        total_conflicts = sum(conflict_summary.values())
        
        if total_conflicts == 0:
            st.markdown("""
            <div class="custom-alert alert-success">
                <h3>✅ Tout est en ordre</h3>
                <p>Aucun conflit détecté dans le planning actuel. Le système est optimal.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
             st.markdown(f"""
            <div class="custom-alert alert-warning">
                <h3>⚠️ Attention requise</h3>
                <p>{total_conflicts} conflits détectés. Veuillez vérifier la section Administration.</p>
            </div>
            """, unsafe_allow_html=True)
             
             # Mini cards for conflicts
             c1, c2, c3, c4 = st.columns(4)
             c1.metric("Conflits Étudiants", conflict_summary.get('etudiants', 0))
             c2.metric("Conflits Profs", conflict_summary.get('professeurs', 0))
             c3.metric("Surcharges Salles", conflict_summary.get('capacite', 0))
             c4.metric("Doublons Salles", conflict_summary.get('salles', 0))

    except Exception as e:
        st.error(f"Erreur d'initialisation : {e}")
        st.info("Vérifiez la connexion base de données.")

if __name__ == "__main__":
    main()
