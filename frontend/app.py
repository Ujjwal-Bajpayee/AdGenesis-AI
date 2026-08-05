import os
import json
import time
import requests
import streamlit as st
import pandas as pd

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="AdGenesis AI - Marketing Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1E1B4B 0%, #0F172A 60%, #020617 100%);
        color: #F8FAFC;
    }
    
    .glass-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    .stat-badge {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(147, 51, 234, 0.2) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #60A5FA 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .agent-pill-done {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34D399;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
        font-weight: 500;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .agent-pill-active {
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.5);
        color: #60A5FA;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: space-between;
        animation: pulse 2s infinite;
    }
    
    .agent-pill-pending {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #64748B;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 12px 28px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #60A5FA 0%, #A78BFA 100%);
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.6);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

if "current_analysis_id" not in st.session_state:
    st.session_state["current_analysis_id"] = None

st.sidebar.markdown("## ⚡ AdGenesis AI")
st.sidebar.caption("Autonomous Marketing Intelligence Platform")

navigation = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Video",
        "Agent Pipeline",
        "Creative Analysis",
        "Prediction",
        "Creative Brief",
        "Recommendations",
        "A/B Testing",
        "Marketing Report",
        "History"
    ]
)

ALL_AGENTS = [
    "Media Extraction Pipeline",
    "Video Analysis Agent",
    "Audio Analysis Agent",
    "OCR Agent",
    "Caption Understanding Agent",
    "Creative Analysis Agent",
    "Prediction Agent",
    "Recommendation Agent",
    "Creative Brief Agent",
    "Experiment Agent",
    "Budget Recommendation Agent",
    "Marketing Report Agent"
]

ESTIMATED_SECONDS_PER_AGENT = 3.0

def fetch_analysis_data(analysis_id):
    try:
        res = requests.get(f"{API_BASE_URL}/analysis/{analysis_id}")
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

def fetch_workflow_status(analysis_id):
    try:
        res = requests.get(f"{API_BASE_URL}/status/{analysis_id}")
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

if navigation == "Dashboard":
    st.title("📊 Creative Performance Dashboard")
    st.markdown("Autonomous multi-agent intelligence platform for high-converting video ads.")

    history_items = []
    try:
        res = requests.get(f"{API_BASE_URL}/history")
        if res.status_code == 200:
            history_items = res.json()
    except Exception:
        history_items = []

    total_analyses = len(history_items)
    avg_score = round(sum([item.get("overall_score", 0) for item in history_items]) / total_analyses, 1) if total_analyses > 0 else 85.0
    top_score = max([item.get("overall_score", 0) for item in history_items]) if total_analyses > 0 else 94.0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-badge"><div class="stat-value">{total_analyses}</div><div class="stat-label">Creatives Analyzed</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-badge"><div class="stat-value">{avg_score}</div><div class="stat-label">Avg Quality Score</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-badge"><div class="stat-value">{top_score}</div><div class="stat-label">Top Score Achieved</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-badge"><div class="stat-value">11</div><div class="stat-label">Autonomous AI Agents</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Recent Creative Evaluated")
    if history_items:
        df = pd.DataFrame(history_items)
        st.dataframe(df[["analysis_id", "video_filename", "campaign_goal", "status", "overall_score", "created_at"]], use_container_width=True)
    else:
        st.info("No video evaluations recorded yet. Upload a video creative to get started!")

elif navigation == "Upload Video":
    st.title("🎬 Upload Marketing Creative")
    st.markdown("Submit an Instagram Reel or promotional video for autonomous multi-agent analysis.")

    with st.form("upload_form"):
        uploaded_file = st.file_uploader("Select Video File (.mp4, .mov)", type=["mp4", "mov", "avi", "mkv"])
        caption = st.text_area("Instagram Caption / Copy Text", placeholder="Paste the caption text, hashtags, and CTA link...")
        campaign_goal = st.selectbox("Campaign Goal", ["Direct Conversions", "Brand Awareness", "Lead Generation", "App Installs", "Engagement Boost"])
        
        st.caption("⏱️ Estimated Autonomous Pipeline Execution Time: ~30-40 seconds")
        submit_button = st.form_submit_button("🚀 Run Autonomous AI Analysis")

    if submit_button:
        if not uploaded_file:
            st.error("Please upload a video file first.")
        else:
            with st.spinner("Uploading creative and launching multi-agent pipeline..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"caption": caption, "campaign_goal": campaign_goal}
                    res = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data)
                    
                    if res.status_code == 200:
                        resp_json = res.json()
                        analysis_id = resp_json["analysis_id"]
                        st.session_state["current_analysis_id"] = analysis_id
                        st.success(f"Pipeline launched! Analysis ID: `{analysis_id}`")
                        st.info("Navigate to **Agent Pipeline** to watch real-time execution progress!")
                    else:
                        st.error(f"Failed to launch pipeline: {res.text}")
                except Exception as e:
                    st.error(f"Error connecting to server: {str(e)}")

elif navigation == "Agent Pipeline":
    st.title("⚡ Multi-Agent Execution Pipeline")
    st.markdown("Monitor real-time agent execution status and remaining estimated completion time.")

    analysis_id = st.session_state.get("current_analysis_id")
    if not analysis_id:
        st.warning("No active analysis selected. Upload a video creative first or select one from History.")
    else:
        st.markdown(f"**Target Analysis ID:** `{analysis_id}`")
        wf = fetch_workflow_status(analysis_id)
        
        if wf:
            status = wf.get("status", "processing")
            current_agent = wf.get("current_agent", "Media Extraction Pipeline")
            exec_order = wf.get("execution_order", [])
            logs = wf.get("agent_logs", [])

            completed_count = len(exec_order)
            total_count = len(ALL_AGENTS)
            
            if status == "completed":
                progress_val = 1.0
                remaining_sec = 0
            else:
                progress_val = min(0.95, max(0.08, completed_count / total_count))
                remaining_agents = max(0, total_count - completed_count)
                remaining_sec = int(remaining_agents * ESTIMATED_SECONDS_PER_AGENT)

            col_prog, col_time = st.columns([3, 1])
            with col_prog:
                st.progress(progress_val)
            with col_time:
                if status == "completed":
                    st.success("✅ Complete (~30s)")
                else:
                    st.info(f"⏳ ~{remaining_sec}s remaining")

            st.markdown(f"### Pipeline Status: `{status.upper()}`")

            col_left, col_right = st.columns([1, 1])

            with col_left:
                st.markdown("### Agent Execution Order")
                for agent_name in ALL_AGENTS:
                    if agent_name in exec_order and (agent_name != current_agent or status == "completed"):
                        st.markdown(f'<div class="agent-pill-done"><span>✅ {agent_name}</span><span>Completed</span></div>', unsafe_allow_html=True)
                    elif agent_name == current_agent and status != "completed":
                        st.markdown(f'<div class="agent-pill-active"><span>🔄 {agent_name}</span><span>Executing...</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="agent-pill-pending"><span>⚪ {agent_name}</span><span>Queued</span></div>', unsafe_allow_html=True)

            with col_right:
                st.markdown("### Agent State & Log Stream")
                for log_item in logs:
                    st.json(log_item)
        else:
            st.info("Fetching execution pipeline status...")

elif navigation == "Creative Analysis":
    st.title("🔍 Multimodal Creative Intelligence")
    analysis_id = st.session_state.get("current_analysis_id")
    data = fetch_analysis_data(analysis_id) if analysis_id else None

    if not data:
        st.info("Select an active analysis to view creative diagnostics.")
    else:
        synth = data.get("creative_synthesis", {})
        video = data.get("video_analysis", {})
        audio = data.get("audio_analysis", {})
        ocr = data.get("ocr_analysis", {})

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Visual & Structural Diagnostics")
            st.write(f"**Opening Hook:** {synth.get('hook_evaluation')}")
            st.write(f"**Storytelling Format:** {synth.get('storytelling_quality')}")
            st.write(f"**Editing Speed:** {video.get('pacing')} ({video.get('scenes_detected')} scene cuts)")
            st.write(f"**Products Identified:** {', '.join(video.get('products_identified', []))}")
            st.write(f"**Target Audience:** {synth.get('target_audience')}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Audio & Copy Intelligence")
            st.write(f"**Vocal Emotional Tone:** {audio.get('emotional_tone')}")
            st.write(f"**Background Music:** {audio.get('background_music_mood')}")
            st.write(f"**On-Screen Text CTA:** {ocr.get('primary_cta')}")
            st.write(f"**Speech Transcript:** {audio.get('transcript')}")
            st.markdown('</div>', unsafe_allow_html=True)

        col_s, col_w = st.columns(2)
        with col_s:
            st.markdown("### 💪 Creative Strengths")
            for item in synth.get("strengths", []):
                st.success(item)
        with col_w:
            st.markdown("### ⚠️ Creative Weaknesses")
            for item in synth.get("weaknesses", []):
                st.warning(item)

elif navigation == "Prediction":
    st.title("📈 Performance Predictions")
    analysis_id = st.session_state.get("current_analysis_id")
    data = fetch_analysis_data(analysis_id) if analysis_id else None

    if not data:
        st.info("Select an active analysis to view predictions.")
    else:
        pred = data.get("prediction", {})
        score = pred.get("overall_quality_score", 0.0)

        st.markdown(f'<div class="stat-badge" style="margin-bottom: 20px;"><div class="stat-value">{score} / 100</div><div class="stat-label">Overall Creative Quality Score</div></div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Predicted Engagement", pred.get("expected_engagement_rate", "N/A"))
        with c2:
            st.metric("Predicted Watch Time", pred.get("expected_watch_time_seconds", "N/A"))
        with c3:
            st.metric("Predicted CTR", pred.get("expected_ctr", "N/A"))
        with c4:
            st.metric("Conversion Rate Lift", pred.get("expected_conversions_estimate", "N/A"))

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Predictive Rationale & AI Reasoning")
        st.info(pred.get("reasoning", "No reasoning available."))

elif navigation == "Creative Brief":
    st.title("📋 Generated Creative Brief")
    analysis_id = st.session_state.get("current_analysis_id")
    data = fetch_analysis_data(analysis_id) if analysis_id else None

    if not data:
        st.info("Select an active analysis to view the creative brief.")
    else:
        brief_res = requests.get(f"{API_BASE_URL}/brief/{analysis_id}")
        if brief_res.status_code == 200:
            brief = brief_res.json()
            st.markdown(f"### Campaign Objective: `{brief.get('campaign_goal')}`")
            st.write(f"**Target Audience:** {brief.get('target_audience')}")
            st.write(f"**Opening Hook:** {brief.get('opening_hook')}")
            st.write(f"**Voiceover Script:** {brief.get('voiceover_script')}")
            st.write(f"**Visual Style:** {brief.get('visual_style')}")
            st.write(f"**Recommended CTA:** {brief.get('cta')}")

            st.markdown("### Scene-by-Scene Production Breakdown")
            scenes = brief.get("scene_by_scene_breakdown", [])
            if scenes:
                st.table(pd.DataFrame(scenes))

            st.download_button(
                "📥 Download Brief JSON",
                data=json.dumps(brief, indent=2),
                file_name=f"Creative_Brief_{analysis_id}.json",
                mime="application/json"
            )

elif navigation == "Recommendations":
    st.title("💡 Optimization Recommendations")
    analysis_id = st.session_state.get("current_analysis_id")
    data = fetch_analysis_data(analysis_id) if analysis_id else None

    if not data:
        st.info("Select an active analysis to view recommendations.")
    else:
        recs = data.get("recommendations", {})
        st.write(f"**Upgraded Hook:** {recs.get('better_hook')}")
        st.write(f"**Upgraded Opening:** {recs.get('better_opening')}")
        st.write(f"**Upgraded Pacing:** {recs.get('better_pacing')}")
        st.write(f"**Upgraded CTA:** {recs.get('better_cta')}")
        st.write(f"**Upgraded Storytelling:** {recs.get('better_storytelling')}")
        st.write(f"**Recommended Hashtags:** {', '.join(recs.get('better_hashtags', []))}")

elif navigation == "A/B Testing":
    st.title("🧪 Structured A/B Testing Experiments")
    analysis_id = st.session_state.get("current_analysis_id")
    data = fetch_analysis_data(analysis_id) if analysis_id else None

    if not data:
        st.info("Select an active analysis to view experiment ideas.")
    else:
        experiments = data.get("experiments", [])
        for exp in experiments:
            with st.expander(f"🧪 {exp.get('title', 'Experiment')}", expanded=True):
                st.write(f"**Hypothesis:** {exp.get('hypothesis')}")
                st.write(f"**Action Plan:** {exp.get('what_to_change')}")
                st.write(f"**Expected Impact:** {exp.get('expected_impact')}")
                st.write(f"**Confidence Score:** {exp.get('confidence_score', 0.8) * 100}%")

elif navigation == "Marketing Report":
    st.title("📄 Complete Marketing Report")
    analysis_id = st.session_state.get("current_analysis_id")
    
    if not analysis_id:
        st.info("Select an active analysis to view the report.")
    else:
        rep_res = requests.get(f"{API_BASE_URL}/report/{analysis_id}")
        if rep_res.status_code == 200:
            report = rep_res.json()
            md_content = report.get("markdown_content", "")
            
            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "📥 Export Markdown Report",
                    data=md_content,
                    file_name=f"AdGenesis_Report_{analysis_id}.md",
                    mime="text/markdown"
                )
            with c2:
                pdf_url = f"{API_BASE_URL}/report/{analysis_id}/pdf"
                st.markdown(f"[📥 Download Official PDF Report]({pdf_url})")

            st.markdown("---")
            st.markdown(md_content)

elif navigation == "History":
    st.title("📚 Saved Creative Evaluations")
    try:
        res = requests.get(f"{API_BASE_URL}/history")
        if res.status_code == 200:
            items = res.json()
            for item in items:
                col_info, col_act = st.columns([3, 1])
                with col_info:
                    st.write(f"**{item.get('video_filename')}** | Score: `{item.get('overall_score')}/100` | ID: `{item.get('analysis_id')}`")
                with col_act:
                    if st.button("Inspect", key=item.get("analysis_id")):
                        st.session_state["current_analysis_id"] = item.get("analysis_id")
                        st.success(f"Loaded `{item.get('analysis_id')}`!")
    except Exception as e:
        st.error(f"Failed to load history: {str(e)}")
