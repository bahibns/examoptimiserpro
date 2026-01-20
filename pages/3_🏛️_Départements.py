import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.analytics import Analytics
from src.styles import apply_custom_style

st.set_page_config(
    page_title="Départements - Gestion",
    page_icon="🏛️",
    layout="wide"
)

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_analytics(_db):
    return Analytics(_db)

def main():
    apply_custom_style()
    st.title("🏛️ Gestion Départementale")
    st.markdown("Vue et validation par Chef de Département")
    
    db = get_database()
    analytics = get_analytics(db)
    
    departements = db.get_departements()
    
    if not departements:
        st.warning("Aucun département trouvé")
        return
    
    dept_options = {dept['nom']: dept['id'] for dept in departements}
    
    selected_dept_name = st.selectbox(
        "Sélectionnez votre département",
        options=list(dept_options.keys())
    )
    
    dept_id = dept_options[selected_dept_name]
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Vue d'ensemble", "📚 Formations", "👨‍🏫 Professeurs", "📅 Examens"])
    
    with tab1:
        st.header(f"📊 Vue d'ensemble - {selected_dept_name}")
        
        try:
            dept_stats = analytics.get_department_stats()
            dept_data = dept_stats[dept_stats['departement'] == selected_dept_name].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👨‍🎓 Étudiants", f"{dept_data['nb_etudiants']:,}")
            
            with col2:
                st.metric("👨‍🏫 Professeurs", f"{dept_data['nb_professeurs']:,}")
            
            with col3:
                st.metric("📚 Formations", dept_data['nb_formations'])
            
            with col4:
                st.metric("📖 Modules", dept_data['nb_modules'])
            
            st.markdown("---")
            
            col5, col6 = st.columns(2)
            
            with col5:
                st.metric("📝 Examens planifiés", dept_data['nb_examens_planifies'])
            
            with col6:
                ratio = dept_data['nb_etudiants'] / max(dept_data['nb_professeurs'], 1)
                st.metric("📊 Ratio Étudiants/Prof", f"{ratio:.1f}")
            
            st.markdown("---")
            
            st.subheader("📈 Statistiques Détaillées")
            
            formations = db.get_formations(dept_id)
            
            if formations:
                formations_df = pd.DataFrame(formations)
                
                formation_stats = []
                for formation in formations:
                    etudiants = db.get_etudiants(formation['id'])
                    modules = db.get_modules(formation['id'])
                    
                    formation_stats.append({
                        'Formation': formation['nom'],
                        'Niveau': formation['niveau'],
                        'Code': formation['code'],
                        'Étudiants': len(etudiants),
                        'Modules': len(modules)
                    })
                
                stats_df = pd.DataFrame(formation_stats)
                
                fig = px.bar(
                    stats_df,
                    x='Formation',
                    y='Étudiants',
                    color='Niveau',
                    title='Répartition des Étudiants par Formation',
                    text='Étudiants'
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Erreur: {e}")
    
    with tab2:
        st.header("📚 Formations du Département")
        
        formations = db.get_formations(dept_id)
        
        if formations:
            for formation in formations:
                with st.expander(f"📖 {formation['nom']} ({formation['code']})"):
                    col_f1, col_f2, col_f3 = st.columns(3)
                    
                    with col_f1:
                        st.write(f"**Niveau:** {formation['niveau']}")
                    
                    with col_f2:
                        etudiants = db.get_etudiants(formation['id'])
                        st.write(f"**Étudiants:** {len(etudiants)}")
                    
                    with col_f3:
                        modules = db.get_modules(formation['id'])
                        st.write(f"**Modules:** {len(modules)}")
                    
                    if modules:
                        st.markdown("##### Modules:")
                        modules_df = pd.DataFrame(modules)
                        st.dataframe(
                            modules_df[['nom', 'code', 'credits', 'semestre', 'duree_examen']],
                            use_container_width=True,
                            hide_index=True
                        )
        else:
            st.info("Aucune formation trouvée pour ce département")
    
    with tab3:
        st.header("👨‍🏫 Professeurs du Département")
        
        professeurs = db.get_professeurs(dept_id)
        
        if professeurs:
            st.metric("Total Professeurs", len(professeurs))
            
            profs_df = pd.DataFrame(professeurs)
            
            grade_counts = profs_df['grade'].value_counts()
            
            col_grade1, col_grade2 = st.columns(2)
            
            with col_grade1:
                fig_pie = px.pie(
                    values=grade_counts.values,
                    names=grade_counts.index,
                    title='Répartition par Grade'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_grade2:
                charge_profs = analytics.get_professor_workload()
                dept_charge = charge_profs[charge_profs['departement'] == selected_dept_name]
                
                if not dept_charge.empty:
                    fig_bar = px.bar(
                        dept_charge.head(10),
                        x='nom',
                        y='nb_surveillances',
                        title='Top 10 - Charge de Surveillance',
                        labels={'nb_surveillances': 'Surveillances', 'nom': 'Professeur'}
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            st.markdown("---")
            
            search = st.text_input("🔍 Rechercher un professeur")
            
            if search:
                profs_df = profs_df[
                    profs_df['nom'].str.contains(search, case=False, na=False) |
                    profs_df['prenom'].str.contains(search, case=False, na=False)
                ]
            
            st.dataframe(
                profs_df[['nom', 'prenom', 'email', 'grade', 'specialite']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Aucun professeur trouvé pour ce département")
    
    with tab4:
        st.header("📅 Examens du Département")
        
        periodes = db.get_periodes_examen(actif=True)
        
        if periodes:
            periode_options = {
                f"{p['nom']}": p['id'] 
                for p in periodes
            }
            
            selected_periode = st.selectbox(
                "Période d'examen",
                options=list(periode_options.keys())
            )
            
            periode_id = periode_options[selected_periode]
            
            formations = db.get_formations(dept_id)
            formation_ids = [f['id'] for f in formations]
            
            all_examens = db.get_examens(periode_id)
            
            if all_examens:
                examens_df = pd.DataFrame(all_examens)
                
                modules = db.get_modules()
                modules_df = pd.DataFrame(modules)
                
                dept_modules = modules_df[modules_df['formation_id'].isin(formation_ids)]
                dept_module_ids = dept_modules['id'].tolist()
                
                dept_examens = examens_df[examens_df['module_id'].isin(dept_module_ids)]
                
                if not dept_examens.empty:
                    st.metric("Examens du département", len(dept_examens))
                    
                    col_exam1, col_exam2 = st.columns(2)
                    
                    with col_exam1:
                        total_students = dept_examens['nb_inscrits'].sum()
                        st.metric("Total étudiants", f"{total_students:,}")
                    
                    with col_exam2:
                        unique_dates = dept_examens['date_heure'].dt.date.nunique()
                        st.metric("Jours d'examens", unique_dates)
                    
                    st.markdown("---")
                    
                    dept_examens.loc[:, 'date'] = pd.to_datetime(dept_examens['date_heure']).dt.date
                    
                    exams_by_date = dept_examens.groupby('date').size().reset_index(name='count')
                    
                    fig_timeline = px.bar(
                        exams_by_date,
                        x='date',
                        y='count',
                        title='Nombre d\'Examens par Jour',
                        labels={'count': 'Nombre d\'examens', 'date': 'Date'}
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)
                    
                    st.markdown("---")
                    
                    st.subheader("📋 Liste des Examens")
                    
                    st.dataframe(
                        dept_examens[['date_heure', 'module_nom', 'salle_nom', 'professeur', 'nb_inscrits', 'duree_minutes']],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    if st.button("✅ Valider le planning du département"):
                        st.success("✅ Planning validé pour le département " + selected_dept_name)
                        st.balloons()
                else:
                    st.info("Aucun examen planifié pour ce département")
            else:
                st.info("Aucun examen planifié pour cette période")
        else:
            st.warning("Aucune période d'examen active")

if __name__ == "__main__":
    main()
