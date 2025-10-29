import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# YouTube API Key
API_KEY = "AIzaSyDCGBvdrpEkRO4XqCRW04u8JThpkBgZEwE"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Configuration
st.set_page_config(page_title="Premium Viral Niche Finder", layout="wide")
st.title("💰 YouTube Viral Finder - Global High-CPM Markets")
st.markdown("*Target 30+ premium countries (excluding South Asia)*")

# ===== EXPANDED COUNTRY FILTER =====
st.sidebar.header("🌍 SELECT TARGET COUNTRIES")

# Organize by CPM tier
st.sidebar.markdown("### 🥇 Tier 1: Highest CPM ($7-32)")
col1, col2 = st.sidebar.columns(2)
with col1:
    us = st.sidebar.checkbox("🇺🇸 USA ($32)", value=True, key="us")
    au = st.sidebar.checkbox("🇦🇺 Australia ($36)", value=True, key="au")
    no = st.sidebar.checkbox("🇳🇴 Norway ($20)", value=False, key="no")
    gb = st.sidebar.checkbox("🇬🇧 UK ($13)", value=True, key="gb")
    ca = st.sidebar.checkbox("🇨🇦 Canada ($29)", value=False, key="ca")
with col2:
    ch = st.sidebar.checkbox("🇨🇭 Switzerland ($23)", value=False, key="ch")
    nz = st.sidebar.checkbox("🇳🇿 New Zealand ($28)", value=False, key="nz")
    dk = st.sidebar.checkbox("🇩🇰 Denmark ($17)", value=False, key="dk")
    de = st.sidebar.checkbox("🇩🇪 Germany ($14)", value=False, key="de")

st.sidebar.markdown("### 🥈 Tier 2: Very High CPM ($4-7)")
col3, col4 = st.sidebar.columns(2)
with col3:
    nl = st.sidebar.checkbox("🇳🇱 Netherlands ($18)", value=False, key="nl")
    se = st.sidebar.checkbox("🇸🇪 Sweden ($18)", value=False, key="se")
    be = st.sidebar.checkbox("🇧🇪 Belgium ($20)", value=False, key="be")
    at = st.sidebar.checkbox("🇦🇹 Austria ($11)", value=False, key="at")
    fi = st.sidebar.checkbox("🇫🇮 Finland ($22)", value=False, key="fi")
with col4:
    ie = st.sidebar.checkbox("🇮🇪 Ireland ($8)", value=False, key="ie")
    fr = st.sidebar.checkbox("🇫🇷 France ($10)", value=False, key="fr")
    sg = st.sidebar.checkbox("🇸🇬 Singapore ($9)", value=False, key="sg")
    jp = st.sidebar.checkbox("🇯🇵 Japan ($11)", value=False, key="jp")

st.sidebar.markdown("### 🥉 Tier 3: High CPM ($2-4)")
col5, col6 = st.sidebar.columns(2)
with col5:
    es = st.sidebar.checkbox("🇪🇸 Spain ($8)", value=False, key="es")
    it = st.sidebar.checkbox("🇮🇹 Italy ($8)", value=False, key="it")
    kr = st.sidebar.checkbox("🇰🇷 South Korea ($12)", value=False, key="kr")
    ae = st.sidebar.checkbox("🇦🇪 UAE ($8)", value=False, key="ae")
    il = st.sidebar.checkbox("🇮🇱 Israel ($9)", value=False, key="il")
with col6:
    hk = st.sidebar.checkbox("🇭🇰 Hong Kong ($12)", value=False, key="hk")
    pl = st.sidebar.checkbox("🇵🇱 Poland ($8)", value=False, key="pl")
    cz = st.sidebar.checkbox("🇨🇿 Czech Rep ($7)", value=False, key="cz")
    pt = st.sidebar.checkbox("🇵🇹 Portugal ($11)", value=False, key="pt")

st.sidebar.markdown("### 💵 Tier 4: Medium-High CPM ($1-2)")
col7, col8 = st.sidebar.columns(2)
with col7:
    mx = st.sidebar.checkbox("🇲🇽 Mexico ($8)", value=False, key="mx")
    br = st.sidebar.checkbox("🇧🇷 Brazil ($5)", value=False, key="br")
    sa = st.sidebar.checkbox("🇸🇦 Saudi Arabia ($8)", value=False, key="sa")
    gr = st.sidebar.checkbox("🇬🇷 Greece ($8)", value=False, key="gr")
with col8:
    ro = st.sidebar.checkbox("🇷🇴 Romania ($7)", value=False, key="ro")
    hu = st.sidebar.checkbox("🇭🇺 Hungary ($6)", value=False, key="hu")
    za = st.sidebar.checkbox("🇿🇦 South Africa ($6)", value=False, key="za")

# Build country mapping
country_map = {
    # Tier 1 (Highest CPM)
    "us": ("US", "🇺🇸 USA", "Very High", "$32"),
    "au": ("AU", "🇦🇺 Australia", "Very High", "$36"),
    "no": ("NO", "🇳🇴 Norway", "Very High", "$20"),
    "gb": ("GB", "🇬🇧 UK", "Very High", "$13"),
    "ca": ("CA", "🇨🇦 Canada", "Very High", "$29"),
    "ch": ("CH", "🇨🇭 Switzerland", "Very High", "$23"),
    "nz": ("NZ", "🇳🇿 New Zealand", "Very High", "$28"),
    "dk": ("DK", "🇩🇰 Denmark", "Very High", "$17"),
    "de": ("DE", "🇩🇪 Germany", "High", "$14"),
    # Tier 2 (Very High CPM)
    "nl": ("NL", "🇳🇱 Netherlands", "High", "$18"),
    "se": ("SE", "🇸🇪 Sweden", "High", "$18"),
    "be": ("BE", "🇧🇪 Belgium", "High", "$20"),
    "at": ("AT", "🇦🇹 Austria", "High", "$11"),
    "fi": ("FI", "🇫🇮 Finland", "High", "$22"),
    "ie": ("IE", "🇮🇪 Ireland", "High", "$8"),
    "fr": ("FR", "🇫🇷 France", "High", "$10"),
    "sg": ("SG", "🇸🇬 Singapore", "High", "$9"),
    "jp": ("JP", "🇯🇵 Japan", "High", "$11"),
    # Tier 3 (High CPM)
    "es": ("ES", "🇪🇸 Spain", "Medium-High", "$8"),
    "it": ("IT", "🇮🇹 Italy", "Medium-High", "$8"),
    "kr": ("KR", "🇰🇷 South Korea", "Medium-High", "$12"),
    "ae": ("AE", "🇦🇪 UAE", "Medium-High", "$8"),
    "il": ("IL", "🇮🇱 Israel", "Medium-High", "$9"),
    "hk": ("HK", "🇭🇰 Hong Kong", "Medium-High", "$12"),
    "pl": ("PL", "🇵🇱 Poland", "Medium-High", "$8"),
    "cz": ("CZ", "🇨🇿 Czechia", "Medium-High", "$7"),
    "pt": ("PT", "🇵🇹 Portugal", "Medium-High", "$11"),
    # Tier 4 (Medium-High CPM)
    "mx": ("MX", "🇲🇽 Mexico", "Medium", "$8"),
    "br": ("BR", "🇧🇷 Brazil", "Medium", "$5"),
    "sa": ("SA", "🇸🇦 Saudi Arabia", "Medium", "$8"),
    "gr": ("GR", "🇬🇷 Greece", "Medium", "$8"),
    "ro": ("RO", "🇷🇴 Romania", "Medium", "$7"),
    "hu": ("HU", "🇭🇺 Hungary", "Medium", "$6"),
    "za": ("ZA", "🇿🇦 South Africa", "Medium", "$6"),
}

# Build selected regions list
target_regions = []
selected_countries_display = []
for key, (code, name, tier, cpm) in country_map.items():
    if locals()[key]:  # Check if checkbox is selected
        target_regions.append(code)
        selected_countries_display.append(name)

# Display selected countries
if target_regions:
    st.sidebar.success(f"✅ **Selected {len(target_regions)} countries**")
    with st.sidebar.expander("View Selected Countries"):
        st.write(", ".join(selected_countries_display))
else:
    st.sidebar.error("⚠️ Select at least one country!")

st.sidebar.markdown("---")

# Other Settings
st.sidebar.header("⚙️ Search Settings")
days = st.sidebar.number_input("Days to Search:", min_value=1, max_value=30, value=14)
max_subs = st.sidebar.number_input("Max Subscribers:", min_value=100, max_value=100000, value=15000)
min_views = st.sidebar.number_input("Minimum Views:", min_value=100, max_value=1000000, value=1000)
results_per_keyword = st.sidebar.slider("Results Per Keyword:", 5, 20, 10)

# Search Strategy
st.sidebar.subheader("🎯 Search Strategy")
search_mode = st.sidebar.radio(
    "Choose Mode:",
    ["Fast (20 keywords)", "Balanced (40 keywords)", "Deep (100+ keywords)"]
)

show_debug = st.sidebar.checkbox("Show Debug Info", value=False)

# KEYWORDS (Same as before)
if search_mode == "Fast (20 keywords)":
    keywords = [
        "how to retire early", "retirement planning tips", "best retirement advice",
        "social security tips", "medicare explained", "passive income ideas",
        "real estate investing beginners", "how to lose weight after 50",
        "health tips for seniors", "dividend investing explained",
        "side hustle ideas", "make money online", "stock market beginners",
        "gardening tips beginners", "home improvement ideas",
        "best places to retire", "cooking for two", "senior fitness",
        "financial planning retirement", "downsizing tips",
    ]
elif search_mode == "Balanced (40 keywords)":
    keywords = [
        "how to retire early", "retirement planning tips", "best retirement advice",
        "social security tips", "how to save for retirement", "retirement income ideas",
        "medicare explained", "medicare advantage plans", "financial planning retirement",
        "how to lose weight after 50", "health tips for seniors", "senior fitness",
        "arthritis pain relief", "heart health tips", "healthy aging tips",
        "real estate investing beginners", "passive income ideas", "dividend investing",
        "stock market beginners", "how to invest money", "side hustle ideas",
        "make money online", "financial freedom tips",
        "gardening tips beginners", "vegetable garden tips", "home improvement ideas",
        "best places to retire", "RV living full time", "downsizing your home",
        "cooking for two", "easy dinner recipes", "budget cooking tips",
        "smartphone tips seniors", "avoiding online scams", "world war 2 documentary",
        "american history explained", "ancient civilizations",
    ]
else:  # Deep
    keywords = [
        "how to retire early", "retirement planning tips", "best retirement advice",
        "social security tips 2025", "how to save for retirement", "retirement income ideas",
        "retirement mistakes avoid", "retire on social security", "early retirement tips",
        "medicare explained simply", "medicare vs medicare advantage", "medicare supplement plans",
        "medicare part d plans", "health insurance seniors", "long term care insurance",
        "how to lose weight after 50", "health tips for seniors", "senior fitness routine",
        "arthritis pain relief natural", "heart health after 60", "blood pressure control",
        "diabetes management tips", "joint pain relief", "healthy aging secrets",
        "real estate investing beginners", "passive income ideas 2025", "dividend investing explained",
        "stock market basics", "how to invest in stocks", "best investment strategies",
        "side hustle ideas 2025", "make money online", "work from home jobs",
        "affiliate marketing beginners", "dropshipping tutorial",
        "home improvement ideas", "DIY home projects", "gardening tips beginners",
        "vegetable garden tips", "container gardening", "home organization tips",
        "easy dinner recipes", "cooking for two", "quick meal ideas",
        "best places to retire", "RV living full time", "retirement travel tips",
        "relationship advice over 50", "dating after 50", "grandparenting tips",
        "world war 2 documentary", "ancient history explained", "cold war documentary",
        "smartphone tips seniors", "avoiding online scams", "facebook tutorial seniors",
        "estate planning explained", "how to write a will", "living trust vs will",
        "classic car restoration", "woodworking for beginners", "fishing tips beginners",
    ]

# Main Search Button
if st.button("🔍 SEARCH VIRAL OPPORTUNITIES", type="primary", use_container_width=True):
    if not target_regions:
        st.error("⚠️ **Please select at least one country!**")
    else:
        st.info(f"**🌍 Searching {len(target_regions)} countries:** {', '.join(selected_countries_display[:5])}{'...' if len(selected_countries_display) > 5 else ''}")
        
        try:
            start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
            all_results = []
            total_videos_found = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_searches = len(keywords) * len(target_regions)
            current_search = 0
            
            # Search each country
            for region_code in target_regions:
                # Get country display name
                region_name = next((name for key, (code, name, _, _) in country_map.items() if code == region_code), region_code)
                st.write(f"### 🔎 {region_name}")
                
                for keyword in keywords:
                    current_search += 1
                    status_text.text(f"[{region_name}] {keyword} ({current_search}/{total_searches})")
                    progress_bar.progress(current_search / total_searches)
                    
                    search_params = {
                        "part": "snippet",
                        "q": keyword,
                        "type": "video",
                        "order": "date",
                        "publishedAfter": start_date,
                        "maxResults": results_per_keyword,
                        "regionCode": region_code,
                        "relevanceLanguage": "en",
                        "videoDuration": "medium",
                        "key": API_KEY,
                    }
                    
                    try:
                        response = requests.get(YOUTUBE_SEARCH_URL, params=search_params, timeout=10)
                        data = response.json()
                        
                        if "error" in data:
                            if "quotaExceeded" in str(data.get("error", {})):
                                st.error("⚠️ **API Quota Exceeded!** Reduce countries/keywords.")
                                break
                            continue
                        
                        if "items" not in data or not data["items"]:
                            continue
                        
                        videos = data["items"]
                        total_videos_found += len(videos)
                        
                        video_ids = [v["id"]["videoId"] for v in videos if "id" in v and "videoId" in v["id"]]
                        channel_ids = [v["snippet"]["channelId"] for v in videos if "snippet" in v]
                        
                        if not video_ids:
                            continue
                        
                        # Get statistics
                        stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
                        stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params, timeout=10)
                        stats_data = stats_response.json()
                        
                        channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
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
                                engagement_rate = round(((likes + comments) / views * 100), 2) if views > 0 else 0
                                
                                # Get CPM tier for this country
                                cpm_tier = next((tier for key, (code, _, tier, _) in country_map.items() if code == region_code), "Medium")
                                
                                all_results.append({
                                    "Country": region_name,
                                    "CPM Tier": cpm_tier,
                                    "Keyword": keyword,
                                    "Title": video["snippet"].get("title", "N/A")[:80],
                                    "URL": f"https://www.youtube.com/watch?v={video_id}",
                                    "Views": views,
                                    "Likes": likes,
                                    "Comments": comments,
                                    "Subscribers": subs,
                                    "Viral Score": viral_score,
                                    "Engagement": f"{engagement_rate}%",
                                    "Published": video["snippet"].get("publishedAt", "")[:10]
                                })
                        
                        time.sleep(0.15)
                        
                    except Exception as e:
                        if show_debug:
                            st.write(f"Error: {str(e)}")
            
            status_text.empty()
            progress_bar.empty()
            
            # DISPLAY RESULTS
            if all_results:
                df = pd.DataFrame(all_results)
                df = df.sort_values("Viral Score", ascending=False)
                
                st.success(f"🎉 **Found {len(df)} viral opportunities across {len(df['Country'].unique())} countries!**")
                
                # Metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Total Videos", len(df))
                with col2:
                    st.metric("Countries", len(df['Country'].unique()))
                with col3:
                    st.metric("Avg Viral Score", f"{df['Viral Score'].mean():.1f}")
                with col4:
                    st.metric("Total Views", f"{df['Views'].sum():,}")
                with col5:
                    very_high_cpm = len(df[df['CPM Tier'] == 'Very High'])
                    st.metric("Very High CPM", very_high_cpm)
                
                # Country Breakdown
                st.subheader("📊 Results by Country")
                country_stats = df.groupby(['Country', 'CPM Tier']).agg({
                    'Title': 'count',
                    'Views': 'sum',
                    'Viral Score': 'mean'
                }).rename(columns={'Title': 'Videos', 'Views': 'Total Views', 'Viral Score': 'Avg Viral'})
                st.dataframe(country_stats, use_container_width=True)
                
                # Full Results
                st.subheader("📋 All Results")
                st.dataframe(df, use_container_width=True, height=400)
                
                # Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Full Report (CSV)",
                    data=csv,
                    file_name=f"viral_global_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Top 25 Results
                st.subheader("🔥 Top 25 Viral Opportunities")
                for idx, row in df.head(25).iterrows():
                    with st.expander(f"#{idx+1} [{row['Country']}] {row['Title']}"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**Keyword:** {row['Keyword']}")
                            st.write(f"**URL:** {row['URL']}")
                            st.write(f"**Published:** {row['Published']}")
                        with col2:
                            st.metric("Viral Score", f"{row['Viral Score']:.1f}")
                            st.metric("Views", f"{row['Views']:,}")
                            st.metric("Subs", f"{row['Subscribers']:,}")
                            st.info(f"**{row['CPM Tier']} CPM**")
            else:
                st.warning("❌ No results found.")
                st.info("Try: Fast mode, fewer countries, or lower Min Views to 500")
        
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Sidebar Info
with st.sidebar:
    st.markdown("---")
    st.subheader("💰 CPM Tiers Explained")
    st.markdown("""
    **Very High ($13-36):** USA, Australia, Norway, UK, Canada, Switzerland, NZ, Denmark
    
    **High ($8-22):** Germany, Netherlands, Sweden, Belgium, Austria, Finland, Ireland, France, Singapore, Japan
    
    **Medium-High ($7-12):** Spain, Italy, Korea, UAE, Israel, Hong Kong, Poland, Czechia, Portugal
    
    **Medium ($5-8):** Mexico, Brazil, Saudi Arabia, Greece, Romania, Hungary, South Africa
    """)
    
    st.markdown("---")
    st.info("**🚫 Excluded:** All South Asian countries (India, Pakistan, Bangladesh, Sri Lanka, Nepal)")
    
    st.markdown("---")
    if target_regions:
        estimated_cost = len(keywords) * len(target_regions) * 100
        st.warning(f"⚠️ **API Cost:** ~{estimated_cost:,} units")
        if estimated_cost > 10000:
            st.error("⚠️ Exceeds daily limit! Use Fast mode or fewer countries.")
