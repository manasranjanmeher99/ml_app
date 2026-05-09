import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    layout="wide"
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------

matches = pd.read_csv(r"C:\Users\ASUS\OneDrive\Desktop\matches.csv")
deliveries = pd.read_csv(r"C:\Users\ASUS\OneDrive\Desktop\deliveries.csv")

# -------------------------------------------------
# Title
# -------------------------------------------------

st.title("🏏 IPL / Cricket Analytics Dashboard")

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.header("Filters")

season = st.sidebar.selectbox(
    "Select Season",
    sorted(matches['season'].dropna().unique())
)

filtered_matches = matches[matches['season'] == season]

# -------------------------------------------------
# KPI Section
# -------------------------------------------------

total_matches = filtered_matches.shape[0]

total_teams = pd.concat([
    filtered_matches['team1'],
    filtered_matches['team2']
]).nunique()

total_players = deliveries['batsman'].nunique()


col1, col2, col3 = st.columns(3)

col1.metric("🏏 Matches", total_matches)
col2.metric("👥 Teams", total_teams)
col3.metric("⭐ Players", total_players)

st.markdown("---")

# -------------------------------------------------
# Top Run Scorers
# -------------------------------------------------

st.subheader("🔥 Top Run Scorers")

batsman_runs = (
    deliveries.groupby('batsman')['batsman_runs']
    .sum()
    .reset_index()
    .sort_values(by='batsman_runs', ascending=False)
    .head(10)
)

fig1 = px.bar(
    batsman_runs,
    x='batsman',
    y='batsman_runs',
    title='Top 10 Run Scorers'
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------
# Top Wicket Takers
# -------------------------------------------------

st.subheader("🎯 Top Wicket Takers")

# Filter wicket deliveries
wickets = deliveries[deliveries['player_dismissed'].notna()]

# Count wickets by bowler
bowler_wickets = (
    wickets.groupby('bowler')
    .size()
    .reset_index(name='wickets')
    .sort_values(by='wickets', ascending=False)
    .head(10)
)

fig2 = px.bar(
    bowler_wickets,
    x='bowler',
    y='wickets',
    title='Top 10 Wicket Takers'
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# Team Wins Analysis
# -------------------------------------------------

st.subheader("🏆 Team Wins Analysis")

team_wins = (
    matches['winner']
    .value_counts()
    .reset_index()
)

team_wins.columns = ['Team', 'Wins']

fig3 = px.pie(
    team_wins,
    names='Team',
    values='Wins',
    title='Team Winning Percentage'
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# Toss Decision Analysis
# -------------------------------------------------

st.subheader("🪙 Toss Decision Analysis")

fig4 = px.histogram(
    matches,
    x='toss_decision',
    title='Toss Decisions'
)

st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------
# Match Win By Runs
# -------------------------------------------------

st.subheader("📈 Match Win Margin Analysis")

fig5 = px.histogram(
    matches,
    x='win_by_runs',
    nbins=20,
    title='Win By Runs Distribution'
)

st.plotly_chart(fig5, use_container_width=True)

# -------------------------------------------------
# Team Comparison
# -------------------------------------------------

st.subheader("⚔️ Team Comparison")

teams = sorted(matches['team1'].dropna().unique())

team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", teams, index=1)

team1_wins = matches[matches['winner'] == team1].shape[0]
team2_wins = matches[matches['winner'] == team2].shape[0]

comparison_df = pd.DataFrame({
    'Team': [team1, team2],
    'Wins': [team1_wins, team2_wins]
})

fig6 = px.bar(
    comparison_df,
    x='Team',
    y='Wins',
    title='Team Comparison'
)

st.plotly_chart(fig6, use_container_width=True)

# -------------------------------------------------
# Player Strike Rate Analysis
# -------------------------------------------------

st.subheader("🚀 Player Strike Rate Analysis")

# Player stats
player_stats = deliveries.groupby('batsman').agg({
    'batsman_runs': 'sum',
    'ball': 'count'
}).reset_index()

# Rename ball column
player_stats.rename(columns={'ball': 'balls_faced'}, inplace=True)

# Strike rate calculation
player_stats['strike_rate'] = (
    player_stats['batsman_runs'] /
    player_stats['balls_faced']
) * 100

# Minimum balls filter
player_stats = player_stats[
    player_stats['balls_faced'] > 100
]

# Top players
player_stats = player_stats.sort_values(
    by='strike_rate',
    ascending=False
).head(10)

# Scatter chart
fig7 = px.scatter(
    player_stats,
    x='balls_faced',
    y='strike_rate',
    size='batsman_runs',
    hover_name='batsman',
    title='Best Strike Rates'
)

st.plotly_chart(fig7, use_container_width=True)

# -------------------------------------------------
# Raw Dataset
# -------------------------------------------------

st.subheader("📄 Match Dataset")

st.dataframe(filtered_matches)