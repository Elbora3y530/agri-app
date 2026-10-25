# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import datetime
import json
import os
import base64
import requests

PASSWORD = "332007"
DATA_FILE = "agri_data.json"

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_REPO = st.secrets.get("GITHUB_REPO", "")

def get_github_file_info():
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return None
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATA_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

def load_data():
    file_info = get_github_file_info()
    if file_info and "content" in file_info:
        try:
            content = base64.b64decode(file_info["content"]).decode("utf-8")
            data = json.loads(content)
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
            return
        except Exception as e:
            st.error(f"خطأ في تحميل البيانات من GitHub: {e}")
            
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
        except Exception as e:
            st.error(f"خطأ في تحميل البيانات المحلية: {e}")

def save_data():
    try:
        data = {
            "lands": st.session_state.get("lands", []),
            "land_accounts": st.session_state.get("land_accounts", []),
            "stations": st.session_state.get("stations", []),
            "station_supplies": st.session_state.get("station_supplies", []),
            "saved_profits": st.session_state.get("saved_profits", {}),
            "client_settings": st.session_state.get("client_settings", {}),
            "last_date": str(st.session_state.get("last_date", datetime.date.today()))
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        if GITHUB_TOKEN and GITHUB_REPO:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATA_FILE}"
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            file_info = get_github_file_info()
            sha = file_info["sha"] if file_info else None
            json_str = json.dumps(data, ensure_ascii=False, indent=4)
            encoded_content = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
            payload = {"message": "Update agri data", "content": encoded_content}
            if sha:
                payload["sha"] = sha
            requests.put(url, headers=headers, json=payload)
        st.success("تم الحفظ بنجاح!")
    except Exception as e:
        st.error(f"فشل الحفظ: {e}")

def clean_float(val):
    try:
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip()
        return float(val_str) if val_str else 0.0
    except Exception:
        return 0.0

st.set_page_config(
    page_title="شركة الرحمة - نظام إدارة الأراضي والمحاصيل",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
    <style>
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
    input[type=number] {
      -moz-appearance: textfield;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f1f3f5 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-right: 5px solid #1E88E5;
        margin-bottom: 15px;
    }
    @media print {
        @page {
            size: A4 portrait;
            margin: 0mm;
        }
        html, body {
            height: 100%;
            overflow: hidden !important;
            background: #fff !important;
        }
        [data-testid="stSidebar"], header, footer, .stButton, .main .block-container > div:not(#print-section) {
            display: none !important;
        }
        body * {
            visibility: hidden;
        }
        #print-section, #print-section * {
            visibility: visible !important;
        }
        #print-section {
            position: fixed !important;
            top: 10mm !important;
            right: 10mm !important;
            left: 10mm !important;
            width: 190mm !important;
            max-height: 275mm !important;
            direction: rtl;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: white !important;
            box-sizing: border-box;
            page-break-after: avoid !important;
            page-break-inside: avoid !important;
        }
    }
    .print-box {
        border: 2px solid #333;
        padding: 15px;
        border-radius: 10px;
        background-color: #fff;
        direction: rtl;
        width: 100%;
        box-sizing: border-box;
    }
    .print-header {
        text-align: center;
        border-bottom: 2px solid #333;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    .print-header h2 {
        font-size: 18px;
        margin: 3px 0;
    }
    .print-header h3 {
        font-size: 15px;
        margin: 3px 0;
    }
    .print-content {
        background-color: #f8f9fa;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        line-height: 1.8;
        font-size: 13px;
    }
    .print-footer {
        background-color: #e8f5e9;
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #c8e6c9;
        text-align: center;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

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

if "data_loaded" not in st.session_state:
    load_data()
    st.session_state.data_loaded = True

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
                        st.success(f"تم إضافه العميل ({owner_name}) بنجاح!")
                        st.rerun()
                else:
                    st.error("يرجى إدخال اسم صاحب الأرض.")
                    
    with tab_client_page:
        if st.session_state.lands:
            client_display_map = {f"{l['owner']} ({l.get('type', 'بطاطا تحت الشرب')})": l["owner"] for l in st.session_state.lands}
            display_list = ["-- اختر اسم العميل --"] + list(client_display_map.keys())
            
            col_sel, col_del = st.columns([3, 1])
            with col_sel:
                selected_display = st.selectbox("اختر اسم العميل لفتح صفحته الخاصة:", display_list, index=0)
            
            if selected_display and selected_display != "-- اختر اسم العميل --":
                selected_client = client_display_map[selected_display]
                
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
                    
                    if client_category == "بطاطا تحت الشرب":
                        with st.form(f"client_trans_{selected_client}", clear_on_submit=True):
                            st.subheader("تسجيل حركة جديدة (مصاريف، وارد، أو سلف نقدية)")
                            
                            col_tr1, col_tr2 = st.columns(2)
                            with col_tr1:
                                record_date = st.date_input("التاريخ", value=st.session_state.last_date)
                                exp_option = st.selectbox("نوع المصروف", ["بدون مصروف", "جراندات", "أنفار", "فطار", "مناديب", "شكاير", "آخر (اكتب يدوي)"])
                                custom_exp = st.text_input("اكتب نوع المصروف (إذا اخترت آخر)")
                                final_exp_desc = custom_exp if exp_option == "آخر (اكتب يدوي)" and custom_exp.strip() else (exp_option if exp_option != "بدون مصروف" else "بدون مصروف")
                                exp_amount_in = st.text_input("قيمة المصروف (جنيه)", value="0")
                            
                            with col_tr2:
                                sader_in = st.text_input("وارد صادر (بالوزن)", value="0")
                                second_in = st.text_input("وارد درجة ثانية (بالوزن)", value="0")
                                farza_in = st.text_input("وارد فرزة (بالوزن)", value="0")
                                advanced_in = st.text_input("استلام صاحب الأرض فلوس (سلفة نقدية)", value="0")
                            
                            add_trans_btn = st.form_submit_button("إضافة الحركة إلى صفحة العميل")
                            
                            if add_trans_btn:
                                st.session_state.last_date = record_date
                                st.session_state.land_accounts.append({
                                    "owner": selected_client,
                                    "date": str(record_date),
                                    "expense_desc": final_exp_desc,
                                    "expense_amount": clean_float(exp_amount_in),
                                    "sader": clean_float(sader_in),
                                    "second": clean_float(second_in),
                                    "farza": clean_float(farza_in),
                                    "advanced_cash": clean_float(advanced_in)
                                })
                                save_data()
                                st.success("تم إضافه الحركه بنجاح!")
                                st.rerun()

                        st.markdown("---")
                        st.subheader(f"📊 جدول سجل حركات وتفاصيل أرض {selected_client}")
                        client_records = [r for r in st.session_state.land_accounts if r["owner"] == selected_client]
                        
                        if client_records:
                            col_h1, col_h2, col_h3, col_h4, col_h5, col_h6, col_h7, col_h8 = st.columns([1.2, 1.2, 1, 1, 1, 1, 1, 1])
                            with col_h1: st.markdown("**التاريخ**")
                            with col_h2: st.markdown("**المصروف**")
                            with col_h3: st.markdown("**قيمة المصروف**")
                            with col_h4: st.markdown("**صادر**")
                            with col_h5: st.markdown("**ثانية**")
                            with col_h6: st.markdown("**فرزة**")
                            with col_h7: st.markdown("**سلفة**")
                            with col_h8: st.markdown("**إجراءات**")
                            st.markdown("---")

                            for idx, record in enumerate(client_records):
                                cols_row = st.columns([1.2, 1.2, 1, 1, 1, 1, 1, 1])
                                with cols_row[0]: st.write(f"📅 {record['date']}")
                                with cols_row[1]: st.write(f"{record.get('expense_desc', '-')}")
                                with cols_row[2]: st.write(f"{record.get('expense_amount', 0):,.2f} ج")
                                with cols_row[3]: st.write(f"{record.get('sader', 0):,.1f}")
                                with cols_row[4]: st.write(f"{record.get('second', 0):,.1f}")
                                with cols_row[5]: st.write(f"{record.get('farza', 0):,.1f}")
                                with cols_row[6]: st.write(f"{record.get('advanced_cash', 0):,.2f} ج")
                                with cols_row[7]:
                                    c_edit, c_del = st.columns(2)
                                    with c_edit:
                                        if st.button("✏️", key=f"edit_c_{selected_client}_{idx}"):
                                            st.session_state[f"editing_c_{selected_client}_{idx}"] = True
                                    with c_del:
                                        if st.button("🗑️", key=f"del_c_{selected_client}_{idx}"):
                                            st.session_state.land_accounts.remove(record)
                                            save_data()
                                            st.success("تم الحذف بنجاح!")
                                            st.rerun()

                                if st.session_state.get(f"editing_c_{selected_client}_{idx}", False):
                                    with st.form(f"form_edit_c_{selected_client}_{idx}"):
                                        st.write("✏️ **تعديل الحركة:**")
                                        ed_date = st.date_input("التاريخ", value=datetime.datetime.strptime(record['date'], "%Y-%m-%d").date())
                                        ed_desc = st.text_input("نوع المصروف", value=record.get('expense_desc', ''))
                                        ed_exp = st.text_input("قيمة المصروف", value=str(record.get('expense_amount', 0)))
                                        ed_sad = st.text_input("وارد صادر", value=str(record.get('sader', 0)))
                                        ed_sec = st.text_input("وارد درجة ثانية", value=str(record.get('second', 0)))
                                        ed_far = st.text_input("وارد فرزة", value=str(record.get('farza', 0)))
                                        ed_adv = st.text_input("سلفة نقدية", value=str(record.get('advanced_cash', 0)))

                                        if st.form_submit_button("💾 حفظ التعديل"):
                                            record['date'] = str(ed_date)
                                            record['expense_desc'] = ed_desc
                                            record['expense_amount'] = clean_float(ed_exp)
                                            record['sader'] = clean_float(ed_sad)
                                            record['second'] = clean_float(ed_sec)
                                            record['farza'] = clean_float(ed_far)
                                            record['advanced_cash'] = clean_float(ed_adv)
                                            st.session_state[f"editing_c_{selected_client}_{idx}"] = False
                                            save_data()
                                            st.success("تم التعديل بنجاح!")
                                            st.rerun()

                            st.markdown("---")
                            st.markdown("### 🧮 تصفية الحساب النهائي للعميل (بطاطا تحت الشرب):")
                            current_client_settings = st.session_state.client_settings.get(selected_client, {"discount": 0.0, "price": 0.0})
                            
                            with st.form(f"settlement_form_{selected_client}"):
                                col_f1, col_f2 = st.columns(2)
                                with col_f1:
                                    discount_in = st.text_input("نسبة الخصم (%)", value=str(current_client_settings.get("discount", 0.0)))
                                with col_f2:
                                    price_in = st.text_input("سعر الكيلو / الوحدة (جنيه)", value=str(current_client_settings.get("price", 0.0)))
                                
                                save_settings_btn = st.form_submit_button("💾 حفظ نسبة الخصم والسعر")
                                if save_settings_btn:
                                    st.session_state.client_settings[selected_client] = {
                                        "discount": clean_float(discount_in), 
                                        "price": clean_float(price_in)
                                    }
                                    save_data()
                                    st.success("تم حفظ إعدادات الحساب بنجاح!")
                                    st.rerun()
                            
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
                            
                            remaining_balance = total_money_value - total_advanced
                            
                            st.markdown("### 📜 كشف حساب نهائي:")
                            st.info(f"""
                            * **إجمالي وزن صادر خام:** {total_sader:,.2f} كجم
                            * **إجمالي وزن درجة ثانية خام:** {total_second:,.2f} كجم
                            * **إجمالي وزن فرزة خام:** {total_farza:,.2f} كجم
                            * **إجمالي الأوزان الخام بالكامل:** {gross_weight:,.2f} كجم
                            * **خصم نسبة ({active_discount}%):** {discount_value:,.2f} كجم
                            * **إجمالي الوزن الصافي بعد الخصم:** {net_weight:,.2f} كجم
                            * **إجمالي قيمة البطاطا (الوزن الصافي × السعر {active_price:,.2f} ج):** {total_money_value:,.2f} جنيه
                            * **إجمالي الفلوس التي أخذها العميل (سُلف نقدية):** {total_advanced:,.2f} جنيه
                            """)
                            st.success(f"## 💰 المبلغ الباقي للعميل نهائياً: {remaining_balance:,.2f} جنيه")

                            print_html = f"""
                            <div id="print-section">
                                <div class="print-box">
                                    <div class="print-header">
                                        <h2>🌾 شركة الرحمة لإدارة الأراضي والمحاصيل</h2>
                                        <p>📞 01000108658 | 01019381124</p>
                                        <h3>📜 كشف حساب نهائي للعميل: {selected_client}</h3>
                                        <p><b>التاريخ:</b> {datetime.date.today().strftime('%Y-%m-%d')} | <b>نوع التعامل:</b> بطاطا تحت الشرب</p>
                                    </div>
                                    <div class="print-content">
                                        <p>• <b>إجمالي وزن صادر خام:</b> {total_sader:,.2f} كجم</p>
                                        <p>• <b>إجمالي وزن درجة ثانية خام:</b> {total_second:,.2f} كجم</p>
                                        <p>• <b>إجمالي وزن فرزة خام:</b> {total_farza:,.2f} كجم</p>
                                        <p>• <b>إجمالي الأوزان الخام بالكامل:</b> {gross_weight:,.2f} كجم</p>
                                        <p>• <b>خصم نسبة ({active_discount}%):</b> {discount_value:,.2f} كجم</p>
                                        <p>• <b>إجمالي الوزن الصافي بعد الخصم:</b> {net_weight:,.2f} كجم</p>
                                        <p>• <b>إجمالي قيمة البطاطا (الوزن الصافي × السعر {active_price:,.2f} ج):</b> {total_money_value:,.2f} جنيه</p>
                                        <p>• <b>إجمالي الفلوس التي أخذها العميل (سُلف نقدية):</b> {total_advanced:,.2f} جنيه</p>
                                    </div>
                                    <div class="print-footer">
                                        <h3 style="color: #2e7d32; margin: 0;">💰 المبلغ الباقي للعميل نهائياً: {remaining_balance:,.2f} جنيه</h3>
                                    </div>
                                    <br><br>
                                    <div style="display: flex; justify-content: space-between; text-align: center; padding: 0 30px; font-size: 13px;">
                                        <div><b>توقيع العميل:</b> ..........................</div>
                                        <div><b>توقيع الإدارة:</b> ..........................</div>
                                    </div>
                                </div>
                            </div>
                            """
                            st.markdown(print_html, unsafe_allow_html=True)
                            
                            if st.button("🖨️ طباعة كشف الحساب / حفظ PDF (A4)", type="primary"):
                                st.components.v1.html("<script>window.parent.print();</script>", height=0)

                        else:
                            st.info("لا توجد حركات مسجلة لهذا العميل حتى الآن.")

                    else:
                        with st.form(f"box_client_trans_{selected_client}", clear_on_submit=True):
                            st.subheader("تسجيل توريد ومصاريف (صادر في البوكسة)")
                            
                            c_b1, c_b2 = st.columns(2)
                            with c_b1:
                                b_date = st.date_input("التاريخ", value=st.session_state.last_date)
                                b_exp_opt = st.selectbox("نوع المصروف", ["بدون مصروف", "جراندات", "أنفار", "فطار", "مناديب", "شكاير", "آخر (اكتب يدوي)"])
                                b_cust_exp = st.text_input("اكتب نوع المصروف المخصص")
                                b_final_desc = b_cust_exp if b_exp_opt == "آخر (اكتب يدوي)" and b_cust_exp.strip() else (b_exp_opt if b_exp_opt != "بدون مصروف" else "بدون مصروف")
                                b_exp_in = st.text_input("قيمة المصروف (جنيه)", value="0")
                                b_adv_in = st.text_input("فلوس أخذها صاحب الأرض (سلفة)", value="0")
                            with c_b2:
                                b_raw_in = st.text_input("وزن بطاطا صادر خام", value="0")
                                b_disc_type = st.radio("نوع الخصم", ["خصم بالنسبة (%)", "خصم بالكيلو"], horizontal=True, key=f"b_dtype_{selected_client}")
                                b_disc_in = st.text_input("قيمة الخصم", value="0")
                                b_price_in = st.text_input("سعر الكيلو", value="0")

                            add_box_btn = st.form_submit_button("حفظ حركة الصادر في البوكسة")
                            if add_box_btn:
                                raw_w = clean_float(b_raw_in)
                                disc_v = clean_float(b_disc_in)
                                prc = clean_float(b_price_in)
                                
                                if b_disc_type == "خصم بالنسبة (%)":
                                    calc_net = raw_w - (raw_w * (disc_v / 100.0))
                                else:
                                    calc_net = max(0.0, raw_w - disc_v)
                                    
                                calc_tot = calc_net * prc
                                
                                st.session_state.last_date = b_date
                                st.session_state.land_accounts.append({
                                    "owner": selected_client,
                                    "date": str(b_date),
                                    "expense_desc": b_final_desc,
                                    "expense_amount": clean_float(b_exp_in),
                                    "raw_weight": raw_w,
                                    "disc_type": b_disc_type,
                                    "discount_pct": disc_v,
                                    "net_weight": calc_net,
                                    "price": prc,
                                    "total_price": calc_tot,
                                    "advanced_cash": clean_float(b_adv_in)
                                })
                                save_data()
                                st.success("تم إضافه الحركه بنجاح!")
                                st.rerun()

                        st.markdown("---")
                        st.subheader(f"📋 جدول حركات صادر البوكسة: {selected_client}")
                        box_records = [r for r in st.session_state.land_accounts if r["owner"] == selected_client and "raw_weight" in r]

                        if box_records:
                            col_bh1, col_bh2, col_bh3, col_bh4, col_bh5, col_bh6, col_bh7, col_bh8, col_bh9 = st.columns([1.1, 1.1, 1, 1, 1, 1, 1, 1, 1])
                            with col_bh1: st.markdown("**التاريخ**")
                            with col_bh2: st.markdown("**المصروف**")
                            with col_bh3: st.markdown("**المبلغ**")
                            with col_bh4: st.markdown("**خام**")
                            with col_bh5: st.markdown("**الخصم**")
                            with col_bh6: st.markdown("**الصافي**")
                            with col_bh7: st.markdown("**السعر**")
                            with col_bh8: st.markdown("**السلفة**")
                            with col_bh9: st.markdown("**إجراءات**")
                            st.markdown("---")

                            for b_idx, b_rec in enumerate(box_records):
                                cols_brow = st.columns([1.1, 1.1, 1, 1, 1, 1, 1, 1, 1])
                                d_lbl = "%" if b_rec.get('disc_type') == "خصم بالنسبة (%)" else "كجم"
                                
                                with cols_brow[0]: st.write(f"📅 {b_rec['date']}")
                                with cols_brow[1]: st.write(f"{b_rec.get('expense_desc', '-')}")
                                with cols_brow[2]: st.write(f"{b_rec.get('expense_amount', 0):,.2f} ج")
                                with cols_brow[3]: st.write(f"{b_rec.get('raw_weight', 0):,.1f}")
                                with cols_brow[4]: st.write(f"{b_rec.get('discount_pct', 0)} {d_lbl}")
                                with cols_brow[5]: st.write(f"**{b_rec.get('net_weight', 0):,.1f}**")
                                with cols_brow[6]: st.write(f"{b_rec.get('price', 0):,.2f}")
                                with cols_brow[7]: st.write(f"{b_rec.get('advanced_cash', 0):,.2f} ج")
                                with cols_brow[8]:
                                    c_bedit, c_bdel = st.columns(2)
                                    with c_bedit:
                                        if st.button("✏️", key=f"edit_box_{selected_client}_{b_idx}"):
                                            st.session_state[f"editing_box_{selected_client}_{b_idx}"] = True
                                    with c_bdel:
                                        if st.button("🗑️", key=f"del_box_{selected_client}_{b_idx}"):
                                            st.session_state.land_accounts.remove(b_rec)
                                            save_data()
                                            st.success("تم الحذف بنجاح!")
                                            st.rerun()

                                if st.session_state.get(f"editing_box_{selected_client}_{b_idx}", False):
                                    with st.form(f"form_edit_box_{selected_client}_{b_idx}"):
                                        st.write("✏️ **تعديل حركة البوكسة:**")
                                        eb_date = st.date_input("التاريخ", value=datetime.datetime.strptime(b_rec['date'], "%Y-%m-%d").date())
                                        eb_desc = st.text_input("المصروف", value=b_rec.get('expense_desc', ''))
                                        eb_exp = st.text_input("قيمة المصروف", value=str(b_rec.get('expense_amount', 0)))
                                        eb_raw = st.text_input("الوزن الخام", value=str(b_rec.get('raw_weight', 0)))
                                        eb_disc_type = st.radio("نوع الخصم", ["خصم بالنسبة (%)", "خصم بالكيلو"], index=0 if b_rec.get('disc_type') == "خصم بالنسبة (%)" else 1)
                                        eb_disc = st.text_input("قيمة الخصم", value=str(b_rec.get('discount_pct', 0)))
                                        eb_prc = st.text_input("السعر", value=str(b_rec.get('price', 0)))
                                        eb_adv = st.text_input("السلفة", value=str(b_rec.get('advanced_cash', 0)))

                                        if st.form_submit_button("💾 حفظ التعديل"):
                                            r_w = clean_float(eb_raw)
                                            d_v = clean_float(eb_disc)
                                            p_c = clean_float(eb_prc)
                                            
                                            if eb_disc_type == "خصم بالنسبة (%)":
                                                c_n = r_w - (r_w * (d_v / 100.0))
                                            else:
                                                c_n = max(0.0, r_w - d_v)
                                                
                                            c_t = c_n * p_c

                                            b_rec['date'] = str(eb_date)
                                            b_rec['expense_desc'] = eb_desc
                                            b_rec['expense_amount'] = clean_float(eb_exp)
                                            b_rec['raw_weight'] = r_w
                                            b_rec['disc_type'] = eb_disc_type
                                            b_rec['discount_pct'] = d_v
                                            b_rec['net_weight'] = c_n
                                            b_rec['price'] = p_c
                                            b_rec['total_price'] = c_t
                                            b_rec['advanced_cash'] = clean_float(eb_adv)
                                            st.session_state[f"editing_box_{selected_client}_{b_idx}"] = False
                                            save_data()
                                            st.success("تم التعديل بنجاح!")
                                            st.rerun()

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
                            * **إجمالي الفلوس التي أخذها صاحب الأرض (سُلف):** {tot_adv_box:,.2f} جنيه
                            """)
                            st.success(f"### 💰 باقي له نهائياً: {final_box_rem:,.2f} جنيه")

                            print_b_html = f"""
                            <div id="print-section">
                                <div class="print-box">
                                    <div class="print-header">
                                        <h2>🌾 شركة الرحمة لإدارة الأراضي والمحاصيل</h2>
                                        <p>📞 01000108658 | 01019381124</p>
                                        <h3>📜 كشف حساب نهائي للعميل: {selected_client}</h3>
                                        <p><b>التاريخ:</b> {datetime.date.today().strftime('%Y-%m-%d')} | <b>نوع التعامل:</b> بطاطا صادر في البوكسة</p>
                                    </div>
                                    <div class="print-content">
                                        <p>• <b>إجمالي المصاريف:</b> {tot_exp_box:,.2f} جنيه</p>
                                        <p>• <b>إجمالي وزن البطاطا الصادر (خام):</b> {tot_raw_box:,.2f} كجم</p>
                                        <p>• <b>إجمالي وزن البطاطا بعد الخصم:</b> {tot_net_box:,.2f} كجم</p>
                                        <p>• <b>إجمالي سعر البطاطا:</b> {tot_price_box:,.2f} جنيه</p>
                                        <p>• <b>إجمالي الفلوس التي أخذها العميل (سُلف نقدية):</b> {tot_adv_box:,.2f} جنيه</p>
                                    </div>
                                    <div class="print-footer">
                                        <h3 style="color: #2e7d32; margin: 0;">💰 المبلغ الباقي للعميل نهائياً: {final_box_rem:,.2f} جنيه</h3>
                                    </div>
                                    <br><br>
                                    <div style="display: flex; justify-content: space-between; text-align: center; padding: 0 30px; font-size: 13px;">
                                        <div><b>توقيع العميل:</b> ..........................</div>
                                        <div><b>توقيع الإدارة:</b> ..........................</div>
                                    </div>
                                </div>
                            </div>
                            """
                            st.markdown(print_b_html, unsafe_allow_html=True)
                            
                            if st.button("🖨️ طباعة كشف الحساب / حفظ PDF (A4)", type="primary", key="btn_print_box"):
                                st.components.v1.html("<script>window.parent.print();</script>", height=0)

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
                        st.success("تم إضافه المحطة بنجاح!")
                        st.rerun()
                else:
                    st.error("يرجى إدخال اسم المحطة.")
                    
    with tab_st_page:
        if st.session_state.stations:
            station_list = ["-- اختر اسم المحطة --"] + [s["name"] for s in st.session_state.stations]
            
            col_st_sel, col_st_del = st.columns([3, 1])
            with col_st_sel:
                selected_station = st.selectbox("اختر المحطة لفتح صفحتها الخاصة:", station_list, index=0)
            
            if selected_station and selected_station != "-- اختر اسم المحطة --":
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
                    with col_m1: st.metric("إجمالي الوزن الخام", f"{total_raw_w:,.2f}")
                    with col_m2: st.metric("إجمالي الوزن الصافي", f"{total_net_w:,.2f}")
                    with col_m3: st.metric("إجمالي الفلوس", f"{total_station_money:,.2f} ج")
                    with col_m4: st.metric("المدفوع من المحطة", f"{total_station_paid:,.2f} ج")
                    with col_m5: st.metric("باقي ليا عند المحطة", f"{remaining_on_station:,.2f} ج")
                    st.markdown("---")

                    with st.form(f"trans_st_{selected_station}", clear_on_submit=True):
                        st.subheader("تسجيل توريد سيارة جديد ودفعات نقدية")
                        
                        c_st_a, c_st_b = st.columns(2)
                        with c_st_a:
                            sup_date = st.date_input("تاريخ التوريد", value=st.session_state.last_date)
                            car_number = st.text_input("رقم السيارة")
                            raw_weight_in = st.text_input("الوزن الخام", value="0")
                            paid_today_in = st.text_input("المبلغ الذي دفعته المحطة اليوم", value="0")
                        with c_st_b:
                            disc_type = st.radio("نوع الخصم", ["خصم بالنسبة (%)", "خصم بالكيلو"], horizontal=True)
                            disc_val_in = st.text_input("قيمة الخصم", value="0")
                            price_st_in = st.text_input("السعر", value="0")
                        
                        add_st_sup = st.form_submit_button("حفظ التوريد لصفحة المحطة")
                        
                        if add_st_sup:
                            r_w = clean_float(raw_weight_in)
                            d_v = clean_float(disc_val_in)
                            p_s = clean_float(price_st_in)
                            
                            if disc_type == "خصم بالنسبة (%)":
                                c_net = r_w - (r_w * (d_v / 100.0))
                            else:
                                c_net = max(0.0, r_w - d_v)

                            c_tot = c_net * p_s

                            st.session_state.last_date = sup_date
                            st.session_state.station_supplies.append({
                                "station": selected_station,
                                "date": str(sup_date),
                                "car": car_number,
                                "weight": r_w,
                                "disc_type": disc_type,
                                "discount": d_v,
                                "net_weight": c_net,
                                "price": p_s,
                                "total_money": c_tot,
                                "paid_amount": clean_float(paid_today_in)
                            })
                            save_data()
                            st.success("تم إضافه الحركه بنجاح!")
                            st.rerun()

                    st.markdown("---")
                    if st_records:
                        st.subheader(f"📋 جدول حركات وتوريدات محطة: {selected_station}")
                        
                        c_h1, c_h2, c_h3, c_h4, c_h5, c_h6, c_h7, c_h8, c_h9 = st.columns([1.1, 1, 1, 1, 1, 0.8, 1.1, 1.1, 1])
                        with c_h1: st.markdown("**التاريخ**")
                        with c_h2: st.markdown("**رقم السيارة**")
                        with c_h3: st.markdown("**الوزن الخام**")
                        with c_h4: st.markdown("**الخصم**")
                        with c_h5: st.markdown("**الصافي**")
                        with c_h6: st.markdown("**السعر**")
                        with c_h7: st.markdown("**الإجمالي**")
                        with c_h8: st.markdown("**المدفوع**")
                        with c_h9: st.markdown("**إجراءات**")
                        st.markdown("---")

                        for idx_st, s_rec in enumerate(st_records):
                            cols_row = st.columns([1.1, 1, 1, 1, 1, 0.8, 1.1, 1.1, 1])
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
                                c_sedit, c_sdel = st.columns(2)
                                with c_sedit:
                                    if st.button("✏️", key=f"edit_st_{selected_station}_{idx_st}"):
                                        st.session_state[f"editing_st_{selected_station}_{idx_st}"] = True
                                with c_sdel:
                                    if st.button("🗑️", key=f"del_st_{selected_station}_{idx_st}"):
                                        st.session_state.station_supplies.remove(s_rec)
                                        save_data()
                                        st.success("تم الحذف بنجاح!")
                                        st.rerun()

                            if st.session_state.get(f"editing_st_{selected_station}_{idx_st}", False):
                                with st.form(f"form_edit_st_{selected_station}_{idx_st}"):
                                    st.write("✏️ **تعديل توريد المحطة:**")
                                    es_date = st.date_input("التاريخ", value=datetime.datetime.strptime(s_rec['date'], "%Y-%m-%d").date())
                                    es_car = st.text_input("رقم السيارة", value=s_rec.get('car', ''))
                                    es_raw = st.text_input("الوزن الخام", value=str(s_rec.get('weight', 0)))
                                    es_disc_type = st.radio("نوع الخصم", ["خصم بالنسبة (%)", "خصم بالكيلو"], index=0 if s_rec.get('disc_type') == "خصم بالنسبة (%)" else 1)
                                    es_disc = st.text_input("قيمة الخصم", value=str(s_rec.get('discount', 0)))
                                    es_prc = st.text_input("السعر", value=str(s_rec.get('price', 0)))
                                    es_paid = st.text_input("المبلغ المدفوع", value=str(s_rec.get('paid_amount', 0)))

                                    if st.form_submit_button("💾 حفظ التعديل"):
                                        r_w = clean_float(es_raw)
                                        d_v = clean_float(es_disc)
                                        p_s = clean_float(es_prc)
                                        
                                        if es_disc_type == "خصم بالنسبة (%)":
                                            c_n = r_w - (r_w * (d_v / 100.0))
                                        else:
                                            c_n = max(0.0, r_w - d_v)

                                        c_t = c_n * p_s

                                        s_rec['date'] = str(es_date)
                                        s_rec['car'] = es_car
                                        s_rec['weight'] = r_w
                                        s_rec['disc_type'] = es_disc_type
                                        s_rec['discount'] = d_v
                                        s_rec['net_weight'] = c_n
                                        s_rec['price'] = p_s
                                        s_rec['total_money'] = c_t
                                        s_rec['paid_amount'] = clean_float(es_paid)
                                        st.session_state[f"editing_st_{selected_station}_{idx_st}"] = False
                                        save_data()
                                        st.success("تم التعديل بنجاح!")
                                        st.rerun()

                        print_st_html = f"""
                        <div id="print-section">
                            <div class="print-box">
                                <div class="print-header">
                                    <h2>🌾 شركة الرحمة لإدارة الأراضي والمحاصيل</h2>
                                    <p>📞 01000108658 | 01019381124</p>
                                    <h3>📜 كشف حساب نهائي للمحطة: {selected_station}</h3>
                                    <p><b>التاريخ:</b> {datetime.date.today().strftime('%Y-%m-%d')} | <b>تليفون المحطة:</b> {st_info['phone']}</p>
                                </div>
                                <div class="print-content">
                                    <p>• <b>إجمالي الوزن الخام:</b> {total_raw_w:,.2f} كجم</p>
                                    <p>• <b>إجمالي الوزن الصافي بعد الخصم:</b> {total_net_w:,.2f} كجم</p>
                                    <p>• <b>إجمالي قيمة المحصول المستحقة:</b> {total_station_money:,.2f} جنيه</p>
                                    <p>• <b>إجمالي المبلغ المدفوع من المحطة:</b> {total_station_paid:,.2f} جنيه</p>
                                </div>
                                <div style="background-color: #e3f2fd; padding: 10px; border-radius: 8px; border: 1px solid #bbdefb; text-align: center; margin-top: 10px;">
                                    <h3 style="color: #1565c0; margin: 0;">💰 المبلغ الباقي لشركة الرحمة عند المحطة: {remaining_on_station:,.2f} جنيه</h3>
                                </div>
                                <br><br>
                                <div style="display: flex; justify-content: space-between; text-align: center; padding: 0 30px; font-size: 13px;">
                                    <div><b>توقيع إدارة المحطة:</b> ..........................</div>
                                    <div><b>توقيع إدارة الشركة:</b> ..........................</div>
                                </div>
                            </div>
                        </div>
                        """
                        st.markdown(print_st_html, unsafe_allow_html=True)

                        if st.button("🖨️ طباعة كشف حساب المحطة / حفظ PDF (A4)", type="primary", key="btn_print_st"):
                            st.components.v1.html("<script>window.parent.print();</script>", height=0)

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
        client_display_map_p = {f"{l['owner']} ({l.get('type', 'بطاطا تحت الشرب')})": l["owner"] for l in st.session_state.lands}
        display_list_p = ["-- اختر اسم العميل --"] + list(client_display_map_p.keys())
        
        selected_display_p = st.selectbox("ابحث واختار العميل لعرض وتحديد أسعار بيع أوزان البطاطا:", display_list_p, index=0)
        
        if selected_display_p and selected_display_p != "-- اختر اسم العميل --":
            selected_prof_owner = client_display_map_p[selected_display_p]
            owner_recs = [r for r in st.session_state.land_accounts if r["owner"] == selected_prof_owner]
            
            st.markdown("---")
            st.subheader(f"🌾 جدول أوزان البطاطا المسجلة للعميل: {selected_prof_owner}")

            if owner_recs:
                saved_profits_dict = st.session_state.saved_profits.get(selected_prof_owner, {})
                
                total_expenses_p = sum(r.get("expense_amount", 0) for r in owner_recs)
                total_advanced_p = sum(r.get("advanced_cash", 0) for r in owner_recs)

                with st.form(f"detailed_profit_form_{selected_prof_owner}"):
                    st.markdown("##### قم بتحديد سعر البيع لكل وزنة على حدة في الجدول أدناه:")
                    
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
                                st.text_input(f"سعر صادر #{idx}", value=str(saved_profits_dict.get(f"sad_{idx}", 0.0)), key=f"p_sad_{selected_prof_owner}_{idx}", label_visibility="collapsed")
                        
                        if sec_w > 0:
                            cols_cp = st.columns([1.5, 1.5, 2, 2])
                            with cols_cp[0]: st.write(f"📅 {rec_date}")
                            with cols_cp[1]: st.write("درجة ثانية")
                            with cols_cp[2]: st.write(f"{sec_w:,.1f} كجم")
                            with cols_cp[3]:
                                st.text_input(f"سعر ثانية #{idx}", value=str(saved_profits_dict.get(f"sec_{idx}", 0.0)), key=f"p_sec_{selected_prof_owner}_{idx}", label_visibility="collapsed")

                        if far_w > 0:
                            cols_cp = st.columns([1.5, 1.5, 2, 2])
                            with cols_cp[0]: st.write(f"📅 {rec_date}")
                            with cols_cp[1]: st.write("فرزة")
                            with cols_cp[2]: st.write(f"{far_w:,.1f} كجم")
                            with cols_cp[3]:
                                st.text_input(f"سعر فرزة #{idx}", value=str(saved_profits_dict.get(f"far_{idx}", 0.0)), key=f"p_far_{selected_prof_owner}_{idx}", label_visibility="collapsed")

                        if raw_b_w > 0:
                            cols_cp = st.columns([1.5, 1.5, 2, 2])
                            with cols_cp[0]: st.write(f"📅 {rec_date}")
                            with cols_cp[1]: st.write("صادر بوكسة (صافي)")
                            with cols_cp[2]: st.write(f"{net_b_w:,.1f} كجم")
                            with cols_cp[3]:
                                st.text_input(f"سعر بوكسة #{idx}", value=str(saved_profits_dict.get(f"box_{idx}", 0.0)), key=f"p_box_{selected_prof_owner}_{idx}", label_visibility="collapsed")

                    st.markdown("---")
                    save_all_prices = st.form_submit_button("💾 حفظ أسعار البيع وحساب صافي الربح / الخسارة النهائي")
                    
                    if save_all_prices:
                        temp_dict = {}
                        for idx, rec in enumerate(owner_recs):
                            if rec.get("sader", 0.0) > 0:
                                temp_dict[f"sad_{idx}"] = clean_float(st.session_state.get(f"p_sad_{selected_prof_owner}_{idx}", 0.0))
                            if rec.get("second", 0.0) > 0:
                                temp_dict[f"sec_{idx}"] = clean_float(st.session_state.get(f"p_sec_{selected_prof_owner}_{idx}", 0.0))
                            if rec.get("farza", 0.0) > 0:
                                temp_dict[f"far_{idx}"] = clean_float(st.session_state.get(f"p_far_{selected_prof_owner}_{idx}", 0.0))
                            if rec.get("raw_weight", 0.0) > 0:
                                temp_dict[f"box_{idx}"] = clean_float(st.session_state.get(f"p_box_{selected_prof_owner}_{idx}", 0.0))
                        
                        st.session_state.saved_profits[selected_prof_owner] = temp_dict
                        save_data()
                        st.success("تم حفظ أسعار البيع والنتائج بنجاح!")
                        st.rerun()

                final_sales_rev = 0.0
                for idx, rec in enumerate(owner_recs):
                    saved_item_prices = saved_profits_dict
                    if rec.get("sader", 0.0) > 0:
                        final_sales_rev += rec.get("sader", 0.0) * clean_float(saved_item_prices.get(f"sad_{idx}", 0.0))
                    if rec.get("second", 0.0) > 0:
                        final_sales_rev += rec.get("second", 0.0) * clean_float(saved_item_prices.get(f"sec_{idx}", 0.0))
                    if rec.get("farza", 0.0) > 0:
                        final_sales_rev += rec.get("farza", 0.0) * clean_float(saved_item_prices.get(f"far_{idx}", 0.0))
                    if rec.get("raw_weight", 0.0) > 0:
                        final_sales_rev += rec.get("net_weight", 0.0) * clean_float(saved_item_prices.get(f"box_{idx}", 0.0))

                total_cost = total_expenses_p + total_advanced_p
                net_profit_loss = final_sales_rev - total_cost

                st.markdown("---")
                st.subheader(f"📊 ملخص النتيجة المالية لأرض: {selected_prof_owner}")
                
                res_col1, res_col2, res_col3, res_col4 = st.columns(4)
                with res_col1: st.metric("إجمالي قيمة البيع", f"{final_sales_rev:,.2f} جنيه")
                with res_col2: st.metric("إجمالي المصاريف", f"{total_expenses_p:,.2f} جنيه")
                with res_col3: st.metric("ما أخذه صاحب الأرض", f"{total_advanced_p:,.2f} جنيه")
                with res_col4: st.metric("صافي النتيجة", f"{net_profit_loss:,.2f} جنيه")
                    
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
            
            c_rem = c_total_val - c_advanced
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
