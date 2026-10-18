# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import datetime
import json
import os

# ==========================================
# 🔐 إعدادات كلمة السر وملف الحفظ الدائم
# ==========================================
PASSWORD = "332007"
DATA_FILE = "agri_data.json"

# وظيفة لحفظ البيانات بصفة مستمرة ودائمة
def save_data():
    data = {
        "lands": st.session_state.lands,
        "land_accounts": st.session_state.land_accounts,
        "stations": st.session_state.stations,
        "station_supplies": st.session_state.station_supplies,
        "saved_profits": st.session_state.saved_profits,
        "client_settings": st.session_state.client_settings,
        "last_date": str(st.session_state.last_date)
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# وظيفة لتحميل البيانات المسجلة مسبقاً
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.lands = data.get("lands", [])
                st.session_state.land_accounts = data.get("land_accounts", [])
                st.session_state.stations = data.get("stations", [])
                st.session_state.station_supplies = data.get("station_supplies", [])
                st.session_state.saved_profits = data.get("saved_profits", {})
                st.session_state.client_settings = data.get("client_settings", {})
                
                last_d_str = data.get("last_date", str(datetime.date.today()))
                try:
                    st.session_state.last_date = datetime.datetime.strptime(last_d_str, "%Y-%m-%d").date()
                except Exception:
                    st.session_state.last_date = datetime.date.today()
        except Exception:
            pass

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="شركة الرحمة - نظام إدارة الأراضي والمحاصيل",
    page_icon="🌾",
    layout="wide"
)

# ==========================================
# 🎨 تنسيقات CSS العصرية لإخفاء الزائد والناقص وتحسين الواجهة
# ==========================================
st.markdown("""
    <style>
    /* إخفاء أزرار الزائد والناقص من خانات الأرقام تماماً لتكتب براحتك */
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
    input[type=number] {
      -moz-appearance: textfield;
    }
    
    /* تنسيق عام للخطوط والخلفيات والأزرار */
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #ced4da !important;
        padding: 10px !important;
        font-size: 16px !important;
    }
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
        border-color: #1E88E5 !important;
        box-shadow: 0 0 8px rgba(30, 136, 229, 0.3) !important;
    }
    
    /* كروت الإحصائيات الفخمة */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f1f3f5 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-right: 5px solid #1E88E5;
        margin-bottom: 15px;
    }
    
    @media print {
        .no-print { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lands" not in st.session_state:
    st.session_state.lands = []
if "land_accounts" not in st.session_state:
    st.session_state.land_accounts = []
if "stations" not in st.session_state:
    st.session_state.stations = []
if "station_supplies" not in st.session_state:
    st.session_state.station_supplies = []
if "saved_profits" not in st.session_state:
    st.session_state.saved_profits = {}
if "client_settings" not in st.session_state:
    st.session_state.client_settings = {}
if "last_date" not in st.session_state:
    st.session_state.last_date = datetime.date.today()

# تحميل البيانات عند بداية التشغيل
if "data_loaded" not in st.session_state:
    load_data()
    st.session_state.data_loaded = True


# ==========================================
# 🔒 شاشة تسجيل الدخول بكلمة السر
# ==========================================
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c_login1, c_login2, c_login3 = st.columns([1, 2, 1])
    with c_login2:
        st.markdown("<div style='text-align: center; padding: 30px; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
        st.markdown("<h2>🌾 شركة الرحمة لإدارة الأراضي</h2>", unsafe_allow_html=True)
        st.caption("📞 تليفون: 01019381124 | 01000108658")
        st.markdown("<hr>", unsafe_allow_html=True)
        input_pass = st.text_input("🔐 أدخل كلمة السر للدخول للنظام:", type="password")
        if st.button("تسجيل الدخول", type="primary", use_container_width=True):
            if input_pass == PASSWORD:
                st.session_state.authenticated = True
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("❌ كلمة السر غير صحيحة، يرجى المحاولة مرة أخرى.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ==========================================
# 📋 القائمة الجانبية (Sidebar) المحدثة والأنيقة
# ==========================================
st.sidebar.markdown("### 🌾 شركة الرحمة")
st.sidebar.caption("📞 01019381124 | 01000108658")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "انتقل إلى القسم:",
    [
        "1. حسابات الأراضي والعملاء",
        "2. التوريد للمحطات",
        "3. صافي أرباحي من الأرض",
        "4. الموقف المالي للشركة"
    ]
)

st.sidebar.markdown("---")
if st.sidebar.button("🔒 تسجيل الخروج", type="secondary", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()


# ==========================================
# 1. حسابات الأراضي والعملاء
# ==========================================
if app_mode == "1. حسابات الأراضي والعملاء":
    st.title("🌾 حسابات الأراضي والعملاء")
    st.caption("📞 تليفون: 01019381124 | 01000108658")
    
    tab_add_land, tab_client_page = st.tabs(["➕ إضافة أرض / عميل جديد", "📁 صفحة حسابات العملاء المخصصة"])
    
    with tab_add_land:
        st.subheader("تسجيل أرض وصاحب أرض جديد وتحديد نوع التعامل")
        with st.form("land_reg_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                owner_name = st.text_input("اسم صاحب الأرض (العميل)")
                phone_num = st.text_input("رقم التليفون")
            with c2:
                land_loc = st.text_input("موقع الأرض / الحوض")
                land_type = st.selectbox("نوع التعامل / العميل", ["بطاطا تحت الشرب", "بطاطا صادر في البوكسة"])
            
            save_l = st.form_submit_button("حفظ وحجز صفحة للعميل")
            if save_l:
                if owner_name.strip():
                    existing_names = [l["owner"] for l in st.session_state.lands]
                    if owner_name in existing_names:
                        st.warning("هذا العميل مسجل مسبقاً.")
                    else:
                        st.session_state.lands.append({
                            "owner": owner_name, 
                            "phone": phone_num, 
                            "location": land_loc,
                            "type": land_type
                        })
                        save_data()
                        st.success(f"تم إنشاء صفحة للعميل ({owner_name}) نوع ({land_type}) بنجاح وحفظها دائمياً!")
                        st.rerun()
                else:
                    st.error("يرجى إدخال اسم صاحب الأرض.")
                    
    with tab_client_page:
        if st.session_state.lands:
            land_list = [l["owner"] for l in st.session_state.lands]
            
            col_sel, col_del = st.columns([3, 1])
            with col_sel:
                selected_client = st.selectbox("اختر اسم العميل لفتح صفحته الخاصة:", land_list)
            with col_del:
                st.write("")
                st.write("")
                if st.button("🗑️ حذف العميل بالكامل", type="secondary"):
                    st.session_state.lands = [l for l in st.session_state.lands if l["owner"] != selected_client]
                    st.session_state.land_accounts = [r for r in st.session_state.land_accounts if r["owner"] != selected_client]
                    if selected_client in st.session_state.saved_profits:
                        del st.session_state.saved_profits[selected_client]
                    if selected_client in st.session_state.client_settings:
                        del st.session_state.client_settings[selected_client]
                    save_data()
                    st.success(f"تم حذف العميل ({selected_client}) وكل حركاته بنجاح!")
                    st.rerun()

            client_info = next((l for l in st.session_state.lands if l["owner"] == selected_client), None)
            
            if client_info:
                client_category = client_info.get("type", "بطاطا تحت الشرب")
                st.markdown("---")
                st.header(f"📂 صفحة العميل: {selected_client} — ({client_category})")
                st.write(f"📱 **رقم التليفون:** {client_info['phone']} | 📍 **موقع الأرض:** {client_info['location']}")
                
                # ---------------------------------------------------------
                # النوع الأول: بطاطا تحت الشرب
                # ---------------------------------------------------------
                if client_category == "بطاطا تحت الشرب":
                    with st.form(f"client_trans_{selected_client}", clear_on_submit=True):
                        st.subheader("تسجيل حركة جديدة (مصاريف، وارد، أو سلف نقدية)")
                        
                        col_tr1, col_tr2 = st.columns(2)
                        with col_tr1:
                            record_date = st.date_input("التاريخ", value=st.session_state.last_date)
                            exp_option = st.selectbox("نوع المصروف", ["بدون مصروف", "جراندات", "أنفار", "فطار", "مناديب", "شكاير", "آخر (اكتب يدوي)"])
                            custom_exp = st.text_input("اكتب نوع المصروف (إذا اخترت آخر)")
                            final_exp_desc = custom_exp if exp_option == "آخر (اكتب يدوي)" and custom_exp.strip() else (exp_option if exp_option != "بدون مصروف" else "بدون مصروف")
                            exp_amount = st.number_input("قيمة المصروف (جنيه)", min_value=0.0, step=1.0, format="%.2f")
                        
                        with col_tr2:
                            sader_weight = st.number_input("وارد صادر (بالوزن)", min_value=0.0, step=1.0, format="%.2f")
                            second_weight = st.number_input("وارد درجة ثانية (بالوزن)", min_value=0.0, step=1.0, format="%.2f")
                            farza_weight = st.number_input("وارد فرزة (بالوزن)", min_value=0.0, step=1.0, format="%.2f")
                            advanced_cash = st.number_input("استلام صاحب الأرض فلوس (سلفة نقدية)", min_value=0.0, step=1.0, format="%.2f")
                        
                        add_trans_btn = st.form_submit_button("إضافة الحركة إلى صفحة العميل")
                        
                        if add_trans_btn:
                            st.session_state.last_date = record_date
                            st.session_state.land_accounts.append({
                                "owner": selected_client,
                                "date": str(record_date),
                                "expense_desc": final_exp_desc,
                                "expense_amount": exp_amount,
                                "sader": sader_weight,
                                "second": second_weight,
                                "farza": farza_weight,
                                "advanced_cash": advanced_cash
                            })
                            save_data()
                            st.success(f"تمت إضافة الحركة بنجاح إلى صفحة {selected_client}!")
                            st.rerun()

                    st.markdown("---")
                    st.subheader(f"📊 جدول سجل حركات وتفاصيل أرض {selected_client}")
                    client_records = [r for r in st.session_state.land_accounts if r["owner"] == selected_client]
                    
                    if client_records:
                        # عرض الحركات في جدول مرتب كالأعمدة والصفوف
                        col_h1, col_h2, col_h3, col_h4, col_h5, col_h6, col_h7, col_h8 = st.columns([1.2, 1.2, 1, 1, 1, 1, 1, 0.6])
                        with col_h1: st.markdown("**التاريخ**")
                        with col_h2: st.markdown("**المصروف**")
                        with col_h3: st.markdown("**قيمة المصروف**")
                        with col_h4: st.markdown("**صادر**")
                        with col_h5: st.markdown("**ثانية**")
                        with col_h6: st.markdown("**فرزة**")
                        with col_h7: st.markdown("**سلفة**")
                        with col_h8: st.markdown("**حذف**")
                        st.markdown("---")

                        for idx, record in enumerate(client_records):
                            cols_row = st.columns([1.2, 1.2, 1, 1, 1, 1, 1, 0.6])
                            with cols_row[0]: st.write(f"📅 {record['date']}")
                            with cols_row[1]: st.write(f"{record.get('expense_desc', '-')}")
                            with cols_row[2]: st.write(f"{record.get('expense_amount', 0):,.2f} ج")
                            with cols_row[3]: st.write(f"{record.get('sader', 0):,.1f}")
                            with cols_row[4]: st.write(f"{record.get('second', 0):,.1f}")
                            with cols_row[5]: st.write(f"{record.get('farza', 0):,.1f}")
                            with cols_row[6]: st.write(f"{record.get('advanced_cash', 0):,.2f} ج")
                            with cols_row[7]:
                                if st.button("🗑️", key=f"del_client_rec_{selected_client}_{idx}"):
                                    st.session_state.land_accounts.remove(record)
                                    save_data()
                                    st.success("تم الحذف بنجاح!")
                                    st.rerun()
                        
                        st.markdown("---")
                        st.markdown("### 🧮 تصفية الحساب النهائي:")
                        current_client_settings = st.session_state.client_settings.get(selected_client, {"discount": 0.0, "price": 0.0})
                        
                        with st.form(f"settlement_form_{selected_client}"):
                            col_f1, col_f2 = st.columns(2)
                            with col_f1:
                                discount_pct = st.number_input("نسبة الخصم (%)", min_value=0.0, max_value=100.0, value=float(current_client_settings.get("discount", 0.0)), step=1.0, format="%.2f")
                            with col_f2:
                                price_per_unit = st.number_input("سعر الوحدة (جنيه)", min_value=0.0, value=float(current_client_settings.get("price", 0.0)), step=1.0, format="%.2f")
                            
                            save_settings_btn = st.form_submit_button("💾 حفظ نسبة الخصم والسعر")
                            if save_settings_btn:
                                st.session_state.client_settings[selected_client] = {"discount": discount_pct, "price": price_per_unit}
                                save_data()
                                st.success("تم حفظ إعدادات الحساب بنجاح!")
                        
                        active_discount = st.session_state.client_settings.get(selected_client, {}).get("discount", 0.0)
                        active_price = st.session_state.client_settings.get(selected_client, {}).get("price", 0.0)
                        
                        total_sader = sum(r.get("sader", 0) for r in client_records)
                        total_second = sum(r.get("second", 0) for r in client_records)
                        total_farza = sum(r.get("farza", 0) for r in client_records)
                        gross_weight = total_sader + total_second + total_farza
                        
                        discount_value = gross_weight * (active_discount / 100.0)
                        net_weight = gross_weight - discount_value
                        total_money_value = net_weight * active_price
                        total_advanced = sum(r.get("advanced_cash", 0) for r in client_records)
                        total_expenses = sum(r.get("expense_amount", 0) for r in client_records)
                        
                        remaining_balance = total_money_value - (total_advanced + total_expenses)
                        
                        st.info(f"""
                        * **إجمالي الأوزان:** {gross_weight:,.2f}
                        * **نسبة الخصم ({active_discount}%):** {discount_value:,.2f}
                        * **صافي الوزن:** {net_weight:,.2f}
                        * **إجمالي القيمة:** {total_money_value:,.2f} جنيه
                        * **إجمالي المصاريف:** {total_expenses:,.2f} جنيه
                        * **إجمالي السلف:** {total_advanced:,.2f} جنيه
                        """)
                        st.success(f"### 💰 باقي له نهائياً: {remaining_balance:,.2f} جنيه")

                    else:
                        st.info("لا توجد حركات مسجلة لهذا العميل حتى الآن.")

                # ---------------------------------------------------------
                # النوع الثاني: بطاطا صادر في البوكسة
                # ---------------------------------------------------------
                else:
                    with st.form(f"box_client_trans_{selected_client}", clear_on_submit=True):
                        st.subheader("تسجيل توريد ومصاريف (صادر في البوكسة)")
                        
                        c_b1, c_b2 = st.columns(2)
                        with c_b1:
                            b_date = st.date_input("التاريخ", value=st.session_state.last_date)
                            b_exp_opt = st.selectbox("نوع المصروف", ["بدون مصروف", "جراندات", "أنفار", "فطار", "مناديب", "شكاير", "آخر (اكتب يدوي)"])
                            b_cust_exp = st.text_input("اكتب نوع المصروف المخصص")
                            b_final_desc = b_cust_exp if b_exp_opt == "آخر (اكتب يدوي)" and b_cust_exp.strip() else (b_exp_opt if b_exp_opt != "بدون مصروف" else "بدون مصروف")
                            b_exp_amt = st.number_input("قيمة المصروف (جنيه)", min_value=0.0, step=1.0, format="%.2f")
                        with c_b2:
                            b_raw_w = st.number_input("وزن بطاطا صادر خام", min_value=0.0, step=1.0, format="%.2f")
                            b_disc_pct = st.number_input("نسبة الخصم (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0, format="%.2f")
                            b_price = st.number_input("سعر الكيلو", min_value=0.0, step=1.0, format="%.2f")
                            b_adv_cash = st.number_input("فلوس أخذها صاحب الأرض (سلفة)", min_value=0.0, step=1.0, format="%.2f")

                        calc_net_w = b_raw_w - (b_raw_w * (b_disc_pct / 100.0))
                        calc_tot_p = calc_net_w * b_price
                        st.info(f"📌 **معاينة:** الوزن بعد الخصم = `{calc_net_w:,.2f}` | 💵 **الإجمالي:** `{calc_tot_p:,.2f}` جنيه")

                        add_box_btn = st.form_submit_button("حفظ حركة الصادر في البوكسة")
                        if add_box_btn:
                            st.session_state.last_date = b_date
                            st.session_state.land_accounts.append({
                                "owner": selected_client,
                                "date": str(b_date),
                                "expense_desc": b_final_desc,
                                "expense_amount": b_exp_amt,
                                "raw_weight": b_raw_w,
                                "discount_pct": b_disc_pct,
                                "net_weight": calc_net_w,
                                "price": b_price,
                                "total_price": calc_tot_p,
                                "advanced_cash": b_adv_cash
                            })
                            save_data()
                            st.success("تم حفظ الحركة بنجاح!")
                            st.rerun()

                    st.markdown("---")
                    st.subheader(f"📋 جدول حركات صادر البوكسة: {selected_client}")
                    box_records = [r for r in st.session_state.land_accounts if r["owner"] == selected_client and "raw_weight" in r]

                    if box_records:
                        # جدول لعرض صادر البوكسة
                        col_bh1, col_bh2, col_bh3, col_bh4, col_bh5, col_bh6, col_bh7, col_bh8, col_bh9 = st.columns([1.1, 1.1, 1, 1, 1, 1, 1, 1, 0.6])
                        with col_bh1: st.markdown("**التاريخ**")
                        with col_bh2: st.markdown("**المصروف**")
                        with col_bh3: st.markdown("**قيمة المصروف**")
                        with col_bh4: st.markdown("**خام**")
                        with col_bh5: st.markdown("**الخصم %**")
                        with col_bh6: st.markdown("**الصافي**")
                        with col_bh7: st.markdown("**السعر**")
                        with col_bh8: st.markdown("**السلفة**")
                        with col_bh9: st.markdown("**حذف**")
                        st.markdown("---")

                        for b_idx, b_rec in enumerate(box_records):
                            cols_brow = st.columns([1.1, 1.1, 1, 1, 1, 1, 1, 1, 0.6])
                            with cols_brow[0]: st.write(f"📅 {b_rec['date']}")
                            with cols_brow[1]: st.write(f"{b_rec.get('expense_desc', '-')}")
                            with cols_brow[2]: st.write(f"{b_rec.get('expense_amount', 0):,.2f} ج")
                            with cols_brow[3]: st.write(f"{b_rec.get('raw_weight', 0):,.1f}")
                            with cols_brow[4]: st.write(f"{b_rec.get('discount_pct', 0)}%")
                            with cols_brow[5]: st.write(f"**{b_rec.get('net_weight', 0):,.1f}**")
                            with cols_brow[6]: st.write(f"{b_rec.get('price', 0):,.2f}")
                            with cols_brow[7]: st.write(f"{b_rec.get('advanced_cash', 0):,.2f} ج")
                            with cols_brow[8]:
                                if st.button("🗑️", key=f"del_box_rec_{selected_client}_{b_idx}"):
                                    st.session_state.land_accounts.remove(b_rec)
                                    save_data()
                                    st.success("تم الحذف بنجاح!")
                                    st.rerun()

                        st.markdown("---")
                        tot_exp_box = sum(r.get('expense_amount', 0) for r in box_records)
                        tot_raw_box = sum(r.get('raw_weight', 0) for r in box_records)
                        tot_net_box = sum(r.get('net_weight', 0) for r in box_records)
                        tot_price_box = sum(r.get('total_price', 0) for r in box_records)
                        tot_adv_box = sum(r.get('advanced_cash', 0) for r in box_records)
                        
                        final_box_rem = tot_price_box - (tot_exp_box + tot_adv_box)

                        st.info(f"""
                        * **إجمالي المصاريف:** {tot_exp_box:,.2f} جنيه
                        * **إجمالي وزن البطاطا الصادر (خام):** {tot_raw_box:,.2f} كجم
                        * **إجمالي وزن البطاطا بعد الخصم:** {tot_net_box:,.2f} كجم
                        * **إجمالي سعر البطاطا:** {tot_price_box:,.2f} جنيه
                        * **إجمالي الفلوس التي أخذها صاحب الأرض:** {tot_adv_box:,.2f} جنيه
                        """)
                        st.success(f"### 💰 باقي له نهائياً: {final_box_rem:,.2f} جنيه")

                        if st.button(f"🖨️ طباعة كشف حساب صادر البوكسة: {selected_client}", key=f"print_box_{selected_client}"):
                            st.markdown("---")
                            print_box_html = f"""
                            <div style="text-align: center; border: 2px solid #333; padding: 25px; border-radius: 10px;">
                                <h2>شركة الرحمة لإدارة الأراضي</h2>
                                <p><b>أرقام التليفونات:</b> 01019381124 | 01000108658</p>
                                <h3>كشف حساب نهائي (صادر في البوكسة): {selected_client}</h3>
                                <hr>
                                <p><b>إجمالي المصاريف:</b> {tot_exp_box:,.2f} جنيه</p>
                                <p><b>إجمالي وزن البطاطا الصادر خام:</b> {tot_raw_box:,.2f} كجم</p>
                                <p><b>إجمالي وزن البطاطا بعد الخصم:</b> {tot_net_box:,.2f} كجم</p>
                                <p><b>إجمالي سعر البطاطا:</b> {tot_price_box:,.2f} جنيه</p>
                                <p><b>إجمالي الفلوس التي أخذها:</b> {tot_adv_box:,.2f} جنيه</p>
                                <h2>المبلغ الباقي له نهائياً: {final_box_rem:,.2f} جنيه</h2>
                            </div>
                            <script>window.print();</script>
                            """
                            st.markdown(print_box_html, unsafe_allow_html=True)
                    else:
                        st.info("لا توجد حركات صادر في البوكسة مسجلة حتى الآن.")
        else:
            st.warning("يرجى إضافة عميل/أرض أولاً.")


# ==========================================
# 2. التوريد للمحطات
# ==========================================
elif app_mode == "2. التوريد للمحطات":
    st.title("🏭 التوريد للمحطات وحساباتها")
    st.caption("📞 تليفون: 01019381124 | 01000108658")
    
    tab_add_st, tab_st_page = st.tabs(["➕ تسجيل محطة جديدة", "📁 صفحات المحطات والتوريدات اليومية"])
    
    with tab_add_st:
        st.subheader("تسجيل محطة جديدة في النظام")
        with st.form("add_station_form", clear_on_submit=True):
            col_st1, col_st2 = st.columns(2)
            with col_st1:
                st_name_input = st.text_input("اسم المحطة")
            with col_st2:
                st_phone_input = st.text_input("رقم تليفون المحطة")
                
            save_st_btn = st.form_submit_button("حفظ وحجز صفحة للمحطة")
            if save_st_btn:
                if st_name_input.strip():
                    existing_st = [s["name"] for s in st.session_state.stations]
                    if st_name_input.strip() in existing_st:
                        st.warning("هذه المحطة مسجلة مسبقاً.")
                    else:
                        st.session_state.stations.append({"name": st_name_input.strip(), "phone": st_phone_input.strip()})
                        save_data()
                        st.success(f"تمت إضافة المحطة ({st_name_input.strip()}) بنجاح!")
                        st.rerun()
                else:
                    st.error("يرجى إدخال اسم المحطة.")
                    
    with tab_st_page:
        if st.session_state.stations:
            station_list = [s["name"] for s in st.session_state.stations]
            
            col_st_sel, col_st_del = st.columns([3, 1])
            with col_st_sel:
                selected_station = st.selectbox("اختر المحطة لفتح صفحتها الخاصة:", station_list)
            with col_st_del:
                st.write("")
                st.write("")
                if st.button("🗑️ حذف المحطة بالكامل", type="secondary"):
                    st.session_state.stations = [s for s in st.session_state.stations if s["name"] != selected_station]
                    st.session_state.station_supplies = [s for s in st.session_state.station_supplies if s["station"] != selected_station]
                    save_data()
                    st.success("تم حذف المحطة بنجاح!")
                    st.rerun()

            st_info = next((s for s in st.session_state.stations if s["name"] == selected_station), None)
            
            if st_info:
                st.markdown("---")
                st.header(f"🏭 الصفحة الخاصة بالمحطة: {selected_station}")
                st.write(f"📱 **رقم تليفون المحطة:** {st_info['phone']}")
                
                st_records = [s for s in st.session_state.station_supplies if s["station"] == selected_station]
                total_raw_w = sum(s.get("weight", 0) for s in st_records)
                total_net_w = sum(s.get("net_weight", 0) for s in st_records)
                total_station_money = sum(s.get("total_money", 0) for s in st_records)
                total_station_paid = sum(s.get("paid_amount", 0) for s in st_records)
                remaining_on_station = total_station_money - total_station_paid

                st.markdown("---")
                st.subheader("📊 ملخص الحساب الفوري مع المحطة:")
                col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
                with col_m1:
                    st.metric("إجمالي الوزن الخام", f"{total_raw_w:,.2f}")
                with col_m2:
                    st.metric("إجمالي الوزن بعد الخصم", f"{total_net_w:,.2f}")
                with col_m3:
                    st.metric("إجمالي فلوس البطاطا", f"{total_station_money:,.2f} ج")
                with col_m4:
                    st.metric("إجمالي ما دفعته المحطة", f"{total_station_paid:,.2f} ج")
                with col_m5:
                    st.metric("باقي ليا عند المحطة", f"{remaining_on_station:,.2f} ج")
                st.markdown("---")

                with st.form(f"trans_st_{selected_station}", clear_on_submit=True):
                    st.subheader("تسجيل توريد سيارة جديد ودفعات نقدية")
                    
                    c_st_a, c_st_b = st.columns(2)
                    with c_st_a:
                        sup_date = st.date_input("تاريخ التوريد", value=st.session_state.last_date)
                        car_number = st.text_input("رقم السيارة")
                        raw_weight = st.number_input("الوزن الخام", min_value=0.0, step=1.0, format="%.2f")
                        paid_today = st.number_input("المبلغ الذي دفعته المحطة اليوم (إن وجدت)", min_value=0.0, step=1.0, value=0.0, format="%.2f")
                    with c_st_b:
                        disc_type = st.radio("نوع الخصم", ["خصم بالنسبة (%)", "خصم بالكيلو"], horizontal=True)
                        disc_val = st.number_input("قيمة الخصم", min_value=0.0, step=1.0, format="%.2f")
                        price_st = st.number_input("السعر", min_value=0.0, step=1.0, format="%.2f")
                    
                    if disc_type == "خصم بالنسبة (%)":
                        calc_net_w = raw_weight - (raw_weight * (disc_val / 100.0))
                    else:
                        calc_net_w = max(0.0, raw_weight - disc_val)

                    calc_total = calc_net_w * price_st
                    st.info(f"📌 **معاينة سريعة للتوريد:** الوزن بعد الخصم = `{calc_net_w:,.2f}` | 💵 **الإجمالي:** `{calc_total:,.2f}` جنيه")
                        
                    add_st_sup = st.form_submit_button("حفظ التوريد لصفحة المحطة")
                    
                    if add_st_sup:
                        st.session_state.last_date = sup_date
                        st.session_state.station_supplies.append({
                            "station": selected_station,
                            "date": str(sup_date),
                            "car": car_number,
                            "weight": raw_weight,
                            "disc_type": disc_type,
                            "discount": disc_val,
                            "net_weight": calc_net_w,
                            "price": price_st,
                            "total_money": calc_total,
                            "paid_amount": paid_today
                        })
                        save_data()
                        st.success("تم حفظ التوريد بنجاح!")
                        st.rerun()

                st.markdown("---")
                if st_records:
                    st.subheader(f"📋 جدول حركات وتوريدات محطة: {selected_station}")
                    
                    # جدول عريض ومنسق كالأعمدة والصفوف
                    c_h1, c_h2, c_h3, c_h4, c_h5, c_h6, c_h7, c_h8, c_h9 = st.columns([1.2, 1, 1, 1, 1, 0.8, 1.2, 1.2, 0.6])
                    with c_h1: st.markdown("**التاريخ**")
                    with c_h2: st.markdown("**رقم السيارة**")
                    with c_h3: st.markdown("**الوزن الخام**")
                    with c_h4: st.markdown("**الخصم**")
                    with c_h5: st.markdown("**الصافي**")
                    with c_h6: st.markdown("**السعر**")
                    with c_h7: st.markdown("**الإجمالي**")
                    with c_h8: st.markdown("**المدفوع**")
                    with c_h9: st.markdown("**حذف**")
                    st.markdown("---")

                    for idx_st, s_rec in enumerate(st_records):
                        cols_row = st.columns([1.2, 1, 1, 1, 1, 0.8, 1.2, 1.2, 0.6])
                        d_type_lbl = "%" if s_rec.get('disc_type') == "خصم بالنسبة (%)" else "كجم"
                        
                        with cols_row[0]: st.write(f"📅 {s_rec['date']}")
                        with cols_row[1]: st.write(f"🚗 {s_rec.get('car', '-')}")
                        with cols_row[2]: st.write(f"{s_rec.get('weight', 0):,.1f}")
                        with cols_row[3]: st.write(f"{s_rec.get('discount', 0)} {d_type_lbl}")
                        with cols_row[4]: st.write(f"**{s_rec.get('net_weight', 0):,.1f}**")
                        with cols_row[5]: st.write(f"{s_rec.get('price', 0):,.2f}")
                        with cols_row[6]: st.write(f"**{s_rec.get('total_money', 0):,.2f} ج**")
                        with cols_row[7]: st.write(f"{s_rec.get('paid_amount', 0):,.2f} ج")
                        with cols_row[8]:
                            if st.button("🗑️", key=f"del_st_tbl_{selected_station}_{idx_st}"):
                                st.session_state.station_supplies.remove(s_rec)
                                save_data()
                                st.success("تم الحذف بنجاح!")
                                st.rerun()
                else:
                    st.info("لا توجد توريدات مسجلة لهذه المحطة حتى الآن.")
        else:
            st.warning("يرجى إضافة محطة أولاً.")


# ==========================================
# 3. صافي أرباحي من الأرض
# ==========================================
elif app_mode == "3. صافي أرباحي من الأرض":
    st.title("📈 صفحة أرباحي الخاصة من الأراضي")
    st.caption("📞 تليفون: 01019381124 | 01000108658")
    
    if st.session_state.lands:
        land_list = [l["owner"] for l in st.session_state.lands]
        selected_prof_owner = st.selectbox("ابحث واختار العميل لعرض وتحديد أسعار بيع أوزان البطاطا:", land_list)
        
        owner_recs = [r for r in st.session_state.land_accounts if r["owner"] == selected_prof_owner]
        
        st.markdown("---")
        st.subheader(f"🌾 جدول أوزان البطاطا المسجلة للعميل: {selected_prof_owner}")

        if owner_recs:
            saved_profits_dict = st.session_state.saved_profits.get(selected_prof_owner, {})
            
            total_sales_revenue = 0.0
            total_expenses_p = sum(r.get("expense_amount", 0) for r in owner_recs)
            total_advanced_p = sum(r.get("advanced_cash", 0) for r in owner_recs)

            with st.form(f"detailed_profit_form_{selected_prof_owner}"):
                st.markdown("##### قم بتحديد سعر البيع لكل وزنة على حدة في الجدول أدناه:")
                
                # جدول أرباح الأراضي
                cp_h1, cp_h2, cp_h3, cp_h4 = st.columns([1.5, 1.5, 2, 2])
                with cp_h1: st.markdown("**التاريخ**")
                with cp_h2: st.markdown("**نوع الوِزنة**")
                with cp_h3: st.markdown("**الوزن**")
                with cp_h4: st.markdown("**سعر البيع (أنت تكتبه)**")
                st.markdown("---")

                for idx, rec in enumerate(owner_recs):
                    rec_date = rec.get("date", "بدون تاريخ")
                    sad_w = rec.get("sader", 0.0)
                    sec_w = rec.get("second", 0.0)
                    far_w = rec.get("farza", 0.0)
                    raw_b_w = rec.get("raw_weight", 0.0)
                    net_b_w = rec.get("net_weight", 0.0)

                    if sad_w > 0:
                        cols_cp = st.columns([1.5, 1.5, 2, 2])
                        with cols_cp[0]: st.write(f"📅 {rec_date}")
                        with cols_cp[1]: st.write("وارد صادر")
                        with cols_cp[2]: st.write(f"{sad_w:,.1f} كجم")
                        with cols_cp[3]:
                            st.number_input(f"سعر صادر #{idx}", min_value=0.0, value=float(saved_profits_dict.get(f"sad_{idx}", 0.0)), step=1.0, format="%.2f", key=f"p_sad_{selected_prof_owner}_{idx}", label_visibility="collapsed")
                    
                    if sec_w > 0:
                        cols_cp = st.columns([1.5, 1.5, 2, 2])
                        with cols_cp[0]: st.write(f"📅 {rec_date}")
                        with cols_cp[1]: st.write("درجة ثانية")
                        with cols_cp[2]: st.write(f"{sec_w:,.1f} كجم")
                        with cols_cp[3]:
                            st.number_input(f"سعر ثانية #{idx}", min_value=0.0, value=float(saved_profits_dict.get(f"sec_{idx}", 0.0)), step=1.0, format="%.2f", key=f"p_sec_{selected_prof_owner}_{idx}", label_visibility="collapsed")

                    if far_w > 0:
                        cols_cp = st.columns([1.5, 1.5, 2, 2])
                        with cols_cp[0]: st.write(f"📅 {rec_date}")
                        with cols_cp[1]: st.write("فرزة")
                        with cols_cp[2]: st.write(f"{far_w:,.1f} كجم")
                        with cols_cp[3]:
                            st.number_input(f"سعر فرزة #{idx}", min_value=0.0, value=float(saved_profits_dict.get(f"far_{idx}", 0.0)), step=1.0, format="%.2f", key=f"p_far_{selected_prof_owner}_{idx}", label_visibility="collapsed")

                    if raw_b_w > 0:
                        cols_cp = st.columns([1.5, 1.5, 2, 2])
                        with cols_cp[0]: st.write(f"📅 {rec_date}")
                        with cols_cp[1]: st.write("صادر بوكسة (صافي)")
                        with cols_cp[2]: st.write(f"{net_b_w:,.1f} كجم")
                        with cols_cp[3]:
                            st.number_input(f"سعر بوكسة #{idx}", min_value=0.0, value=float(saved_profits_dict.get(f"box_{idx}", 0.0)), step=1.0, format="%.2f", key=f"p_box_{selected_prof_owner}_{idx}", label_visibility="collapsed")

                st.markdown("---")
                save_all_prices = st.form_submit_button("💾 حفظ أسعار البيع وحساب صافي الربح / الخسارة النهائي")
                
                if save_all_prices:
                    temp_dict = {}
                    for idx, rec in enumerate(owner_recs):
                        if rec.get("sader", 0.0) > 0:
                            temp_dict[f"sad_{idx}"] = st.session_state.get(f"p_sad_{selected_prof_owner}_{idx}", 0.0)
                        if rec.get("second", 0.0) > 0:
                            temp_dict[f"sec_{idx}"] = st.session_state.get(f"p_sec_{selected_prof_owner}_{idx}", 0.0)
                        if rec.get("farza", 0.0) > 0:
                            temp_dict[f"far_{idx}"] = st.session_state.get(f"p_far_{selected_prof_owner}_{idx}", 0.0)
                        if rec.get("raw_weight", 0.0) > 0:
                            temp_dict[f"box_{idx}"] = st.session_state.get(f"p_box_{selected_prof_owner}_{idx}", 0.0)
                    
                    st.session_state.saved_profits[selected_prof_owner] = temp_dict
                    save_data()
                    st.success("تم حفظ أسعار البيع والنتائج بنجاح!")
                    st.rerun()

            final_sales_rev = 0.0
            for idx, rec in enumerate(owner_recs):
                saved_item_prices = saved_profits_dict
                if rec.get("sader", 0.0) > 0:
                    final_sales_rev += rec.get("sader", 0.0) * saved_item_prices.get(f"sad_{idx}", 0.0)
                if rec.get("second", 0.0) > 0:
                    final_sales_rev += rec.get("second", 0.0) * saved_item_prices.get(f"sec_{idx}", 0.0)
                if rec.get("farza", 0.0) > 0:
                    final_sales_rev += rec.get("farza", 0.0) * saved_item_prices.get(f"far_{idx}", 0.0)
                if rec.get("raw_weight", 0.0) > 0:
                    final_sales_rev += rec.get("net_weight", 0.0) * saved_item_prices.get(f"box_{idx}", 0.0)

            total_cost = total_expenses_p + total_advanced_p
            net_profit_loss = final_sales_rev - total_cost

            st.markdown("---")
            st.subheader(f"📊 ملخص النتيجة المالية لأرض: {selected_prof_owner}")
            
            res_col1, res_col2, res_col3, res_col4 = st.columns(4)
            with res_col1:
                st.metric("إجمالي قيمة البيع", f"{final_sales_rev:,.2f} جنيه")
            with res_col2:
                st.metric("إجمالي المصاريف", f"{total_expenses_p:,.2f} جنيه")
            with res_col3:
                st.metric("ما أخذه صاحب الأرض", f"{total_advanced_p:,.2f} جنيه")
            with res_col4:
                st.metric("صافي النتيجة", f"{net_profit_loss:,.2f} جنيه")
                
            if net_profit_loss > 0:
                st.success(f"🎉 **صافي المكسب للأرض:** {net_profit_loss:,.2f} جنيه")
            elif net_profit_loss < 0:
                st.error(f"⚠️ **صافي الخسارة للأرض:** {abs(net_profit_loss):,.2f} جنيه")
            else:
                st.info("⚖️ **النتيجة متكافئة.**")
        else:
            st.info("لا توجد حركات مسجلة لهذا العميل حتى الآن.")
    else:
        st.warning("يرجى إضافة أراضٍ مسجلة أولاً.")


# ==========================================
# 4. الموقف المالي للشركة
# ==========================================
elif app_mode == "4. الموقف المالي للشركة":
    st.title("💼 الموقف المالي الشامل للشركة")
    st.caption("📞 تليفون: 01019381124 | 01000108658")
    st.markdown("متابعة لحظية لإجمالي الأموال التي لك لدى المحطات، والمبالغ المستحقة للعملاء (الباقي له).")
    st.markdown("---")
    
    total_all_stations_remaining = 0.0
    for st_obj in st.session_state.stations:
        st_name = st_obj["name"]
        st_recs = [s for s in st.session_state.station_supplies if s["station"] == st_name]
        if st_recs:
            t_money = sum(s.get("total_money", 0) for s in st_recs)
            t_paid = sum(s.get("paid_amount", 0) for s in st_recs)
            total_all_stations_remaining += (t_money - t_paid)

    total_all_clients_remaining = 0.0
    for land_obj in st.session_state.lands:
        c_name = land_obj["owner"]
        c_type = land_obj.get("type", "بطاطا تحت الشرب")
        c_recs = [r for r in st.session_state.land_accounts if r["owner"] == c_name]
        
        if c_type == "بطاطا تحت الشرب" and c_recs:
            c_settings = st.session_state.client_settings.get(c_name, {"discount": 0.0, "price": 0.0})
            c_disc = c_settings.get("discount", 0.0)
            c_price = c_settings.get("price", 0.0)
            
            c_gross = sum(r.get("sader", 0) + r.get("second", 0) + r.get("farza", 0) for r in c_recs)
            c_net_w = c_gross - (c_gross * (c_disc / 100.0))
            c_total_val = c_net_w * c_price
            c_advanced = sum(r.get("advanced_cash", 0) for r in c_recs)
            c_exp = sum(r.get("expense_amount", 0) for r in c_recs)
            
            c_rem = c_total_val - (c_advanced + c_exp)
            if c_rem > 0:
                total_all_clients_remaining += c_rem

        elif c_type == "بطاطا صادر في البوكسة" and c_recs:
            box_recs = [r for r in c_recs if "raw_weight" in r]
            if box_recs:
                tot_exp_b = sum(r.get("expense_amount", 0) for r in box_recs)
                tot_price_b = sum(r.get("total_price", 0) for r in box_recs)
                tot_adv_b = sum(r.get("advanced_cash", 0) for r in box_recs)
                box_rem = tot_price_b - (tot_exp_b + tot_adv_b)
                if box_rem > 0:
                    total_all_clients_remaining += box_rem

    col_fin1, col_fin2 = st.columns(2)
    with col_fin1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏭 إجمالي الفلوس اللي ليك بره</h3>
            <h2 style="color: #1E88E5;">{total_all_stations_remaining:,.2f} جنيه</h2>
            <p>مستحقات لك لدى المحطات</p>
        </div>
        """, unsafe_allow_html=True)
    with col_fin2:
        st.markdown(f"""
        <div class="metric-card" style="border-right-color: #e03131;">
            <h3>🌾 إجمالي الفلوس اللي عليك بره</h3>
            <h2 style="color: #e03131;">{total_all_clients_remaining:,.2f} جنيه</h2>
            <p>مستحقات للعملاء (باقي له)</p>
        </div>
        """, unsafe_allow_html=True)
