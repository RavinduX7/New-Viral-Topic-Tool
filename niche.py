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
st.title("💰 Premium YouTube Automation Finder (High CPM Markets)")
st.markdown("*Target USA, UK, CA, AU, DE viewers with high purchasing power (50+ demographic)*")

# Sidebar Configuration
st.sidebar.header("⚙️ Search Settings")
days = st.sidebar.number_input("Days to Search (1-30):", min_value=1, max_value=30, value=14)
max_subs = st.sidebar.number_input("Max Subscribers:", min_value=100, max_value=100000, value=15000)
min_views = st.sidebar.number_input("Minimum Views:", min_value=100, max_value=1000000, value=1000)
results_per_keyword = st.sidebar.slider("Results Per Keyword:", 3, 10, 5)

# Target Markets Selection
st.sidebar.subheader("🌍 Target Markets")
target_regions = st.sidebar.multiselect(
    "Select Countries (High CPM):",
    ["US", "GB", "CA", "AU", "DE"],
    default=["US", "GB", "CA", "AU", "DE"]
)

show_debug = st.sidebar.checkbox("Show Debug Info", value=False)

# HIGH CPM KEYWORDS TARGETING 50+ DEMOGRAPHIC (High Purchasing Power)
keywords = [
    # RETIREMENT & FINANCE (HIGHEST CPM: $15-30) - Perfect for 50+
    "Retirement Planning", "Retirement Income Strategies", "Social Security Tips",
    "How to Retire Early", "Retirement Savings", "401k Withdrawal Strategies",
    "Pension Planning", "Retirement Budget", "Best Places to Retire",
    "Retirement Advice", "Financial Planning for Retirement", "Retire at 60",
    "Medicare Explained", "Retirement Living", "Downsizing in Retirement",
    "Retirement Investment Strategies", "Tax Planning Retirement", "Estate Planning",
    
    # PERSONAL FINANCE & INVESTING (HIGH CPM: $12-25) - Appeals to Wealth Demographic
    "Personal Finance Tips", "Investment Strategies", "Stock Market Investing",
    "Real Estate Investing", "Passive Income Ideas", "Dividend Investing",
    "Financial Independence", "Wealth Building", "Money Management",
    "Smart Investing", "Financial Advice", "Investment Portfolio",
    
    # HEALTH & WELLNESS FOR SENIORS (HIGH CPM: $8-15) - Huge 50+ Market
    "Health Tips for Seniors", "Healthy Aging", "Senior Fitness",
    "Arthritis Pain Relief", "Heart Health Tips", "Blood Pressure Control",
    "Diabetes Management", "Weight Loss After 50", "Senior Nutrition",
    "Joint Pain Relief", "Memory Improvement", "Brain Health",
    "Senior Wellness", "Aging Well", "Longevity Tips",
    
    # MEDICARE & INSURANCE (VERY HIGH CPM: $20-40) - 50+ Essential Topic
    "Medicare Explained", "Medicare Advantage", "Medicare Supplement",
    "Medicare Part D", "Health Insurance for Seniors", "Life Insurance Over 50",
    "Long Term Care Insurance", "Medicare Open Enrollment",
    
    # REAL ESTATE (HIGH CPM: $10-20) - Appeals to Property Owners
    "Real Estate Tips", "Buying a House", "Selling Your Home",
    "Home Equity", "Reverse Mortgage Explained", "Downsizing Your Home",
    "Real Estate Market", "Property Investment", "Home Buying Guide",
    
    # TECHNOLOGY FOR SENIORS (MEDIUM CPM: $6-12) - Growing Demographic
    "Technology for Seniors", "Smartphone Tutorial", "iPad for Beginners",
    "Facebook for Seniors", "Online Security Tips", "Avoiding Scams",
    "Easy Tech Tips", "Computer Basics", "Internet Safety Seniors",
    
    # COOKING & RECIPES (MEDIUM CPM: $4-8) - Traditional Cooking Appeals to 50+
    "Traditional Recipes", "Classic Cooking", "Comfort Food Recipes",
    "Easy Dinner Recipes", "Healthy Cooking", "Meal Prep for Seniors",
    "Cooking for Two", "Quick Dinner Ideas", "Budget Cooking",
    
    # GARDENING & HOMESTEADING (MEDIUM CPM: $5-10) - Popular with 50+
    "Gardening Tips", "Vegetable Garden", "Backyard Gardening",
    "Container Gardening", "Garden Design", "Homesteading",
    "Raised Bed Garden", "Flower Gardening", "Organic Gardening",
    
    # TRAVEL FOR SENIORS (MEDIUM CPM: $6-12) - Retirees Love Travel
    "Senior Travel Tips", "Best Travel Destinations", "RV Living",
    "Retirement Travel", "Budget Travel", "Travel Over 60",
    "Cruise Travel", "European Travel", "Travel Safety Tips",
    
    # HOME IMPROVEMENT & DIY (MEDIUM CPM: $6-10) - Homeowner Demographic
    "Home Improvement", "DIY Projects", "Home Repair", "Home Renovation",
    "Home Organization", "Woodworking Projects", "Painting Tips",
    
    # LEGAL & ESTATE PLANNING (HIGH CPM: $15-30) - Critical for 50+
    "Estate Planning", "Will and Testament", "Power of Attorney",
    "Living Trust", "Probate Process", "Legal Advice Seniors",
    
    # RELATIONSHIP & FAMILY (MEDIUM CPM: $5-10) - Grandparenting Content
    "Grandparenting Tips", "Family Relationships", "Marriage After 50",
    "Dating Over 50", "Relationship Advice", "Dealing with Adult Children",
    
    # HISTORY & DOCUMENTARIES (MEDIUM CPM: $5-8) - Educational Content for Mature Audience
    "World War 2 Documentary", "History Channel", "Ancient History",
    "American History", "Historical Events", "History Explained",
    "Cold War History", "Vietnam War", "World History",
    
    # NEWS & CURRENT EVENTS (MEDIUM CPM: $4-8) - Engaged Political Demographics
    "Breaking News", "Political News", "Economic News", "World News",
    "Business News", "Financial News", "Current Events",
    
    # CLASSIC CARS & HOBBIES (MEDIUM CPM: $6-12) - Appeals to Male 50+
    "Classic Cars", "Car Restoration", "Vintage Cars", "Muscle Cars",
    "Car Collecting", "Car Shows", "Antique Cars",
    
    # FAITH & SPIRITUALITY (MEDIUM CPM: $5-10) - Strong 50+ Demographic
    "Christian Faith", "Bible Study", "Spiritual Growth", "Prayer",
    "Church Services", "Faith Journey", "Religious Teaching",
]

# Function to check if channel is from target countries
def is_target_region(channel_data):
    """Check if channel is from target countries (approximation via description/content)"""
    # Note: YouTube API doesn't directly filter by uploader country reliably
    # This is a limitation of the API, but we use regionCode to influence results
    return True  # We'll rely on regionCode parameter in search

# Fetch Data Button
if st.button("🔍 Find Premium Opportunities", type="primary"):
    if not target_regions:
        st.error("⚠️ Please select at least one target country!")
    else:
        try:
            start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
            all_results = []
            api_errors = []
            total_videos_found = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_searches = len(keywords) * len(target_regions)
            current_search = 0
            
            # Search for each region
            for region in target_regions:
                st.write(f"🌍 **Searching in: {region}**")
                
                for keyword in keywords:
                    current_search += 1
                    status_text.text(f"Searching: {keyword} in {region} ({current_search}/{total_searches})")
                    progress_bar.progress(current_search / total_searches)
                    
                    search_params = {
                        "part": "snippet",
                        "q": keyword,
                        "type": "video",
                        "order": "date",
                        "publishedAfter": start_date,
                        "maxResults": results_per_keyword,
                        "regionCode": region,  # Target specific country
                        "relevanceLanguage": "en",  # English content
                        "key": API_KEY,
                    }
                    
                    try:
                        response = requests.get(YOUTUBE_SEARCH_URL, params=search_params, timeout=10)
                        data = response.json()
                        
                        if show_debug and current_search <= 3:
                            st.write(f"**Sample API Response for '{keyword}' in {region}:**", data)
                        
                        if "error" in data:
                            api_errors.append(f"{keyword} ({region}): {data['error'].get('message', 'Unknown')}")
                            continue
                        
                        if "items" not in data or not data["items"]:
                            continue
                        
                        videos = data["items"]
                        total_videos_found += len(videos)
                        
                        video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
                        channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]
                        
                        if not video_ids or not channel_ids:
                            continue
                        
                        # Fetch video statistics
                        stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
                        stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params, timeout=10)
                        stats_data = stats_response.json()
                        
                        if "items" not in stats_data:
                            continue
                        
                        # Fetch channel statistics
                        channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
                        channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params, timeout=10)
                        channel_data = channel_response.json()
                        
                        if "items" not in channel_data:
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
                            
                            # APPLY FILTERS
                            if subs <= max_subs and views >= min_views:
                                viral_score = round(views / max(subs, 1), 2)
                                engagement_rate = round(((likes + comments) / views * 100), 2) if views > 0 else 0
                                
                                # Estimate CPM based on keyword category
                                cpm_estimate = "Medium"
                                if any(k in keyword.lower() for k in ["retirement", "medicare", "insurance", "estate", "investment", "finance"]):
                                    cpm_estimate = "Very High ($15-40)"
                                elif any(k in keyword.lower() for k in ["real estate", "health", "legal", "tax"]):
                                    cpm_estimate = "High ($8-20)"
                                else:
                                    cpm_estimate = "Medium ($4-10)"
                                
                                all_results.append({
                                    "Region": region,
                                    "Keyword": keyword,
                                    "Title": video["snippet"].get("title", "N/A"),
                                    "URL": f"https://www.youtube.com/watch?v={video_id}",
                                    "Views": views,
                                    "Likes": likes,
                                    "Comments": comments,
                                    "Subscribers": subs,
                                    "Viral Score": viral_score,
                                    "Engagement": f"{engagement_rate}%",
                                    "Est. CPM": cpm_estimate,
                                    "Published": video["snippet"].get("publishedAt", "")[:10]
                                })
                        
                        time.sleep(0.15)
                        
                    except requests.exceptions.Timeout:
                        api_errors.append(f"{keyword} ({region}): Timeout")
                    except Exception as e:
                        api_errors.append(f"{keyword} ({region}): {str(e)}")
            
            status_text.empty()
            progress_bar.empty()
            
            # Show debug info
            if show_debug:
                st.info(f"📊 **Debug:** Videos fetched: {total_videos_found} | After filtering: {len(all_results)}")
                if api_errors:
                    with st.expander("⚠️ API Errors"):
                        st.write("\n".join(api_errors[:20]))
            
            # Display Results
            if all_results:
                df = pd.DataFrame(all_results)
                df = df.sort_values("Viral Score", ascending=False)
                
                st.success(f"💰 Found {len(df)} PREMIUM opportunities in {', '.join(target_regions)}!")
                
                # Display Key Metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Total Videos", len(df))
                with col2:
                    st.metric("Avg Viral Score", f"{df['Viral Score'].mean():.2f}")
                with col3:
                    st.metric("Total Views", f"{df['Views'].sum():,}")
                with col4:
                    st.metric("Top Score", f"{df['Viral Score'].max():.2f}")
                with col5:
                    very_high_cpm = len(df[df['Est. CPM'].str.contains('Very High', na=False)])
                    st.metric("Very High CPM", very_high_cpm)
                
                # CPM Distribution
                st.subheader("💵 CPM Distribution")
                cpm_counts = df['Est. CPM'].value_counts()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Very High CPM", cpm_counts.get('Very High ($15-40)', 0))
                with col2:
                    st.metric("High CPM", cpm_counts.get('High ($8-20)', 0))
                with col3:
                    st.metric("Medium CPM", cpm_counts.get('Medium ($4-10)', 0))
                
                # Display DataFrame
                st.dataframe(df, use_container_width=True, height=400)
                
                # Download CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Premium Report (CSV)",
                    data=csv,
                    file_name=f"premium_opportunities_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )
                
                # Top 15 Most Viral Videos
                st.subheader("🔥 Top 15 Premium Opportunities")
                for idx, row in df.head(15).iterrows():
                    with st.expander(f"#{idx+1} - {row['Title'][:70]}... ({row['Region']})"):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"**Keyword:** {row['Keyword']}")
                            st.write(f"**URL:** {row['URL']}")
                            st.write(f"**Region:** {row['Region']}")
                            st.write(f"**Published:** {row['Published']}")
                        with col2:
                            st.metric("Viral Score", row['Viral Score'])
                            st.metric("Views", f"{row['Views']:,}")
                            st.metric("Subscribers", f"{row['Subscribers']:,}")
                            st.metric("Engagement", row['Engagement'])
                            st.info(f"**CPM:** {row['Est. CPM']}")
            else:
                st.warning("❌ No opportunities found with current settings.")
                st.info("""
                **💡 Optimization Tips:**
                1. ✅ Increase Days to 21-30
                2. ✅ Lower Min Views to 500
                3. ✅ Increase Max Subs to 25,000
                4. ✅ Try fewer target countries first
                5. ✅ Enable Debug Mode to see API responses
                """)
        
        except Exception as e:
            st.error(f"⚠️ Critical Error: {e}")

# Instructions
with st.sidebar:
    st.markdown("---")
    st.subheader("💡 Strategy Guide")
    st.markdown("""
    **Why This Works:**
    - 50+ viewers = 48% of US consumer spending
    - Higher ad engagement (10%+ better than Gen Z)
    - Premium CPM rates ($15-40 for finance)
    - Loyal, engaged audience
    
    **Best Niches for 50+:**
    1. 🏦 Retirement/Finance (Highest CPM)
    2. 🏥 Health/Medicare (Very High CPM)
    3. 🏠 Real Estate (High CPM)
    4. 👴 Senior Lifestyle (Medium CPM)
    5. 📚 History/Education (Steady views)
    """)
    
    st.markdown("---")
    st.warning(f"⚠️ **Estimated API Cost:** ~{len(keywords) * len(target_regions) * 100:,} units")
    st.caption("You have 10,000 units/day. Optimize by reducing countries or keywords if needed.")
    
    st.markdown("---")
    st.info("🎯 **Pro Tip:** Focus on 'Very High CPM' results for maximum earnings!")
