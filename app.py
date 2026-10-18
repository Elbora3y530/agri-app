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

# تطبيق تنسيقات CSS لتحسين الإدخال وتحديد المربع النشط باللون الأزرق
st.markdown("""
    <style>
    div[data-baseweb="input"] input:focus, div[data-baseweb="select"] input:focus {
        border-color: #1E88E5 !important;
        box-shadow: 0 0 8px rgba(30, 136, 229, 0.5) !important;
    }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        border-radius: 8px !important;
        font-size: 16px !important;
    }
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
                content = json.load(f)
                if isinstance(content, dict):
                    if "lands" not in content:
                        content["lands"] = {}
                    if "stations" not in content:
                        content["stations"] = {}
                    return content
        except Exception:
            pass
    return {
        "lands": {},
        "stations": {}
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# الشاشة الرئيسية والعنوان مع الأرقام القديمة
st.title("🌱 شركة الرحمة لإدارة الأراضي")
st.caption("📞 تليفون: 01025700760 | 01090449553")

# تسجيل الدخول بكلمة السر الجديدة 332007
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("login_form"):
        st.subheader("🔒 يرجى إدخال كلمة السر للدخول للنظام")
        pwd = st.text_input("كلمة السر", type="password")
        btn = st.form_submit_button("تسجيل الدخول")
        if btn:
            if pwd == "332007":
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

        # --- النوع الأول: بطاطا تحت الشرب ---
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
                        land_info["payments"].append({"amount": pay_amount, "note": pay_note})
                        save_data(data)
                        st.success("تم تسجيل الدفعة بنجاح!")
                        st.rerun()

            with tab2:
                total_expenses = sum(x["amount"] for x in land_info.get("expenses", []))
                total_payments = sum(x["amount"] for x in land_info.get("payments", []))
                
                col1, col2 = st.columns(2)
                col1.metric("إجمالي المصاريف", f"{total_expenses:,.2f} جنيه")
                col2.metric("إجمالي المبالغ المستلمة (دفوعات)", f"{total_payments:,.2f} جنيه")

                st.write("---")
                st.write("##### جدول المصروفات")
                if land_info.get("expenses"):
                    df_exp = pd.DataFrame(land_info["expenses"])
                    st.dataframe(df_exp, use_container_width=True)
                    if st.button("🗑️ مسح آخر مصروف"):
                        land_info["expenses"].pop()
                        save_data(data)
                        st.rerun()

        # --- النوع الثاني: بطاطا صادر في البوكسة ---
        else:
            tab1, tab2 = st.tabs(["➕ إدخال حركة جديدة", "🧾 كشف الحساب والطباعة"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    with st.form("box_exp_form", clear_on_submit=True):
                        st.write("##### إضافة مصروفات")
                        exp_opt = st.selectbox("نوع المصروف", ["جراندات", "أنفار", "فطار", "مناديب", "شكاير", "آخر"])
                        cust_exp = st.text_input("نوع مصروف مخصص")
                        e_type = cust_exp if exp_opt == "آخر" and cust_exp else exp_opt
                        val = st.number_input("القيمة (جنيه)", min_value=0.0)
                        if st.form_submit_button("حفظ المصروف"):
                            land_info["expenses"].append({"type": e_type, "amount": val})
                            save_data(data)
                            st.success("تم الحفظ!")
                            st.rerun()

                with col2:
                    with st.form("box_pay_form", clear_on_submit=True):
                        st.write("##### فلوس أخذها صاحب الأرض")
                        p_val = st.number_input("المبلغ (جنيه)", min_value=0.0)
                        if st.form_submit_button("حفظ الدفعة"):
                            land_info["payments"].append({"amount": p_val})
                            save_data(data)
                            st.success("تم الحفظ!")
                            st.rerun()

                st.write("---")
                with st.form("box_supply_form", clear_on_submit=True):
                    st.write("##### إضافة توريد بطاطا صادر")
                    raw_weight = st.number_input("وزن بطاطا صادر خام (كجم)", min_value=0.0)
                    discount_rate = st.number_input("نسبة الخصم (%)", min_value=0.0, max_value=100.0)
                    price_per_kg = st.number_input("السعر للكيلو (جنيه)", min_value=0.0)
                    
                    if st.form_submit_button("حفظ التوريد (Enter ↵)"):
                        net_weight = raw_weight * (1 - (discount_rate / 100.0))
                        total_price = net_weight * price_per_kg
                        land_info["supplies"].append({
                            "raw_weight": raw_weight,
                            "discount_rate": discount_rate,
                            "net_weight": net_weight,
                            "price_per_kg": price_per_kg,
                            "total_price": total_price
                        })
                        save_data(data)
                        st.success("تم تسجيل توريد البطاطا الصادر بنجاح!")
                        st.rerun()

            with tab2:
                tot_exp = sum(x["amount"] for x in land_info.get("expenses", []))
                tot_pay = sum(x["amount"] for x in land_info.get("payments", []))
                tot_raw_w = sum(x.get("raw_weight", 0) for x in land_info.get("supplies", []))
                tot_net_w = sum(x.get("net_weight", 0) for x in land_info.get("supplies", []))
                tot_potato_val = sum(x.get("total_price", 0) for x in land_info.get("supplies", []))
                
                remaining_for_him = tot_potato_val - (tot_exp + tot_pay)

                st.markdown("### 📜 شركة الرحمة لإدارة الأراضي")
                st.caption(f"📞 تليفون: 01025700760 | 01090449553")
                st.caption(f"كشف حساب العميل: {selected_land} | نوع العميل: بطاطا صادر في البوكسة")
                st.write("---")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("إجمالي بطاطا صادر (خام)", f"{tot_raw_w:,.1f} كجم")
                c2.metric("إجمالي الوزن بعد الخصم", f"{tot_net_w:,.1f} كجم")
                c3.metric("إجمالي سعر البطاطا", f"{tot_potato_val:,.2f} جنيه")

                c4, c5, c6 = st.columns(3)
                c4.metric("إجمالي المصاريف", f"{tot_exp:,.2f} جنيه")
                c5.metric("إجمالي الفلوس التي أخذها", f"{tot_pay:,.2f} جنيه")
                
                balance_label = "باقي له" if remaining_for_him >= 0 else "باقي عليه"
                c6.metric(f"💰 النتيجة النهائية ({balance_label})", f"{abs(remaining_for_him):,.2f} جنيه")

                st.write("---")
                st.write("##### تفاصيل توريدات البطاطا")
                if land_info.get("supplies"):
                    df_s = pd.DataFrame(land_info["supplies"])
                    st.dataframe(df_s, use_container_width=True)

# ---------------------------------------------------------
# 2. توريد المحطات
# ---------------------------------------------------------
elif menu == "🏭 توريد المحطات":
    st.header("🏭 توريد المحطات والتوليدات")
    
    with st.expander("➕ إضافة محطة جديدة"):
        with st.form("add_station_form", clear_on_submit=True):
            st_name = st.text_input("اسم المحطة")
            if st.form_submit_button("حفظ المحطة") and st_name:
                if st_name not in data["stations"]:
                    data["stations"][st_name] = {"supplies": [], "payments": []}
                    save_data(data)
                    st.success("تمت إضافة المحطة!")
                    st.rerun()

    st_list = list(data["stations"].keys())
    if not st_list:
        st.info("لا توجد محطات مضافة حتى الآن.")
    else:
        selected_st = st.selectbox("اختر المحطة", st_list)
        st_data = data["stations"][selected_st]

        tot_supp_val = sum(x.get("total_price", 0) for x in st_data.get("supplies", []))
        tot_st_pay = sum(x.get("amount", 0) for x in st_data.get("payments", []))
        st_rem = tot_supp_val - tot_st_pay

        col_top1, col_top2, col_top3 = st.columns(3)
        col_top1.metric("إجمالي المستحق على المحطة", f"{tot_supp_val:,.2f} جنيه")
        col_top2.metric("💳 الفلوس التي دفعتها المحطة", f"{tot_st_pay:,.2f} جنيه")
        col_top3.metric("المبلغ المتبقي (لي عند المحطة)", f"{st_rem:,.2f} جنيه")

        st.write("---")
        t1, t2 = st.tabs(["➕ إضافة توريد / دفعة", "📊 السجلات والبيانات"])
        
        with t1:
            with st.form("station_supply_form", clear_on_submit=True):
                st.write("##### تسجيل توريد محطة")
                w_raw = st.number_input("الوزن الخام (كجم)", min_value=0.0)
                disc_type = st.radio("نوع الخصم", ["خصم بالكيلو", "خصم بالنسبة (%)"], horizontal=True)
                disc_val = st.number_input("قيمة الخصم", min_value=0.0)
                price_kg = st.number_input("سعر الكيلو (جنيه)", min_value=0.0)
                
                if st.form_submit_button("حفظ التوريد (Enter ↵)"):
                    if disc_type == "خصم بالكيلو":
                        w_net = max(0.0, w_raw - disc_val)
                    else:
                        w_net = w_raw * (1 - (disc_val / 100.0))
                    
                    tot_p = w_net * price_kg
                    st_data["supplies"].append({
                        "raw_weight": w_raw,
                        "discount_type": disc_type,
                        "discount_value": disc_val,
                        "net_weight": w_net,
                        "price_per_kg": price_kg,
                        "total_price": tot_p
                    })
                    save_data(data)
                    st.success("تم حفظ التوريد للمحطة!")
                    st.rerun()

            with st.form("station_pay_form", clear_on_submit=True):
                st.write("##### تسجيل دفعة مقبوضة من المحطة")
                st_p_amount = st.number_input("المبلغ المستلم من المحطة (جنيه)", min_value=0.0)
                if st.form_submit_button("حفظ الدفعة"):
                    st_data["payments"].append({"amount": st_p_amount})
                    save_data(data)
                    st.success("تم تسجيل الدفعة!")
                    st.rerun()

        with t2:
            st.write("##### توريدات المحطة")
            if st_data.get("supplies"):
                st.dataframe(pd.DataFrame(st_data["supplies"]), use_container_width=True)

# ---------------------------------------------------------
# 3. صافي أرباح الأراضي
# ---------------------------------------------------------
elif menu == "📈 صافي أرباح الأراضي":
    st.header("📈 تحديد الأرباح وتكلفة المبيعات")
    
    lands_list = list(data["lands"].keys())
    if not lands_list:
        st.info("قم بإضافة عملاء أولاً.")
    else:
        sel_l = st.selectbox("اختر العميل للبحث وعرض أوزان البطاطا", lands_list)
        l_info = data["lands"][sel_l]
        
        st.subheader(f"بيانات ومبيعات العميل: {sel_l}")
        
        supplies = l_info.get("supplies", [])
        if not supplies:
            st.warning("لا توجد توريدات مسجلة لهذا العميل حتى الآن.")
        else:
            st.write("##### قم بتحديد سعر البيع لكل توريد بشكل منفصل:")
            
            total_sales = 0.0
            for idx, sup in enumerate(supplies):
                with st.container():
                    st.markdown(f"**التوريد #{idx + 1}** - وزن الصافي: `{sup.get('net_weight', 0):,.1f} كجم`")
                    sell_price = st.number_input(f"سعر بيع التوريد #{idx + 1} (لكل كجم)", min_value=0.0, key=f"sell_{sel_l}_{idx}")
                    sub_total = sell_price * sup.get('net_weight', 0)
                    st.caption(f"إجمالي بيع التوريد: {sub_total:,.2f} جنيه")
                    total_sales += sub_total
                    st.write("---")

            tot_e = sum(x["amount"] for x in l_info.get("expenses", []))
            tot_p = sum(x["amount"] for x in l_info.get("payments", []))
            
            net_profit = total_sales - (tot_e + tot_p)

            m1, m2, m3 = st.columns(3)
            m1.metric("إجمالي المبيعات", f"{total_sales:,.2f} جنيه")
            m2.metric("التكلفة (مصاريف + دفوعات)", f"{(tot_e + tot_p):,.2f} جنيه")
            
            p_label = "صافي الربح 🟢" if net_profit >= 0 else "صافي الخسارة 🔴"
            m3.metric(p_label, f"{abs(net_profit):,.2f} جنيه")

# ---------------------------------------------------------
# 4. الموقف المالي
# ---------------------------------------------------------
elif menu == "📊 الموقف المالي":
    st.header("📊 الموقف المالي الشامل")
    
    total_due_from_stations = 0.0
    for st_n, st_v in data.get("stations", {}).items():
        s_val = sum(x.get("total_price", 0) for x in st_v.get("supplies", []))
        p_val = sum(x.get("amount", 0) for x in st_v.get("payments", []))
        total_due_from_stations += (s_val - p_val)

    total_due_to_clients = 0.0
    for l_n, l_v in data.get("lands", {}).items():
        if l_v.get("type") == "بطاطا صادر في البوكسة":
            tot_exp = sum(x["amount"] for x in l_v.get("expenses", []))
            tot_pay = sum(x["amount"] for x in l_v.get("payments", []))
            tot_potato_val = sum(x.get("total_price", 0) for x in l_v.get("supplies", []))
            rem = tot_potato_val - (tot_exp + tot_pay)
            if rem > 0:
                total_due_to_clients += rem

    col_f1, col_f2 = st.columns(2)
    col_f1.metric("💵 إجمالي المبالغ المستحقة لك (عند المحطات)", f"{total_due_from_stations:,.2f} جنيه")
    col_f2.metric("🔻 إجمالي المبالغ المستحقة عليك (باقي للعملاء)", f"{total_due_to_clients:,.2f} جنيه")
