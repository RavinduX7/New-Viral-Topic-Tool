import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# YOUR 4 API KEYS - AUTOMATIC ROTATION SYSTEM
API_KEYS = [
    "AIzaSyDCGBvdrpEkRO4XqCRW04u8JThpkBgZEwE",  # Key 1
    "AIzaSyCsQOpAt_ils7wX4e5cPjCHy381w3RBIxk",  # Key 2
    "AIzaSyAvi5dznmjpopFjRW-OTSnw9Sd-Hj3PjoQ",  # Key 3
    "AIzaSyBYtN2JA8eDsn_zuo6YmVoFizEMerKTtRk",  # Key 4
]

current_key_index = 0

def get_next_api_key():
    """Automatically rotate to next API key when quota exceeded"""
    global current_key_index
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    return API_KEYS[current_key_index]

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Configuration
st.set_page_config(page_title="Multi-Key Viral Finder Pro", layout="wide")
st.title("💰 YouTube Viral Finder - 4 API Keys (40K Units/Day)")
st.markdown("*Automatic key rotation when quota exceeded*")

# Sidebar - Country Selection
st.sidebar.header("🌍 SELECT COUNTRIES")

col1, col2 = st.sidebar.columns(2)
with col1:
    us = st.sidebar.checkbox("🇺🇸 USA", value=True)
    gb = st.sidebar.checkbox("🇬🇧 UK", value=True)
    ca = st.sidebar.checkbox("🇨🇦 Canada", value=True)
    au = st.sidebar.checkbox("🇦🇺 Australia", value=False)
    de = st.sidebar.checkbox("🇩🇪 Germany", value=False)
with col2:
    no = st.sidebar.checkbox("🇳🇴 Norway", value=False)
    se = st.sidebar.checkbox("🇸🇪 Sweden", value=False)
    nl = st.sidebar.checkbox("🇳🇱 Netherlands", value=False)
    fr = st.sidebar.checkbox("🇫🇷 France", value=False)
    jp = st.sidebar.checkbox("🇯🇵 Japan", value=False)

# Build target regions
country_map = {
    "us": "US", "gb": "GB", "ca": "CA", "au": "AU", "de": "DE",
    "no": "NO", "se": "SE", "nl": "NL", "fr": "FR", "jp": "JP"
}

target_regions = []
for key, code in country_map.items():
    if locals()[key]:
        target_regions.append(code)

if target_regions:
    st.sidebar.success(f"✅ {len(target_regions)} countries selected")
else:
    st.sidebar.error("⚠️ Select at least one country!")

st.sidebar.markdown("---")

# Settings
st.sidebar.header("⚙️ SEARCH SETTINGS")
days = st.sidebar.number_input("Days to Search:", min_value=1, max_value=30, value=14)
max_subs = st.sidebar.number_input("Max Subscribers:", min_value=100, max_value=100000, value=15000)
min_views = st.sidebar.number_input("Minimum Views:", min_value=100, max_value=1000000, value=1000)
results_per_keyword = st.sidebar.slider("Results Per Keyword:", 5, 20, 10)

# Keyword Strategy
st.sidebar.subheader("🎯 KEYWORD MODE")
keyword_mode = st.sidebar.selectbox(
    "Choose:",
    ["Economy (10 keywords)", "Balanced (20 keywords)", "Standard (40 keywords)", "Deep (100 keywords)"]
)

# Keywords by mode
if "Economy" in keyword_mode:
    keywords = [
        "retirement planning tips", "medicare explained", "passive income ideas",
        "how to lose weight after 50", "real estate investing beginners",
        "side hustle ideas", "stock market beginners", "senior fitness",
        "make money online", "health tips seniors",
    ]
elif "Balanced" in keyword_mode:
    keywords = [
        "retirement planning tips", "medicare explained", "social security tips",
        "passive income ideas", "how to lose weight after 50", "senior fitness",
        "real estate investing beginners", "dividend investing", "side hustle ideas",
        "make money online", "stock market beginners", "financial planning retirement",
        "health tips seniors", "arthritis pain relief", "gardening tips beginners",
        "home improvement ideas", "cooking for two", "best places to retire",
        "smartphone tips seniors", "world war 2 documentary",
    ]
elif "Standard" in keyword_mode:
    keywords = [
        "retirement planning tips", "medicare explained", "social security tips",
        "how to save for retirement", "passive income ideas", "financial freedom",
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
    ]
else:  # Deep
    keywords = [
        # RETIREMENT & FINANCE (Very High CPM)
        "retirement planning tips", "medicare explained", "social security tips",
        "how to retire early", "retirement income ideas", "best retirement advice",
        "401k withdrawal strategy", "retire on social security", "financial planning retirement",
        "early retirement tips", "retirement budget", "pension planning",
        # MEDICARE & INSURANCE
        "medicare vs medicare advantage", "medicare supplement plans", "medicare part d",
        "health insurance seniors", "long term care insurance", "medicare open enrollment",
        # HEALTH FOR 50+
        "how to lose weight after 50", "health tips for seniors", "senior fitness routine",
        "arthritis pain relief natural", "heart health after 60", "blood pressure control",
        "diabetes management tips", "joint pain relief", "improve memory naturally",
        "healthy aging secrets", "senior nutrition tips", "boost energy after 50",
        # INVESTING & MONEY
        "real estate investing beginners", "passive income ideas 2025", "dividend investing explained",
        "stock market basics", "how to invest in stocks", "best investment strategies",
        "how to invest 100k", "retirement investment tips", "financial independence",
        # MAKE MONEY ONLINE
        "side hustle ideas 2025", "make money online", "work from home jobs",
        "passive income streams", "online business ideas", "affiliate marketing beginners",
        "dropshipping tutorial", "how to make money fast", "earn money online",
        # HOME & LIFESTYLE
        "gardening tips beginners", "vegetable garden tips", "home improvement ideas",
        "container gardening", "raised bed garden", "home organization tips",
        "decluttering tips", "woodworking projects", "DIY home projects",
        # FOOD & COOKING
        "easy dinner recipes", "cooking for two", "quick meal ideas",
        "healthy cooking tips", "budget cooking", "meal prep ideas",
        "comfort food recipes", "traditional recipes",
        # TRAVEL & RETIREMENT LIFESTYLE
        "best places to retire", "RV living full time", "retirement travel tips",
        "budget travel tips", "senior travel", "downsizing your home",
        # RELATIONSHIPS
        "relationship advice over 50", "dating after 50", "grandparenting tips",
        "dealing with adult children", "marriage after 50",
        # HISTORY & EDUCATION
        "world war 2 documentary", "ancient history explained", "american history",
        "cold war documentary", "vietnam war", "historical mysteries",
        # TECHNOLOGY
        "smartphone tips seniors", "ipad for beginners", "avoiding online scams",
        "facebook tutorial seniors", "computer basics", "internet safety",
        # LEGAL & ESTATE
        "estate planning explained", "how to write a will", "power of attorney",
        "living trust vs will", "probate process",
    ]

# Calculate quota usage
estimated_searches = len(keywords) * len(target_regions)
estimated_cost = estimated_searches * 100

st.sidebar.markdown("---")
st.sidebar.subheader("📊 QUOTA CALCULATOR")
st.sidebar.metric("Estimated Cost", f"{estimated_cost:,} units")
st.sidebar.metric("Available", "40,000 units")

if estimated_cost <= 40000:
    remaining = 40000 - estimated_cost
    st.sidebar.success(f"✅ {remaining:,} units remaining")
    st.sidebar.progress(estimated_cost / 40000)
else:
    st.sidebar.error(f"⚠️ Exceeds limit by {estimated_cost - 40000:,} units")

st.sidebar.caption(f"Searches: {len(keywords)} keywords × {len(target_regions)} countries = {estimated_searches}")

# Main Search Button
if st.button("🔍 START SEARCH (Auto Key Rotation)", type="primary", use_container_width=True):
    if not target_regions:
        st.error("⚠️ Select at least one country!")
    else:
        st.info(f"🔑 Using 4 API keys with auto-rotation | 🌍 {len(target_regions)} countries | 🎯 {len(keywords)} keywords")
        
        try:
            start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
            all_results = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            key_status = st.empty()
            
            total_searches = len(keywords) * len(target_regions)
            current_search = 0
            key_switches = 0
            
            for region in target_regions:
                for keyword in keywords:
                    current_search += 1
                    status_text.text(f"[{region}] {keyword} ({current_search}/{total_searches})")
                    key_status.info(f"🔑 Using API Key #{current_key_index + 1}/4")
                    progress_bar.progress(current_search / total_searches)
                    
                    current_key = API_KEYS[current_key_index]
                    
                    search_params = {
                        "part": "snippet",
                        "q": keyword,
                        "type": "video",
                        "order": "date",
                        "publishedAfter": start_date,
                        "maxResults": results_per_keyword,
                        "regionCode": region,
                        "relevanceLanguage": "en",
                        "videoDuration": "medium",
                        "key": current_key,
                    }
                    
                    try:
                        response = requests.get(YOUTUBE_SEARCH_URL, params=search_params, timeout=10)
                        data = response.json()
                        
                        # Handle quota exceeded - auto switch to next key
                        if "error" in data:
                            error_reason = data["error"].get("errors", [{}])[0].get("reason", "")
                            
                            if "quotaExceeded" in error_reason:
                                key_switches += 1
                                st.warning(f"⚠️ Key #{current_key_index + 1} exhausted. Switching to Key #{current_key_index + 2}...")
                                
                                current_key = get_next_api_key()
                                search_params["key"] = current_key
                                
                                # Retry with new key
                                response = requests.get(YOUTUBE_SEARCH_URL, params=search_params, timeout=10)
                                data = response.json()
                                
                                if "error" in data:
                                    st.error(f"❌ All 4 API keys exhausted! Found {len(all_results)} results before limit.")
                                    break
                            else:
                                continue
                        
                        if "items" not in data or not data["items"]:
                            continue
                        
                        videos = data["items"]
                        video_ids = [v["id"]["videoId"] for v in videos if "id" in v and "videoId" in v["id"]]
                        channel_ids = list(set([v["snippet"]["channelId"] for v in videos if "snippet" in v]))
                        
                        if not video_ids:
                            continue
                        
                        # Get stats
                        stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": current_key}
                        stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params, timeout=10)
                        stats_data = stats_response.json()
                        
                        channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": current_key}
                        channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params, timeout=10)
                        channel_data = channel_response.json()
                        
                        if "items" not in stats_data or "items" not in channel_data:
                            continue
                        
                        stats = stats_data["items"]
                        channels = channel_data["items"]
                        
                        for video in videos:
                            video_id = video["id"]["videoId"]
                            stat = next((s for s in stats if s["id"] == video_id), None)
                            if not stat:
                                continue
                            
                            channel_id = video["snippet"]["channelId"]
                            channel = next((c for c in channels if c["id"] == channel_id), None)
                            if not channel:
                                continue
                            
                            views = int(stat["statistics"].get("viewCount", 0))
                            likes = int(stat["statistics"].get("likeCount", 0))
                            comments = int(stat["statistics"].get("commentCount", 0))
                            subs = int(channel["statistics"].get("subscriberCount", 0))
                            
                            if subs <= max_subs and views >= min_views:
                                viral_score = round(views / max(subs, 1), 2)
                                engagement = round(((likes + comments) / views * 100), 2) if views > 0 else 0
                                
                                all_results.append({
                                    "Country": region,
                                    "Keyword": keyword,
                                    "Title": video["snippet"].get("title", "N/A")[:80],
                                    "URL": f"https://www.youtube.com/watch?v={video_id}",
                                    "Views": views,
                                    "Likes": likes,
                                    "Comments": comments,
                                    "Subs": subs,
                                    "Viral Score": viral_score,
                                    "Engagement": f"{engagement}%",
                                    "Published": video["snippet"].get("publishedAt", "")[:10]
                                })
                        
                        time.sleep(0.15)
                        
                    except Exception as e:
                        continue
            
            status_text.empty()
            key_status.empty()
            progress_bar.empty()
            
            if key_switches > 0:
                st.info(f"🔄 Auto-switched API keys {key_switches} times during search")
            
            # DISPLAY RESULTS
            if all_results:
                df = pd.DataFrame(all_results)
                df = df.sort_values("Viral Score", ascending=False)
                
                st.success(f"🎉 **Found {len(df)} viral opportunities across {len(df['Country'].unique())} countries!**")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Videos", len(df))
                with col2:
                    st.metric("Countries", len(df['Country'].unique()))
                with col3:
                    st.metric("Avg Viral Score", f"{df['Viral Score'].mean():.1f}")
                with col4:
                    st.metric("Total Views", f"{df['Views'].sum():,}")
                
                # Country breakdown
                st.subheader("📊 Results by Country")
                country_stats = df.groupby('Country').agg({
                    'Title': 'count',
                    'Views': 'sum',
                    'Viral Score': 'mean'
                }).rename(columns={'Title': 'Videos', 'Views': 'Total Views', 'Viral Score': 'Avg Viral'})
                st.dataframe(country_stats, use_container_width=True)
                
                # Full table
                st.subheader("📋 All Results")
                st.dataframe(df, use_container_width=True, height=400)
                
                # Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Full Report (CSV)",
                    data=csv,
                    file_name=f"viral_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Top 20
                st.subheader("🔥 Top 20 Viral Opportunities")
                for idx, row in df.head(20).iterrows():
                    with st.expander(f"#{idx+1} [{row['Country']}] {row['Title']}"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**Keyword:** {row['Keyword']}")
                            st.write(f"**URL:** {row['URL']}")
                            st.write(f"**Published:** {row['Published']}")
                        with col2:
                            st.metric("Viral Score", f"{row['Viral Score']:.1f}")
                            st.metric("Views", f"{row['Views']:,}")
                            st.metric("Subs", f"{row['Subs']:,}")
                            st.metric("Engagement", row['Engagement'])
            else:
                st.warning("❌ No results found. Try adjusting filters or different countries.")
        
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Sidebar Info
with st.sidebar:
    st.markdown("---")
    st.subheader("🔑 Your API Keys")
    st.success("✅ 4 Keys Active")
    st.metric("Total Daily Quota", "40,000 units")
    st.caption("Each key: 10,000 units")
    st.caption("Resets: Midnight PT (12:30 PM IST)")
    
    st.markdown("---")
    st.subheader("💡 What You Can Do")
    st.markdown("""
    **With 40K units you can:**
    - 100 keywords × 4 countries
    - 40 keywords × 10 countries
    - 20 keywords × 20 countries
    
    **Key rotation is automatic!**
    When one key hits limit, script switches to next key instantly.
    """)
