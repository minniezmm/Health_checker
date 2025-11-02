import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import os

# ---------------------------------------------------
# ⚙️ CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Smart Health Checker",
    page_icon="🩺",
    layout="wide"
)

st.sidebar.title("🩺 Smart Health Checker")
page = st.sidebar.radio("Pages", [
    "Home",
    "Health Data Entry",
    "AI Risk Prediction",
    "Personalized Dashboard"
])

DATA_FILE = "health_data.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Name","Age","Gender","Height","Weight","BMI","Exercise","Smoking","Alcohol"]).to_csv(DATA_FILE, index=False)

# ---------------------------------------------------
# 1️⃣ HOME
# ---------------------------------------------------
if page == "Home":
    st.title("Smart Health Checker: Data-driven Wellness Dashboard")
    st.markdown("""
    ### 
    ระบบแดชบอร์ดสุขภาพอัจฉริยะ ที่ขับเคลื่อนด้วยข้อมูล (Data-driven)
    เพื่อช่วยให้ผู้ใช้สามารถติดตามสุขภาพของตนเองได้แบบเรียลไทม์
    พร้อมระบบ AI สำหรับประเมินและทำนายความเสี่ยงสุขภาพเบื้องต้น
    """)

    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966485.png", width=200)
    st.markdown("#### Smart Foundation")
    st.write("""
    - AI Risk Assessment  
    - Smart BMI Analysis  
    - Personalized Dashboard  
    - Basic Health Insights
    """)
    st.info("เริ่มต้นโดยไปที่เมนู **Health Data Entry** เพื่อกรอกข้อมูลสุขภาพของคุณ")

# ---------------------------------------------------
# HEALTH DATA ENTRY
# ---------------------------------------------------
elif page == "Health Data Entry":
    st.title("Health Data Entry")
    st.markdown("กรอกข้อมูลสุขภาพของคุณเพื่อใช้ในการประเมินความเสี่ยง")

    name = st.text_input("ชื่อ - นามสกุล")
    age = st.number_input("อายุ (ปี)", 0, 120, 30)
    gender = st.radio("เพศ", ["ชาย", "หญิง"])
    height = st.number_input("ส่วนสูง (cm)", 100, 220, 170)
    weight = st.number_input("น้ำหนัก (kg)", 30, 200, 65)
    exercise = st.slider("ออกกำลังกาย (ชม./สัปดาห์)", 0, 20, 3)
    smoking = st.radio("สูบบุหรี่หรือไม่", ["ไม่สูบ", "สูบ"])
    alcohol = st.radio("ดื่มแอลกอฮอล์หรือไม่", ["ไม่ดื่ม", "ดื่ม"])

    bmi = round(weight / ((height / 100) ** 2), 2)
    st.metric("ค่า BMI ของคุณ", f"{bmi}")

    if st.button("บันทึกข้อมูลของคุณ"):
        df = pd.read_csv(DATA_FILE)
        new_row = pd.DataFrame([{
            "Name": name, "Age": age, "Gender": gender,
            "Height": height, "Weight": weight,
            "BMI": bmi, "Exercise": exercise,
            "Smoking": smoking, "Alcohol": alcohol
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("บันทึกข้อมูลเรียบร้อย")

# ---------------------------------------------------
# 3️⃣ AI RISK PREDICTION
# ---------------------------------------------------
elif page == "AI Risk Prediction":
    st.title("AI Health Risk Prediction")
    st.markdown("ใช้ Machine Learning ประเมินความเสี่ยงสุขภาพเบื้องต้น (เช่น โรคเบาหวาน, โรคหัวใจ)")

    st.info("🔹 ใน Phase 1 จะใช้โมเดลจำลอง (mock model) เพื่อสาธิตผลลัพธ์\n🔹 ใน Phase 2 สามารถฝึกโมเดลจริงจาก dataset ได้ (เช่น UCI Heart Disease)")

    # Mock prediction
    df = pd.read_csv(DATA_FILE)
    if len(df) == 0:
        st.warning("ยังไม่มีข้อมูลสุขภาพ กรุณากรอกข้อมูลก่อนในเมนู 💉 Health Data Entry")
    else:
        selected_name = st.selectbox("เลือกชื่อเพื่อประเมิน", df["Name"].unique())
        user = df[df["Name"] == selected_name].iloc[0]
        risk_score = (
            (user["BMI"] - 18.5) * 0.2 +
            (user["Age"] / 50) * 0.3 +
            (0 if user["Exercise"] >= 3 else 1) * 0.5 +
            (1 if user["Smoking"] == "สูบ" else 0) * 0.5
        )

        risk_level = "ต่ำ" if risk_score < 1 else "ปานกลาง" if risk_score < 2 else "สูง"
        color = "#00C853" if risk_level == "ต่ำ" else "#FFD600" if risk_level == "ปานกลาง" else "#D50000"
        icon = "🟢" if risk_level == "ต่ำ" else "🟡" if risk_level == "ปานกลาง" else "🔴"

        st.markdown(f"""
        <div style='padding:15px;border-left:5px solid {color};border-radius:8px;background-color:{color}20'>
        <h3 style='color:{color};text-align:center'>{icon} ระดับความเสี่ยงสุขภาพ: {risk_level}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📈 ปัจจัยที่มีผลต่อความเสี่ยง")
        fig = px.bar(
            x=["BMI", "Age", "Exercise", "Smoking"],
            y=[user["BMI"], user["Age"], user["Exercise"], 1 if user["Smoking"] == "สูบ" else 0],
            color=["BMI", "Age", "Exercise", "Smoking"],
            title="Health Risk Factors Overview"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# 4️⃣ PERSONALIZED DASHBOARD
# ---------------------------------------------------
elif page == "Personalized Dashboard":
    st.title("Personalized Health Dashboard")
    st.markdown("ดูสรุปข้อมูลสุขภาพและกราฟแนวโน้ม")

    df = pd.read_csv(DATA_FILE)
    if len(df) == 0:
        st.warning("ยังไม่มีข้อมูลในระบบ กรุณากรอกข้อมูลก่อน")
    else:
        st.dataframe(df, use_container_width=True)

        # แสดงแนวโน้ม BMI ตามอายุ
        st.markdown("### 📉 แนวโน้ม BMI ตามอายุ")
        fig_bmi = px.scatter(df, x="Age", y="BMI", color="Gender", size="Exercise",
                             title="BMI vs Age", hover_name="Name")
        st.plotly_chart(fig_bmi, use_container_width=True)

        st.markdown("### 🔍 สรุปเชิงลึก")
        avg_bmi = df["BMI"].mean()
        st.info(f"ค่า BMI เฉลี่ยของผู้ใช้ทั้งหมด = {avg_bmi:.2f}")

st.sidebar.markdown("---")
st.sidebar.caption("พัฒนาโดย Mintz Lab 🧠 | DADS5001 Final Project")


