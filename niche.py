import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# YOUR 8 API KEYS - 80,000 UNITS PER DAY!
API_KEYS = [
    "AIzaSyDCGBvdrpEkRO4XqCRW04u8JThpkBgZEwE",  # Key 1
    "AIzaSyCsQOpAt_ils7wX4e5cPjCHy381w3RBIxk",  # Key 2
    "AIzaSyAvi5dznmjpopFjRW-OTSnw9Sd-Hj3PjoQ",  # Key 3
    "AIzaSyBYtN2JA8eDsn_zuo6YmVoFizEMerKTtRk",  # Key 4
    "AIzaSyB6AEPfRsT-jb9MwbgYdc9njQ0gbieg5js",  # Key 5
    "AIzaSyCHFiWoWsrR7qrfH5LIPUsXlFA4ZGydh_k",  # Key 6
    "AIzaSyDS1aGa05f-nnVTQJB2GOyNIl9rxy5yaPs",  # Key 7
    "AIzaSyCmszd5sD12hez1LxO2STexfAe9qOSsOV0",  # Key 8
]

current_key_index = 0
exhausted_keys = set()

def get_next_api_key():
    """Automatically rotate to next available API key"""
    global current_key_index
    attempts = 0
    
    while attempts < len(API_KEYS):
        current_key_index = (current_key_index + 1) % len(API_KEYS)
        if current_key_index not in exhausted_keys:
            return API_KEYS[current_key_index]
        attempts += 1
    
    return None

def test_api_key(key):
    """Test if API key has quota remaining"""
    try:
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={"part": "snippet", "q": "test", "type": "video", "maxResults": 1, "key": key},
            timeout=5
        )
        data = response.json()
        
        if "error" in data:
            if "quotaExceeded" in str(data["error"]):
                return False, "Quota Exceeded"
            return False, data["error"].get("message", "Error")
        return True, "Active"
    except:
        return False, "Connection Error"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit Configuration
st.set_page_config(page_title="Ultimate Viral Finder - 8 Keys", layout="wide")
st.title("🚀 YouTube Viral Finder Pro - 8 API Keys (80K Units/Day)")
st.markdown("*Professional-grade tool with automatic key rotation*")

# API Key Health Check
st.subheader("🔑 API Key Status Monitor")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Check All Keys Health", use_container_width=True):
        with st.spinner("Testing 8 API keys..."):
            key_status = []
            active_count = 0
            
            for idx, key in enumerate(API_KEYS):
                is_active, message = test_api_key(key)
                key_status.append({
                    "Key": f"#{idx+1}",
                    "Preview": f"{key[:15]}...{key[-8:]}",
                    "Status": "✅ Active" if is_active else f"❌ {message}",
                })
                
                if is_active:
                    active_count += 1
                else:
                    exhausted_keys.add(idx)
            
            st.dataframe(pd.DataFrame(key_status), use_container_width=True)
            
            if active_count > 0:
                st.success(f"✅ {active_count}/8 keys active | ~{active_count * 10000:,} units available")
            else:
                st.error("❌ All keys exhausted. Reset at 12:30 PM IST tomorrow.")

with col2:
    st.metric("Total Keys", "8", help="8 × 10,000 = 80,000 units/day")
with col3:
    st.metric("Daily Capacity", "80,000 units", help="Resets midnight PT (12:30 PM IST)")

st.markdown("---")

# Sidebar - Country Selection
st.sidebar.header("🌍 TARGET COUNTRIES")
st.sidebar.caption("Select multiple countries for broader search")

# Tier 1 Countries
st.sidebar.markdown("**🥇 Tier 1 (Highest CPM)**")
col1, col2 = st.sidebar.columns(2)
with col1:
    us = st.sidebar.checkbox("🇺🇸 USA ($32)", value=True)
    au = st.sidebar.checkbox("🇦🇺 Australia ($36)", value=True)
    gb = st.sidebar.checkbox("🇬🇧 UK ($13)", value=True)
with col2:
    ca = st.sidebar.checkbox("🇨🇦 Canada ($29)", value=False)
    no = st.sidebar.checkbox("🇳🇴 Norway ($20)", value=False)
    ch = st.sidebar.checkbox("🇨🇭 Switzerland ($23)", value=False)

# Tier 2 Countries
st.sidebar.markdown("**🥈 Tier 2 (High CPM)**")
col3, col4 = st.sidebar.columns(2)
with col3:
    de = st.sidebar.checkbox("🇩🇪 Germany ($14)", value=False)
    nl = st.sidebar.checkbox("🇳🇱 Netherlands ($18)", value=False)
    se = st.sidebar.checkbox("🇸🇪 Sweden ($18)", value=False)
with col4:
    jp = st.sidebar.checkbox("🇯🇵 Japan ($11)", value=False)
    fr = st.sidebar.checkbox("🇫🇷 France ($10)", value=False)
    sg = st.sidebar.checkbox("🇸🇬 Singapore ($9)", value=False)

# Build target regions
country_map = {
    "us": "US", "au": "AU", "gb": "GB", "ca": "CA", "no": "NO", "ch": "CH",
    "de": "DE", "nl": "NL", "se": "SE", "jp": "JP", "fr": "FR", "sg": "SG"
}

target_regions = []
for key, code in country_map.items():
    if locals()[key]:
        target_regions.append(code)

if target_regions:
    st.sidebar.success(f"✅ {len(target_regions)} countries selected")
else:
    st.sidebar.error("⚠️ Select at least 1 country!")

st.sidebar.markdown("---")

# Search Settings
st.sidebar.header("⚙️ SEARCH SETTINGS")
days = st.sidebar.number_input("Days to Search:", min_value=1, max_value=30, value=14, help="Videos published in last X days")
max_subs = st.sidebar.number_input("Max Subscribers:", min_value=100, max_value=100000, value=15000, help="Filter channels under this size")
min_views = st.sidebar.number_input("Minimum Views:", min_value=100, max_value=1000000, value=1000, help="Filter videos with min views")
results_per_keyword = st.sidebar.slider("Results Per Keyword:", 5, 20, 10, help="Videos to fetch per keyword per country")

# Keyword Mode Selection
st.sidebar.subheader("🎯 KEYWORD STRATEGY")
keyword_mode = st.sidebar.selectbox(
    "Select Mode:",
    [
        "⚡ Fast (10 keywords - 1K units)",
        "⚖️ Balanced (25 keywords - 2.5K units)",
        "🔥 Standard (50 keywords - 5K units)",
        "💎 Deep (100 keywords - 10K units)",
        "🚀 Ultra-Deep (150+ keywords - 15K units)"
    ]
)

# Keyword lists by mode
if "Fast" in keyword_mode:
    keywords = [
        "retirement planning tips", "medicare explained", "passive income ideas",
        "how to lose weight after 50", "real estate investing beginners",
        "side hustle ideas", "stock market beginners", "make money online",
        "health tips seniors", "senior fitness",
    ]
elif "Balanced" in keyword_mode:
    keywords = [
        "retirement planning tips", "medicare explained", "social security tips",
        "passive income ideas", "financial freedom", "how to lose weight after 50",
        "senior fitness", "real estate investing beginners", "dividend investing",
        "side hustle ideas", "make money online", "stock market beginners",
        "financial planning retirement", "health tips seniors", "arthritis pain relief",
        "gardening tips beginners", "home improvement ideas", "cooking for two",
        "best places to retire", "smartphone tips seniors", "world war 2 documentary",
        "estate planning explained", "RV living tips", "budget travel seniors",
        "downsizing your home",
    ]
elif "Standard" in keyword_mode:
    keywords = [
        "retirement planning tips", "medicare explained", "social security tips",
        "how to retire early", "passive income ideas", "financial freedom",
        "how to lose weight after 50", "senior fitness", "heart health tips",
        "real estate investing beginners", "dividend investing", "stock market basics",
        "side hustle ideas", "make money online", "work from home jobs",
        "financial planning retirement", "retirement income ideas", "early retirement",
        "health tips seniors", "arthritis pain relief", "healthy aging",
        "gardening tips beginners", "vegetable garden tips", "home improvement",
        "cooking for two", "easy dinner recipes", "budget cooking",
        "best places to retire", "RV living", "downsizing tips",
        "smartphone tips seniors", "avoiding scams", "world war 2 documentary",
        "american history", "dating after 50", "grandparenting tips",
        "estate planning", "how to invest", "classic cars",
        "blood pressure control", "diabetes management", "memory improvement",
        "medicare advantage", "401k withdrawal", "investment strategies",
        "home organization", "travel over 60", "senior technology",
        "joint pain relief", "nutrition for seniors",
    ]
elif "Deep" in keyword_mode:
    keywords = [
        # RETIREMENT & FINANCE (20)
        "retirement planning tips", "medicare explained", "social security tips",
        "how to retire early", "retirement income ideas", "financial planning retirement",
        "401k withdrawal strategy", "pension planning", "early retirement",
        "retire on social security", "retirement budget", "best retirement calculator",
        "retirement mistakes avoid", "how much to retire", "retirement savings tips",
        "medicare advantage plans", "medicare supplement", "retirement investment",
        "estate planning explained", "how to write a will",
        
        # HEALTH FOR 50+ (20)
        "how to lose weight after 50", "health tips seniors", "senior fitness",
        "arthritis pain relief", "heart health after 60", "blood pressure control",
        "diabetes management", "joint pain relief", "improve memory naturally",
        "healthy aging secrets", "senior nutrition", "boost energy after 50",
        "weight loss tips seniors", "exercise for seniors", "healthy eating over 50",
        "sleep better tips", "stress management seniors", "mental health seniors",
        "vision health tips", "bone health seniors",
        
        # INVESTING & MONEY (20)
        "real estate investing beginners", "passive income ideas 2025", "dividend investing",
        "stock market basics", "how to invest money", "investment strategies",
        "side hustle ideas", "make money online", "work from home jobs",
        "financial freedom tips", "how to invest 100k", "rental property investing",
        "stock trading beginners", "cryptocurrency investing", "index fund investing",
        "retirement portfolio", "passive income streams", "online business ideas",
        "affiliate marketing tips", "dropshipping guide",
        
        # LIFESTYLE & HOME (20)
        "gardening tips beginners", "vegetable garden", "home improvement",
        "container gardening", "raised bed garden", "home organization",
        "decluttering tips", "woodworking projects", "DIY home projects",
        "cooking for two", "easy dinner recipes", "budget cooking",
        "best places to retire", "RV living", "downsizing your home",
        "travel over 60", "budget travel tips", "classic car restoration",
        "fishing tips beginners", "golf tips",
        
        # TECHNOLOGY & EDUCATION (20)
        "smartphone tips seniors", "ipad for beginners", "avoiding online scams",
        "facebook tutorial", "computer basics", "internet safety",
        "world war 2 documentary", "american history", "ancient civilizations",
        "cold war history", "historical mysteries", "vietnam war",
        "dating after 50", "grandparenting tips", "relationship advice over 50",
        "dealing with adult children", "marriage after 50", "family relationships",
        "senior dating tips", "widowhood support",
    ]
else:  # Ultra-Deep
    keywords = [
        # All Deep keywords PLUS:
        "retirement planning tips", "medicare explained", "social security tips",
        "how to retire early", "retirement income ideas", "financial planning retirement",
        "401k withdrawal strategy", "pension planning", "early retirement",
        "retire on social security", "retirement budget", "best retirement calculator",
        "how to lose weight after 50", "health tips seniors", "senior fitness",
        "arthritis pain relief", "heart health after 60", "blood pressure control",
        "real estate investing beginners", "passive income ideas 2025", "dividend investing",
        "stock market basics", "side hustle ideas", "make money online",
        "gardening tips beginners", "vegetable garden", "home improvement",
        "cooking for two", "best places to retire", "RV living",
        "smartphone tips seniors", "avoiding online scams", "world war 2 documentary",
        "estate planning", "power of attorney", "living trust explained",
        "probate process", "inheritance tax", "medicare part d",
        "long term care insurance", "life insurance over 50", "health insurance seniors",
        "diabetes type 2 management", "cholesterol control", "osteoporosis prevention",
        "REITs investing", "bond investing", "ETF investing",
        "rental income", "house flipping", "property management",
        "organic gardening", "composting tips", "raised bed designs",
        "slow cooker recipes", "air fryer recipes", "keto diet over 50",
        "mediterranean diet", "anti inflammatory diet", "gut health",
        "yoga for seniors", "tai chi benefits", "water aerobics",
        "cruise
