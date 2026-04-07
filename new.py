import streamlit as st
import pandas as pd
import json
import os
import time
import random
from datetime import datetime
import io
import plotly.express as px
import plotly.graph_objects as go

# --- 1. GLOBAL CONSTANTS & BRANDING (Fixes KeyErrors) ---
NAVY = "#1e3a8a"
NILE_BLUE = "#3b82f6" 
GOLD = "#facc15"
DB_FILE = "nile_timetable_db.json"
APP_NAME = "Nile Timetable Architect"

st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🏛️")

# --- 2. DATABASE PERSISTENCE ---
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except: pass
    
    # Master Dataset (Provided 42 Courses)
    return [
        {"Code": "COS 101", "Name": "Intro to Computing", "Lecturer": "Ahmed Adeniyi", "Level": "100L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 1},
        {"Code": "GST 111", "Name": "Communication in English", "Lecturer": "GST Dept.", "Level": "100L-IT", "Credit": 2, "Category": "Common", "Dept": "IT", "Prio": 1},
        {"Code": "NUN-IFT 103", "Name": "Intro to IS", "Lecturer": "Dr. Temitope", "Level": "100L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 1},
        {"Code": "MTH 101", "Name": "Elem Math I", "Lecturer": "Prof. Matthew Oluwayemi", "Level": "100L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 1},
        {"Code": "PHY 101", "Name": "General Physics I", "Lecturer": "PHY Dept.", "Level": "100L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 1},
        {"Code": "STA 111", "Name": "Descriptive Statistics", "Lecturer": "Dr. Peter Koleoso", "Level": "100L-IT", "Credit": 3, "Category": "Common", "Dept": "IT", "Prio": 1},
        {"Code": "COS 101", "Name": "Intro to Computing", "Lecturer": "TBA", "Level": "100L-IS", "Credit": 3, "Category": "Core", "Dept": "IS", "Prio": 1},
        {"Code": "NUN-INS 103", "Name": "Business Programming", "Lecturer": "Prince Eru", "Level": "100L-IS", "Credit": 2, "Category": "Core", "Dept": "IS", "Prio": 1},
        {"Code": "STA 111", "Name": "Descriptive Statistics", "Lecturer": "GST Dept.", "Level": "100L-IS", "Credit": 3, "Category": "Common", "Dept": "IS", "Prio": 1},
        {"Code": ".IFT 203", "Name": "Web Tech (Sec 1)", "Lecturer": "Prince Eru", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 2},
        {"Code": ".IFT 203", "Name": "Web Tech (Sec 3)", "Lecturer": "Prince Eru", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 2},
        {"Code": ".IFT 205", "Name": "Intro to IT", "Lecturer": "Mr. Solomon", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 2},
        {"Code": ".IFT 211", "Name": "Digital Logic", "Lecturer": "Mr. Solomon", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 2},
        {"Code": ".SEN 201", "Name": "Software Engineering", "Lecturer": "Prince Eru", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 2},
        {"Code": "COS 201", "Name": "Computer Programming I", "Lecturer": "Omeiza Abdulazeez", "Level": "200L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 2},
        {"Code": "INS 202", "Name": "HCI", "Lecturer": "Prince Eru", "Level": "200L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 2},
        {"Code": "NUN-BUA 101", "Name": "Intro to Business I", "Lecturer": "TBA", "Level": "200L-IS", "Credit": 2, "Category": "Core", "Dept": "IS", "Prio": 2},
        {"Code": "COS 201", "Name": "Programming I (Sec 8)", "Lecturer": "Dr. Salisu Yusuf", "Level": "200L-IS", "Credit": 3, "Category": "Core", "Dept": "IS", "Prio": 2},
        {"Code": "NUN-DTS 201", "Name": "Data Science", "Lecturer": "Noah Gana", "Level": "200L-IS", "Credit": 2, "Category": "Core", "Dept": "IS", "Prio": 2},
        {"Code": "INS 207", "Name": "Intro to IS", "Lecturer": "Prince Eru", "Level": "200L-IS", "Credit": 2, "Category": "Core", "Dept": "IS", "Prio": 2},
        {"Code": ".IFT 302", "Name": "Web App Dev", "Lecturer": "Prince Eru", "Level": "300L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 3},
        {"Code": "NUN-.IFT 303", "Name": "Enterprise Systems", "Lecturer": "Dr. Ridwan", "Level": "300L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 3},
        {"Code": "NUN-.IFT 307", "Name": "SDN", "Lecturer": "Dr. Temitope", "Level": "300L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 3},
        {"Code": ".IFT 308", "Name": "Ethics and Legal IT", "Lecturer": "Dr. Ridwan", "Level": "300L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 3},
        {"Code": ".IFT 342", "Name": "Network Servers", "Lecturer": "Mr. Solomon", "Level": "300L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 3},
        {"Code": "ICT 305", "Name": "Data Communications", "Lecturer": "Mr. Solomon", "Level": "300L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 3},
        {"Code": "IFT 401", "Name": "IT Project Mgt", "Lecturer": "Dr. Ridwan", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 4},
        {"Code": ".IFT 403", "Name": "Mobile Computing", "Lecturer": "Ahmed Adeniyi", "Level": "400L-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 4},
        {"Code": "IFT 413", "Name": "Research Methodology", "Lecturer": "Prof. Prema", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 4},
        {"Code": "IFT 425", "Name": "E-Commerce", "Lecturer": "Dr. Ridwan", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 4},
        {"Code": "IFT 433", "Name": "Operational Mgt", "Lecturer": "Dr. Temitope", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 4},
        {"Code": "IFT 443", "Name": "Network Security", "Lecturer": "Mr. Solomon", "Level": "400L-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 4},
        {"Code": "CSC 709", "Name": "System Analysis", "Lecturer": "Adeniyi Ahmed", "Level": "PGD-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 5},
        {"Code": "IFT 701", "Name": "Database Apps", "Lecturer": "Mr. Solomon", "Level": "PGD-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 5},
        {"Code": "IFT 703", "Name": "MIS", "Lecturer": "Dr. Temitope", "Level": "PGD-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 5},
        {"Code": "IFT 711", "Name": "Info Security", "Lecturer": "Prince Eru", "Level": "PGD-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 5},
        {"Code": "SEN 705", "Name": "OOAD", "Lecturer": "Dr. Anka", "Level": "PGD-IT", "Credit": 2, "Category": "Core", "Dept": "IT", "Prio": 5},
        {"Code": "CSC 811", "Name": "Advanced Programming", "Lecturer": "Assoc. Prof. Akande", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 6},
        {"Code": "IFT 801", "Name": "IT Project Mgt", "Lecturer": "Prof. Prema", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 6},
        {"Code": "IFT 803", "Name": "HCI for IS", "Lecturer": "Dr. Temi", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 6},
        {"Code": "IFT 807", "Name": "Information Security", "Lecturer": "Dr. Nurudeen", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 6},
        {"Code": "IFT 809", "Name": "Cyber Law", "Lecturer": "Dr. Ridwan", "Level": "MSC-IT", "Credit": 3, "Category": "Core", "Dept": "IT", "Prio": 6},
    ]

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'courses_db' not in st.session_state:
    st.session_state.courses_db = load_db()

# --- 3. UNIVERSITY RESOURCE CONSTRAINTS ---
ROOMS = {
    "E101 (Congo)": {"cap": 60},
    "E102 (Congo)": {"cap": 60},
    "E026 (Congo)": {"cap": 190, "avail": {"Monday": (9,11), "Tuesday": (13,17), "Wednesday": (9,13)}},
    "E020 (Congo)": {"cap": 160, "avail": {"Friday": (9,17)}},
    "E125 (Congo)": {"cap": 160, "avail": {"Monday": (9,17)}},
    "D008": {"cap": 130},
    "F206 (Ubangi)": {"cap": 60},
}

CLASS_POPULATIONS = {
    "100L-IT": 100, "100L-IS": 100, "200L-IT": 169, "200L-IS": 94,
    "300L-IT": 113, "400L-IT": 71, "PGD-IT": 20, "MSC-IT": 40
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# --- 4. THE BALANCED QUEUEING ENGINE ---
class BalancedQueueEngine:
    def __init__(self, courses):
        # Multi-stage sorting for optimal outcome
        cat_map = {"Core": 1, "Common": 2, "Elective": 3}
        self.courses = sorted(courses, key=lambda x: (cat_map.get(x['Category'], 4), x['Prio'], -x['Credit']))
        self.schedule = []
        self.busy = set() # Store as (EntityName, Day, Hour)

    def is_free(self, entity, d, h): return (entity, d, h) not in self.busy

    def run(self):
        for course in self.courses:
            placed = False
            duration = int(course['Credit'])
            target_size = CLASS_POPULATIONS.get(course['Level'], 50)
            
            # Day Shuffling Heuristic: Prevents clustering on Monday
            search_days = DAYS.copy()
            random.shuffle(search_days)
            
            for d in search_days:
                # Slot preferences: UG Morning/Afternoon, PG Afternoon/Evening
                h_range = range(15, 19-duration+1) if course['Prio'] >= 5 else range(9, 18-duration+1)
                
                for start_h in h_range:
                    slots = list(range(start_h, start_h + duration))
                    
                    for r_name, r_meta in ROOMS.items():
                        # Hard Constraint 1: Capacity
                        if r_meta['cap'] < target_size: continue
                        
                        # Hard Constraint 2: Room Specific Window
                        if "avail" in r_meta:
                            win = r_meta['avail'].get(d)
                            if not win or not (slots[0] >= win[0] and slots[-1] < win[1]): continue
                        
                        # Hard Constraint 3: Multi-Entity Conflict (Room, Lecturer, and Level Group)
                        if all(self.is_free(r_name, d, h) for h in slots) and \
                           all(self.is_free(course['Lecturer'], d, h) for h in slots) and \
                           all(self.is_free(course['Level'], d, h) for h in slots):
                            
                            # Book the block
                            for h in slots:
                                self.busy.add((r_name, d, h))
                                self.busy.add((course['Lecturer'], d, h))
                                self.busy.add((course['Level'], d, h))
                            
                            self.schedule.append({
                                **course, "Day": d, 
                                "Time": f"{start_h:02d}:00 - {(start_h + duration):02d}:00",
                                "Room": r_name, "RoomCap": r_meta['cap'], "ActualSize": target_size
                            })
                            placed = True; break
                    if placed: break
                if placed: break
            if not placed:
                self.schedule.append({**course, "Day": "OVERFLOW", "Time": "N/A", "Room": "N/A", "RoomCap": 0, "ActualSize": target_size})
        return pd.DataFrame(self.schedule)

# --- 5. EXCEL EXPORTERS (Professional Deliverables) ---
def get_timetable_grid_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        title_fmt = workbook.add_format({'bold': True, 'bg_color': NAVY, 'font_color': 'white', 'border': 1, 'align': 'center'})
        grid_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9})
        header_fmt = workbook.add_format({'bold': True, 'bg_color': '#f1f5f9', 'border': 1})

        for lvl in sorted(df['Level'].unique()):
            sub = df[df['Level'] == lvl]
            sheet = lvl.replace("-", " ")
            time_labels = [f"{h:02d}:00 - {(h+1):02d}:00" for h in range(9, 18)]
            grid = pd.DataFrame(index=time_labels, columns=DAYS).fillna("")
            
            for _, row in sub.iterrows():
                if row['Day'] != "OVERFLOW":
                    s_h = int(row['Time'].split(":")[0])
                    e_h = int(row['Time'].split(" - ")[1].split(":")[0])
                    for h in range(s_h, e_h):
                        grid.at[f"{h:02d}:00 - {(h+1):02d}:00", row['Day']] = f"{row['Code']}\n{row['Room']}\n{row['Lecturer']}"

            grid.to_excel(writer, sheet_name=sheet, startrow=3, startcol=0)
            sub[['Code', 'Name', 'Lecturer', 'Credit', 'Category']].to_excel(writer, sheet_name=sheet, startrow=3, startcol=8, index=False)
            
            ws = writer.sheets[sheet]
            ws.merge_range('A1:F2', f"NILE UNIVERSITY - {lvl} WEEKLY GRID", title_fmt)
            ws.merge_range('I1:M2', f"DEPARTMENTAL COURSE ALLOCATION", title_fmt)
            ws.set_column('A:A', 15, header_fmt)
            ws.set_column('B:F', 20, grid_fmt)
            ws.set_column('I:M', 20, grid_fmt)
    return output.getvalue()

def get_allocation_list_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df[['Level', 'Code', 'Name', 'Lecturer', 'Credit', 'Category']].to_excel(writer, sheet_name="Master Allocation", index=False)
    return output.getvalue()

# --- 6. UI INTERFACE ---
st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, {NAVY} 0%, {NILE_BLUE} 100%); border-radius: 15px; color: white; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 32px;">🏛️ {APP_NAME}</h1>
        <p style="margin:0; opacity: 0.9;">Professional Unified Simulation & Resource Architect | IT & IS Departments</p>
    </div>
    """, unsafe_allow_html=True)

nav = st.sidebar.radio("Main Menu", ["🛠️ Admin: Course Management", "⚙️ Engine: Simulation Run", "📈 Analytics: Performance"])

if nav == "🛠️ Admin: Course Management":
    st.header("🛠️ Super Admin Rights: Course Database")
    st.info("Management page for Course Codes, Lecturers, and Categories. Changes are persistent.")
    
    col1, col2 = st.columns([1, 4])
    dept_f = col1.selectbox("Filter View", ["All", "IT", "IS"])
    db_df = pd.DataFrame(st.session_state.courses_db)
    if dept_f != "All": db_df = db_df[db_df['Level'].str.contains(dept_f)]
    
    edited = st.data_editor(db_df, num_rows="dynamic", use_container_width=True)
    if st.button("💾 Synchronize & Save Changes"):
        st.session_state.courses_db = edited.to_dict('records')
        save_db(st.session_state.courses_db)
        st.success("Database Saved Successfully! Data remains even if you refresh.")

elif nav == "⚙️ Engine: Simulation Run":
    st.header("⚙️ Queueing Simulation Engine")
    st.write("Generating a balanced, conflict-free timetable using stochastic Day-Rotation logic.")
    
    if st.button("🚀 EXECUTE GENERATOR"):
        with st.spinner("Calculating Optimal Resource Distribution..."):
            eng = BalancedQueueEngine(st.session_state.courses_db)
            st.session_state.results = eng.run()
        st.balloons()
    
    if 'results' in st.session_state:
        res = st.session_state.results
        lv = st.selectbox("Academic Level View", sorted(res['Level'].unique()))
        st.dataframe(res[res['Level'] == lv], use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("📥 Professional Deliverables")
        colA, colB = st.columns(2)
        colA.download_button("📥 Download Weekly Grid Excel", get_timetable_grid_excel(res), f"Nile_Weekly_Grid_{datetime.now().strftime('%Y%m%d')}.xlsx")
        colB.download_button("📥 Download Allocation Report Excel", get_allocation_list_excel(res), f"Nile_Allocation_Report_{datetime.now().strftime('%Y%m%d')}.xlsx")

elif nav == "📈 Analytics: Performance":
    st.header("📈 Efficiency & Infrastructure Reports")
    if 'results' in st.session_state:
        res_ok = st.session_state.results[st.session_state.results['Day'] != "OVERFLOW"]
        
        st.subheader("Spatial Fitting (Capacity vs. Student Count)")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=res_ok['Code'], y=res_ok['RoomCap'], name='Room Max Capacity', marker_color=NAVY))
        fig.add_trace(go.Bar(x=res_ok['Code'], y=res_ok['ActualSize'], name='Actual Student Count', marker_color=GOLD))
        fig.update_layout(barmode='group', title="Aiming for Optimal Room Utilization")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Lecturer Load Distribution")
        load = res_ok.groupby('Lecturer')['Credit'].sum().reset_index()
        st.plotly_chart(px.pie(load, values='Credit', names='Lecturer', hole=0.4), use_container_width=True)
    else:
        st.info("Run the simulation first to view analytics.")

st.divider()
st.caption(f"FCOM Timetable Project | Nile University Faculty of Computing | Version 6.0")
