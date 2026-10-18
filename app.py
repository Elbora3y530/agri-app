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
        st.markdown("<h2 style='text-align: center;'>🌾 شركة الرحمة لإدارة الأراضي</h2>", unsafe_allow_html=True)
        st.subheader("🔐 يرجى إدخال كلمة السر للدخول للنظام:")
        input_pass = st.text_input("كلمة السر:", type="password")
        if st.button("تسجيل الدخول", type="primary", use_container_width=True):
            if input_pass == PASSWORD:
                st.session_state.authenticated = True
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("❌ كلمة السر غير صحيحة، يرجى المحاولة مرة أخرى.")
    st.stop()


# ==========================================
# 📋 القائمة الجانبية للتطبيق
# ==========================================
st.sidebar.title("شركة الرحمة 🌾")
st.sidebar.write("أهلاً بك في النظام القياسي")

if st.sidebar.button("🔒 تسجيل الخروج", type="secondary"):
    st.session_state.authenticated = False
    st.rerun()

app_mode = st.sidebar.radio(
    "انتقل إلى القسم:",
    [
        "1. حسابات الأراضي والعملاء",
        "2. التوريد للمحطات",
        "3. صافي أرباحي من الأرض",
        "4. الموقف المالي للشركة"
    ]
)


# ==========================================
# 1. حسابات الأراضي والعملاء
# ==========================================
if app_mode == "1. حسابات الأراضي والعملاء":
    st.title("🌾 حسابات الأراضي والعملاء")
    
    tab_add_land, tab_client_page = st.tabs(["➕ إضافة أرض / عميل جديد", "📁 صفحة حسابات العملاء المخصصة"])
    
    with tab_add_land:
        st.subheader("تسجيل أرض وصاحب أرض جديد")
        with st.form("land_reg_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                owner_name = st.text_input("اسم صاحب الأرض (العميل)")
            with c2:
                phone_num = st.text_input("رقم التليفون")
            with c3:
                land_loc = st.text_input("موقع الأرض / الحوض")
            
            save_l = st.form_submit_button("حفظ وحجز صفحة للعميل")
            if save_l:
                if owner_name.strip():
                    existing_names = [l["owner"] for l in st.session_state.lands]
                    if owner_name in existing_names:
                        st.warning("هذا العميل مسجل مسبقاً.")
                    else:
                        st.session_state.lands.append({"owner": owner_name, "phone": phone_num, "location": land_loc})
                        save_data()
                        st.success(f"تم إنشاء صفحة خاصة بالعميل ({owner_name}) بنجاح وحفظها دائمياً!")
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
                st.markdown("---")
                st.header(f"📂 الصفحة الخاصة بالعميل: {selected_client}")
                st.write(f"📱 **رقم التليفون:** {client_info['phone']} | 📍 **موقع الأرض:** {client_info['location']}")
                
                with st.form(f"client_trans_{selected_client}", clear_on_submit=True):
                    st.subheader("تسجيل وارد، مصاريف، أو سلف جديدة للعميل")
                    
                    col_tr1, col_tr2 = st.columns(2)
                    with col_tr1:
                        crop_item = st.text_input("الصنف (نوع المحصول)")
                        exp_desc = st.text_input("اسم المصروف (مثل: عمالة، سماد...)")
                        record_date = st.date_input("التاريخ (ثابت حتى تغيره)", value=st.session_state.last_date)
                    with col_tr2:
                        sader_weight = st.number_input("وارد صادر (بالوزن)", min_value=0.0, step=1.0)
                        second_weight = st.number_input("وارد درجة ثانية (بالوزن)", min_value=0.0, step=1.0)
                        farza_weight = st.number_input("وارد فرزة (بالوزن)", min_value=0.0, step=1.0)
                    
                    col_tr3, col_tr4 = st.columns(2)
                    with col_tr3:
                        exp_amount = st.number_input("قيمة المصروف (جنيه)", min_value=0.0, step=50.0)
                    with col_tr4:
                        advanced_cash = st.number_input("استلام صاحب الأرض فلوس (سلفة نقدية)", min_value=0.0, step=50.0)
                        
                    add_trans_btn = st.form_submit_button("إضافة إلى صفحة العميل")
                    
                    if add_trans_btn:
                        st.session_state.last_date = record_date
                        st.session_state.land_accounts.append({
                            "owner": selected_client,
                            "date": str(record_date),
                            "item": crop_item,
                            "expense_desc": exp_desc if exp_desc.strip() else "بدون وصف",
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
                st.subheader(f"📊 سجل حركات وتفاصيل أرض {selected_client}")
                client_records = [r for r in st.session_state.land_accounts if r["owner"] == selected_client]
                
                if client_records:
                    for idx, record in enumerate(client_records):
                        cols_row = st.columns([7, 1])
                        with cols_row[0]:
                            exp_label = record['expense_desc'] if record['expense_amount'] > 0 else "لا يوجد مصروف"
                            st.write(f"📅 **التاريخ:** {record['date']} | **الصنف:** {record['item']} | **صادر:** {record['sader']} | **ثانية:** {record['second']} | **فرزة:** {record['farza']} | **{exp_label}:** {record['expense_amount']} ج | **سلف:** {record['advanced_cash']} ج")
                        with cols_row[1]:
                            if st.button("🗑️ حذف", key=f"del_rec_{selected_client}_{idx}"):
                                st.session_state.land_accounts.remove(record)
                                save_data()
                                st.success("تم حذف هذه الحركة بنجاح!")
                                st.rerun()
                    
                    st.markdown("---")
                    st.markdown("### 🧮 تصفية الحساب وإصدار كشف الحساب النهائي:")
                    
                    current_client_settings = st.session_state.client_settings.get(selected_client, {"discount": 0.0, "price": 0.0})
                    
                    with st.form(f"settlement_form_{selected_client}"):
                        col_f1, col_f2 = st.columns(2)
                        with col_f1:
                            discount_pct = st.number_input("نسبة الخصم (%) المحددة", min_value=0.0, max_value=100.0, value=float(current_client_settings.get("discount", 0.0)), step=0.5)
                        with col_f2:
                            price_per_unit = st.number_input("سعر الوحدة (جنيه)", min_value=0.0, value=float(current_client_settings.get("price", 0.0)), step=0.5)
                        
                        save_settings_btn = st.form_submit_button("💾 حفظ نسبة الخصم والسعر وحساب الصافي")
                        
                        if save_settings_btn:
                            st.session_state.client_settings[selected_client] = {
                                "discount": discount_pct,
                                "price": price_per_unit
                            }
                            save_data()
                            st.success("تم حفظ نسبة الخصم والسعر لهذا العميل بصفة دائمة!")
                    
                    active_discount = st.session_state.client_settings.get(selected_client, {}).get("discount", 0.0)
                    active_price = st.session_state.client_settings.get(selected_client, {}).get("price", 0.0)
                    
                    total_sader = sum(r["sader"] for r in client_records)
                    total_second = sum(r["second"] for r in client_records)
                    total_farza = sum(r["farza"] for r in client_records)
                    gross_weight = total_sader + total_second + total_farza
                    
                    discount_value = gross_weight * (active_discount / 100.0)
                    net_weight = gross_weight - discount_value
                    total_money_value = net_weight * active_price
                    
                    total_advanced = sum(r["advanced_cash"] for r in client_records)
                    remaining_balance = total_money_value - total_advanced
                    
                    st.info(f"""
                    * **إجمالي الوزن (صادر + ثانية + فرزة):** {gross_weight:,.2f}
                    * **نسبة الخصم المحفوظة ({active_discount}%):** {discount_value:,.2f}
                    * **صافي الوزن بعد الخصم:** {net_weight:,.2f}
                    * **سعر الوحدة المحفوظ:** {active_price:,.2f} جنيه
                    * **إجمالي القيمة (صافي الوزن × السعر):** {total_money_value:,.2f} جنيه
                    * **ما استلمه صاحب الأرض (سلف / فلوس فقط):** {total_advanced:,.2f} جنيه
                    """)
                    
                    st.success(f"### 💰 الباقي له نهائياً: {remaining_balance:,.2f} جنيه")
                    
                    if st.button(f"🖨️ طباعة كشف حساب العميل: {selected_client}", key=f"print_{selected_client}"):
                        st.markdown("---")
                        print_html = f"""
                        <div style="text-align: center; border: 2px solid #333; padding: 25px; border-radius: 10px;">
                            <h2>شركة الرحمة</h2>
                            <p><b>أرقام التليفونات:</b> 01000108685 - 01019381124</p>
                            <h3>كشف حساب نهائي لصاحب الأرض: {selected_client}</h3>
                            <hr>
                            <p><b>وارد صادر (بالوزن):</b> {total_sader:,.2f}</p>
                            <p><b>وارد درجة ثانية (بالوزن):</b> {total_second:,.2f}</p>
                            <p><b>وارد فرزة (بالوزن):</b> {total_farza:,.2f}</p>
                            <p><b>نسبة الخصم المحددة:</b> {active_discount}%</p>
                            <p><b>صافي الوزن بعد الخصم:</b> {net_weight:,.2f}</p>
                            <p><b>سعر الوحدة:</b> {active_price:,.2f} جنيه</p>
                            <p><b>إجمالي مستحقات الوارد:</b> {total_money_value:,.2f} جنيه</p>
                            <p><b>ما استلمه صاحب الأرض (سلف):</b> {total_advanced:,.2f} جنيه</p>
                            <h2>المبلغ الباقي له نهائياً: {remaining_balance:,.2f} جنيه</h2>
                        </div>
                        <script>
                            window.print();
                        </script>
                        """
                        st.markdown(print_html, unsafe_allow_html=True)
                else:
                    st.info("لا توجد حركات مسجلة في صفحة هذا العميل حتى الآن.")
        else:
            st.warning("يرجى إضافة عميل/أرض أولاً.")


# ==========================================
# 2. التوريد للمحطات
# ==========================================
elif app_mode == "2. التوريد للمحطات":
    st.title("🏭 التوريد للمحطات وحساباتها")
    
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
                        st.session_state.stations.append({
                            "name": st_name_input.strip(),
                            "phone": st_phone_input.strip()
                        })
                        save_data()
                        st.success(f"تمت إضافة المحطة ({st_name_input.strip()}) بنجاح وحفظها!")
                        st.rerun()
                else:
                    st.error("يرجى إدخال اسم المحطة.")
                    
    with tab_st_page:
        if st.session_state.stations:
            station_list = [s["name"] for s in st.session_state.stations]
            
            col_st_sel, col_st_del = st.columns([3, 1])
            with col_st_sel:
                selected_station = st.selectbox("اختر المحطة لفتح صفحتها الخاصة وإدخال التوريدات:", station_list)
            with col_st_del:
                st.write("")
                st.write("")
                if st.button("🗑️ حذف المحطة بالكامل", type="secondary"):
                    st.session_state.stations = [s for s in st.session_state.stations if s["name"] != selected_station]
                    st.session_state.station_supplies = [s for s in st.session_state.station_supplies if s["station"] != selected_station]
                    save_data()
                    st.success(f"تم حذف المحطة ({selected_station}) وكافة توريداتها بنجاح!")
                    st.rerun()

            st_info = next((s for s in st.session_state.stations if s["name"] == selected_station), None)
            
            if st_info:
                st.markdown("---")
                st.header(f"🏭 الصفحة الخاصة بالمحطة: {selected_station}")
                st.write(f"📱 **رقم تليفون المحطة:** {st_info['phone']}")
                
                with st.form(f"trans_st_{selected_station}", clear_on_submit=True):
                    st.subheader("تسجيل بيانات توريد سيارة ودفعات نقدية جديدة للمحطة")
                    
                    c_st_a, c_st_b = st.columns(2)
                    with c_st_a:
                        sup_date = st.date_input("تاريخ التوريد", value=st.session_state.last_date)
                        car_number = st.text_input("رقم السيارة")
                        raw_weight = st.number_input("الوزن الخام", min_value=0.0, step=1.0)
                    with c_st_b:
                        discount_pct_st = st.number_input("نسبة الخصم (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
                        price_st = st.number_input("السعر", min_value=0.0, step=0.5)
                    
                    calc_net_w = raw_weight - (raw_weight * (discount_pct_st / 100.0))
                    calc_total = calc_net_w * price_st
                    st.info(f"📌 **معاينة سريعة للتوريد:** الوزن بعد الخصم = `{calc_net_w:,.2f}` | 💵 **الإجمالي (الوزن بعد الخصم × السعر):** `{calc_total:,.2f}` جنيه")
                    
                    st.markdown("---")
                    st.markdown("##### 💵 خانة الفلوس التي دفعتها المحطة:")
                    paid_today = st.number_input("المبلغ الذي دفعته المحطة (جنيه)", min_value=0.0, step=100.0, value=0.0)
                        
                    add_st_sup = st.form_submit_button("حفظ التوريد لصفحة المحطة")
                    
                    if add_st_sup:
                        st.session_state.last_date = sup_date
                        net_w = raw_weight - (raw_weight * (discount_pct_st / 100.0))
                        total_car_money = net_w * price_st
                        
                        st.session_state.station_supplies.append({
                            "station": selected_station,
                            "date": str(sup_date),
                            "car": car_number,
                            "weight": raw_weight,
                            "discount": discount_pct_st,
                            "net_weight": net_w,
                            "price": price_st,
                            "total_money": total_car_money,
                            "paid_amount": paid_today
                        })
                        save_data()
                        st.success("تم إضافة التوريد والحساب لصفحة المحطة بنجاح وحفظه دائمياً!")
                        st.rerun()

                st.markdown("---")
                st_records = [s for s in st.session_state.station_supplies if s["station"] == selected_station]
                
                if st_records:
                    st.subheader(f"📋 سجل حركات وتوريدات محطة: {selected_station}")
                    for idx_st, s_rec in enumerate(st_records):
                        cols_st_row = st.columns([7, 1])
                        with cols_st_row[0]:
                            paid_txt = f"{s_rec['paid_amount']:,.2f} ج"
                            st.write(f"📅 **التاريخ:** {s_rec['date']} | 🚗 **السيارة:** {s_rec['car']} | **الوزن الخام:** {s_rec['weight']:,.2f} | **الخصم:** {s_rec['discount']}% | **صافي الوزن:** {s_rec['net_weight']:,.2f} | **السعر:** {s_rec['price']} ج | **الإجمالي:** {s_rec['total_money']:,.2f} ج | **المقْبوض (المدفوع):** {paid_txt}")
                        with cols_st_row[1]:
                            if st.button("🗑️ حذف", key=f"del_st_rec_{selected_station}_{idx_st}"):
                                st.session_state.station_supplies.remove(s_rec)
                                save_data()
                                st.success("تم حذف السجل بنجاح!")
                                st.rerun()
                            
                    st.markdown("---")
                    st.subheader("🧮 تصفية الحساب النهائي مع المحطة:")
                    
                    total_raw_w = sum(s["weight"] for s in st_records)
                    total_net_w = sum(s["net_weight"] for s in st_records)
                    total_station_money = sum(s["total_money"] for s in st_records)
                    total_station_paid = sum(s["paid_amount"] for s in st_records)
                    remaining_on_station = total_station_money - total_station_paid
                    
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
                else:
                    st.info("لا توجد توريدات مسجلة لهذه المحطة حتى الآن.")
        else:
            st.warning("يرجى إضافة محطة أولاً من التبويب الأول.")


# ==========================================
# 3. صافي أرباحي من الأرض
# ==========================================
elif app_mode == "3. صافي أرباحي من الأرض":
    st.title("📈 صفحة أرباحي الخاصة من الأراضي")
    
    if st.session_state.lands:
        land_list = [l["owner"] for l in st.session_state.lands]
        selected_prof_owner = st.selectbox("اختر الأرض / العميل لفتح صفحته الخاصة وحفظ أرباحها:", land_list)
        
        owner_recs = [r for r in st.session_state.land_accounts if r["owner"] == selected_prof_owner]
        
        total_sader_w = sum(r["sader"] for r in owner_recs) if owner_recs else 0.0
        total_second_w = sum(r["second"] for r in owner_recs) if owner_recs else 0.0
        total_farza_w = sum(r["farza"] for r in owner_recs) if owner_recs else 0.0
        
        total_expenses_p = sum(r["expense_amount"] for r in owner_recs) if owner_recs else 0.0
        total_advanced_p = sum(r["advanced_cash"] for r in owner_recs) if owner_recs else 0.0
        
        st.markdown("---")
        st.subheader(f"🌾 أوزان وتكاليف أرض: {selected_prof_owner}")
        
        col_w1, col_w2, col_w3 = st.columns(3)
        with col_w1:
            st.info(f"**إجمالي الصادر:** {total_sader_w:,.2f}")
        with col_w2:
            st.info(f"**إجمالي الدرجة الثانية:** {total_second_w:,.2f}")
        with col_w3:
            st.info(f"**إجمالي الفرزة:** {total_farza_w:,.2f}")
            
        st.markdown("### 💵 تحديد سعر بيع كل وزنة (أنا بعتها بكام؟):")
        
        saved_data = st.session_state.saved_profits.get(selected_prof_owner, {"p_sader": 0.0, "p_second": 0.0, "p_farza": 0.0})
        
        with st.form(f"profit_calc_form_{selected_prof_owner}"):
            c_p1, c_p2, c_p3 = st.columns(3)
            with c_p1:
                price_sader = st.number_input("سعر بيع الصادر (جنيه)", min_value=0.0, value=float(saved_data.get("p_sader", 0.0)), step=0.5)
            with c_p2:
                price_second = st.number_input("سعر بيع الدرجة الثانية (جنيه)", min_value=0.0, value=float(saved_data.get("p_second", 0.0)), step=0.5)
            with c_p3:
                price_farza = st.number_input("سعر بيع الفرزة (جنيه)", min_value=0.0, value=float(saved_data.get("p_farza", 0.0)), step=0.5)
                
            save_profit_btn = st.form_submit_button("💾 حفظ وحساب صافي الربح / الخسارة للأرض")
            
            if save_profit_btn:
                st.session_state.saved_profits[selected_prof_owner] = {
                    "p_sader": price_sader,
                    "p_second": price_second,
                    "p_farza": price_farza
                }
                save_data()
                saved_data = st.session_state.saved_profits[selected_prof_owner]
                st.success("تم حفظ الأسعار والنتائج في صفحة هذا العميل بنجاح!")
        
        cur_p_sader = saved_data.get("p_sader", 0.0)
        cur_p_second = saved_data.get("p_second", 0.0)
        cur_p_farza = saved_data.get("p_farza", 0.0)
        
        total_sales_revenue = (total_sader_w * cur_p_sader) + (total_second_w * cur_p_second) + (total_farza_w * cur_p_farza)
        total_cost = total_expenses_p + total_advanced_p
        net_profit_loss = total_sales_revenue - total_cost
        
        st.markdown("---")
        st.subheader(f"📊 ملخص النتيجة المالية المحفوظة لأرض: {selected_prof_owner}")
        
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        with res_col1:
            st.metric("إجمالي قيمة البيع", f"{total_sales_revenue:,.2f} جنيه")
        with res_col2:
            st.metric("إجمالي المصاريف", f"{total_expenses_p:,.2f} جنيه")
        with res_col3:
            st.metric("ما استلمه صاحب الأرض", f"{total_advanced_p:,.2f} جنيه")
        with res_col4:
            st.metric("صافي النتيجة", f"{net_profit_loss:,.2f} جنيه")
            
        if net_profit_loss > 0:
            st.success(f"🎉 **الأرض حققت مكسباً صافياً قدره:** {net_profit_loss:,.2f} جنيه")
        elif net_profit_loss < 0:
            st.error(f"⚠️ **الأرض حققت خسارة قدرها:** {abs(net_profit_loss):,.2f} جنيه")
        else:
            st.info("⚖️ **النتيجة متكافئة (لا يوجد مكسب ولا خسارة).**")
    else:
        st.warning("يرجى إضافة أراضٍ مسجلة أولاً.")


# ==========================================
# 4. الموقف المالي للشركة (القسم الجديد المستقل)
# ==========================================
elif app_mode == "4. الموقف المالي للشركة":
    st.title("💼 الموقف المالي الشامل للشركة")
    st.markdown("هنا يمكنك متابعة إجمالي الأموال التي لك لدى المحطات، والأموال التي عليك للعملاء أصحاب الأراضي بشكل لحظي.")
    st.markdown("---")
    
    # 1. حساب إجمالي الفلوس اللي ليك بره عند كل المحطات
    total_all_stations_remaining = 0.0
    for st_obj in st.session_state.stations:
        st_name = st_obj["name"]
        st_recs = [s for s in st.session_state.station_supplies if s["station"] == st_name]
        if st_recs:
            t_money = sum(s["total_money"] for s in st_recs)
            t_paid = sum(s["paid_amount"] for s in st_recs)
            total_all_stations_remaining += (t_money - t_paid)

    # 2. حساب إجمالي الفلوس اللي عليك بره لكل العملاء (الباقي لهم نهائياً)
    total_all_clients_remaining = 0.0
    for land_obj in st.session_state.lands:
        c_name = land_obj["owner"]
        c_recs = [r for r in st.session_state.land_accounts if r["owner"] == c_name]
        if c_recs:
            c_settings = st.session_state.client_settings.get(c_name, {"discount": 0.0, "price": 0.0})
            c_disc = c_settings.get("discount", 0.0)
            c_price = c_settings.get("price", 0.0)
            
            c_gross = sum(r["sader"] + r["second"] + r["farza"] for r in c_recs)
            c_net_w = c_gross - (c_gross * (c_disc / 100.0))
            c_total_val = c_net_w * c_price
            c_advanced = sum(r["advanced_cash"] for r in c_recs)
            
            c_rem = c_total_val - c_advanced
            total_all_clients_remaining += c_rem

    # عرض المبالغ في بطاقات واضحة ومميزة
    col_fin1, col_fin2 = st.columns(2)
    
    with col_fin1:
        st.metric(
            label="🏭 إجمالي الفلوس اللي ليك بره (عند كل المحطات)", 
            value=f"{total_all_stations_remaining:,.2f} جنيه",
            delta="إجمالي المستحقات لك"
        )
        
    with col_fin2:
        st.metric(
            label="🌾 إجمالي الفلوس اللي عليك بره (لكل العملاء)", 
            value=f"{total_all_clients_remaining:,.2f} جنيه",
            delta="إجمالي المستحقات للعملاء",
            delta_color="inverse"
        )