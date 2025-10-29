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
max_subs = st.sidebar.number_input("Max Subscribers:", min_value=100, max_value=100000, value=10000)
min_views = st.sidebar.number_input("Minimum Views:", min_value=100, max_value=1000000, value=1000)  # LOWERED DEFAULT
results_per_keyword = st.sidebar.slider("Results Per Keyword:", 3, 10, 5)
show_debug = st.sidebar.checkbox("Show Debug Info", value=False)

# VIRAL AUTOMATION-FOCUSED KEYWORDS
keywords = [
    # TRUE CRIME & HORROR
    "True Horror Stories", "Scary True Stories", "Horror Story Animation", 
    "True Crime Stories", "Unsolved Mysteries", "Creepy True Stories",
    "Real Horror Stories", "Paranormal Stories", "Ghost Stories Real",
    
    # CELEBRITY GOSSIP
    "Celebrity Gossip", "Celebrity News Today", "Hollywood Drama",
    "Celebrity Scandals", "Entertainment News", "Celebrity Breakup",
    
    # REDDIT STORIES
    "Reddit Stories", "AITA Stories", "Reddit Cheating Stories",
    "Relationship Reddit Stories", "Entitled Parents Reddit", "Revenge Stories Reddit",
    "Reddit Drama", "Ask Reddit Stories", "Petty Revenge Reddit",
    
    # MYSTERY & CONSPIRACY
    "Unsolved Mysteries", "Conspiracy Theories", "Mystery Solved",
    "Strange Mysteries", "Unexplained Mysteries", "Missing Person Cases",
    
    # AI & TECHNOLOGY
    "AI News", "ChatGPT Tutorial", "AI Tools", "Tech News 2025",
    "AI Automation", "Make Money with AI", "Future Technology",
    
    # MOTIVATION & SUCCESS
    "Motivational Speech", "Success Motivation", "Millionaire Mindset",
    "Motivational Video", "Entrepreneur Motivation", "Life Lessons",
    
    # MAKE MONEY ONLINE
    "Make Money Online", "Passive Income", "Side Hustle Ideas",
    "How to Make Money", "Earn Money Online", "Online Business Ideas",
    
    # AMAZING FACTS
    "Amazing Facts", "Mind Blowing Facts", "Did You Know Facts",
    "Psychology Facts", "Interesting Facts", "Space Facts",
    
    # ANIMALS & PETS
    "Funny Animals", "Cute Animals", "Animal Rescue", "Funny Dogs",
    "Funny Cats", "Baby Animals", "Wild Animals",
    
    # LUXURY LIFESTYLE
    "Luxury Lifestyle", "Rich Lifestyle", "Billionaire Lifestyle",
    "Luxury Cars", "Mansion Tour", "Expensive Things",
    
    # HEALTH & FITNESS
    "Weight Loss Tips", "Lose Belly Fat", "Fitness Motivation",
    "Health Tips", "Mental Health", "Gym Motivation",
    
    # FOOD
    "Food Recipes", "Easy Recipes", "Cooking Hacks", "Street Food",
    
    # HISTORY
    "History Documentary", "World War 2", "Ancient History",
    
    # RELATIONSHIP
    "Relationship Advice", "Dating Tips", "Toxic Relationship Signs",
    
    # LIFE HACKS
    "Life Hacks", "Useful Life Hacks", "DIY Projects", "Cleaning Hacks",
]

# Fetch Data Button
if st.button("🔍 Find Viral Opportunities", type="primary"):
    try:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []
        api_errors = []
        total_videos_found = 0
        
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
                "order": "date",  # CHANGED FROM viewCount (it's broken in API)
                "publishedAfter": start_date,
                "maxResults": results_per_keyword,
                "key": API_KEY,
            }
            
            try:
                response = requests.get(YOUTUBE_SEARCH_URL, params=search_params, timeout=10)
                data = response.json()
                
                # DEBUG: Show API response
                if show_debug:
                    st.write(f"**API Response for '{keyword}':**", data)
                
                # Check for API errors
                if "error" in data:
                    api_errors.append(f"{keyword}: {data['error'].get('message', 'Unknown error')}")
                    continue
                
                if "items" not in data or not data["items"]:
                    if show_debug:
                        st.warning(f"No items returned for: {keyword}")
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
                
                # Match videos with their stats and channels
                for video in videos:
                    video_id = video["id"]["videoId"]
                    
                    # Find matching stats
                    stat = next((s for s in stats if s["id"] == video_id), None)
                    if not stat:
                        continue
                    
                    # Find matching channel
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
                        
                        all_results.append({
                            "Keyword": keyword,
                            "Title": video["snippet"].get("title", "N/A"),
                            "URL": f"https://www.youtube.com/watch?v={video_id}",
                            "Views": views,
                            "Likes": likes,
                            "Comments": comments,
                            "Subscribers": subs,
                            "Viral Score": viral_score,
                            "Engagement Rate": f"{engagement_rate}%",
                            "Published": video["snippet"].get("publishedAt", "")[:10]
                        })
                
                time.sleep(0.2)  # Avoid API rate limits
                
            except requests.exceptions.Timeout:
                api_errors.append(f"{keyword}: Request timeout")
            except Exception as e:
                api_errors.append(f"{keyword}: {str(e)}")
        
        status_text.empty()
        progress_bar.empty()
        
        # Show debug info
        if show_debug:
            st.info(f"📊 **Debug Info:**\n- Total videos fetched: {total_videos_found}\n- Videos after filtering: {len(all_results)}")
            if api_errors:
                st.error(f"⚠️ **API Errors ({len(api_errors)}):**\n" + "\n".join(api_errors[:10]))
        
        # Display Results
        if all_results:
            df = pd.DataFrame(all_results)
            df = df.sort_values("Viral Score", ascending=False)
            
            st.success(f"🎉 Found {len(df)} VIRAL opportunities!")
            
            # Display Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Videos", len(df))
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
                file_name=f"viral_opportunities_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
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
            st.warning("❌ No viral opportunities found with current filters.")
            st.info("""
            **💡 Try these solutions:**
            1. ✅ **Lower Min Views** to 500 or 1,000
            2. ✅ **Increase Max Subscribers** to 20,000+
            3. ✅ **Increase Days** to 14-30 days
            4. ✅ **Enable Debug Mode** to see what's being returned
            5. ✅ Check your API quota usage: https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas
            """)
            
            if show_debug:
                st.write(f"**Total videos fetched before filtering:** {total_videos_found}")
    
    except Exception as e:
        st.error(f"⚠️ Critical Error: {e}")
        st.info("Check your API key or network connection.")

# Instructions
with st.sidebar:
    st.markdown("---")
    st.subheader("📖 Quick Start")
    st.markdown("""
    **Recommended Settings:**
    - Days: 7-14
    - Max Subs: 10,000
    - Min Views: 1,000
    - Results: 5 per keyword
    
    **Viral Score Meaning:**
    - 50+ = Very viral
    - 20-50 = Good potential
    - 10-20 = Decent
    - <10 = Low viral potential
    """)
    
    st.markdown("---")
    st.warning("⚠️ **API Quota:** Search costs 100 units each. You have 10,000 units/day.")
    st.info(f"**Current Search Cost:** ~{len(keywords) * 100} units")
