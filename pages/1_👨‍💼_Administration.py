import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import Database
from src.scheduler import ExamScheduler
from src.analytics import Analytics
from src.styles import apply_custom_style
st.set_page_config(
    page_title="Administration - Génération d'EDT",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_scheduler(_db):
    return ExamScheduler(_db)

@st.cache_resource
def get_analytics(_db):
    return Analytics(_db)

def main():
    apply_custom_style()
    
    # --- HERO SECTION ---
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">👨‍💼 Administration des Examens</div>
            <div class="hero-subtitle">Génération automatique et optimisation des emplois du temps d'examens</div>
        </div>
    """, unsafe_allow_html=True)
    
    db = get_database()
    scheduler = get_scheduler(db)
    analytics = get_analytics(db)
    
    tab1, tab2, tab3 = st.tabs(["🚀 Génération d'EDT", "📋 Examens Planifiés", "🏛️ Planning par Département"])
    
    # --- TAB 1: GÉNÉRATION ---
    with tab1:
        st.markdown('<div class="section-header"><h3>🚀 Génération Automatique d\'Emploi du Temps</h3></div>', unsafe_allow_html=True)
        
        periodes = db.get_periodes_examen(actif=True)
        
        if not periodes:
            st.markdown("""
            <div class="custom-alert alert-warning">
                <h4>⚠️ Aucune période d'examen active trouvée</h4>
                <p>Créez une période d'examen dans la base de données pour continuer</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            periode_options = {
                f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] 
                for p in periodes
            }
            
            selected_periode = st.selectbox(
                "Sélectionnez la période d'examen",
                options=list(periode_options.keys())
            )
            
            periode_id = periode_options[selected_periode]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                <div class="info-box">
                    <h4>📋 Contraintes appliquées:</h4>
                    <ul>
                        <li>✓ Maximum 1 examen par jour par étudiant</li>
                        <li>✓ Maximum 3 examens par jour par professeur</li>
                        <li>✓ Respect de la capacité des salles (20 étudiants max)</li>
                        <li>✓ Pas de chevauchement de salles</li>
                        <li>✓ Priorité aux professeurs du département</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                annee_universitaire = st.text_input(
                    "Année universitaire",
                    value="2025-2026"
                )
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            
            with col_btn1:
                if st.button("🚀 Générer l'EDT", type="primary", use_container_width=True):
                    with st.spinner("Génération en cours... Optimisé pour ~10 secondes"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("Initialisation...")
                        progress_bar.progress(10)
                        
                        try:
                            status_text.text("Génération du planning...")
                            progress_bar.progress(30)
                            
                            # Use ExamScheduler for scheduling
                            success, result = scheduler.generate_schedule(periode_id, annee_universitaire)
                            
                            progress_bar.progress(80)
                            status_text.text("Finalisation...")
                            
                            if success:
                                progress_bar.progress(100)
                                status_text.text("Terminé!")
                                
                                st.markdown(f"""
                                <div class="custom-alert alert-success">
                                    <h4>✅ EDT généré avec succès en {result['execution_time']:.2f} secondes!</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col_r1, col_r2, col_r3 = st.columns(3)
                                
                                def display_result_card(col, label, value, icon):
                                    with col:
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <div class="metric-label">{icon} {label}</div>
                                            <div class="metric-value">{value}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                
                                display_result_card(col_r1, "Examens planifiés", result['scheduled'], "✅")
                                display_result_card(col_r2, "Modules non planifiés", result['failed'], "⚠️")
                                display_result_card(col_r3, "Conflits détectés", result['total_conflicts'], "🔍")
                                
                                st.markdown("<br>", unsafe_allow_html=True)
                                
                                if result['failed'] > 0:
                                    st.markdown("""
                                    <div class="custom-alert alert-warning">
                                        <h4>⚠️ Certains modules n'ont pas pu être planifiés</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    failed_df = pd.DataFrame(result['failed_modules'])
                                    st.dataframe(failed_df, use_container_width=True)
                                
                                if result['total_conflicts'] > 0:
                                    st.markdown(f"""
                                    <div class="custom-alert alert-error">
                                        <h4>❌ {result['total_conflicts']} conflit(s) détecté(s)</h4>
                                        <p>Consultez l'onglet 'Détection de Conflits'</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                st.balloons()
                            else:
                                st.markdown(f"""
                                <div class="custom-alert alert-error">
                                    <h4>❌ Erreur lors de la génération</h4>
                                    <p>{result.get('error', 'Erreur inconnue')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        except Exception as e:
                            st.markdown(f"""
                            <div class="custom-alert alert-error">
                                <h4>❌ Erreur: {e}</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            import traceback
                            st.code(traceback.format_exc())
            
            with col_btn2:
                if st.button("🔄 Optimiser l'EDT", use_container_width=True, type="secondary"):
                    with st.spinner("Optimisation en cours..."):
                        try:
                            optimizations = scheduler.optimize_schedule(periode_id)
                            st.markdown(f"""
                            <div class="custom-alert alert-success">
                                <h4>✅ {optimizations} optimisation(s) effectuée(s)</h4>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"""
                            <div class="custom-alert alert-error">
                                <h4>❌ Erreur: {e}</h4>
                            </div>
                            """, unsafe_allow_html=True)
            
            with col_btn3:
                if st.button("🗑️ Supprimer tous les examens", use_container_width=True):
                    if st.checkbox("Confirmer la suppression"):
                        try:
                            db.delete_all_examens(periode_id)
                            st.markdown("""
                            <div class="custom-alert alert-success">
                                <h4>✅ Tous les examens ont été supprimés</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            st.rerun()
                        except Exception as e:
                            st.markdown(f"""
                            <div class="custom-alert alert-error">
                                <h4>❌ Erreur: {e}</h4>
                            </div>
                            """, unsafe_allow_html=True)
    
    # --- TAB 2: EXAMENS PLANIFIÉS ---
    with tab2:
        st.markdown('<div class="section-header"><h3>📋 Examens Planifiés</h3></div>', unsafe_allow_html=True)
        
        periodes = db.get_periodes_examen(actif=True)
        
        if periodes:
            periode_options = {
                f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] 
                for p in periodes
            }
            
            selected_periode_view = st.selectbox(
                "Période d'examen",
                options=list(periode_options.keys()),
                key="view_periode"
            )
            
            periode_id_view = periode_options[selected_periode_view]
            
            examens = db.get_examens(periode_id_view)
            
            if examens:
                df = pd.DataFrame(examens)
                
                # Metric card for total
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📊 Total d'examens planifiés</div>
                    <div class="metric-value">{len(examens)}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_filter1, col_filter2 = st.columns(2)
                
                with col_filter1:
                    search_module = st.text_input("🔍 Rechercher un module")
                
                with col_filter2:
                    search_salle = st.text_input("🔍 Rechercher une salle")
                
                if search_module:
                    df = df[df['module_nom'].str.contains(search_module, case=False, na=False)]
                
                if search_salle:
                    df = df[df['salle_nom'].str.contains(search_salle, case=False, na=False)]
                
                st.dataframe(
                    df[['date_heure', 'module_nom', 'salle_nom', 'professeur', 'nb_inscrits', 'duree_minutes', 'statut']],
                    use_container_width=True,
                    hide_index=True
                )
                
                if st.button("📥 Exporter en CSV"):
                    csv = df.to_csv(index=False, encoding='utf-8')
                    st.download_button(
                        label="Télécharger le CSV",
                        data=csv,
                        file_name=f"examens_{periode_id_view}.csv",
                        mime="text/csv"
                    )
            else:
                st.markdown("""
                <div class="custom-alert alert-warning">
                    <h4>ℹ️ Aucun examen planifié pour cette période</h4>
                </div>
                """, unsafe_allow_html=True)
    
    # --- TAB 3: PLANNING PAR DÉPARTEMENT ---
    with tab3:
        st.markdown('<div class="section-header"><h3>🏛️ Planning par Département</h3></div>', unsafe_allow_html=True)
        
        periodes = db.get_periodes_examen(actif=True)
        
        if periodes:
            periode_options = {
                f"{p['nom']} ({p['date_debut']} - {p['date_fin']})": p['id'] 
                for p in periodes
            }
            
            selected_periode_dept = st.selectbox(
                "Période d'examen",
                options=list(periode_options.keys()),
                key="dept_periode"
            )
            
            periode_id_dept = periode_options[selected_periode_dept]
            
            # Get departments
            departements = db.get_departements()
            
            if departements:
                # Department selector
                dept_names = {d['nom']: d['id'] for d in departements}
                selected_dept = st.selectbox(
                    "Sélectionnez un département",
                    options=["Tous les départements"] + list(dept_names.keys())
                )
                
                # Get all exams with department info
                query = """
                    SELECT 
                        e.id,
                        e.date_heure,
                        e.duree_minutes,
                        e.nb_inscrits,
                        m.nom as module_nom,
                        m.code as module_code,
                        l.nom as salle_nom,
                        l.batiment,
                        p.nom || ' ' || p.prenom as professeur,
                        d.nom as departement,
                        f.nom as formation
                    FROM examens e
                    JOIN modules m ON e.module_id = m.id
                    JOIN lieu_examen l ON e.salle_id = l.id
                    JOIN professeurs p ON e.prof_responsable_id = p.id
                    JOIN formations f ON m.formation_id = f.id
                    JOIN departements d ON f.dept_id = d.id
                    WHERE e.periode_id = %s
                    ORDER BY d.nom, e.date_heure, m.nom
                """
                
                examens_dept = db.execute_query(query, (periode_id_dept,))
                
                if examens_dept:
                    # Filter by department if selected
                    if selected_dept != "Tous les départements":
                        examens_dept = [e for e in examens_dept if e['departement'] == selected_dept]
                    
                    if examens_dept:
                        df_dept = pd.DataFrame(examens_dept)
                        
                        # Summary metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        def display_dept_card(col, label, value, icon):
                            with col:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-label">{icon} {label}</div>
                                    <div class="metric-value">{value}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        display_dept_card(col1, "Total Examens", len(examens_dept), "📝")
                        display_dept_card(col2, "Départements", df_dept['departement'].nunique(), "🏛️")
                        display_dept_card(col3, "Total Étudiants", f"{df_dept['nb_inscrits'].sum():,}", "👨‍🎓")
                        display_dept_card(col4, "Salles Utilisées", df_dept['salle_nom'].nunique(), "🏫")
                        
                        st.markdown("---")
                        
                        # Display format selector
                        display_format = st.radio(
                            "Format d'affichage",
                            ["Par Département et Date", "Liste Détaillée"],
                            horizontal=True
                        )
                        
                        if display_format == "Par Département et Date":
                            # Group by department
                            for dept_name in sorted(df_dept['departement'].unique()):
                                with st.expander(f"🏛️ {dept_name}", expanded=(selected_dept != "Tous les départements")):
                                    dept_exams = df_dept[df_dept['departement'] == dept_name]
                                    
                                    st.markdown(f"**{len(dept_exams)} examens planifiés**")
                                    
                                    # Group by date
                                    dept_exams['date'] = pd.to_datetime(dept_exams['date_heure']).dt.date
                                    dept_exams['heure'] = pd.to_datetime(dept_exams['date_heure']).dt.strftime('%H:%M')
                                    
                                    for date in sorted(dept_exams['date'].unique()):
                                        st.markdown(f"### 📅 {date.strftime('%A %d %B %Y')}")
                                        
                                        date_exams = dept_exams[dept_exams['date'] == date].sort_values('heure')
                                        
                                        for _, exam in date_exams.iterrows():
                                            col_time, col_info = st.columns([1, 4])
                                            
                                            with col_time:
                                                st.markdown(f"**{exam['heure']}**")
                                                st.caption(f"{exam['duree_minutes']} min")
                                            
                                            with col_info:
                                                st.markdown(f"**{exam['module_nom']}** ({exam['module_code']})")
                                                st.markdown(f"📍 {exam['salle_nom']} - {exam['batiment']} | 👨‍🏫 {exam['professeur']} | 👥 {exam['nb_inscrits']} étudiants")
                                                st.markdown(f"🎓 Formation: {exam['formation']}")
                                        
                                        st.markdown("---")
                        
                        else:  # Liste Détaillée
                            st.dataframe(
                                df_dept[['date_heure', 'departement', 'module_nom', 'module_code', 
                                        'salle_nom', 'batiment', 'professeur', 'nb_inscrits', 'duree_minutes']],
                                use_container_width=True,
                                hide_index=True
                            )
                        
                        # Export options
                        st.markdown("---")
                        col_exp1, col_exp2 = st.columns(2)
                        
                        with col_exp1:
                            if st.button("📥 Exporter en CSV", key="export_csv_dept"):
                                csv = df_dept.to_csv(index=False, encoding='utf-8')
                                st.download_button(
                                    label="Télécharger le CSV",
                                    data=csv,
                                    file_name=f"planning_departements_{periode_id_dept}.csv",
                                    mime="text/csv",
                                    key="download_csv_dept"
                                )
                        
                        with col_exp2:
                            if st.button("📊 Exporter en Excel", key="export_excel_dept"):
                                import io
                                output = io.BytesIO()
                                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                    df_dept.to_excel(writer, index=False, sheet_name='Planning')
                                output.seek(0)
                                st.download_button(
                                    label="Télécharger Excel",
                                    data=output,
                                    file_name=f"planning_departements_{periode_id_dept}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="download_excel_dept"
                                )
                    else:
                        st.markdown(f"""
                        <div class="custom-alert alert-warning">
                            <h4>ℹ️ Aucun examen planifié pour le département {selected_dept}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="custom-alert alert-warning">
                        <h4>ℹ️ Aucun examen planifié pour cette période</h4>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="custom-alert alert-warning">
                    <h4>⚠️ Aucun département trouvé</h4>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-alert alert-warning">
                <h4>⚠️ Aucune période d'examen active</h4>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()