import streamlit as st
import random
from datetime import datetime, timedelta

event_data = [
    {
        "title": "🎉 Hiragana Speed Quiz",
        "description": "Earn double XP by completing the quiz within the time limit!",
        "end_time": datetime.now() + timedelta(hours=2)
    },
    # {
    #     "title": "🧠 Memory Match: Spanish Nouns",
    #     "description": "Timed event to help with vocabulary recall. Ends soon!",
    #     "end_time": datetime.now() + timedelta(minutes=30)
    # },
    # {
    #     "title": "⛔ Expired Practice Drill",
    #     "description": "This should not show anymore.",
    #     "end_time": datetime.now() - timedelta(minutes=10)
    # }
]

if "in_hiragana_event" not in st.session_state:
    st.session_state.in_hiragana_event = False
if "hiragana_start_time" not in st.session_state:
    st.session_state.hiragana_start_time = None
if "hiragana_score" not in st.session_state:
    st.session_state.hiragana_score = 0
if "hiragana_q" not in st.session_state:
    st.session_state.hiragana_q = 0
if "badges" not in st.session_state:
    st.session_state.badges = set()


hiragana_questions = [
    {"char": "あ", "answer": "a"},
    {"char": "い", "answer": "i"},
    {"char": "う", "answer": "u"},
    {"char": "え", "answer": "e"},
    {"char": "お", "answer": "o"},
    # {"char": "か", "answer": "ka"},
    # {"char": "き", "answer": "ki"},
    # {"char": "く", "answer": "ku"},
    # {"char": "け", "answer": "ke"},
    # {"char": "こ", "answer": "ko"},
]


# --- INIT SESSION STATE ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 3
if 'last_practiced' not in st.session_state:
    st.session_state.last_practiced = datetime.today().date()
if 'freeze' not in st.session_state:
    st.session_state.freeze = 1
if 'vocab_review' not in st.session_state:
    st.session_state.vocab_review = ['apple', 'water', 'cat', 'book']
if "lessons_completed" not in st.session_state:
    st.session_state.lessons_completed = 0


# --- SIDEBAR MENU ---
st.sidebar.title("🧭 Navigation")
PAGES = ["🏠 Home", "📚 Lessons", "🧠 Review", "🧠 AI Features"]

selected_page = st.sidebar.radio("Go to", PAGES)


# --- HOME PAGE ---
if selected_page == "🏠 Home":
    st.set_page_config(page_title="LingoLearn Home", layout="centered")
    st.markdown("<h1 style='color:#58cc02;'>🏠 LingoLearn Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray;'>Welcome back! Let's keep the streak alive 🔥</p>", unsafe_allow_html=True)

    # Streak & XP
    st.divider()
    st.subheader("📈 Your Progress")
    col1, col2, col3 = st.columns(3)
    col1.metric("XP", f"{st.session_state.xp} XP")
    col2.metric("🔥 Streak", f"{st.session_state.streak} Days")
    col3.metric("🧊 Freezes", st.session_state.freeze)

    st.divider()

    # Daily Feed
    st.subheader("📰 Daily Feed")
    tabs = st.tabs(["News", "Memes", "Vlogs"])
    with tabs[0]:
        st.markdown("> 日本では新しい再生可能エネルギー法が可決されました。🌱")
        st.caption("Translation: A new renewable energy law has been passed in Japan.")
    with tabs[1]:
        st.image("https://i.imgflip.com/4/4t0m5.jpg", caption="なにお見ている")
    with tabs[2]:
        st.video("https://www.youtube.com/watch?v=N8XaLy1gWV0&ab_channel=MikuRealJapanese")

    st.divider()
    st.subheader("📅 Event Calendar")

    now = datetime.now()
    active_events = [event for event in event_data if event["end_time"] > now]

    if not active_events:
        st.info("No active events right now. Check back later!")
    else:
        for i, event in enumerate(active_events):
            time_remaining = event["end_time"] - now
            with st.container():
                st.markdown(f"#### {event['title']}")
                st.write(event["description"])
                st.warning(f"⏰ Time remaining: {str(time_remaining).split('.')[0]}")
            if "hiragana" in event["title"].lower():
                if st.button("Enter Hiragana Speed Quiz"):
                    st.session_state.in_hiragana_event = True
                    st.session_state.hiragana_start_time = datetime.now()
                    st.session_state.hiragana_q = 0
                    st.session_state.hiragana_score = 0

                st.markdown("---")
    if st.session_state.in_hiragana_event:
        if st.session_state.hiragana_start_time is None:
            st.session_state.hiragana_start_time = datetime.now()

        time_left = 60 - int((datetime.now() - st.session_state.hiragana_start_time).total_seconds())
        
        if time_left <= 0 or st.session_state.hiragana_q >= len(hiragana_questions):
            st.session_state.in_hiragana_event = False
            st.success(f"⏰ Time’s up or quiz completed! You scored {st.session_state.hiragana_score} / 5.")
            st.session_state.hiragana_start_time = None
            if st.session_state.hiragana_q >= 5:
                if "Hiragana Champ 🏅" not in st.session_state.badges:
                    st.session_state.badges.add("Hiragana Champ 🏅")
                    st.balloons()
                    st.success("🎉 You’ve earned the **Hiragana Champ 🏅** badge! Limited time only!")
                else:
                    st.info("✅ You've already earned the Hiragana Champ 🏅 badge.")
        else:
            st.markdown(f"## ⏳ Time Left: {time_left}s")
            current_q = hiragana_questions[st.session_state.hiragana_q]
            st.markdown(f"### What sound is this Hiragana character: `{current_q['char']}`?")
            
            # Key must be unique per question
            input_key = f"hiragana_input_{st.session_state.hiragana_q}"
            user_input = st.text_input("Your answer:", key=f"hiragana_input_{st.session_state.hiragana_q}")
            submit_clicked = st.button("Submit")

        if submit_clicked:
            if user_input.strip().lower() == current_q["answer"]:
                st.success("✅ Correct!")
                st.session_state.hiragana_score += 1
                st.session_state.hiragana_q += 1
                st.rerun()
            elif user_input.strip() != "":
                st.error(f"❌ Incorrect. The correct answer is: {current_q['answer']}")
        
    st.divider()

    # Today’s Challenge
    st.subheader("🎯 Today’s Challenge")
    col1, col2, col3 = st.columns(3)
    col1.metric("XP Goal", "50 XP")
    col2.metric("Time Left", str(timedelta(hours=3, minutes=45)))
    col3.metric("Tasks", "2/3 Done ✅")
    st.progress(0.67)

    with st.expander("📋 View Tasks"):
        st.checkbox("✅ Complete 1 vocabulary quiz")
        st.checkbox("✅ Review 3 flashcards")
        st.checkbox("⬜ Chat with native speaker")

    st.divider()

    if "show_akiko_chat" not in st.session_state:
        st.session_state.show_akiko_chat = False
    if "akiko_history" not in st.session_state:
        st.session_state.akiko_history = []

    st.subheader("💬 Native Chat Updates")
    st.markdown("**Akiko 🇯🇵 replied to your message 3 hours ago.**")

    if st.session_state.show_akiko_chat:
        st.markdown("### 💬 Chat with Akiko 🇯🇵")
        st.info("📌 Try using 5 words you learned this week (e.g., りんご, ありがとう, たべます...)")
        st.chat_message("assistant").markdown("こんにちは！元気ですか？ (Hello! How are you?)")

        akiko_reply = st.chat_input("Reply to Akiko in English or Japanese...", key="akiko_input")
        if akiko_reply:
            st.chat_message("user").markdown(akiko_reply)
            st.session_state.akiko_history.append(akiko_reply)
            st.chat_message("assistant").markdown("いいですね！もっと話しましょう〜 (Nice! Let's talk more!)")

    toggle_label = "❌ Close Akiko Chat" if st.session_state.show_akiko_chat else "💬 Chat with Akiko"
    if st.button(toggle_label, key="toggle_akiko_chat"):
        st.session_state.show_akiko_chat = not st.session_state.show_akiko_chat


# --- LESSON PAGE ---
elif selected_page == "📚 Lessons":
    st.title("📚 Lessons")

    mode = st.selectbox("Select Skill", ["Listening", "Speaking", "Reading", "Writing"])

    if mode == "Listening":
        st.markdown("### 🔊 Listen and choose the correct meaning:")
        st.audio("https://www.soundjay.com/human/japanese-hello-konnichiwa-01.mp3", format="audio/mp3")
        answer = st.radio("What did you hear?", ["Hello", "Goodbye", "Thank you", "I'm hungry"], key="listen_q")
        if st.button("Submit Listening"):
            if answer == "Hello":
                st.success("✅ Correct! +10 XP")
                st.session_state.xp += 10
                st.session_state.lessons_completed += 1
            else:
                st.error("❌ Oops, that’s not right.")

    elif mode == "Speaking":
        st.markdown("### 🗣️ Say the phrase below:")
        st.markdown("> Say: **Good morning** in Japanese")
        answer = st.text_input("Type what you would say:")
        if st.button("Submit Speaking"):
            st.success("✅ Well said! +10 XP")
            st.session_state.xp += 10                
            st.session_state.lessons_completed += 1
            # else:
            #     st.error("❌ Try again. Hint: It starts with 'お...'")

    elif mode == "Reading":
        st.markdown("### 📖 Read and answer the question:")
        st.markdown("> りんごをたべます。")
        answer = st.radio("What does this mean?", [
            "I eat apples", 
            "I drink water", 
            "I see a dog", 
            "I buy a book"
        ], key="read_q")
        if st.button("Submit Reading"):
            if answer == "I eat apples":
                st.success("✅ Correct! +10 XP")
                st.session_state.xp += 10
                st.session_state.lessons_completed += 1
            else:
                st.error("❌ Not quite! That sentence is about eating apples.")

    elif mode == "Writing":
        st.markdown("### ✍️ Translate into Japanese:")
        st.markdown("> I am a student.")
        answer = st.text_input("Type in Japanese (romaji is okay):")
        if st.button("Submit Writing"):
            if answer.strip().lower() in ["watashi wa gakusei desu", "わたしはがくせいです"]:
                st.success("✅ Nice! +10 XP")
                st.session_state.xp += 10
                st.session_state.lessons_completed += 1
            else:
                st.error("❌ Hmm, that's not the usual way to say it.")


elif selected_page == "🧠 AI Features":
    st.title("🧠 AI Features")
    st.markdown("Unlock personalized learning support powered by AI!")

    # --- Feature 1: AI-Powered Tutor / Chat Partner / Writing Assistant ---
    st.subheader("🗣️ AI Tutor, Chat Partner, & Writing Assistant")
    prompt = st.text_area("Ask a question, write something, or start a conversation:", key="ai_tutor_input")
    if st.button("💬 Send to AI"):
        if prompt:
            st.info("🤖 AI says (mock response):")
            st.write(f"『{prompt}』... sounds interesting! Here's how I'd respond or improve it... [This will be AI-powered soon!]")

    # --- Feature 2: Micro-feedback ---
    st.subheader("🔍 Personalized Micro-Feedback")
    grammar_trends = [
        "You frequently forget to use particles like 'を' or 'は'.",
        "Your use of verb tense is improving, but watch out for て-form mistakes.",
        "You sometimes mix up 'kore' vs 'sore'."
    ]
    st.info("🤖 Based on your recent practice, here are some tips:")
    for tip in grammar_trends:
        st.write(f"• {tip}")

    # --- Feature 3: Progress Summary ---
    st.subheader("📈 AI Progress Summary (After 3 Lessons)")
    if st.session_state.get("lessons_completed", 0) >= 3:
        st.success("🎉 You've completed 3 lessons!")
        st.markdown("**AI Summary:**")
        st.write("- ✅ Your vocabulary recall is getting faster.")
        st.write("- ⚠️ Focus more on listening comprehension.")
        st.write("- 🎯 Keep practicing sentence structure with particles.")
    else:
        st.info("📘 Complete 3 lessons to unlock your AI progress summary.")



# --- REVIEW PAGE ---
elif selected_page == "🧠 Review":
    st.title("🧠 Vocabulary Review")

    if st.session_state.vocab_review:
        word = random.choice(st.session_state.vocab_review)
        st.markdown(f"Translate: **{word}**")
        answer = st.text_input("Your answer:")
        if st.button("Submit"):
            st.success("Saved! We’ll review it again later.")
            st.session_state.vocab_review.remove(word)
    else:
        st.markdown("🎉 No vocab left to review today!")
