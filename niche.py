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
st.set_page_config(page_title="Viral Niche Finder Pro", layout="wide")
st.title("🚀 YouTube Automation Viral Niche Finder Pro")
st.markdown("*Find viral opportunities from small channels for fast monetization*")

# Sidebar Configuration
st.sidebar.header("⚙️ Search Settings")
days = st.sidebar.number_input("Days to Search (1-30):", min_value=1, max_value=30, value=7)
max_subs = st.sidebar.number_input("Max Subscribers:", min_value=100, max_value=50000, value=5000)
min_views = st.sidebar.number_input("Minimum Views:", min_value=1000, max_value=1000000, value=10000)
results_per_keyword = st.sidebar.slider("Results Per Keyword:", 3, 10, 5)

# VIRAL AUTOMATION-FOCUSED KEYWORDS (Proven High-Performing Niches)
keywords = [
    # TRUE CRIME & HORROR (HIGH CPM + VIRAL POTENTIAL)
    "True Horror Stories", "Scary True Stories", "Horror Story Animation", 
    "True Crime Stories", "Unsolved Mysteries", "Creepy True Stories",
    "Real Horror Stories", "True Scary Stories Animated", "Mr Nightmare Type Stories",
    "Paranormal Stories", "Ghost Stories Real", "Urban Legends",
    "Creepypasta Stories", "Reddit Scary Stories", "Let's Not Meet Stories",
    
    # CELEBRITY GOSSIP & ENTERTAINMENT (ALWAYS TRENDING)
    "Celebrity Gossip", "Celebrity News Today", "Hollywood Drama",
    "Celebrity Scandals", "Entertainment News", "Celebrity Breakup",
    "Celebrity Couples", "Red Carpet Moments", "Celebrity Fails",
    "Celebrity Transformation", "Celeb Before After", "Celebrity Lifestyle",
    
    # REDDIT STORIES (PROVEN VIRAL NICHE)
    "Reddit Stories", "AITA Stories", "Reddit Cheating Stories",
    "Relationship Reddit Stories", "Entitled Parents Reddit", "Revenge Stories Reddit",
    "Reddit Drama", "Ask Reddit Stories", "Petty Revenge Reddit",
    "Malicious Compliance Reddit", "Reddit Nuclear Revenge", "Reddit Update Stories",
    
    # MYSTERY & CONSPIRACY (HIGH ENGAGEMENT)
    "Unsolved Mysteries 2025", "Conspiracy Theories", "Mystery Solved",
    "Strange Mysteries", "Unexplained Mysteries", "Missing Person Cases",
    "Cold Case Files", "Mystery Documentary", "Conspiracy Theory Explained",
    "Strange Disappearances", "Creepy Mysteries", "Unsolved Cases",
    
    # AI & TECHNOLOGY (TRENDING NOW)
    "AI News", "ChatGPT Tutorial", "AI Tools", "Tech News 2025",
    "AI Automation", "Make Money with AI", "AI vs Human", 
    "Future Technology", "AI Innovation", "Tech Trends 2025",
    
    # MOTIVATION & SUCCESS (HIGH CPM)
    "Motivational Speech", "Success Motivation", "Millionaire Mindset",
    "Motivational Video", "Entrepreneur Motivation", "Life Lessons",
    "Self Improvement", "Discipline Motivation", "Sigma Male Motivation",
    "Success Stories", "Motivational Quotes", "Rise and Grind",
    
    # MAKE MONEY ONLINE (HIGHEST CPM NICHE)
    "Make Money Online", "Passive Income", "Side Hustle Ideas 2025",
    "How to Make Money", "Earn Money Online", "Make Money Fast",
    "Online Business Ideas", "Affiliate Marketing", "Dropshipping Tutorial",
    "Work From Home Jobs", "Make Money as a Teenager", "Easy Money Online",
    
    # AMAZING FACTS & EDUCATIONAL (VIRAL + SHORTS FRIENDLY)
    "Amazing Facts", "Mind Blowing Facts", "Did You Know Facts",
    "Psychology Facts", "Scary Facts", "Interesting Facts",
    "Unknown Facts", "Space Facts", "Ocean Mysteries", "Brain Facts",
    "Human Body Facts", "Science Facts", "History Facts",
    
    # ANIMALS & PETS (ALWAYS VIRAL)
    "Funny Animals", "Cute Animals", "Animal Rescue", "Funny Dogs",
    "Funny Cats", "Animal Fails", "Baby Animals", "Wild Animals",
    "Animal Attacks", "Animal Saves", "Pet Videos", "Dog Rescue Stories",
    
    # LUXURY & LIFESTYLE (HIGH CPM)
    "Luxury Lifestyle", "Rich Lifestyle", "Billionaire Lifestyle",
    "Luxury Cars", "Mansion Tour", "Expensive Things", "Luxury Life",
    "Luxury Homes", "Supercar Videos", "Rich Kids",
    
    # HEALTH & FITNESS (HIGH CPM + ENGAGEMENT)
    "Weight Loss Tips", "Lose Belly Fat", "Fitness Motivation",
    "Health Tips", "How to Lose Weight Fast", "Gym Motivation",
    "Mental Health", "Anxiety Relief", "Sleep Better",
    
    # FOOD & COOKING (VIRAL SHORTS)
    "Food Recipes", "Easy Recipes", "Cooking Hacks", "Street Food",
    "Food Mukbang", "Recipe Videos", "Quick Meals", "Food Challenge",
    
    # HISTORY & DOCUMENTARY (HIGH WATCH TIME)
    "History Documentary", "World War 2", "Ancient History",
    "History Explained", "Historical Mysteries", "Ancient Civilizations",
    
    # RELATIONSHIP & DATING (HIGH ENGAGEMENT)
    "Relationship Advice", "Dating Tips", "Toxic Relationship Signs",
    "Relationship Psychology", "Red Flags Dating", "Relationship Goals",
    
    # LIFE HACKS & DIY (SHORTS VIRAL)
    "Life Hacks", "Useful Life Hacks", "DIY Projects", "Cleaning Hacks",
    "Amazing Life Hacks", "5 Minute Crafts", "Smart Life Hacks",
]

# Fetch Data Button
if st.button("🔍 Find Viral Opportunities", type="primary"):
    try:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_keywords = len(keywords)
        
        for idx, keyword in enumerate(keywords):
            status_text.text(f"Searching: {keyword} ({idx+1}/{total_keywords})")
            progress_bar.progress((idx + 1) / total_keywords)
            
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": results_per_keyword,
                "key": API_KEY,
            }
            
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()
            
            if "items" not in data or not data["items"]:
                continue
            
            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
            channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]
            
            if not video_ids or not channel_ids:
                continue
            
            # Fetch video statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()
            
            if "items" not in stats_data:
                continue
            
            # Fetch channel statistics
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()
            
            if "items" not in channel_data:
                continue
            
            stats = stats_data["items"]
            channels = channel_data["items"]
            
            for video, stat, channel in zip(videos, stats, channels):
                views = int(stat["statistics"].get("viewCount", 0))
                likes = int(stat["statistics"].get("likeCount", 0))
                comments = int(stat["statistics"].get("commentCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))
                
                # ADVANCED FILTERING FOR VIRAL POTENTIAL
                if subs < max_subs and views >= min_views:
                    viral_score = round(views / max(subs, 1), 2)  # Views per subscriber
                    engagement_rate = round(((likes + comments) / views * 100), 2) if views > 0 else 0
                    
                    all_results.append({
                        "Keyword": keyword,
                        "Title": video["snippet"].get("title", "N/A"),
                        "URL": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                        "Views": views,
                        "Likes": likes,
                        "Comments": comments,
                        "Subscribers": subs,
                        "Viral Score": viral_score,
                        "Engagement Rate": f"{engagement_rate}%",
                        "Published": video["snippet"].get("publishedAt", "")[:10]
                    })
            
            time.sleep(0.1)  # Avoid API rate limits
        
        status_text.empty()
        progress_bar.empty()
        
        # Display Results
        if all_results:
            # Sort by Viral Score (highest first)
            df = pd.DataFrame(all_results)
            df = df.sort_values("Viral Score", ascending=False)
            
            st.success(f"🎉 Found {len(df)} VIRAL opportunities!")
            
            # Display Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Videos Found", len(df))
            with col2:
                st.metric("Avg Viral Score", f"{df['Viral Score'].mean():.2f}")
            with col3:
                st.metric("Total Views", f"{df['Views'].sum():,}")
            with col4:
                st.metric("Top Viral Score", f"{df['Viral Score'].max():.2f}")
            
            # Display DataFrame
            st.dataframe(df, use_container_width=True, height=400)
            
            # Download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV Report",
                data=csv,
                file_name=f"viral_opportunities_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
            
            # Top 10 Most Viral Videos
            st.subheader("🔥 Top 10 Most Viral Videos")
            for idx, row in df.head(10).iterrows():
                with st.expander(f"#{idx+1} - {row['Title'][:60]}..."):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Keyword:** {row['Keyword']}")
                        st.write(f"**URL:** {row['URL']}")
                        st.write(f"**Published:** {row['Published']}")
                    with col2:
                        st.metric("Viral Score", row['Viral Score'])
                        st.metric("Views", f"{row['Views']:,}")
                        st.metric("Subscribers", f"{row['Subscribers']:,}")
                        st.metric("Engagement", row['Engagement Rate'])
        else:
            st.warning("❌ No viral opportunities found. Try adjusting your filters.")
    
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        st.info("Check your API key or try reducing the number of searches.")

# Instructions
with st.sidebar:
    st.markdown("---")
    st.subheader("📖 How to Use")
    st.markdown("""
    1. **Set your filters** (Days, Max Subs, Min Views)
    2. **Click 'Find Viral Opportunities'**
    3. **Review Viral Score** - Higher = More viral potential
    4. **Download CSV** for analysis
    5. **Create similar content** in winning niches
    
    **Viral Score = Views ÷ Subscribers**
    
    Higher scores = Small channels with viral content!
    """)
    
    st.markdown("---")
    st.info("💡 **Tip:** Focus on keywords with Viral Score > 50 for best results!")
