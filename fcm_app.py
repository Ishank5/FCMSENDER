import streamlit as st
import firebase_admin
from firebase_admin import credentials, messaging, firestore
import json
from datetime import datetime
import random

# Load service account key from Streamlit secrets
try:
    service_account_key = json.loads(st.secrets["firebase"]["service_account_key"])
except Exception as e:
    st.error("❌ Firebase credentials not found in secrets. Please add them in Streamlit Cloud settings.")
    st.stop()

LOVELY_TITLES = [
    "💕 Sweet Reminder",
    "🌹 Just for You",
    "✨ Thinking of You",
    "💖 Love Note",
    "🌙 Moon & Stars",
    "☀️ Sunshine",
    "💫 Special Message",
    "🦋 Beautiful Soul",
    "🌸 My Precious Flower",
    "🍯 My Sweet Honeybee",
    "🎀 Wrapped in Love",
    "🌼 Morning Bloom",
    "🍫 My Sweet Treat",
    "🌊 My Calm Ocean",
    "🕊️ Peace of My Heart",
    "🌈 My Rainbow",
    "🔥 My Spark",
    "💎 My Gem",
    "🍓 Berry Sweet",
    "🎶 My Melody",
    "📖 My Favorite Story",
    "🍒 Cherry on Top",
    "💐 My Bouquet of Joy",
    "🦄 My Magic",
    "🥰 My Angel",
    "👑 My Queen",
    "💍 Forever Promise",
    "🧸 My Teddy Hug",
    "🌻 My Sunshine Bloom",
    "🍀 My Lucky Charm",
    "⭐ My Guiding Star",
    "💌 Heart Whisper",
    "🎇 Fireworks of Love",
    "🛶 My Safe Harbor",
    "☕ My Cozy Cup",
    "🥀 My Rose",
    "🍦 My Sweet Scoop",
    "🐇 My Soft Bunny",
    "🌒 To My Moon",
    "☁️ My Fluffy Cloud",
    "🐚 My Ocean Pearl",
    "🦢 Grace of My Life",
    "🎂 My Sweet Slice",
    "🍭 Candy Heart",
    "🥧 My Comfort Pie",
    "🍁 My Autumn Leaf",
    "🌷 My Tulip Smile",
    "🐞 My Little Ladybug",
    "💫 My Galaxy",
    "🌟 My Shooting Star",
    "🐱 My Kitty Love",
    "🎨 My Masterpiece",
    "🪄 My Magic Spell",
    "💃 My Dancing Queen",
    "🕊️ My Dove",
    "🍉 My Summer Sweet",
    "🥂 My Celebration",
    "🏰 My Fairytale",
    "🛏️ My Sweet Dream",
    "🍪 My Cookie Love",
    "📸 My Favorite Picture",
    "🧩 My Missing Piece",
    "🎧 My Favorite Song",
    "🍋 My Sweet Zest",
    "🎐 My Wind Chime",
    "🐝 My Busy Bee",
    "🌹 My Red Rose",
    "🥀 My Soft Petal",
    "🪞 My Reflection",
    "🎇 Spark in My Night",
    "🍎 My Apple Heart",
    "🧸 Hug in a Note",
    "🫧 Bubble of Love",
    "🪽 Angel Whisper",
    "🍯 Honey Drop",
    "🕯️ My Candle Light",
    "🌌 My Universe",
    "🏵️ Blooming Heart",
    "🧁 Cupcake Kiss",
    "🍂 Golden Leaf",
    "🦋 My Butterfly",
    "🍓 Strawberry Hug",
    "🎈 Balloon of Joy",
    "🌿 Fresh Breeze",
    "🐚 Ocean Whisper",
    "🦙 Cuddle Cloud",
    "🌸 Cherry Blossom",
    "🪐 Orbiting Love",
    "🌊 Wave of Love",
    "🎀 Ribboned Heart",
    "🧡 Warm Glow",
    "💜 Violet Dream",
    "💛 Golden Smile",
    "🤍 Pure Light",
    "💗 Heartbeat Song",
    "🥹 Soft Smile",
    "🫶 Soul Hug",
    "🌷 Garden of Us"
]

LOVELY_MESSAGES = [
    "With you, life feels like poetry in motion.",
    "Your smile is my favorite notification.",
    "Every moment with you is a treasure.",
    "You make ordinary days feel extraordinary.",
    "My heart beats in rhythm with yours.",
    "You're the reason my world is brighter.",
    "In your eyes, I found my home.",
    "Your love is my favorite adventure.",
    "You're my today and all of my tomorrows.",
    "Distance means nothing when you mean everything.",
    "Your happiness is my favorite sound.",
    "You're the missing piece I never knew I needed.",
    "Your laughter is my favorite melody.",
    "With you, even silence feels sweet.",
    "Every sunrise feels warmer with you in my heart.",
    "You make my world bloom like spring.",
    "Your love paints my sky with colors.",
    "Holding your hand feels like home.",
    "Your voice is my daily comfort.",
    "You’re my softest thought before sleep.",
    "Every text from you is a hug in words.",
    "Your name is my favorite prayer.",
    "You’re my forever favorite hello.",
    "Every memory with you is a keepsake.",
    "You are the spark in my quiet days.",
    "My heart smiles every time I see you.",
    "You are my sweetest serendipity.",
    "You make time stop and fly all at once.",
    "Your soul is the most beautiful art.",
    "Being with you feels like a fairytale.",
    "Your hugs are my safe place.",
    "Every moment apart only deepens my love.",
    "Your touch lingers like stardust.",
    "You are the dream I don’t want to wake up from.",
    "Your kindness melts me every time.",
    "You make love feel so simple and pure.",
    "Your eyes hold galaxies I could get lost in.",
    "Every heartbeat whispers your name.",
    "I find joy just knowing you exist.",
    "Your smile lights up my darkest days.",
    "With you, every road feels right.",
    "Your love is my gentle anchor.",
    "I love the way your soul hugs mine.",
    "Your warmth is my favorite season.",
    "Every kiss feels like magic.",
    "You make my heart dance endlessly.",
    "Your love is my greatest gift.",
    "Every thought of you is a sweet escape.",
    "You’re my reason to believe in forever.",
    "With you, love feels effortless.",
    "Your embrace is my favorite destination.",
    "Your words heal me like soft rain.",
    "Every glance from you makes me blush.",
    "You’re the glow in my universe.",
    "My day begins and ends with you in mind.",
    "You make me feel loved in every way.",
    "Your presence is the calm in my storm.",
    "Every heartbeat feels like a poem for you.",
    "You’re the sweetest chapter of my story.",
    "Your love is my compass in life.",
    "Every whisper of yours is a lullaby.",
    "You’re my safe haven and adventure at once.",
    "Every smile from you feels like sunshine.",
    "Your heart is the home I was searching for.",
    "You make ordinary words sound like love songs.",
    "Every second with you feels like forever.",
    "You are my sweetest addiction.",
    "You make love feel brand new every day.",
    "Every dream of mine has your face in it.",
    "Your soul shines brighter than any star.",
    "I’m happiest when I’m loving you.",
    "You turn the simplest moments magical.",
    "Every hug is a promise of forever.",
    "Your laughter is the music of my heart.",
    "I fall for you more every single day.",
    "Your kindness is my favorite language.",
    "Every “I love you” feels brand new with you.",
    "You are my endless sunshine.",
    "You make my heart sing softly.",
    "Every message from you feels like a gift.",
    "You are the poem I never stop writing.",
    "My heart dances only for you.",
    "Every breath feels fuller with you.",
    "You are my sweetest muse.",
    "With you, life is painted in love.",
    "Every time I miss you, I smile instead.",
    "You’re the hug my soul craves.",
    "Every dream is sweeter with you in it.",
    "You are my heart’s favorite melody.",
    "With you, forever feels too short.",
    "Every kiss is a story I cherish.",
    "You are the starlight in my midnight sky.",
    "Every thought of you feels like sunshine.",
    "You are my miracle in everyday life.",
    "With you, love feels like breathing.",
    "You are the most beautiful part of me."
]


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_key)
            firebase_admin.initialize_app(cred)
        return True
    except Exception as e:
        st.error(f"Firebase initialization failed: {str(e)}")
        return False

def store_message_in_firestore(title, message):
    """Store message in Firestore collection"""
    try:
        db = firestore.client()
        now = datetime.now()
        
        # Create document data
        doc_data = {
            'date': now.strftime('%Y-%m-%d'),
            'message': f"{title} - {message}",
            'timestamp': now
        }
        
        # Add to collection with auto ID
        doc_ref = db.collection('love_messages').document()
        doc_ref.set(doc_data)
        
        return True, doc_ref.id
    except Exception as e:
        return False, str(e)

def send_fcm_message(title, body, device_token, custom_data=None):
    """Send FCM message with given title and body"""
    try:
        # Store message in Firestore first
        store_success, doc_id = store_message_in_firestore(title, body)
        
        # Prepare custom data
        data = custom_data or {}
        data['timestamp'] = str(datetime.now())
        
        # Create the message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    channel_id='high_importance_channel',
                    priority='max',
                    sound='default'
                )
            ),
            token=device_token,
        )
        
        # Send the message
        response = messaging.send(message)
        return True, response, store_success, doc_id
        
    except Exception as e:
        return False, str(e), False, None

# Hardcoded FCM tokens
RECIPIENT_TOKENS = {
    "Shreya": "fqlrHoQJQ-2DdqZ6NUbxYR:APA91bGUUpP9kIfYSDgL7Xfb08wVT_Yg2wjnok6VYL1kDd5mz4TV8Am69wl94aZ0GkMGSVZybQTi_TZWJqpfwY7tcWBd3v1KneNvFlsKXByruiQetv7HM1w",
    "Ishank": "cdG8vZTET0eEkRAN-dd-8S:APA91bEJ3QzYgJe8FmplUByTl-VWoXaorMKRmHbjNXwXZXBp24mPKm6osqr8O4SUXyKY9ncoGzaX2DfTEq72PN4r3SCs-8E8rf3HTGHDWePmR4RscYrZBw8"
}

def main():
    st.title("🔔 FCM Message Sender")
    st.markdown("Send Firebase Cloud Messages easily!")
    
    # Initialize Firebase
    if not initialize_firebase():
        st.stop()
    
    # Input form
    with st.form("fcm_form"):
        st.subheader("👤 Recipient Selection")
        
        # Recipient selection instead of token input
        selected_recipient = st.selectbox(
            "Send to:",
            options=list(RECIPIENT_TOKENS.keys()),
            help="Choose the recipient for your message"
        )
        
        # Get the corresponding token
        device_token = RECIPIENT_TOKENS[selected_recipient]
        
        st.subheader("💌 Message Details")
        
        # Message type selection
        message_type = st.radio(
            "Message Type:",
            ["Custom Message", "Send Random"],
            help="Choose to send your own message or a random lovely message"
        )
        
        if message_type == "Custom Message":
            title = st.text_input(
                "Message Title", 
                placeholder="Enter notification title",
                help="This will appear as the notification title"
            )
            
            body = st.text_area(
                "Message Body", 
                placeholder="Enter your message here...",
                height=100,
                help="This will appear as the notification content"
            )
        else:
            # Random message preview
            if st.form_submit_button("🎲 Preview Random Message", type="secondary"):
                random_title = random.choice(LOVELY_TITLES)
                random_body = random.choice(LOVELY_MESSAGES)
                st.info(f"**Preview:**\n\n**Title:** {random_title}\n\n**Message:** {random_body}")
            
            title = ""  # Will be set randomly
            body = ""   # Will be set randomly
        
        # Optional: Custom data
        with st.expander("Advanced Options (Optional)"):
            custom_key = st.text_input("Custom Data Key", placeholder="e.g., action_type")
            custom_value = st.text_input("Custom Data Value", placeholder="e.g., open_screen")
        
        # Submit button
        if message_type == "Custom Message":
            submitted = st.form_submit_button("📤 Send Message", type="primary")
        else:
            submitted = st.form_submit_button("💕 Send Random Love Message", type="primary")
        
        if submitted:
            # Handle random message
            if message_type == "Send Random":
                title = random.choice(LOVELY_TITLES)
                body = random.choice(LOVELY_MESSAGES)
            
            if not title or not body:
                st.error("❌ Please fill in both title and message body!")
            else:
                # Prepare custom data
                custom_data = {}
                if custom_key and custom_value:
                    custom_data[custom_key] = custom_value
                
                # Show loading spinner
                with st.spinner(f"Sending message to {selected_recipient}..."):
                    success, response, store_success, doc_id = send_fcm_message(title, body, device_token, custom_data)
                
                if success:
                    st.success(f"✅ Message sent successfully to {selected_recipient}!")
                    st.info(f"FCM Response ID: {response}")
                    
                    if store_success:
                        st.success(f"💾 Message stored in Firestore! Document ID: {doc_id}")
                    else:
                        st.warning(f"⚠️ Message sent but failed to store in Firestore: {doc_id}")
                    
                    # Show sent message preview
                    with st.expander("📱 Message Preview"):
                        st.write(f"**Recipient:** {selected_recipient}")
                        st.write(f"**Title:** {title}")
                        st.write(f"**Body:** {body}")
                        if custom_data:
                            st.write(f"**Custom Data:** {custom_data}")
                else:
                    st.error(f"❌ Failed to send message to {selected_recipient}: {response}")
    
    # Device info (updated sidebar)
    with st.sidebar:
        st.subheader("🚀 Deployment Ready!")
        st.success("This app uses Streamlit secrets for secure credential storage")
        
        st.subheader("📊 How to Use")
        st.text("1. Select recipient")
        st.text("2. Choose message type") 
        st.text("3. Send your message!")
        st.text("4. Check recipient's device!")
        
        st.subheader("👥 Recipients")
        st.text("• Shreya")
        st.text("• Ishank")
        
        st.subheader("💾 Storage")
        st.text("All messages are stored")
        st.text("in 'love_messages' collection")
        
        st.subheader("🔧 Setup for Deployment")
        st.code('''
# Add to Streamlit secrets:
[firebase]
service_account_key = """
{your full service account key JSON}
"""
        ''', language="toml")

if __name__ == "__main__":
    main()
