import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyDCGBvdrpEkRO4XqCRW04u8JThpkBgZEwE"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# Comprehensive List of Keywords Across Multiple Niches
keywords = [
    # RELATIONSHIP & REDDIT STORIES
    "Affair Relationship Stories", "Reddit Update", "Reddit Relationship Advice", "Reddit Relationship", 
    "Reddit Cheating", "AITA Update", "Open Marriage", "Open Relationship", "X BF Caught", 
    "Stories Cheat", "X GF Reddit", "AskReddit Surviving Infidelity", "GurlCan Reddit", 
    "Cheating Story Actually Happened", "Cheating Story Real", "True Cheating Story", 
    "Reddit Cheating Story", "R/Surviving Infidelity", "Surviving Infidelity", 
    "Reddit Marriage", "Wife Cheated I Can't Forgive", "Reddit AP", "Exposed Wife", 
    "Cheat Exposed", "AITA Reddit Stories", "Family Drama Reddit", "Entitled Parents Reddit",
    
    # MOTIVATION & INSPIRATION
    "Motivational Speech", "Best Motivational Video", "Morning Motivation", 
    "Success Motivation", "Gym Motivation", "Study Motivation", "Life Motivation",
    "Motivational Quotes", "Inspiration Daily", "Never Give Up Motivation",
    "Motivational Stories Real Life", "Success Stories", "Millionaire Mindset",
    "Discipline Motivation", "Workout Motivation", "Entrepreneur Motivation",
    "Overcoming Failure", "Rise and Grind", "Motivational Speech for Success",
    "Self Improvement", "Personal Development", "Growth Mindset",
    
    # HEALTH & WELLNESS
    "Weight Loss Tips", "Healthy Diet Plan", "Mental Health Awareness",
    "Anxiety Relief", "Stress Management", "Meditation for Beginners",
    "Yoga for Weight Loss", "Healthy Eating Habits", "Natural Remedies",
    "Immune System Boost", "Sleep Better Tips", "Mental Wellness",
    "Depression Help", "Mindfulness Meditation", "Health and Wellness",
    "Fitness Transformation", "Lose Belly Fat", "Healthy Lifestyle",
    "Nutrition Tips", "Holistic Health", "Wellness Journey",
    
    # ANIMALS & PETS
    "Cute Animals Compilation", "Funny Dog Videos", "Funny Cat Videos",
    "Animal Rescue Stories", "Wildlife Documentary", "Baby Animals Cute",
    "Pet Training Tips", "Dog Training", "Cat Behavior", "Exotic Pets",
    "Animal Facts Amazing", "Wild Animals", "Pet Care Tips",
    "Funny Animal Moments", "Animals Being Derps", "Puppy Videos",
    "Kitten Videos", "Animal Friendships", "Dog Rescue", "Cat Rescue",
    "Amazing Animal Saves", "Wildlife Conservation", "Cute Pets Compilation",
    "Pet Adoption Stories", "Dog Breeds", "Cat Breeds",
    
    # HISTORY
    "History Documentary", "World War 2 Stories", "Ancient Civilizations",
    "History Facts Interesting", "Historical Mysteries", "Ancient Egypt",
    "Roman Empire History", "Medieval History", "Vikings History",
    "World War 1 Documentary", "Cold War History", "Ancient Rome",
    "Historical Figures", "Unsolved Historical Mysteries", "Ancient Greece",
    "History of the World", "American History", "European History",
    "Historical Events", "Ancient History", "Modern History",
    "History Explained", "True History Stories", "Hidden History",
    
    # AMAZING FACTS & TRIVIA
    "Amazing Facts", "Interesting Facts", "Mind Blowing Facts",
    "Unknown Facts", "Did You Know Facts", "Science Facts",
    "Space Facts", "Psychology Facts", "Human Body Facts",
    "Animal Facts", "Ocean Facts", "Brain Facts", "Universe Facts",
    "History Facts", "Geography Facts", "Technology Facts",
    "Random Facts", "Fun Facts", "Weird Facts", "Creepy Facts",
    "Facts You Didn't Know", "Shocking Facts", "True Facts",
    
    # SCIENCE & TECHNOLOGY
    "Science Experiments", "Space Exploration", "Tech News",
    "Artificial Intelligence Explained", "Future Technology",
    "How Things Work", "Quantum Physics", "Space Documentary",
    "NASA Latest", "Tesla Technology", "Robot Technology",
    "Science Explained Simple", "Physics Facts", "Chemistry Experiments",
    
    # MYSTERY & UNEXPLAINED
    "Unsolved Mysteries", "True Crime Stories", "Mystery Documentary",
    "Paranormal Activity", "Ghost Stories Real", "Creepy Stories",
    "Scary True Stories", "Urban Legends", "Conspiracy Theories",
    "Unexplained Mysteries", "Missing Person Cases", "Cold Case Solved",
    
    # FINANCE & BUSINESS
    "Make Money Online", "Passive Income Ideas", "Stock Market Investing",
    "Crypto Trading", "Personal Finance Tips", "Side Hustle Ideas",
    "Get Rich", "Business Ideas", "Financial Freedom",
    "Investing for Beginners", "Real Estate Investing", "Dropshipping Tutorial",
    
    # FOOD & COOKING
    "Easy Recipes", "Cooking Hacks", "Food Mukbang", "Street Food",
    "Baking Recipes", "Quick Meals", "Healthy Recipes", "Food Challenge",
    "Restaurant Style Recipes", "Dessert Recipes", "Vegan Recipes",
    
    # DIY & LIFE HACKS
    "Life Hacks", "DIY Projects", "Home Improvement", "Cleaning Hacks",
    "Organization Ideas", "Crafts DIY", "5 Minute Crafts", "Home Decor DIY",
    
    # EDUCATION & TUTORIALS
    "How To Tutorial", "Learn English", "Math Tricks", "Study Tips",
    "Educational Videos", "Physics Explained", "Chemistry Tutorial",
    "History Lesson", "Science Tutorial", "Language Learning",
    
    # GAMING
    "Gaming Highlights", "Gameplay Walkthrough", "Gaming News",
    "Minecraft Tutorial", "Fortnite Gameplay", "Gaming Tips Tricks",
    
    # TRAVEL & ADVENTURE
    "Travel Vlog", "Best Places to Visit", "Travel Guide",
    "Adventure Travel", "Budget Travel Tips", "World Tour",
    "Hidden Gems Travel", "Solo Travel", "Travel Documentary",
    
    # SPIRITUALITY & PHILOSOPHY
    "Spiritual Awakening", "Philosophy Explained", "Life Lessons",
    "Wisdom Quotes", "Stoicism Philosophy", "Buddhism Teachings",
    "Law of Attraction", "Meditation Guide", "Enlightenment",
    
    # CARS & VEHICLES
    "Car Review", "Luxury Cars", "Classic Cars", "Car Restoration",
    "Supercar Videos", "Car Modification", "Electric Cars"
]

# Fetch Data Button
if st.button("Fetch Data"):
    try:
        # Calculate date range
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        # Iterate over the list of keywords
        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")

            # Define search parameters
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            # Fetch video data
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            # Check if "items" key exists
            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
            channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]

            if not video_ids or not channel_ids:
                st.warning(f"Skipping keyword: {keyword} due to missing video/channel data.")
                continue

            # Fetch video statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            if "items" not in stats_data or not stats_data["items"]:
                st.warning(f"Failed to fetch video statistics for keyword: {keyword}")
                continue

            # Fetch channel statistics
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()

            if "items" not in channel_data or not channel_data["items"]:
                st.warning(f"Failed to fetch channel statistics for keyword: {keyword}")
                continue

            stats = stats_data["items"]
            channels = channel_data["items"]

            # Collect results
            for video, stat, channel in zip(videos, stats, channels):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 3000:  # Only include channels with fewer than 3,000 subscribers
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        # Display results
        if all_results:
            st.success(f"Found {len(all_results)} results across all keywords!")
            for result in all_results:
                st.markdown(
                    f"**Title:** {result['Title']}  \n"
                    f"**Description:** {result['Description']}  \n"
                    f"**URL:** [Watch Video]({result['URL']})  \n"
                    f"**Views:** {result['Views']}  \n"
                    f"**Subscribers:** {result['Subscribers']}"
                )
                st.write("---")
        else:
            st.warning("No results found for channels with fewer than 3,000 subscribers.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
