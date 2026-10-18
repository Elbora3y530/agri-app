import streamlit as st
import json
import os
import pandas as pd

# إعدادات الصفحة والتصميم
st.set_page_config(
    page_title="شركة الرحمة لإدارة الأراضي",
    page_icon="🌱",
    layout="wide"
)

# تطبيق تنسيقات CSS لتحسين الإدخال، تحديد المربع النشط باللون الأزرق، وتنسيق الموبايل
st.markdown("""
    <style>
    /* تحسين إطار التركيز الأزرق للمربعات */
    div[data-baseweb="input"] input:focus, div[data-baseweb="select"] input:focus {
        border-color: #1E88E5 !important;
        box-shadow: 0 0 8px rgba(30, 136, 229, 0.5) !important;
    }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        border-radius: 8px !important;
        font-size: 16px !important;
    }
    /* تحسين مظهر الكروت والبطاقات */
    .css-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #e9ecef;
        margin-bottom: 15px;
    }
    /* طباعة كشف الحساب */
    @media print {
        .no-print { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "agri_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "lands": {},
        "stations": {}
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تهيئة بيانات الحلسة
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# الشاشة الرئيسية والعنوان
st.title("🌱 شركة الرحمة لإدارة الأراضي")
st.caption("📞 تليفون: 01000000000 | 01100000000")

# تسجيل الدخول البسيط
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("login_form"):
        st.subheader("🔒 يرجى إدخال كلمة السر للدخول للنظام")
        pwd = st.text_input("كلمة السر", type="password")
        btn = st.form_submit_button("تسجيل الدخول")
        if btn:
            if pwd == "1234":  # يمكنك تغيير كلمة السر هنا
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("كلمة السر غير صحيحة!")
    st.stop()

# القائمة الرئيسية
menu = st.sidebar.radio(
    "القائمة الرئيسية",
    ["🏜️ حسابات الأراضي", "🏭 توريد المحطات", "📈 صافي أرباح الأراضي", "📊 الموقف المالي"]
)

# ---------------------------------------------------------
# 1. حسابات الأراضي
# ---------------------------------------------------------
if menu == "🏜️ حسابات الأراضي":
    st.header("🏜️ إدارة حسابات الأراضي والعملاء")
    
    # إضافة أرض/عميل جديد
    with st.expander("➕ إضافة أرض / عميل جديد"):
        with st.form("add_land_form", clear_on_submit=True):
            land_name = st.text_input("اسم العميل / الأرض")
            land_type = st.selectbox("نوع التعامل / العميل", ["بطاطا تحت الشرب", "بطاطا صادر في البوكسة"])
            submit_land = st.form_submit_button("إضافة العملاء / الأرض")
            if submit_land and land_name:
                if land_name not in data["lands"]:
                    data["lands"][land_name] = {
                        "type": land_type,
                        "expenses": [],
                        "supplies": [],
                        "payments": []
                    }
                    save_data(data)
                    st.success(f"تمت إضافة العميل {land_name} بنجاح!")
                    st.rerun()
                else:
                    st.warning("اسم العميل موجود بالفعل!")

    lands_list = list(data["lands"].keys())
    if not lands_list:
        st.info("لا يوجد عملاء مضافين حتى الآن.")
    else:
        selected_land = st.selectbox("اختر العميل / الأرض لمراجعة الحسابات", lands_list)
        land_info = data["lands"][selected_land]
        land_type = land_info.get("type", "بطاطا تحت الشرب")
        
        st.subheader(f"صفحة حساب: {selected_land} ({land_type})")

        # ------------------- نوع 1: بطاطا تحت الشرب -------------------
        if land_type == "بطاطا تحت الشرب":
            tab1, tab2 = st.tabs(["➕ إضافة مصروفات / دفعات", "📋 كشف الحساب والعمليات"])
            
            with tab1:
                with st.form("under_drinking_expense_form", clear_on_submit=True):
                    st.write("##### إضافة مصروف جديد")
                    exp_option = st.selectbox("نوع المصروف", ["جراندات", "أنفار", "فطار", "مناديب", "شكاير", "آخر (اكتب يدوي)"])
                    custom_exp = st.text_input("اكتب نوع المصروف (إذا اخترت آخر)")
                    exp_type = custom_exp if exp_option == "آخر (اكتب يدوي)" and custom_exp else exp_option
                    
                    amount = st.number_input("المبلغ / القيمة (جنيه)", min_value=0.0, step=50.0)
                    submit_exp = st.form_submit_button("حفظ وإضافة المصروف (Enter ↵)")
                    if submit_exp and amount > 0:
                        land_info["expenses"].append({"type": exp_type, "amount": amount})
                        save_data(data)
                        st.success("تم تسجيل المصروف بنجاح!")
                        st.rerun()

                with st.form("under_drinking_payment_form", clear_on_submit=True):
                    st.write("##### إضافة دفعة/فلوس أخذها صاحب الأرض")
                    pay_amount = st.number_input("المبلغ المدفوع لصاحب الأرض (جنيه)", min_value=0.0, step=50.0)
                    pay_note = st.text_input("ملاحظات / البيان")
                    submit_pay = st.form_submit_button("حفظ الدفعة (Enter ↵)")
                    if submit_pay and pay_amount > 0:
                        land
