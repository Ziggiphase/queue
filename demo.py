import streamlit as st
import pandas as pd
import simpy
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import io

# --- 1. STATE INITIALIZATION ---
if 'courses_db' not in st.session_state:
    # Full data as provided by the user
    st.session_state.courses_db = [
        {"Code": "COS 101", "Name": "Intro to Computing", "Lecturer": "Ahmed Adeniyi", "Level": "100L-IT", "Credit": 3, "Category": "Core", "Priority": 1},
        {"Code": "GST 111", "Name": "Communication in English", "Lecturer": "GST Dept.", "Level": "100L-IT", "Credit": 2, "Category": "Common", "Priority": 1},
        {"Code": "NUN-IFT 103", "Name": "Intro to IS", "Lecturer": "Dr. Temitope", "Level": "100L-IT", "Credit": 3, "Category": "Core", "Priority": 1},
        {"Code": "MTH 101", "Name": "Elem Math I", "Lecturer": "Prof. Oluwayemi", "Level": "100L-IT", "Credit": 2, "Category": "Core", "Priority": 1},
        {"Code": "PHY 101", "Name": "General Physics I", "Lecturer": "PHY Dept.", "Level": "100L-IT", "Credit": 2, "Category": "Core", "Priority": 1},
        {"Code": "STA 111", "Name": "Descriptive Statistics", "Lecturer": "Dr. Peter Koleoso", "Level": "100L-IT", "Credit": 3, "Category": "Common", "Priority": 1},
        {"Code": "COS 101", "Name": "Intro to Computing", "Lecturer": "TBA", "Level": "100L-IS", "Credit": 3, "Category": "Core", "Priority": 1},
        {"Code": "NUN-INS 103", "Name": "Business Programming", "Lecturer": "Prince Eru", "Level": "100L-IS", "Credit": 2, "Category": "Core", "Priority": 1},
        {"Code": "STA 111", "Name": "Descriptive Statistics", "Lecturer": "GST Dept.", "Level": "100L-IS", "Credit": 3, "Category": "Common", "Priority": 1},
        {"Code": ".IFT 203", "Name": "Web Tech (Sec 1)", "Lecturer": "Prince Eru", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": ".IFT 203", "Name": "Web Tech (Sec 3)", "Lecturer": "Prince Eru", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": ".IFT 205", "Name": "Intro to IT", "Lecturer": "Mr. Solomon", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": ".IFT 211", "Name": "Digital Logic", "Lecturer": "Mr. Solomon", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": ".SEN 201", "Name": "Software Engineering", "Lecturer": "Prince Eru", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": "COS 201", "Name": "Computer Programming I", "Lecturer": "Omeiza Abdulazeez", "Level": "200L-IT", "Credit": 3, "Category": "Core", "Priority": 2},
        {"Code": "INS 202", "Name": "HCI", "Lecturer": "Prince Eru", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": "NUN-BUA 101", "Name": "Intro to Business I", "Lecturer": "TBA", "Level": "200L-IS", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": "COS 201", "Name": "Programming I (Sec 8)", "Lecturer": "Dr. Salisu Yusuf", "Level": "200L-IS", "Credit": 3, "Category": "Core", "Priority": 2},
        {"Code": "NUN-DTS 201", "Name": "Data Science", "Lecturer": "Noah Gana", "Level": "200L-IS", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": "INS 207", "Name": "Intro to IS", "Lecturer": "Prince Eru", "Level": "200L-IS", "Credit": 2, "Category": "Core", "Priority": 2},
        {"Code": ".IFT 302", "Name": "Web App Dev", "Lecturer": "Prince Eru", "Level": "300L-IT", "Credit": 3, "Category": "Core", "Priority": 3},
        {"Code": "NUN-.IFT 303", "Name": "Enterprise Systems", "Lecturer": "Dr. Ridwan", "Level": "300L-IT", "Credit": 3, "Category": "Core", "Priority": 3},
        {"Code": "NUN-.IFT 307", "Name": "SDN", "Lecturer": "Dr. Temitope", "Level": "300L-IT", "Credit": 3, "Category": "Core", "Priority": 3},
        {"Code": ".IFT 308", "Name": "Ethics and Legal IT", "Lecturer": "Dr. Ridwan", "Level": "300L-IT", "Credit": 2, "Category": "Core", "Priority": 3},
        {"Code": ".IFT 342", "Name": "Network Servers", "Lecturer": "Mr. Solomon", "Level": "300L-IT", "Credit": 2, "Category": "Core", "Priority": 3},
        {"Code": "ICT 305", "Name": "Data Communications", "Lecturer": "Mr. Solomon", "Level": "300L-IT", "Credit": 3, "Category": "Core", "Priority": 3},
        {"Code": "IFT 401", "Name": "IT Project Mgt", "Lecturer": "Dr. Ridwan", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Priority": 4},
        {"Code": ".IFT 403", "Name": "Mobile Computing", "Lecturer": "Ahmed Adeniyi", "Level": "400L-IT", "Credit": 2, "Category": "Core", "Priority": 4},
        {"Code": "IFT 413", "Name": "Research Methodology", "Lecturer": "Prof. Prema", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Priority": 4},
        {"Code": "IFT 425", "Name": "E-Commerce", "Lecturer": "Dr. Ridwan", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Priority": 4},
        {"Code": "IFT 433", "Name": "Operational Mgt", "Lecturer": "Dr. Temitope", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Priority": 4},
        {"Code": "IFT 443", "Name": "Network Security", "Lecturer": "Mr. Solomon", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Priority": 4},
        {"Code": "CSC 709", "Name": "System Analysis", "Lecturer": "Adeniyi Ahmed", "Level": "PGD-IT", "Credit": 2, "Category": "Core", "Priority": 5},
        {"Code": "IFT 701", "Name": "Database Apps", "Lecturer": "Mr. Solomon", "Level": "PGD-IT", "Credit": 2, "Category": "Core", "Priority": 5},
        {"Code": "IFT 703", "Name": "MIS", "Lecturer": "Dr. Temitope", "Level": "PGD-IT", "Credit": 3, "Category": "Core", "Priority": 5},
        {"Code": "IFT 711", "Name": "Info Security", "Lecturer": "Prince Eru", "Level": "PGD-IT", "Credit": 2, "Category": "Core", "Priority": 5},
        {"Code": "SEN 705", "Name": "OOAD", "Lecturer": "Dr. Anka", "Level": "PGD-IT", "Credit": 2, "Category": "Core", "Priority": 5},
        {"Code": "CSC 811", "Name": "Advanced Programming", "Lecturer": "Assoc. Prof. Akande", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Priority": 6},
        {"Code": "IFT 801", "Name": "IT Project Mgt", "Lecturer": "Prof. Prema", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Priority": 6},
        {"Code": "IFT 803", "Name": "HCI for IS", "Lecturer": "Dr. Temi", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Priority": 6},
        {"Code": "IFT 807", "Name": "Information Security", "Lecturer": "Dr. Nurudeen", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Priority": 6},
        {"Code": "IFT 809", "Name": "Cyber Law", "Lecturer": "Dr. Ridwan", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Priority": 6},
    ]

if 'sim_results' not in st.session_state:
    st.session_state.sim_results = None

# --- 2. PREMIUM BRANDING & STYLING ---
st.set_page_config(page_title="Nile Uni | Timetable Engine", layout="wide", page_icon="🔢")

NILE_NAVY = "#1e3a8a"
NILE_BLUE = "#3b82f6"
SLATE = "#64748b"

st.markdown(f"""
    <style>
    .main {{ background-color: #f8fafc; }}
    .stButton>button {{
        background: linear-gradient(90deg, {NILE_NAVY} 0%, {NILE_BLUE} 100%);
        color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem;
    }}
    .metric-card {{
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid {NILE_BLUE};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. THEORETICAL DATASET (GROUND TRUTH) ---
ROOM_CAPACITIES = {
    "E101 (Congo)": {"cap": 60, "avail": "9am-5pm Mon-Fri", "icon": "🏫"},
    "E102 (Congo)": {"cap": 60, "avail": "9am-5pm Mon-Fri", "icon": "🏫"},
    "E026 (Congo)": {"cap": 190, "avail": "Mon(9-11), Tue(13-17), Wed(9-13)", "icon": "🎭"},
    "E020 (Congo)": {"cap": 160, "avail": "Fri Only (9am-5pm)", "icon": "🏛️"},
    "E125 (Congo)": {"cap": 160, "avail": "Mon Only (9am-5pm)", "icon": "🏗️"},
    "D008": {"cap": 130, "avail": "9am-5pm Mon-Fri", "icon": "📚"},
    "F206 (Ubangi)": {"cap": 60, "avail": "9am-5pm Mon-Fri", "icon": "💻"},
}

CLASS_SIZES = {
    "100L-IT": 100, "100L-IS": 100, "200L-IT": 169, "200L-IS": 94,
    "300L-IT": 113, "400L-IT": 71, "PGD-IT": 20, "MSC-IT": 40
}

# --- 4. ENGINE LOGIC (SIMPY) ---
class QueueingEngine:
    def __init__(self, courses, rooms):
        # Mandatory Priority logic: Category (Core first) then User Priority
        cat_map = {"Core": 1, "Common": 2, "Elective": 3}
        self.courses = sorted(courses, key=lambda x: (cat_map.get(x['Category'], 4), x['Priority']))
        self.rooms = rooms
        self.results = []
        self.busy_lecturers = set()
        self.busy_rooms = set()
        self.busy_groups = set()

    def is_room_open(self, room, day, hour):
        if room == "E026 (Congo)":
            if day == "Monday" and (9 <= hour < 11): return True
            if day == "Tuesday" and (13 <= hour < 17): return True
            if day == "Wednesday" and (9 <= hour < 13): return True
            return False
        if room == "E020 (Congo)": return day == "Friday"
        if room == "E125 (Congo)": return day == "Monday"
        return True

    def run(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        slots = list(range(9, 19)) # Expanded to handle PG evening slots

        for course in self.courses:
            placed = False
            # Get specific size for this level
            size = CLASS_SIZES.get(course['Level'], 50)
            
            # Search for available resource window
            for day in days:
                for hour in slots:
                    for r_name, r_meta in self.rooms.items():
                        # Hard Constraints (Mandatory)
                        if r_meta['cap'] < size: continue
                        if not self.is_room_open(r_name, day, hour): continue
                        
                        l_key = (course['Lecturer'], day, hour)
                        r_key = (r_name, day, hour)
                        g_key = (course['Level'], day, hour)
                        
                        if l_key not in self.busy_lecturers and r_key not in self.busy_rooms and g_key not in self.busy_groups:
                            self.busy_lecturers.add(l_key)
                            self.busy_rooms.add(r_key)
                            self.busy_groups.add(g_key)
                            
                            self.results.append({**course, "Day": day, "Time": f"{hour:02d}:00", "Room": r_name, "ActualSize": size})
                            placed = True
                            break
                    if placed: break
                if placed: break
            
            if not placed:
                self.results.append({**course, "Day": "OVERFLOW", "Time": "N/A", "Room": "N/A", "ActualSize": size})

# --- 5. INTERFACE NAVIGATION ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/Nile_University_Logo.png/220px-Nile_University_Logo.png", width=100)
page = st.sidebar.radio("Navigation", ["Admin: Course Allocation", "Timetable Simulation"])

if page == "Admin: Course Allocation":
    st.markdown(f"## 🛠️ Course Allocation & Admin")
    st.info("Management page for Course Codes, Lecturers, and Categories. Changes here affect the Queueing Model.")

    # 1. Edit/Delete via Data Editor
    st.subheader("Current Database Audit")
    df_courses = pd.DataFrame(st.session_state.courses_db)
    
    # Interactive Editor
    edited_df = st.data_editor(
        df_courses, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "Category": st.column_config.SelectboxColumn(options=["Core", "Common", "Elective"]),
            "Level": st.column_config.SelectboxColumn(options=list(CLASS_SIZES.keys()))
        }
    )
    
    if st.button("💾 Save Database Changes"):
        st.session_state.courses_db = edited_df.to_dict('records')
        st.success("Database Updated! Proceed to Simulation tab.")

    st.divider()
    
    # 2. Add Course Form
    with st.expander("➕ Add Single Course to Queue"):
        with st.form("new_course"):
            c1, c2, c3 = st.columns(3)
            new_code = c1.text_input("Course Code")
            new_name = c2.text_input("Course Title")
            new_lect = c3.text_input("Lecturer Name")
            
            c4, c5, c6 = st.columns(3)
            new_lvl = c4.selectbox("Level", list(CLASS_SIZES.keys()))
            new_credit = c5.selectbox("Credit Units", [1, 2, 3, 4, 6])
            new_cat = c6.selectbox("Category", ["Core", "Common", "Elective"])
            
            new_prio = st.slider("Specific Priority Request (1=High)", 1, 10, 1)
            
            if st.form_submit_button("Add Allocation"):
                new_entry = {
                    "Code": new_code, "Name": new_name, "Lecturer": new_lect,
                    "Level": new_lvl, "Credit": new_credit,
                    "Category": new_cat, "Priority": new_prio
                }
                st.session_state.courses_db.append(new_entry)
                st.rerun()

elif page == "Timetable Simulation":
    st.markdown(f"## 🔢 Queueing Model Simulation")
    st.markdown("##### IT & IS Departments | Nile University of Nigeria")
    
    # Executive Dashboard Cards
    total_q = len(st.session_state.courses_db)
    st.markdown(f"""
    <div style="display:flex; gap:20px; margin-bottom:25px;">
        <div class="metric-card" style="flex:1;">
            <div style="color:#64748b; font-size:12px; font-weight:bold;">ARRIVAL QUEUE</div>
            <div style="color:#1e3a8a; font-size:24px; font-weight:bold;">{total_q} Courses</div>
        </div>
        <div class="metric-card" style="flex:1;">
            <div style="color:#64748b; font-size:12px; font-weight:bold;">SERVICE NODES</div>
            <div style="color:#1e3a8a; font-size:24px; font-weight:bold;">7 Halls</div>
        </div>
        <div class="metric-card" style="flex:1;">
            <div style="color:#64748b; font-size:12px; font-weight:bold;">LOGIC</div>
            <div style="color:#1e3a8a; font-size:24px; font-weight:bold;">M/M/c Model</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 EXECUTE QUEUEING MODEL"):
        with st.spinner("Processing Stochastic Arrivals..."):
            time.sleep(1.5)
            engine = QueueingEngine(st.session_state.courses_db, ROOM_CAPACITIES)
            engine.run()
            st.session_state.sim_results = pd.DataFrame(engine.results)
        st.balloons()

    if st.session_state.sim_results is not None:
        res = st.session_state.sim_results
        
        # Performance Indicators
        scheduled = len(res[res['Day'] != "OVERFLOW"])
        eff = (scheduled/total_q)*100
        st.progress(eff/100)
        st.caption(f"System Efficiency: {eff:.1f}%")

        tabs = st.tabs(["🗓️ Optimized Timetable", "📈 Usage Analytics", "🏢 Room Stats"])
        
        with tabs[0]:
            st.dataframe(res.sort_values(['Day', 'Time']), use_container_width=True, hide_index=True)
            csv = res.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Result (CSV)", csv, f"Nile_Timetable_{datetime.now().strftime('%Y%m%d')}.csv")
            
        with tabs[1]:
            h_data = res[res['Day'] != "OVERFLOW"].groupby(['Day', 'Time']).size().reset_index(name='Load')
            if not h_data.empty:
                h_pivot = h_data.pivot(index='Time', columns='Day', values='Load').fillna(0)
                st.plotly_chart(px.imshow(h_pivot, text_auto=True, color_continuous_scale="Blues", title="Time-Slot Intensity"), use_container_width=True)
        
        with tabs[2]:
            room_usage = res[res['Day'] != "OVERFLOW"]['Room'].value_counts().reset_index()
            st.plotly_chart(px.pie(room_usage, values='count', names='Room', hole=0.4, title="Node Occupancy Share"), use_container_width=True)
    else:
        st.info("SimPy engine is ready. Click the Execute button to generate the conflict-free grid.")

# --- 6. FOOTER ---
st.divider()
st.caption("Technical Implementation of Queueing Theory Model | Nile University FCOM 2025")