import streamlit as st
import time

# ==========================================
# 1. การตั้งค่าหน้าเว็บ (Web Configuration)
# ==========================================
st.set_page_config(page_title="Piccolo Analytics Hub", layout="wide", initial_sidebar_state="expanded")

# ตกแต่ง UI ด้วย CSS
st.markdown("""
    <style>
    .big-font { font-size: 24px !important; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #00ff00; }
    /* ปุ่มบาคาร่า */
    div.stButton > button:first-child { font-weight: bold; font-size: 18px; height: 3em;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. เมนู Sidebar สลับโหมดการทำงาน
# ==========================================
st.sidebar.title("🔥 เลือกโหมดการทำงาน")
mode = st.sidebar.radio("ระบบวิเคราะห์ (Analytics Engine)", ["⚽ Football Pro Analyzer", "🃏 Baccarat AI Tracker (V2)"])
st.sidebar.markdown("---")

# ==========================================
# 3. หมวดวิเคราะห์ฟุตบอล (Football Pro Analyzer)
# ==========================================
if mode == "⚽ Football Pro Analyzer":
    st.title("⚽ ระบบวิเคราะห์ฟุตบอลขั้นเทพ (Odds Flow & xG)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📋 ข้อมูลแมตช์")
        home = st.text_input("เจ้าบ้าน", "Tottenham Hotspur")
        away = st.text_input("ทีมเยือน", "Arsenal")
        fav = st.selectbox("ทีมต่อคือใคร?", ["เจ้าบ้าน", "ทีมเยือน"])
        
    with col2:
        st.subheader("💰 ทิศทางราคา (Odds)")
        hdp_open = st.number_input("ราคาต่อรอง (เปิด)", value=0.5, step=0.25)
        hdp_close = st.number_input("ราคาต่อรอง (ปัจจุบัน)", value=0.25, step=0.25)
        
    with col3:
        st.subheader("📊 สถิติความคาดหวัง (xG)")
        xg_home = st.number_input("xG เจ้าบ้าน", value=1.8, step=0.1)
        xg_away = st.number_input("xG ทีมเยือน", value=1.2, step=0.1)
        
    st.markdown("---")
    if st.button("⚡ กดเพื่อสแกนทรรศนะฟุตบอล", use_container_width=True, type="primary"):
        with st.spinner('กำลังเจาะระบบเทียบราคาเจ้ามือ...'):
            time.sleep(1)
            odds_dropped = hdp_close < hdp_open
            xg_diff = xg_home - xg_away if fav == "เจ้าบ้าน" else xg_away - xg_home
            
            st.subheader("🎯 สรุปการฟันธง (AI Verdict)")
            if odds_dropped and xg_diff > 0.3:
                st.success(f"🔥 ฟันธง: **ต่อ {home if fav=='เจ้าบ้าน' else away}** (ราคาไหลลง + xG ข่ม)")
            elif not odds_dropped and xg_diff < 0:
                st.warning(f"💎 ฟันธง: **รอง {away if fav=='เจ้าบ้าน' else home}** (สวนราคาเจ้ามือ)")
            else:
                st.info("➖ ฟันธง: **ข้าม (No Bet) หรือ รอดูราคาหน้างาน**")

# ==========================================
# 4. หมวดวิเคราะห์บาคาร่า (Baccarat AI Tracker V2)
# ==========================================
elif mode == "🃏 Baccarat AI Tracker (V2)":
    st.title("🃏 Baccarat AI: Advanced Pattern Recognition")
    st.markdown("คลิกบันทึกผลแต่ละไม้ ระบบจะอ่านเค้าไพ่และคำนวณไม้ถัดไปให้อัตโนมัติ")
    
    # ใช้งาน Session State เพื่อจำประวัติไพ่โดยไม่ต้องพิมพ์ใหม่
    if 'bac_history' not in st.session_state:
        st.session_state.bac_history = []
        
    # UI ปุ่มกด
    st.subheader("👉 บันทึกผลไม้ล่าสุด")
    btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns(5)
    
    if btn_col1.button("🔵 PLAYER", use_container_width=True):
        st.session_state.bac_history.append('P')
    if btn_col2.button("🔴 BANKER", use_container_width=True):
        st.session_state.bac_history.append('B')
    if btn_col3.button("🟢 TIE (เสมอ)", use_container_width=True):
        st.session_state.bac_history.append('T')
    if btn_col4.button("↩️ ลบไม้ล่าสุด", use_container_width=True):
        if len(st.session_state.bac_history) > 0:
            st.session_state.bac_history.pop()
    if btn_col5.button("🗑️️ ล้างกระดาน (เริ่มขอนใหม่)", use_container_width=True):
        st.session_state.bac_history = []

    # แสดงประวัติไพ่บนหน้าจอ
    st.markdown("### 📊 ประวัติไพ่ขอนนี้ (Board History)")
    history_str = " ".join([("🔵" if x=='P' else "🔴" if x=='B' else "🟢") for x in st.session_state.bac_history])
    st.write(history_str if history_str else "ยังไม่มีข้อมูล กรุณากดบันทึกผล")
    
    st.markdown("---")
    
    # ==========================================
    # ลอจิก AI วิเคราะห์เค้าไพ่ขั้นสูง (Pattern Engine)
    # ==========================================
    # ตัด Tie ออกจากการคำนวณเค้าไพ่หลัก
    core_history = [x for x in st.session_state.bac_history if x != 'T']
    
    if len(core_history) < 2:
        st.info("⚠️ ขอข้อมูลอย่างน้อย 2-3 ไม้ เพื่อเริ่มจับแพทเทิร์นเค้าไพ่")
    else:
        last2 = core_history[-2:]
        last3 = core_history[-3:] if len(core_history) >= 3 else []
        last4 = core_history[-4:] if len(core_history) >= 4 else []
        
        pred = ""
        reason = ""
        confidence = 0
        
        # 1. เช็คเค้ามังกร (ไหลยาว 3 ไม้ติดขึ้นไป)
        if last3 == ['P', 'P', 'P']:
            pred, reason, confidence = "🔵 PLAYER", "เค้ามังกรน้ำเงิน (ตามน้ำจนกว่าจะขาด)", 85
        elif last3 == ['B', 'B', 'B']:
            pred, reason, confidence = "🔴 BANKER", "เค้ามังกรแดง (ตามน้ำจนกว่าจะขาด)", 85
            
        # 2. เช็คเค้าปิงปอง (สลับ 3 ไม้ติด)
        elif last3 == ['P', 'B', 'P']:
            pred, reason, confidence = "🔴 BANKER", "เค้าปิงปอง (แทงสลับ)", 80
        elif last3 == ['B', 'P', 'B']:
            pred, reason, confidence = "🔵 PLAYER", "เค้าปิงปอง (แทงสลับ)", 80
            
        # 3. เช็คเค้าสองตัวตัด
        elif last4 == ['P', 'P', 'B', 'B']:
            pred, reason, confidence = "🔵 PLAYER", "เค้าสองตัวตัด (เปลี่ยนฝั่ง)", 75
        elif last4 == ['B', 'B', 'P', 'P']:
            pred, reason, confidence = "🔴 BANKER", "เค้าสองตัวตัด (เปลี่ยนฝั่ง)", 75
            
        # 4. หากไม่เข้าแพทเทิร์นหลัก ให้ตามเค้าไพ่ล่าสุด (ไม่สวน)
        else:
            last_win = core_history[-1]
            if last_win == 'P':
                pred, reason, confidence = "🔵 PLAYER", "เค้าไพ่ไม่ชัดเจน (ไหลตามผู้ชนะล่าสุด)", 55
            else:
                pred, reason, confidence = "🔴 BANKER", "เค้าไพ่ไม่ชัดเจน (อิงสถิติ Banker ได้เปรียบ)", 55

        # คำนวณขนาดไม้ (Money Management)
        stake = "2 ไม้ (อัดได้)" if confidence >= 75 else "1 ไม้ (เดินเบา)"
        if confidence <= 60: stake = "1 ไม้ หรือ ข้าม (รอดูเค้า)"

        # แสดงผลการวิเคราะห์
        st.subheader("🤖 AI ฟันธงไม้ต่อไป (Prediction)")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("แทงฝั่ง (Bet On)", pred)
        c2.metric("เค้าไพ่ที่พบ (Pattern)", reason)
        c3.metric("เดินเงิน (Money Mgmt)", stake)
        
        st.write(f"**ความมั่นใจของ AI:** {confidence}%")
        st.progress(confidence)
