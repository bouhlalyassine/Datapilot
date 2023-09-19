import tempfile
import streamlit as st
from settings import *
from streamlit_lottie import st_lottie
import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3

# streamlit run SQL_Data_Pilot.py

st.set_page_config(page_title=TITLE,
    page_icon=PAGE_ICON,
    layout="wide")

with open(css_file) as f: # Load the CSS file
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.markdown("<h2 style=\
    'text-align : center;\
    font-weight : bold ;\
    font-family : Arial;'>\
    SQL Data Pilot</h2>", unsafe_allow_html=True)

st.markdown("""---""")

with st.sidebar :
    clickable_img_logo = get_img_with_href(pp_logo_portfolio, 'https://ybouhlal.streamlit.app/', 70, "blank")
    st.markdown(clickable_img_logo, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    clickable_img = get_img_with_href(linkpic_code, 'https://github.com/bouhlalyassine/SQL_Data_Pilot',
        170, "blank")
    st.markdown(clickable_img, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    nav_menu = option_menu(menu_title=None, options=['Home', 'Example APP'], 
        default_index=0, orientation="vertical",
        icons=["house", "app"],
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"2px", "--hover-color": "#805E83"}
        })

if nav_menu == 'Home':
    st.markdown("<br>", unsafe_allow_html=True)
    colpi1, colpi2 = st.columns([80, 20], gap="small")
    with colpi1:
        st.info("SQL Data Pilot is a webapp example for navigating and analyzing SQL data.\
                It consists of two parts :\
                    \n - 1) Creation of a SQL database, allowing users to modify it if needed and extract data in Excel format\
                    \n - 2) Analysis of provided data and creation of a summary PDF report\
                \n\n ► In order to access the app please click on [Example APP] on the left side menu")
    
    with colpi2:
        lottie_sql_db = load_lottiefile(lottie_sql_db)
        st_lottie(
            lottie_sql_db,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # medium ; high ; low
            height=150)

    st.markdown("<br>", unsafe_allow_html=True)
    esp_1, col_vid_tuto, esp_2 = st.columns([space, tuto_space, space], gap="small")
    with col_vid_tuto :
        with open(tuto_sql_db, "rb") as tuto_file:
            tuto_sql_db_byte = tuto_file.read()
        st.video(tuto_sql_db_byte)


if nav_menu == 'Example APP':
    # st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2= st.tabs(["Data Base | EXCEL File", "Data Analysis | PDF Report"])

    with tab1 :
        # Connect to the database
        conn = sqlite3.connect(sql_db)

        # Load the data from the sales table into a Pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM sales ORDER BY sale_date ASC", conn)
        conn.close()

        displayed_df = st.data_editor(df, num_rows = "dynamic", height=400, 
            use_container_width= True)
    
        temp_exl = tempfile.NamedTemporaryFile(delete=True)
        temp_exl_filename = temp_exl.name + f'.xlsx'
        displayed_df.to_excel(temp_exl_filename, sheet_name='Data', index=False)

        last_file = curstom_excel_df(temp_exl_filename)

        with open(last_file, "rb") as f:
            binary_data = f.read()

        # timestr = time.strftime("%d-%H%M%S")
        excel_namefile  = f"Extracted Data.xlsx"

        st.download_button(
            label="Download Excel File",
            data=binary_data,
            file_name=excel_namefile)
        
        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander('Data Base creation code', expanded=False):
            st.info("Using Python and sqlite3, here is an example code to create a 50 rows SQL Data Base")

            st.code("""
                import sqlite3

                conn = sqlite3.connect('sql_database.db') # Where 'sql_database.db' is a given data base name
                c = conn.cursor()

                # Create the "sales" table
                c.execute('''CREATE TABLE sales (
                                sale_date DATE,
                                customer_name TEXT,
                                product_name TEXT,
                                product_quantity INTEGER,
                                product_unit_buy_price DECIMAL(10, 2),
                                product_unit_sale_price DECIMAL(10, 2)
                            )''')

                # Generate random data and insert it into the sales table
                for i in range(50): # 50 = number of lines I created (for this example)
                    data = generate_random_data() # this is only a function i created, that adds random data to the database
                    c.execute('''INSERT INTO sales (sale_date, customer_name, product_name, product_quantity, product_unit_buy_price, product_unit_sale_price)
                        VALUES (?, ?, ?, ?, ?, ?)''', data)

                # Commit the changes and close the connection
                conn.commit()
                conn.close()""",
                language="python", line_numbers=False)


    with tab2 :
        analysis_df = get_sql_df(displayed_df)
        
        month_fig = month_chart(analysis_df)
        custo_fig = customer_chart(analysis_df)
        prod_fig = product_chart(analysis_df)

        kpis = total_sql_kpi(analysis_df)

        # st.markdown("""---""")

        col0, col1, col2, col3 = st.columns(4)
        with col0 :
            st.subheader("Total Sales")
            st.subheader(f"{kpis[0]:,} $".format(kpis[0]).replace(',', ' '))
            # st.subheader(f"T {total_Arr:,}")
        with col1 :
            st.subheader("Total Taxes (5%)")
            st.subheader(f"{kpis[1]:,} $".format(kpis[1]).replace(',', ' '))
        with col2 :
            st.subheader("Total Net Profit")
            st.subheader(f"{kpis[2]:,} $".format(kpis[2]).replace(',', ' '))
        with col3 :
            st.subheader("Net Profit")
            st.subheader(f"{kpis[3]:,} %".format(kpis[3]).replace(',', ' '))

        st.markdown("""---""")

        st.plotly_chart(month_fig, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.plotly_chart(prod_fig, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.plotly_chart(custo_fig, use_container_width=True)


        figs =[month_fig, prod_fig, custo_fig]

        Byte_pdf = create_PDF(figs, kpis[0], kpis[1], kpis[2], kpis[3])

        st.download_button(
            label="Download PDF Report",  data=Byte_pdf, file_name='Sales Report.pdf',
                mime="application/pdf")
   