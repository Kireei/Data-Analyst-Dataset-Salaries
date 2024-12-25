#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
#######################
# Page configuration
st.set_page_config(
    page_title="Data Science Salaries",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
df= pd.read_csv('data/DataScience_salaries_2024.csv')
#######################

# Sidebar
with st.sidebar:
    st.title('💰 Data Science Salaries')

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)\

# Plots
rata_rata_gaji = df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False)

top_job_title = rata_rata_gaji.head(10).index
df_top = df[df['job_title'].isin(top_job_title)]
df_no_index = df.set_index('job_title')
df_top_means = df_top.groupby('job_title')['salary_in_usd'].mean().reset_index()

col1, col2, col3 = st.columns([3, 0.1, 1])

#Grafik Bar Chart
with col1:
    chart = alt.Chart(df_top_means).mark_bar().encode(
        x=alt.X('job_title', sort='-y', title='Job Title'),
        y=alt.Y('salary_in_usd', title='Average Salary (USD)'),
        tooltip=['job_title', 'salary_in_usd'],
        color=alt.Color('salary_in_usd', scale=alt.Scale(scheme=selected_color_theme)) 
    ).properties(
        title='Rata-rata Gaji di Setiap Pekerjaan Tahun 2020 - 2024',
        width=600,
        height=600
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

with col3:
    st.subheader("Top Job Title")
    top_jobs_df = df_top_means.rename(columns={'salary_in_usd': 'Average Salary (USD)'})
    top_jobs_df['Average Salary (USD)'] = top_jobs_df['Average Salary (USD)'].apply(lambda x: f"{x:.2f}")
    st.table(top_jobs_df.set_index('job_title'))
    
    with st.expander('About', expanded=True):
        st.write('''
            - :orange[**Data**]: [Data Science Salaries 2024](https://www.kaggle.com/datasets/yusufdelikkaya/datascience-salaries-2024/data).
            - :orange[**Data Analysis Result**]: Data is not Perfect, Some Data Exceeds the Median Limit (Outlier).
            ''')
#Line Chart    
def makeLine(df, title="Jumlah Tahun Pekerja Berdasarkan Tingkat"):
    df['work_year'] = df['work_year'].astype(str)

    df_grouped = df.groupby(['work_year', 'experience_level']).size().reset_index(name='Jumlah Pekerja')
    df_grouped = df_grouped.rename(columns={'experience_level': 'Tingkat Pengalaman', 'work_year': 'Tahun Bekerja'})

    line_chart = alt.Chart(df_grouped).mark_line(point=True).encode(
        x=alt.X('Tahun Bekerja:O', title='Tahun Bekerja'),
        y=alt.Y('Jumlah Pekerja', title='Jumlah Pekerja'),
        color=alt.Color('Tingkat Pengalaman', legend=alt.Legend(title='Tingkat Pengalaman')),
        tooltip=['Tahun Bekerja', 'Tingkat Pengalaman', 'Jumlah Pekerja']
    ).properties(
        title=title
    ).interactive()
    return line_chart

line_chart_altair = makeLine(df)
st.altair_chart(line_chart_altair, use_container_width=True)


