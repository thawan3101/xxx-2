import streamlit as st
import random
import time
from collections import Counter

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI เค้าไพ่ อัตโนมัติ",
    layout="centered"
)

st.title("🃏 AI วิเคราะห์เค้าไพ่ (อัตโนมัติ)")

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "vip_until" not in st.session_state:
    st.session_state.vip_until = 0

# ---------------- VIP FUNCTIONS ----------------
def is_vip():
    return time.time() < st.session_state.vip_until

def vip_remaining_minutes():
    return max(0, int((st.session_state.vip_until - time.time()) / 60))

# ---------------- VIP STATUS ----------------
st.subheader("💎 สถานะสมาชิก")

if is_vip():
    st.success(f"VIP ใช้งานได้อีก {vip_remaining_minutes()} นาที")
else:
    st.warning("คุณยังไม่ได้เป็น VIP")

# ---------------- VIP PURCHASE ----------------
with st.expander("💳 ซื้อ VIP"):
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💰 5 บาท / 1 ชม."):
            st.session_state.vip_until = time.time() + (1 * 60 * 60)
            st.success("เปิด VIP 1 ชั่วโมงแล้ว")

        if st.button("💰 10 บาท / 2 ชม."):
            st.session_state.vip_until = time.time() + (2 * 60 * 60)
            st.success("เปิด VIP 2 ชั่วโมงแล้ว")

    with col2:
        if st.button("💰 20 บาท / 4 ชม."):
            st.session_state.vip_until = time.time() + (4 * 60 * 60)
            st.success("เปิด VIP 4 ชั่วโมงแล้ว")

        if st.button("💰 50 บาท / 1 วัน"):
            st.session_state.vip_until = time.time() + (24 * 60 * 60)
            st.success("เปิด VIP 24 ชั่วโมงแล้ว")

    st.caption("⚠️ ตอนนี้เป็นโหมดทดสอบ (ยังไม่ผูกชำระเงินจริง)")

# ---------------- GAME SELECT ----------------
game = st.selectbox(
    "🎮 เลือกเกม",
    ["บาคาร่า", "เสือมังกร", "แดงดำ"]
)

# ---------------- IMAGE UPLOAD ----------------
img = st.file_uploader(
    "📸 อัปโหลดรูปผลล่าสุด (แคปหน้าจอได้)",
    type=["png", "jpg", "jpeg"]
)

# ---------------- GAME LOGIC ----------------
if img:
    st.image(img, use_container_width=True)

    if game == "บาคาร่า":
        choices = ["ผู้เล่น", "เจ้ามือ", "เสมอ"]
    elif game == "เสือมังกร":
        choices = ["เสือ", "มังกร"]
    else:
        choices = ["แดง", "ดำ"]

    # เพิ่มผลล่าสุด (จำลอง AI อ่านรูป)
    st.session_state.history.append(random.choice(choices))

    # วิเคราะห์สถิติ
    st.divider()
    st.subheader("📊 สถิติย้อนหลัง")

    cnt = Counter(st.session_state.history)
    for k, v in cnt.items():
        st.write(f"{k} = {v} ครั้ง ({v/len(st.session_state.history)*100:.1f}%)")

    # ---------------- PREDICTION ----------------
    def predict_next(history, choices, n=10):
        result = []
        last = history[-1]
        for _ in range(n):
            if random.random() < 0.6:
                result.append(last)
            else:
                result.append(random.choice(choices))
        return result

    st.divider()
    st.subheader("🔮 คาดการณ์ล่วงหน้า")

    if is_vip():
        preds = predict_next(st.session_state.history, choices, 10)
        for i, p in enumerate(preds, 1):
            st.write(f"ตาที่ {i} → {p}")
    else:
        st.error("🔒 ฟีเจอร์นี้สำหรับ VIP เท่านั้น")

# ---------------- RESET ----------------
st.divider()
if st.button("🔄 รีเซ็ตทั้งหมด"):
    st.session_state.history = []
    st.experimental_rerun()
