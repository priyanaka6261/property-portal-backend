import os
import pandas as pd
import streamlit as st

from api_client import APIClient, APIError


# ===== PAGE CONFIG =====
st.set_page_config(page_title="Property Portal", page_icon="🏠", layout="wide")

# ===== SIMPLE STYLING (cards + tags) =====
st.markdown(
    """
<style>
.block-container { padding-top: 0.8rem; }

/* cards */
.pp-card {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
  padding: 16px 18px;
}
.pp-card-blue {
  background: #2563EB;
  color: #ffffff;
}
.pp-card-title {
  font-size: 13px;
  color: #6B7280;
}
.pp-card-title-light {
  color: rgba(255,255,255,0.85);
}
.pp-card-value {
  margin-top: 6px;
  font-size: 22px;
  font-weight: 600;
  color: #111827;
}
.pp-card-value-light {
  color: #ffffff;
}

/* panel */
.pp-panel {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
  padding: 18px 20px;
}
.pp-panel-title {
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 10px;
}

/* chip */
.pp-chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  border: 1px solid #E5E7EB;
  margin-right: 4px;
}
.pp-chip-green  { color:#16A34A; border-color:rgba(22,163,74,0.3); }
.pp-chip-amber  { color:#D97706; border-color:rgba(217,119,6,0.3); }
.pp-chip-slate  { color:#4B5563; border-color:rgba(148,163,184,0.6); }
</style>
""",
    unsafe_allow_html=True,
)

# ===== SESSION + CLIENT =====
if "token" not in st.session_state:
    st.session_state.token = None
if "email" not in st.session_state:
    st.session_state.email = None
if "api_url" not in st.session_state:
    st.session_state.api_url = os.getenv(
        "PROPERTY_PORTAL_API_URL", "http://127.0.0.1:8000")

api = APIClient(st.session_state.api_url)


def api_error_box(e: APIError):
    st.error(f"API error ({e.status_code})")
    st.code(str(e.detail))


def as_df(data):
    if isinstance(data, list) and data:
        return pd.DataFrame(data)
    return pd.DataFrame()


# ===== SIDEBAR NAV =====
st.sidebar.image(
    "https://dummyimage.com/80x24/2563eb/ffffff&text=TMS",
    use_column_width=False,
)
st.sidebar.markdown("## ")

st.sidebar.markdown("### Menu")
page = st.sidebar.radio(
    "",
    [
        "Dashboard",
        "All Properties",
        "My Properties",
        "Search",
        "Manage (CRUD)",
        "Login / Register",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("### API")
st.session_state.api_url = st.sidebar.text_input(
    "FastAPI URL", value=st.session_state.api_url
).strip()
api = APIClient(st.session_state.api_url)

if st.session_state.token:
    st.sidebar.success(f"Logged in:\n{st.session_state.email}")
else:
    st.sidebar.info("Not logged in")

# ===== LOGIN / REGISTER PAGE =====
if page == "Login / Register":
    st.title("Login / Register")

    tab_login, tab_reg = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            try:
                res = api.login(email, password)
                token = res.get("access_token")
                if token:
                    st.session_state.token = token
                    st.session_state.email = email
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("No token returned from API.")
            except APIError as e:
                api_error_box(e)

    with tab_reg:
        with st.form("reg_form"):
            r_email = st.text_input("Email", key="reg_email")
            r_password = st.text_input(
                "Password", type="password", key="reg_pw")
            r_role = st.selectbox("Role", ["user", "agent", "admin"])
            r_sub = st.form_submit_button("Register")

        if r_sub:
            try:
                res = api.register(r_email, r_password, r_role)
                st.success("User registered")
                st.json(res)
            except APIError as e:
                api_error_box(e)

    st.stop()

# ===== AUTH GUARD FOR OTHER PAGES =====
if not st.session_state.token:
    st.warning("Please login first (open **Login / Register** in sidebar).")
    st.stop()

token = st.session_state.token

# ===== COMMON DATA LOADS =====
all_props = []
stats = {}

try:
    all_props = api.list_properties(token)
    stats = api.stats()
except APIError as e:
    api_error_box(e)
    st.stop()

df_all = as_df(all_props)

if "price" in df_all.columns:
    df_all["price"] = pd.to_numeric(df_all["price"], errors="coerce")

# ===== HELPER: STATUS COLORS =====


def status_chip(status: str) -> str:
    status = str(status or "").lower()
    if status in ["available"]:
        klass = "pp-chip-green"
    elif status in ["sold", "rented"]:
        klass = "pp-chip-amber"
    else:
        klass = "pp-chip-slate"
    return f'<span class="pp-chip {klass}">{status.title()}</span>'


# ===== DASHBOARD =====
if page == "Dashboard":
    st.title("Dashboard")

    total_properties = len(df_all)
    total_available = int((df_all["status"].str.lower(
    ) == "available").sum()) if "status" in df_all.columns else 0
    total_sold = int((df_all["status"].str.lower() ==
                     "sold").sum()) if "status" in df_all.columns else 0
    total_rented = int((df_all["status"].str.lower() == "rented").sum(
    )) if "status" in df_all.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
<div class="pp-card pp-card-blue">
  <div class="pp-card-title-light">Total Properties</div>
  <div class="pp-card-value-light">{total_properties}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
<div class="pp-card">
  <div class="pp-card-title">Available</div>
  <div class="pp-card-value">{total_available}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
<div class="pp-card">
  <div class="pp-card-title">Sold</div>
  <div class="pp-card-value">{total_sold}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
<div class="pp-card">
  <div class="pp-card-title">Rented</div>
  <div class="pp-card-value">{total_rented}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("")

    col_left, col_right = st.columns((2, 1.1))

    # --- left: all properties with filters ---
    with col_left:
        st.markdown(
            '<div class="pp-panel"><div class="pp-panel-title">All Properties</div>', unsafe_allow_html=True)

        f1, f2, f3 = st.columns(3)
        with f1:
            q = st.text_input("Search title/location", placeholder="e.g. Pune")
        with f2:
            if "status" in df_all.columns:
                status_options = sorted(
                    df_all["status"].dropna().unique().tolist())
            else:
                status_options = []
            status_filter = st.multiselect(
                "Status", status_options, default=status_options)
        with f3:
            if "price" in df_all.columns and df_all["price"].notna().any():
                pmin = float(df_all["price"].min())
                pmax = float(df_all["price"].max())
                # Only show slider if we have a valid range (min < max)
                if pmin < pmax:
                    price_range = st.slider(
                        "Price range", min_value=pmin, max_value=pmax, value=(pmin, pmax))
                else:
                    # If all prices are the same (or 0), use a default range or disable
                    st.info(f"All prices: ${pmin:,.0f}")
                    price_range = None
            else:
                st.info("No price data")
                price_range = None

        df_view = df_all.copy()

        if q:
            mask = False
            for col in [c for c in ["title", "location"] if c in df_view.columns]:
                mask = mask | df_view[col].astype(
                    str).str.contains(q, case=False, na=False)
            df_view = df_view[mask]

        if status_filter and "status" in df_view.columns:
            df_view = df_view[df_view["status"].isin(status_filter)]

        if price_range is not None and "price" in df_view.columns:
            df_view = df_view[
                (df_view["price"] >= price_range[0]) & (
                    df_view["price"] <= price_range[1])
            ]

        st.dataframe(df_view, use_container_width=True, height=360)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- right: stats from /properties/stats ---
    with col_right:
        st.markdown(
            '<div class="pp-panel"><div class="pp-panel-title">Status Stats (/properties/stats)</div>', unsafe_allow_html=True)

        if isinstance(stats, dict) and stats:
            stats_df = pd.DataFrame(
                [{"status": k, "count": v} for k, v in stats.items()]
            ).set_index("status")
            st.bar_chart(stats_df)
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.info("No stats returned.")

        st.markdown("</div>", unsafe_allow_html=True)

# ===== ALL PROPERTIES (SIMPLE TABLE) =====
elif page == "All Properties":
    st.title("All Properties")
    st.dataframe(df_all, use_container_width=True, height=520)

# ===== MY PROPERTIES =====
elif page == "My Properties":
    st.title("My Properties")
    try:
        my_props = api.my_properties(token)
        df_my = as_df(my_props)
        st.dataframe(df_my, use_container_width=True, height=520)
    except APIError as e:
        api_error_box(e)

# ===== SEARCH (USES /properties/search PUBLIC ENDPOINT) =====
elif page == "Search":
    st.title("Search Properties")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        location = st.text_input("Location contains", placeholder="city, area")
    with c2:
        min_price = st.number_input(
            "Min price", min_value=0.0, value=0.0, step=1000.0)
    with c3:
        max_price = st.number_input(
            "Max price", min_value=0.0, value=0.0, step=1000.0)
    with c4:
        run = st.button("Search", type="primary")

    if run:
        try:
            result = api.search_properties(
                location=location or None,
                min_price=min_price if min_price > 0 else None,
                max_price=max_price if max_price > 0 else None,
            )
            df_search = as_df(result)
            st.dataframe(df_search, use_container_width=True, height=520)
        except APIError as e:
            api_error_box(e)

# ===== MANAGE (CREATE / UPDATE / DELETE) =====
elif page == "Manage (CRUD)":
    st.title("Manage Properties (Create / Update / Delete)")

    left, right = st.columns((1.1, 1.4), gap="large")

    # --- create ---
    with left:
        st.markdown(
            '<div class="pp-panel"><div class="pp-panel-title">Create</div>', unsafe_allow_html=True)
        with st.form("create_form"):
            title = st.text_input("Title")
            location = st.text_input("Location")
            price = st.number_input("Price", min_value=0.0, step=1000.0)
            status = st.selectbox("Status", ["available", "sold", "rented"])
            submitted = st.form_submit_button("Create Property")

        if submitted:
            try:
                res = api.create_property(
                    token,
                    title=title,
                    location=location,
                    price=float(price),
                    status=status,
                )
                st.success("Created")
                st.json(res)
                st.rerun()
            except APIError as e:
                api_error_box(e)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- update / delete ---
    with right:
        st.markdown(
            '<div class="pp-panel"><div class="pp-panel-title">Update / Delete</div>', unsafe_allow_html=True)

        if df_all.empty or "id" not in df_all.columns:
            st.info("No properties available.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            pid = st.selectbox("Select property (by id)",
                               df_all["id"].tolist())
            row = df_all[df_all["id"] == pid].iloc[0].to_dict()

            st.markdown("#### Selected")
            st.write(row)

            with st.form("update_form"):
                u_title = st.text_input(
                    "Title", value=str(row.get("title", "")))
                u_location = st.text_input(
                    "Location", value=str(row.get("location", "")))
                u_price = st.number_input(
                    "Price",
                    min_value=0.0,
                    step=1000.0,
                    value=float(row.get("price", 0.0)),
                )
                u_status = st.selectbox(
                    "Status",
                    ["available", "sold", "rented"],
                    index=["available", "sold", "rented"].index(
                        str(row.get("status", "available")).lower()
                    )
                    if str(row.get("status", "available")).lower() in ["available", "sold", "rented"]
                    else 0,
                )
                u_sub = st.form_submit_button("Update Property")

            if u_sub:
                try:
                    res = api.update_property(
                        token,
                        int(pid),
                        u_title,
                        u_location,
                        float(u_price),
                        u_status,
                    )
                    st.success("Updated")
                    st.json(res)
                    st.rerun()
                except APIError as e:
                    api_error_box(e)

            if st.button("Delete Property", type="secondary"):
                try:
                    res = api.delete_property(token, int(pid))
                    st.success("Deleted")
                    st.json(res)
                    st.rerun()
                except APIError as e:
                    api_error_box(e)

            st.markdown("</div>", unsafe_allow_html=True)
