import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import json

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="The Burnout Algorithm",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1117 50%, #0a0a1a 100%);
    color: #e2e8f0;
}

.hero {
    padding: 3rem 2.5rem 2.5rem 2.5rem;
    border-radius: 24px;
    background: linear-gradient(120deg, #7c3aed 0%, #4f46e5 40%, #0ea5e9 100%);
    box-shadow: 0 20px 60px rgba(124, 58, 237, 0.4);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}

.hero h1 {
    color: white;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 12px rgba(0,0,0,0.3);
    line-height: 1.2;
}

.hero p {
    color: rgba(255,255,255,0.85);
    font-size: 1.1rem;
    margin: 0;
    max-width: 700px;
    line-height: 1.6;
}

.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.8rem;
    flex-wrap: wrap;
}

.hero-stat {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    padding: 0.8rem 1.4rem;
    text-align: center;
}

.hero-stat .number {
    font-size: 1.8rem;
    font-weight: 800;
    color: white;
    display: block;
}

.hero-stat .label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.75);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-card {
    padding: 1.4rem 1.6rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
    transition: transform 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(124,58,237,0.4);
}

.metric-card .card-title {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

.metric-card .card-value {
    font-size: 2rem;
    font-weight: 800;
    color: white;
}

.metric-card .card-sub {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.6);
    margin-top: 0.3rem;
}

.insight-box {
    padding: 1.2rem 1.6rem;
    border-radius: 14px;
    background: rgba(124,58,237,0.1);
    border-left: 4px solid #7c3aed;
    margin: 1rem 0;
    font-size: 0.95rem;
    line-height: 1.6;
    color: #e2e8f0;
}

.rotten-mango-card {
    padding: 1.6rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 1.2rem;
}

.rotten-mango-card .part-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #7c3aed;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.rotten-mango-card .part-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.6rem;
}

.rotten-mango-card .part-body {
    font-size: 0.92rem;
    color: rgba(255,255,255,0.7);
    line-height: 1.7;
}

.prediction-card {
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    margin: 1rem 0;
}

.prediction-high {
    background: linear-gradient(135deg, rgba(212,105,107,0.2), rgba(212,105,107,0.05));
    border: 2px solid #d4696b;
}

.prediction-medium {
    background: linear-gradient(135deg, rgba(240,165,0,0.2), rgba(240,165,0,0.05));
    border: 2px solid #f0a500;
}

.prediction-low {
    background: linear-gradient(135deg, rgba(74,124,158,0.2), rgba(74,124,158,0.05));
    border: 2px solid #4a7c9e;
}

.prediction-label {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.prediction-desc {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.7);
    line-height: 1.6;
}

.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

button[data-baseweb="tab"] {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.6) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: white !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1a 0%, #0d1117 100%);
}

div.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #4f46e5);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.8rem;
    font-weight: 700;
    font-size: 1rem;
    box-shadow: 0 6px 20px rgba(124,58,237,0.35);
    transition: all 0.2s ease;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(124,58,237,0.5);
}

.stSlider > div { color: #e2e8f0; }
.stSelectbox > div { color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# LOAD DATA AND MODEL
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('data/cleaned_ai_student_data.csv')

@st.cache_resource
def load_model():
    model = joblib.load('APP/Trained_XGBoost_&_Cleaned_Dataset.pkl')
    with open('OUTPUT/feature_columns.json', 'r') as f:
        features = json.load(f)
    return model, features

df = pd.read_csv('DATA/ai_student_impact_dataset.csv')
model, feature_columns = load_model()

# Colors
COLOR_HIGH = '#d4696b'
COLOR_MEDIUM = '#f0a500'
COLOR_LOW = '#4a7c9e'
COLOR_PURPLE = '#7c3aed'

PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#e2e8f0',
    margin=dict(t=40, b=40, l=40, r=40)
)

# ─────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────
high_pct = round((df['Burnout_Risk_Level'] == 'High').sum() / len(df) * 100, 1)
mean_hrs = round(df['Weekly_GenAI_Hours'].mean(), 1)
high_mean = round(df[df['Burnout_Risk_Level']=='High']['Weekly_GenAI_Hours'].mean(), 1)
low_mean = round(df[df['Burnout_Risk_Level']=='Low']['Weekly_GenAI_Hours'].mean(), 1)
ratio = round(high_mean / low_mean, 1)

st.markdown(f"""
<div class="hero">
    <h1>🔥 The Burnout Algorithm</h1>
    <p>Predicting which students AI is breaking before they break.
    A machine learning study of 50,000 students and the hidden cost
    of unsupported AI adoption in higher education.</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <span class="number">50,000</span>
            <span class="label">Students Analyzed</span>
        </div>
        <div class="hero-stat">
            <span class="number">{high_pct}%</span>
            <span class="label">At High Burnout Risk</span>
        </div>
        <div class="hero-stat">
            <span class="number">{ratio}x</span>
            <span class="label">More AI Hours → High Burnout</span>
        </div>
        <div class="hero-stat">
            <span class="number">53.7%</span>
            <span class="label">Best Model Accuracy</span>
        </div>
        <div class="hero-stat">
            <span class="number">-0.019</span>
            <span class="label">AI Hours vs GPA Correlation</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 The Story",
    "🤖 Model Results",
    "🎯 Predict a Student",
    "ℹ️ About"
])

# ═══════════════════════════════════════════════════════
# TAB 1 — THE STORY
# ═══════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">The Reveal</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
    Every section answers one question and raises the next.
    Follow the thread.
    </div>
    """, unsafe_allow_html=True)

    # PART 1
    st.markdown("""
    <div class="rotten-mango-card">
        <div class="part-label">Cold Open</div>
        <div class="part-title">"The Tool That Was Supposed to Help"</div>
        <div class="part-body">
        50,000 students. AI tools in every pocket, every study session,
        every assignment. Institutions celebrate the adoption numbers.
        Nobody is measuring what it costs.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        burnout_counts = df['Burnout_Risk_Level'].value_counts()
        burnout_pct = df['Burnout_Risk_Level']\
            .value_counts(normalize=True).mul(100).round(1)

        fig_burnout = go.Figure(go.Bar(
            x=['Medium', 'Low', 'High'],
            y=[burnout_counts.get('Medium', 0),
               burnout_counts.get('Low', 0),
               burnout_counts.get('High', 0)],
            text=[f"{burnout_pct.get('Medium',0)}%",
                  f"{burnout_pct.get('Low',0)}%",
                  f"{burnout_pct.get('High',0)}%"],
            textposition='outside',
            marker_color=[COLOR_MEDIUM, COLOR_LOW, COLOR_HIGH],
            marker_line_width=0
        ))
        fig_burnout.update_layout(
            title='Burnout Risk Distribution',
            **PLOT_LAYOUT,
            showlegend=False,
            yaxis_title='Number of Students'
        )
        st.plotly_chart(fig_burnout, use_container_width=True)

    with col2:
        skill_counts = df['Prompt_Engineering_Skill'].value_counts()
        skill_pct = df['Prompt_Engineering_Skill']\
            .value_counts(normalize=True).mul(100).round(1)

        fig_skill = go.Figure(go.Bar(
            x=['Beginner', 'Intermediate', 'Advanced'],
            y=[skill_counts.get('Beginner', 0),
               skill_counts.get('Intermediate', 0),
               skill_counts.get('Advanced', 0)],
            text=[f"{skill_pct.get('Beginner',0)}%",
                  f"{skill_pct.get('Intermediate',0)}%",
                  f"{skill_pct.get('Advanced',0)}%"],
            textposition='outside',
            marker_color=[COLOR_HIGH, COLOR_MEDIUM, COLOR_LOW],
            marker_line_width=0
        ))
        fig_skill.update_layout(
            title='Who Actually Knows How to Use AI?',
            **PLOT_LAYOUT,
            showlegend=False,
            yaxis_title='Number of Students'
        )
        st.plotly_chart(fig_skill, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>1 in 4 students is at high burnout risk.</b>
    Only 27.6% are advanced prompt users.
    More than a third are beginners using tools they don't fully understand
    every single week.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # PART 2
    st.markdown("""
    <div class="rotten-mango-card">
        <div class="part-label">Part 1</div>
        <div class="part-title">"More AI, More Burnout, Not More Grades"</div>
        <div class="part-body">
        Everyone assumed more AI would mean better grades.
        The data says something else entirely.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        order = ['Low', 'Medium', 'High']
        means_hrs = df.groupby('Burnout_Risk_Level')['Weekly_GenAI_Hours']\
            .mean().reindex(order)

        fig_hrs = go.Figure(go.Bar(
            x=order,
            y=means_hrs.values.round(2),
            text=[f"{v:.1f} hrs" for v in means_hrs.values],
            textposition='outside',
            marker_color=[COLOR_LOW, COLOR_MEDIUM, COLOR_HIGH],
            marker_line_width=0
        ))
        fig_hrs.update_layout(
            title='Mean Weekly AI Hours by Burnout Level',
            **PLOT_LAYOUT,
            showlegend=False,
            yaxis_title='Weekly GenAI Hours'
        )
        st.plotly_chart(fig_hrs, use_container_width=True)

    with col4:
        means_gpa = df.groupby('Burnout_Risk_Level')['Post_Semester_GPA']\
            .mean().reindex(order)

        fig_gpa = go.Figure(go.Bar(
            x=order,
            y=means_gpa.values.round(3),
            text=[f"{v:.3f}" for v in means_gpa.values],
            textposition='outside',
            marker_color=[COLOR_LOW, COLOR_MEDIUM, COLOR_HIGH],
            marker_line_width=0
        ))
        fig_gpa.update_layout(
            title='Mean Post-Semester GPA by Burnout Level',
            **PLOT_LAYOUT,
            showlegend=False,
            yaxis_title='GPA',
            yaxis_range=[3.0, 3.6]
        )
        st.plotly_chart(fig_gpa, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    High burnout students use AI <b>{ratio}x more</b> than low burnout students
    (15.21 hrs vs 4.64 hrs). Yet GPA correlation with AI hours is
    <b>-0.019 (essentially zero).</b>
    The cost is real. The academic return is not.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # PART 3
    st.markdown("""
    <div class="rotten-mango-card">
        <div class="part-label">Part 2</div>
        <div class="part-title">"The Protective Factor Nobody Is Teaching"</div>
        <div class="part-body">
        We expected skill to be the antidote. The data says it's
        more complicated.
        </div>
    </div>
    """, unsafe_allow_html=True)

    skill_burnout = df.groupby(
        ['Prompt_Engineering_Skill', 'Burnout_Risk_Level']
    ).size().unstack()
    skill_burnout_pct = skill_burnout.div(
        skill_burnout.sum(axis=1), axis=0
    ) * 100
    skill_order = ['Beginner', 'Intermediate', 'Advanced']
    skill_burnout_pct = skill_burnout_pct.reindex(skill_order)

    fig_skill_burnout = go.Figure()
    for level, color in zip(['Low', 'Medium', 'High'],
                             [COLOR_LOW, COLOR_MEDIUM, COLOR_HIGH]):
        fig_skill_burnout.add_trace(go.Bar(
            name=f'{level} Burnout',
            x=skill_order,
            y=skill_burnout_pct[level].values.round(1),
            marker_color=color,
            text=[f"{v:.1f}%" for v in
                  skill_burnout_pct[level].values.round(1)],
            textposition='outside'
        ))

    fig_skill_burnout.update_layout(
        title='Burnout Risk by Prompt Engineering Skill Level',
        barmode='group',
        **PLOT_LAYOUT,
        yaxis_title='Percentage of Students (%)',
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(255,255,255,0.1)'
        )
    )
    st.plotly_chart(fig_skill_burnout, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    High burnout rates are nearly identical across all skill levels —
    Beginner: 24.6%, Intermediate: 24.9%, Advanced: 25.5%.
    <b>Skill alone does not protect.</b> Advanced users burn out too —
    they just need more hours to get there.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # PART 4
    st.markdown("""
    <div class="rotten-mango-card">
        <div class="part-label">Part 3</div>
        <div class="part-title">"The Behaviour Nobody Talks About"</div>
        <div class="part-body">
        If it's not hours and not skill, is it what you're doing with AI?
        </div>
    </div>
    """, unsafe_allow_html=True)

    use_high = {}
    for use in df['Primary_Use_Case'].unique():
        subset = df[df['Primary_Use_Case'] == use]
        high_p = (subset['Burnout_Risk_Level'] == 'High').sum() / len(subset) * 100
        mean_h = subset['Weekly_GenAI_Hours'].mean()
        use_high[use] = {'high_pct': round(high_p, 1), 'mean_hrs': round(mean_h, 1)}

    use_df = pd.DataFrame(use_high).T.sort_values('high_pct', ascending=True)

    fig_use = go.Figure(go.Bar(
        y=use_df.index,
        x=use_df['high_pct'],
        orientation='h',
        text=[f"{v}%" for v in use_df['high_pct']],
        textposition='outside',
        marker_color=COLOR_PURPLE,
        marker_line_width=0
    ))
    fig_use.update_layout(
        title='% at High Burnout Risk by Primary AI Use Case',
        **PLOT_LAYOUT,
        xaxis_title='% High Burnout Risk',
        xaxis_range=[0, 35]
    )
    st.plotly_chart(fig_use, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Debugging/Troubleshooting carries the highest burnout rate at 27.3%</b>
    not because it is passive, but because it is cognitively exhausting.
    The trap is not in passivity. It is in cognitive load.
    Copywriting/Drafting has the lowest burnout at 23.0% whereby the collaboration
    feels generative rather than grinding.
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TAB 2 — MODEL RESULTS
# ═══════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Model Evaluation</div>',
                unsafe_allow_html=True)

    # Key metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.markdown("""
        <div class="metric-card">
            <div class="card-title">Best Model</div>
            <div class="card-value" style="font-size:1.4rem;">XGBoost</div>
            <div class="card-sub">Tuned with GridSearchCV</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="metric-card">
            <div class="card-title">Best Accuracy</div>
            <div class="card-value">53.7%</div>
            <div class="card-sub">vs 33.3% random baseline</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown("""
        <div class="metric-card">
            <div class="card-title">Macro F1 Score</div>
            <div class="card-value">0.54</div>
            <div class="card-sub">Best across all models</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m4:
        st.markdown("""
        <div class="metric-card">
            <div class="card-title">Models Tested</div>
            <div class="card-value">7</div>
            <div class="card-sub">Across 5 model families</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Model comparison
    models_data = {
        'Model': ['GaussianNB', 'RF (tuned)', 'LightGBM',
                  'RF (default)', 'LR (tuned)', 'CatBoost', 'XGBoost'],
        'Accuracy': [48.6, 50.6, 51.0, 51.3, 51.3, 51.5, 53.7],
        'Macro F1': [0.48, 0.51, 0.51, 0.52, 0.52, 0.52, 0.54],
        'Medium Recall': [27, 42, 35, 43, 32, 34, 61]
    }
    models_df = pd.DataFrame(models_data)

    col_left, col_right = st.columns(2)

    with col_left:
        fig_acc = px.bar(
            models_df.sort_values('Accuracy'),
            x='Accuracy', y='Model',
            orientation='h',
            color='Accuracy',
            color_continuous_scale=['#d4696b', '#f0a500', '#7c3aed'],
            text='Accuracy'
        )
        fig_acc.update_traces(texttemplate='%{text:.1f}%',
                              textposition='outside')
        fig_acc.update_layout(
            title='Model Accuracy Comparison',
            **PLOT_LAYOUT,
            coloraxis_showscale=False,
            xaxis_range=[44, 58],
            xaxis_title='Accuracy (%)'
        )
        fig_acc.add_vline(x=33.3, line_dash='dash',
                          line_color='rgba(255,255,255,0.3)',
                          annotation_text='Random baseline')
        st.plotly_chart(fig_acc, use_container_width=True)

    with col_right:
        fig_f1 = px.bar(
            models_df.sort_values('Macro F1'),
            x='Macro F1', y='Model',
            orientation='h',
            color='Macro F1',
            color_continuous_scale=['#d4696b', '#f0a500', '#7c3aed'],
            text='Macro F1'
        )
        fig_f1.update_traces(texttemplate='%{text:.2f}',
                             textposition='outside')
        fig_f1.update_layout(
            title='Macro F1 Score Comparison',
            **PLOT_LAYOUT,
            coloraxis_showscale=False,
            xaxis_range=[0.44, 0.58],
            xaxis_title='Macro F1'
        )
        st.plotly_chart(fig_f1, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Six different model architectures converge between 48.6% and 53.7%.</b>
    This is not a modelling failure but a signal ceiling.
    Medium burnout represents a genuine transitional state that no model
    can cleanly separate because it doesn't have a sharp real-world boundary.
    XGBoost wins by being the only model to achieve 61% Medium recall.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Confusion matrix
    st.markdown('<div class="section-header">XGBoost Confusion Matrix</div>',
                unsafe_allow_html=True)

    cm_data = np.array([
        [1633, 1548, 93],
        [1148, 2573, 508],
        [193, 1155, 1149]
    ])

    fig_cm = px.imshow(
        cm_data,
        labels=dict(x='Predicted', y='Actual', color='Count'),
        x=['Low', 'Medium', 'High'],
        y=['Low', 'Medium', 'High'],
        color_continuous_scale='Blues',
        text_auto=True
    )
    fig_cm.update_layout(
        title='XGBoost — Final Model Confusion Matrix',
        **PLOT_LAYOUT,
        width=500
    )
    col_cm1, col_cm2 = st.columns([1, 1])
    with col_cm1:
        st.plotly_chart(fig_cm, use_container_width=True)
    with col_cm2:
        st.markdown("""
        <div class="metric-card" style="margin-top:2rem;">
            <div class="card-title">What This Matrix Tells Us</div>
            <br>
            <p style="color:rgba(255,255,255,0.7); line-height:1.7; font-size:0.9rem;">
            The model's errors are <b>structured, not random.</b>
            Misclassifications occur almost exclusively between
            adjacent classes (Low↔Medium and Medium↔High).
            <br><br>
            The model almost never confuses Low with High
            (only 93 cases out of 10,000). It understands the
            burnout spectrum even when it cannot pinpoint the
            exact category.
            <br><br>
            <b>Recommendation:</b> Deploy as an early warning
            signal, not a diagnostic. A student flagged as Medium
            warrants a check-in. High warrants immediate outreach.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Feature importance
    st.markdown('<div class="section-header">Feature Importance</div>',
                unsafe_allow_html=True)

    importance_data = {
        'Feature': [
            'Weekly_GenAI_Hours', 'Usage_Intensity_Score',
            'Pre_Semester_GPA', 'Traditional_Study_Hours',
            'Anxiety_Level_During_Exams', 'Perceived_AI_Dependency',
            'Year_of_Study', 'Tool_Diversity', 'Institutional_Policy',
            'Prompt_Engineering_Skill'
        ],
        'Importance': [
            0.187, 0.149, 0.126, 0.122, 0.068,
            0.066, 0.049, 0.046, 0.034, 0.023
        ]
    }
    imp_df = pd.DataFrame(importance_data).sort_values('Importance')

    fig_imp = px.bar(
        imp_df,
        x='Importance', y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale=['#4a7c9e', '#7c3aed', '#d4696b'],
        text='Importance'
    )
    fig_imp.update_traces(texttemplate='%{text:.3f}',
                          textposition='outside')
    fig_imp.update_layout(
        title='Random Forest — Top 10 Feature Importance',
        **PLOT_LAYOUT,
        coloraxis_showscale=False,
        xaxis_title='Importance Score',
        xaxis_range=[0, 0.22]
    )
    st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Weekly AI hours is the strongest predictor (0.187).</b>
    The engineered Usage_Intensity_Score ranks second (0.149), 
    validating feature engineering. Traditional study hours (0.122)
    is protective. Prompt skill ranks 10th (0.023) confirming
    that skill alone does not protect students from burnout.
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TAB 3 — PREDICT A STUDENT
# ═══════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Predict a Student\'s Burnout Risk</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
    Enter a student's profile below and the XGBoost model will predict
    their burnout risk level. This demonstrates how the model could be
    used as an early warning tool by academic advisors.
    </div>
    """, unsafe_allow_html=True)

    col_inp1, col_inp2 = st.columns(2)

    with col_inp1:
        st.markdown("#### 📚 Academic Profile")
        major = st.selectbox(
            "Major Category",
            ['Arts', 'Business', 'Humanities', 'Medical', 'STEM']
        )
        year = st.selectbox(
            "Year of Study",
            ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
        )
        pre_gpa = st.slider(
            "Pre-Semester GPA", 1.0, 4.0, 3.2, 0.1
        )
        post_gpa_note = st.info(
            "Note: Post-Semester GPA is excluded from prediction "
            "to avoid data leakage because it's an outcome, not an input."
        )

    with col_inp2:
        st.markdown("#### 🤖 AI Usage Profile")
        weekly_hours = st.slider(
            "Weekly GenAI Hours", 0.0, 40.0, 8.0, 0.5
        )
        skill = st.selectbox(
            "Prompt Engineering Skill",
            ['Beginner', 'Intermediate', 'Advanced']
        )
        use_case = st.selectbox(
            "Primary Use Case",
            ['Arts', 'Copywriting/Drafting', 'Debugging/Troubleshooting',
             'Direct_Answer_Generation', 'Ideation', 'Summarizing_Reading']
        )
        tool_diversity = st.slider("Tool Diversity (# of AI tools used)", 1, 5, 3)
        paid_sub = st.radio(
            "Paid AI Subscription?", ['No', 'Yes'], horizontal=True
        )

    col_inp3, col_inp4 = st.columns(2)

    with col_inp3:
        st.markdown("#### 📊 Study & Wellbeing")
        trad_hours = st.slider(
            "Traditional Study Hours/Week", 1.0, 36.0, 11.0, 0.5
        )
        dependency = st.slider(
            "Perceived AI Dependency (1-10)", 1, 10, 4
        )
        anxiety = st.slider(
            "Anxiety Level During Exams (1-10)", 1, 10, 4
        )

    with col_inp4:
        st.markdown("#### 🏫 Institutional Context")
        policy = st.selectbox(
            "Institutional AI Policy",
            ['Strict_Ban', 'Allowed_With_Citation', 'Actively_Encouraged']
        )

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔮 Predict Burnout Risk", key="predict")

    if predict_btn:
        # Encode inputs
        skill_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        year_map = {'Freshman': 1, 'Sophomore': 2, 'Junior': 3,
                    'Senior': 4, 'Graduate': 5}
        policy_map = {'Strict_Ban': 1, 'Allowed_With_Citation': 2,
                      'Actively_Encouraged': 3}

        skill_enc = skill_map[skill]
        year_enc = year_map[year]
        policy_enc = policy_map[policy]
        paid_enc = 1 if paid_sub == 'Yes' else 0
        intensity = weekly_hours / skill_enc

        # One-hot encode major
        major_business = 1 if major == 'Business' else 0
        major_humanities = 1 if major == 'Humanities' else 0
        major_medical = 1 if major == 'Medical' else 0
        major_stem = 1 if major == 'STEM' else 0

        # One-hot encode use case
        use_debug = 1 if use_case == 'Debugging/Troubleshooting' else 0
        use_direct = 1 if use_case == 'Direct_Answer_Generation' else 0
        use_ideation = 1 if use_case == 'Ideation' else 0
        use_summarize = 1 if use_case == 'Summarizing_Reading' else 0

        # Build input dataframe in exact feature order
        input_data = pd.DataFrame([{
            'Year_of_Study': year_enc,
            'Pre_Semester_GPA': pre_gpa,
            'Weekly_GenAI_Hours': weekly_hours,
            'Prompt_Engineering_Skill': skill_enc,
            'Tool_Diversity': tool_diversity,
            'Paid_Subscription': paid_enc,
            'Traditional_Study_Hours': trad_hours,
            'Perceived_AI_Dependency': dependency,
            'Institutional_Policy': policy_enc,
            'Anxiety_Level_During_Exams': anxiety,
            'Usage_Intensity_Score': intensity,
            'Major_Category_Business': major_business,
            'Major_Category_Humanities': major_humanities,
            'Major_Category_Medical': major_medical,
            'Major_Category_STEM': major_stem,
            'Primary_Use_Case_Debugging/Troubleshooting': use_debug,
            'Primary_Use_Case_Direct_Answer_Generation': use_direct,
            'Primary_Use_Case_Ideation': use_ideation,
            'Primary_Use_Case_Summarizing_Reading': use_summarize
        }])

        # Predict
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]

        label_map = {0: 'Low', 1: 'Medium', 2: 'High'}
        pred_label = label_map[prediction]
        confidence = round(probabilities[prediction] * 100, 1)

        # Display result
        color_map = {
            'Low': COLOR_LOW,
            'Medium': COLOR_MEDIUM,
            'High': COLOR_HIGH
        }
        css_class = {
            'Low': 'prediction-low',
            'Medium': 'prediction-medium',
            'High': 'prediction-high'
        }
        emoji_map = {
            'Low': '✅',
            'Medium': '⚠️',
            'High': '🔴'
        }
        desc_map = {
            'Low': 'This student shows low burnout risk based on their profile. '
                   'Current AI usage patterns appear sustainable.',
            'Medium': 'This student is in a transitional zone. '
                      'A check-in from an academic advisor is recommended '
                      'before risk escalates.',
            'High': 'This student shows high burnout risk. '
                    'Immediate outreach from an academic advisor or counselor '
                    'is strongly recommended.'
        }

        col_res1, col_res2 = st.columns([1, 1])

        with col_res1:
            st.markdown(f"""
            <div class="prediction-card {css_class[pred_label]}">
                <div class="prediction-label" style="color:{color_map[pred_label]}">
                    {emoji_map[pred_label]} {pred_label} Burnout Risk
                </div>
                <div style="font-size:1.1rem; color:rgba(255,255,255,0.6);
                            margin-bottom:1rem;">
                    Model confidence: <b style="color:white">{confidence}%</b>
                </div>
                <div class="prediction-desc">{desc_map[pred_label]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_res2:
            # Probability gauge
            fig_gauge = go.Figure()

            for i, (label, color) in enumerate(
                zip(['Low', 'Medium', 'High'],
                    [COLOR_LOW, COLOR_MEDIUM, COLOR_HIGH])
            ):
                fig_gauge.add_trace(go.Bar(
                    x=[label],
                    y=[round(probabilities[i] * 100, 1)],
                    marker_color=color,
                    text=[f"{probabilities[i]*100:.1f}%"],
                    textposition='outside',
                    name=label
                ))

            fig_gauge.update_layout(
                title='Probability Distribution',
                **PLOT_LAYOUT,
                showlegend=False,
                yaxis_title='Probability (%)',
                yaxis_range=[0, 100],
                height=300
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        # Key risk factors
        st.markdown("#### 🔍 Key Risk Factors in This Profile")
        risk_factors = []

        if weekly_hours > 15:
            risk_factors.append(
                f"⚠️ **High AI usage** ({weekly_hours} hrs/week) : "
                f"above the high-burnout mean of 15.2 hrs"
            )
        if skill == 'Beginner' and weekly_hours > 8:
            risk_factors.append(
                "⚠️ **Beginner skill + high hours** : "
                "the highest risk combination in this dataset"
            )
        if dependency >= 7:
            risk_factors.append(
                f"⚠️ **High perceived dependency** ({dependency}/10) : "
                f"second strongest burnout predictor"
            )
        if anxiety >= 7:
            risk_factors.append(
                f"⚠️ **High exam anxiety** ({anxiety}/10) : "
                f"correlated with burnout risk"
            )
        if trad_hours < 5:
            risk_factors.append(
                f"⚠️ **Low traditional study hours** ({trad_hours} hrs) : "
                f"reduced protective buffer"
            )
        if use_case == 'Debugging/Troubleshooting':
            risk_factors.append(
                "⚠️ **Debugging/Troubleshooting** : "
                "highest cognitive load use case (27.3% high burnout rate)"
            )

        protective = []
        if trad_hours > 14:
            protective.append(
                f"✅ **Strong traditional study habit** ({trad_hours} hrs/week)"
            )
        if skill == 'Advanced':
            protective.append("✅ **Advanced prompt skill** : more efficient AI use")
        if weekly_hours < 5:
            protective.append(
                f"✅ **Low AI usage** ({weekly_hours} hrs/week) : "
                f"below the high-burnout threshold"
            )
        if anxiety <= 3:
            protective.append(f"✅ **Low exam anxiety** ({anxiety}/10)")

        if risk_factors:
            st.markdown("**Risk signals:**")
            for r in risk_factors:
                st.markdown(r)

        if protective:
            st.markdown("**Protective factors:**")
            for p in protective:
                st.markdown(p)

        if not risk_factors and not protective:
            st.markdown(
                "This profile sits in the middle range : "
                "no extreme risk signals or strong protective factors detected."
            )

# ═══════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ═══════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">About This Project</div>',
                unsafe_allow_html=True)

    col_a1, col_a2 = st.columns([2, 1])

    with col_a1:
        st.markdown("""
        ### The Burnout Algorithm
        *Predicting Who AI is Breaking Before They Break*

        **Author:** Madlene Oloo
        **LinkedIn:** [linkedin.com/in/madleneachieng](https://linkedin.com/in/madleneachieng)

        ---

        #### The Problem
        AI tools are now embedded in how students study, write, research
        and think. Institutions measure adoption rates and celebrate digital
        transformation milestones. What they are not measuring is what this
        adoption is doing to students on the inside.

        This project addresses a specific, urgent gap: the absence of a
        data-driven early warning system for AI-induced burnout in higher
        education.

        #### The Dataset
        50,000 students | 15 features | 3 burnout classes (Low / Medium / High)
        Source: AI Student Impact Dataset (Kaggle, 2025)

        #### The Models
        Seven model configurations were tested across five families:
        GaussianNB, Random Forest (default + tuned), LightGBM, CatBoost,
        Logistic Regression (tuned), and XGBoost (tuned [winner]).

        #### The Finding
        Six different algorithms converge between 48.6% and 53.7% accuracy
        proving a genuine signal ceiling in the data, not a modelling failure.
        Medium burnout is a transitional state with no sharp boundary.
        XGBoost achieves 53.7% accuracy and 61% Medium recall which is
        the best performance across all metrics.

        #### Tools Used
        Python · pandas · scikit-learn · XGBoost · LightGBM · CatBoost ·
        matplotlib · seaborn · Streamlit · Plotly · Jupyter Notebook · VS Code
        """)

    with col_a2:
        st.markdown("""
        <div class="metric-card">
            <div class="card-title">Project Stats</div>
            <br>
            <p style="color:rgba(255,255,255,0.7);
                      font-size:0.9rem; line-height:2;">
            📊 50,000 students<br>
            🔢 19 features engineered<br>
            🤖 7 models evaluated<br>
            🏆 XGBoost was the best model<br>
            📈 53.7% accuracy<br>
            🎯 0.54 Macro F1<br>
            🔬 5-fold cross validation<br>
            ⚙️ GridSearchCV tuning<br>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card" style="margin-top:1rem;">
            <div class="card-title">Key Finding</div>
            <br>
            <p style="color:rgba(255,255,255,0.7);
                      font-size:0.88rem; line-height:1.7;">
            High burnout students use AI
            <b style="color:white;">3.3x more</b>
            than low burnout students
            with virtually zero impact on GPA.
            The cost is real.
            The academic return is not.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; padding:2rem; color:rgba(255,255,255,0.3);
            font-size:0.8rem; margin-top:2rem;
            border-top:1px solid rgba(255,255,255,0.05);">
    The Burnout Algorithm · Madlene Oloo · 2026 ·
    Built with Python, XGBoost & Streamlit
</div>
""", unsafe_allow_html=True)