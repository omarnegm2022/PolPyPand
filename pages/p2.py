# PageOne contents

# from app import *
# if "progress" not in st.session_state:
import streamlit as st, \
plotly.express as px, pandas as pd
import polars as pl

try: 
    st.session_state.progress = 100
    st.session_state.path = """`.\\Verdict`"""
    with st.sidebar.container(border=True):
            st.text("End of the Project.")
            st.write(st.session_state.path)
            st.progress(st.session_state.progress)
except AttributeError:
    st.warning("""### Err, logs weren't recorded\n ## 🙄 \n""")
    time.sleep(3)
    st.switch_page("/pages/p1.py")

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    # layout="centered",
)

# bar = st.sidebar.progress(st.session_state.progress)
st.title("Hover over the canvas in each tab for more controls and to read the tooltips.")
tab1, tab2, tab3 = st.tabs([
        "📶 Histogram",
        """🥧 Pie""",
        """🍫 bar""",
    ])
try:
    df = pd.read_json("bench_log.jsonl", lines=True)#Gemini hallucination>> ,comment="#")
except ValueError:
    import json
#
    with open("bench_log.jsonl",'r') as file_to_chk:
        df = pd.DataFrame([json.loads(line) for line in file_to_chk if not line.strip().startswith("�")])

with tab1:
    fig = px.histogram(
            # pl.read_ndjson("bench_log.jsonl",ignore_errors=True)
            df
            ,
            x=['framework','function'],
            y="duration_ms",
            color_discrete_map = {0:'#F29A2E',1:'#F22E2E'},#2:'purple',3:'green'}
            title="Durations w.r.t (library, function)"
        )
    with st.container(border=True):
        event_data = st.plotly_chart(fig, on_select="rerun")
with tab2:
    fig = px.pie(
            # pl.read_ndjson("bench_log.jsonl")
            df
            ,
            hover_data=['framework'],
            names="function",
            values="current_ram_MB",
            title="Total Memory usage w.r.t (library, function)"
        )
    with st.container(border=True):
        event_data = st.plotly_chart(fig)#, on_select="rerun")
with tab3:
# df = {}#px.data.tips()
    fig = px.bar(
        # pl.read_ndjson("bench_log.jsonl")
        df
        ,
        color="framework",
        x="function",
        y="ram_peak_MB",
        title="Highest malloc for each function within the framework"
    )
    with st.container(border=True):
        event_data = st.plotly_chart(fig, on_select="rerun")
# st.write(event_data)
with st.sidebar:
    st.title("Benchmarking tools:\n#")
    st.markdown(
    '### <tt style="font-family: monospace; font-weight: normal;">`timeit` — Measure execution time of small code snippets</tt>\n\n > :blue[to find memory leaks, analyze memory usage]', 
    unsafe_allow_html=True
)
    st.markdown("**Source code:** [Lib/timeit.py](https://github.com/python/cpython/blob/3.15/Lib/timeit.py)")
  # st.markdown('***')
    st.divider()
    st.markdown(
    '### <tt style="font-family: monospace; font-weight: normal;">`tracemalloc` — Trace memory allocations</tt>', 
    unsafe_allow_html=True
)
    st.markdown("**Source code:** [Lib/tracemalloc.py](https://github.com/python/cpython/blob/3.15/Lib/tracemalloc.py)")
    with st.container(border=True):
        st.markdown("*#The_end*\n\n Have a look at my portfolio for previous projects: https://omarnegm3.lovable.app/")

st.write("""# Relevant articles:
---
* [Pandas or Polars? The Real 2026 Performance Numbers for Data Science Teams](https://www.refontelearning.com/blog/pandas-vs-polars-performance-comparison)
* [Polars vs Pandas on 10GB: The 2026 Benchmarks, Memory Limits, and the DuckDB Factor](https://vertexfrontier.com/polars-vs-pandas-benchmarks-10gb/)
* [DuckDB 2.0 vs Polars 2.0 vs pandas 3.0: benchmarks on a billion rows](https://plotly.com/blog/duckdb-vs-polars-vs-pandas/)""")


if __name__ == "__main__":
    st.set_option("client.showSidebarNavigation", False)

    df = pd.read_json(
    "log_file.jsonl", lines=True
    #A standard JSON file is structured as a single large array of objects 
    # (e.g., [{"a": 1}, {"a": 2}]). pd.read_json() expects this by default.
#>> .jsonl (JSON Lines or newline-delimited JSON)
)
    print(df.dtypes)  # 'timestamp' will be datetime64[ns]

# Plot directly
    # fig = px.bar(df, x="timestamp", y="duration_ms")
    # fig.show()

    # print(fig_histogram)

# df = dict()
# serial_vals = []
# with open("bench_log.csv",'r') as logfile:
    # df = {k:[] for k in logfile.readline().strip().split(',')}
    # serial_vals = map(lambda val: val.strip().split(','), logfile.readlines())
# for val in serial_vals:
    # for i,k in enumerate(df.keys()):
        # df[k] = val[i]
# _ = ("""line 1602, in build_dataframe
    # pd.DataFrame(args["data_frame"])
# ----------------------^^^^^^^^^^^
# NotImplementedError: 
# Unable to convert data_frame of type <class 'dict'> to pandas DataFrame. 
# Please provide a supported dataframe type or a type that can be passed to pd.DataFrame.
    # """)	