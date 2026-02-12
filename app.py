def calculate_implied_prob(odds, odds_type="Decimal"):
    if odds_type == "Decimal":
        return (1 / odds)
    elif odds_type == "American":
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return abs(odds) / (abs(odds) + 100)
    return 0
from datetime import datetime
import pytz
import streamlit as st
import pandas as pd
import numpy as np

# 1. Setup Page Config
st.set_page_config(page_title="Pro Betting Dashboard", layout="wide")
st.title("🎯 Betting Edge Finder")
# Set to your local Texas time (US/Central)
now = datetime.now(pytz.timezone('US/Central'))
st.caption(f"🕒 Last updated: {now.strftime('%B %d, %Y at %I:%M %p')}")

# 2. Mock Calculation Logic (The "Existing Functions")
def calculate_fair_win_probability(odds):
    """Converts decimal odds to implied probability."""
    return 1 / odds

def calculate_edge(fair_prob, offered_odds):
    """Calculates the edge percentage."""
    implied_prob = 1 / offered_odds
    return fair_prob - implied_prob

# 3. Generating Sample Data
# In a real app, you'd replace this with an API call or CSV upload
data = {
    'Player': ['LeBron James', 'Kevin Durant', 'Steph Curry', 'Luka Doncic', 'Giannis Antetokounmpo'],
    'Offered Odds': [2.10, 1.85, 2.50, 1.90, 2.05],
    'Fair Win %': [0.52, 0.58, 0.45, 0.55, 0.51]
}
df = pd.DataFrame(data)

# Calculate Edge % based on Fair Win % vs Offered Odds
df['Edge %'] = df.apply(lambda x: (x['Fair Win %'] - (1/x['Offered Odds'])), axis=1)

# 4. UI: Metric Cards
if not df.empty:
    # Finding the row with the highest edge
    best_play = df.iloc[df['Edge %'].idxmax()]
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("🔥 Top Value Play", best_play['Player'])
    col_b.metric("Fair Win %", f"{best_play['Fair Win %']:.2%}")
    # Green/Red delta for Edge
    col_c.metric("Edge", f"{best_play['Edge %']:.2%}", 
                 delta=f"{best_play['Edge %']:.2%}")

st.divider()

# 5. Search and Filter Logic
# Move the search and filters to the mobile-friendly sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    search = st.text_input("🔍 Search Player", placeholder="Type a name...")
    st.write("Use this to filter the board for your PrizePicks slips.")

if search:
    df = df[df['Player'].str.contains(search, case=False)]

# 6. Display Table with Heatmap
st.subheader("Market Analysis")
if not df.empty:
    st.table(df.style.background_gradient(subset=['Edge %'], cmap='RdYlGn')
             .format({'Offered Odds': '{:.2f}', 'Fair Win %': '{:.2%}', 'Edge %': '{:.2%}'}))
else:
    st.warning("No players found matching that search.")
