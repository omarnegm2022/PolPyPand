# PageOne contents

import logging

file_notes = """
# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). 
The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
@author: CoreyMSchafer
"""

# logging.basicConfig(filename='test.log', level=logging.DEBUG, 
                    # format='%(asctime)s:%(levelname)s:%(message)s')


import time
import streamlit as st
from DAXops import *
import uuid
st.logo("📊")
st.set_page_config(
    page_title="Exploration",
    page_icon="🔭",
    layout="wide"
)
# Check if a session ID already exists; if not, create it ONCE for this session
if "session_id" not in st.session_state:
  st.session_state.session_id = uuid.uuid4().hex[:8]

# This ID will now stay constant even if the user interacts with widgets
# (though it will reset if they hit browser refresh or close the tab)
# st.write(f"Persistent Session ID: {st.session_state.session_id}")
### st.write("User Header Headers:", st.context.headers)
try: 
    print(st.session_state.file_stats)
    st.session_state.progress = 50
    st.session_state.path = """`.\\Expoloratory\\`"""
    with st.sidebar.container(border=True):
            st.text("Current location:")
            st.write(st.session_state.path)
            st.progress(st.session_state.progress)
except AttributeError:
    st.warning("""### Sorry, but you have to start it again\n ## :orange[:/]""")
    st.session_state.progress = 0
    st.session_state.path = """`Home\\`"""
    time.sleep(3)
    st.switch_page("app.py")

st.success(f"{st.session_state.file_stats[1]}" + '\n\n' + 
    f"Current file size: {st.session_state.file_stats[0]:.3f} MB" + 
    f", with n_records: {st.session_state.file_stats[2]}")
st.write("# Dataset overview\n(where: `i64` refers to INT, `f64` refers to FLOAT)\n")

# setup_logging()
st.write("### After the athletic man, at the top right corner↗️, goes away...\n #### > `hover on the top right corner of the columns to show more options 👀`")
df_view = prep_dataset(st.query_params["fileName"])
st.write(df_view)


# 1. Inject custom CSS to center all table headers and cells
st.markdown(
    """
    <style>
    /* Centers the entire table container on the page*/ 
    .stTable {
        margin-right: auto;
        margin-left: auto;
        width: fit-content !important;
        table-layout: fixed !important;
    }

    th{
        text-align: center !important;
    	word-wrap: break-word !important;
    }
    td{
        text-align: left !important;
    	white-space: no-wrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.text_input(' ',label_visibility='hidden',key="hint",placeholder="""Once you click `Apply`, the comparison table will result below.""")
# 

#`label` got an empty value. This is discouraged for accessibility reasons and 
# may be disallowed in the future by raising an exception. 
#   Please provide a non-empty label and hide it with label_visibility if needed.

# 2. Define your dynamic comparison content
# (Using a dictionary format since it's not a standard dataset)
dax_formula = []


fhead_map = {"    ":[None,'No function selected!'],
"Total":["SUM","   Adds all the numbers in a column."],
"Average":["AVG","   Returns the average (arithmetic mean) of all the numbers in a column."],
"Min_Max":["MxMn","   Returns a minimum value of a column."],
"n_of_distinct":["DISTINCTCOUNT","   Counts the number of distinct values in a column."]}

col_only = ["SUM","AVG"]
with st.sidebar.container() as monitors:
    # try:
        dax_formula.append(fhead_map[st.selectbox(
        "Function Header: ", 
        list(fhead_map.keys()))
    ]
        )
        st.sidebar.info(dax_formula[-1][-1])
    # except KeyError:
        # st.sidebar.info(fhead_map['___'])
#https://discuss.streamlit.io/t/display-order-of-widgets-when-using-callbacks/20993/7
#3rd solution: st.columns
Arguments = set()
if dax_formula[-1][0] == 'DISTINCTCOUNT':#in col_only:
    Arguments.add("Select any column from the table shown:")
else:
    Arguments.add("\nSelect a numerical column from the table shown: (float or integer)")
st.session_state.pd_stats, st.session_state.pl_stats = 0,0
with st.sidebar.container() as mons:
    
    dax_formula.append(st.text_input("Arguments:-"))
    st.text(f"{''.join(Arguments)}")
    # st.text()
    if dax_formula[-2][0] == 'DISTINCTCOUNT' and dax_formula[-1].title().strip() not in [''] + df_view['column'].to_list():
        st.error("Invalid column!")
    elif dax_formula[-1].title().strip() not in ([''] + """Account Length (in months)
Local Calls
Local Mins
Intl Calls
Intl Mins
Extra International Charges
Customer Service Calls
Avg Monthly GB Download
Unlimited Data Plan
Extra Data Charges
Age
Monthly Charge
Total Charges""".split('\n')):
#'' is when the end-user leaves the text box empty.
        st.markdown(":red[not a numerical attribute!]")
fun_apply = st.sidebar.button("Apply")
# st.divider()
if fun_apply:
    # st.session_state.disabled = False
    if dax_formula[0][0] == "MxMn":
        st.sidebar.write("""DAX syntax (to get maximum value:\n\n""" f"""`MAX(Databel[{', '.join(dax_formula[-1:])}])`""")
    else:
        st.sidebar.write("""DAX syntax:\n\n""" f"""`{dax_formula[0][0]}(Databel[{', '.join(dax_formula[-1:])}])`""")
    mat = Matistical(dax_formula[-1])
    # print(dax_formula, getattr(mat,dax_formula[-2][0],None))
    dax_formula = list(getattr(mat,dax_formula[-2][0])())
    st.session_state.pd_stats, st.session_state.pl_stats = dax_formula
    if st.session_state.pd_stats[0] != st.session_state.pl_stats[0]:
        # print("diff!")
        st.warning(f"Pandas returns: {st.session_state.pd_stats[0]}",'\n',f"Polars: {st.session_state.pl_stats[0]}")
    else:
        st.sidebar.text(f"Result: {st.session_state.pd_stats[0]}")
    # st.sidebar.text(f"Result:\n {dax_formula}")    

    comparison_data = {
    """""": ('### :green[⏱️] :grey[Time] :grey[Execution]','### :green[💾] :grey[RAM] :grey[Usage]'),
    """# :green[🐻‍❄️]\n## Pola.rs""": [f"{st.session_state.pl_stats[1]}",
     f"{'\n'.join(st.session_state.pl_stats[2:])}"],
    """# :green[🐼]\n## Pandas""": [f"{st.session_state.pd_stats[1]}", 
    f"{'\n'.join(st.session_state.pd_stats[2:])}"],


}
    st.table(comparison_data)
    # logging.debug(st.session_state.pd_stats); logging.debug(st.session_state.pl_stats)


# st.session_state.pd_stats, st.session_state.pl_stats = dax_formula 
    #Back to the previous value since there is sync of states between the button


# First row: two columns
with st.sidebar.container(border=True):
    st.write("""### Nav buttons:""")
    col1_row1, col2_row1 = st.columns(2)
    
    with col1_row1:
        if st.button("< Home"):
            st.session_state.progress = 0
            st.session_state.path = """`Home\\`"""
            st.switch_page("app.py")
    
    with col2_row1:
        if st.button("Verdict >"):
            st.session_state.progress = 100
            st.session_state.path = ".\\Verdict"
            st.switch_page("pages/p2.py")

import psutil

if False:    #TODO: after completing the MVP
    tab1, tab2, tab3, tab4 = st.tabs([
        " Math & statistical functions",
        " Filter functions",
        " Logical functions",
        "📈 Model",
    
    ])
    if tab == "Home":
        st.header("Home")