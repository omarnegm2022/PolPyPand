file_notes = """
Did you know about the WARNING when run a streamlit script using the command: `python app.py`
__________________________
# WARNING streamlit.runtime.scriptrunner_utils.script_run_context: 
Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.

this warning does not indicate a security vulnerability or a security exploit. 
Instead, it is an architectural limitation of how Streamlit manages user sessions and browser states.
When you run python app.py instead of streamlit run app.py, Streamlit runs in what it calls "bare mode."

Why the Warning Happens (Architectural, Not Security)

Streamlit is designed around a reactive, web-server architecture. 
It needs to know which browser tab is requesting a button click or a data update. 
To track this, Streamlit attaches a ScriptRunContext object to the execution thread.
When you bypass the native bootstrapper by using python app.py:
1. The script runs as a regular, standard Python process.
2. The Streamlit library initializes, but the backend web server (Tornado) and session handlers are never started.
3. Any UI commands (like st.write) run blindly because there is no active browser session thread to talk to, triggering the warning.
"""


# from panDAX_to_poLQS import *

import os
import streamlit as st
# lazy polar and eager panda
st.logo("🔭")
st.set_page_config(
    page_title="Setting up",
    page_icon="📐",
    # layout="wide",
)

if "progress" not in st.session_state or "path" not in st.session_state:
    st.session_state.progress = 0
    st.session_state.path = """`Home\\`"""

# with st.sidebar:
	# sb_container = st.container()
st.title("A benchmark that explores whether Polars can replace Pandas or complement it.")
st.warning("""
### ✨inpsired by:\n
**:blue[[Benchmarking High-Performance pandas Alternatives | a Datacamp tutorial by Zoumana Keita](https://www.datacamp.com/tutorial/benchmarking-high-performance-pandas-alternatives)]**
	""")

st.image(
"https://media.datacamp.com/legacy/image/upload/v1686564840/datarhys_an_absurdist_oil_painting_of_a_cyborg_panda_and_a_cybo_c7deba5e_79f3_498a_ada9_381d6fe0b77a_b943fa043f.png"
)

st.markdown(
"* Image source: \n\n [**https://www.datacamp.com/tutorial/high-performance-data-manipulation-in-python-pandas2-vs-polars**](https://www.datacamp.com/tutorial/high-performance-data-manipulation-in-python-pandas2-vs-polars)"
)

st.markdown("***")
st.error("""
# `/!\\ Disclaimer:` \n
**:blue[This project is open-source, so feel free to contribute improvements if the initial version misses the mark.]**
	""")

target_size_mb = 1
file_path = ''
file_status_container = st.container()
to_proceed = False
with st.sidebar.container():
	for col in st.columns(1):
# https://medium.com/codetodeploy/getting-the-most-out-of-your-streamlit-page-maximizing-the-screen-use-13c2b8c5a87d
		with st.container(border=True):
			st.text("Hello!")

			st.write("""`Home\\`""")
			st.progress(0)
	file_name = st.text_input(
	    "Data source(experimental): ", "")  # Databel - Data.csv
	sb = st.sidebar.button
	sz_n_ram = 0
	if '.' in file_name:
		sz_n_dsk = os.path.getsize(file_name)
		with open(file_name, 'r') as file_to_read:
			header = file_to_read.readline()
			# sample_csv_row = file_to_read.readline()
			rows_original = file_to_read.readlines()
		sample_csv_row = rows_original[0]

		avg_bytes_per_row = len(sample_csv_row.encode('utf-8')) - 1
		header_bytes = len(header.encode('utf-8'))
		num_rows_original = len(rows_original)

		st.text(
		    f"approx. size on disk: {sz_n_dsk/10**6} MB, with number of rows: {num_rows_original}")
		with st.container(border=True):
			target_size_mb = st.number_input(
		    """How much bigger would you like it?\n\n (in MB)""")

	# st.info("Scroll down the image to start!")

# with open(file_path, 'rb') as f:
        # Read the first 4 bytes
        # magic_bytes = f.read(4)#if normal ASCII, the file is de-compressed
# print(magic_bytes)#diabetes.csv
	
	if target_size_mb > 1:  # aug_dataset(target_size_mb, file_name):
		if 'file_stats' not in st.session_state:
			file_stats = {"size":None, "op_state":False, "nlines":0}
			#Soon it will be a list/tuple in the same order keys are defined.

		required_total_rows = ((target_size_mb * 1024 * 1024) -
		                       header_bytes) // avg_bytes_per_row
		required_multiplier = int(required_total_rows // num_rows_original)
		# print(required_multiplier)
		predicted_size_bytes = (
		    avg_bytes_per_row * required_total_rows) + header_bytes
		predicted_size_mb = predicted_size_bytes / (1024 * 1024)

		
		st.info(f"Predicted File Size: {predicted_size_mb:.6f} MB")
		if predicted_size_mb / 1024 > 1:  # TODO: not accurate!!!
			st.error("""You are on the risk crashing the session.
							Stay below 900 MB, Or....
				""")
			st.info("""
				You can Download the project as 🗜️, and expand dataset size according to your device limit. 
				After running the following command in *Anaconda prompt*:
				`streamlit run app.py`
				, opened in the extracted project folder.
				""")
		elif not to_proceed:# st.button("Apply?"):
			new_file_name = "bench_" + file_name
			try:
				with open(new_file_name, 'x') as file_to_write:
					file_to_write.write(header)
					with st.spinner("Augmenting..."):
						for rep in range(required_multiplier):
							file_to_write.writelines(rows_original)
			except (FileNotFoundError, PermissionError, TypeError, OSError) as e:
					st.session_state.file_stats = (
						os.path.getsize(file_name)/1024/1024,
						f""":red[{new_file_name}: {e!s}🥲]""" + "For now, we are using the original dataset.", 
						len(rows_original)
					)
					# st.query_params.from_dict({"fileName": file_name})
					st.switch_page("pages/p1.py", query_params={"fileName": new_file_name})
			# except PermissionError:
			# 	file_status_container.warning("Error: OS permissions prevent reading metadata for this file.")
			# except TypeError:
			# 	file_status_container.warning("Error: The file path must be a string or path-like object.")
			# except OSError as e:
			# 	file_status_container.error(f"System error: {e}")
			else:
				to_proceed = 1
				st.write("Scroll down for the status ↘️")

@st.fragment
# https://youtu.be/ZI7_INDzqbw?si=tfIjWcGqMM8TXNE6
# @st.dialog("Hi")
def proceed():
	with st.form(key="my_container_form"):
	    # st.write("Fill out this container data:")
	    # user_text = st.text_input("Type something...")
	    # user_option = st.selectbox("Pick one", ["A", "B", "C"])
		st.write("""### ✅Done!""")
	    # The application only reruns once this button is clicked
		submit_button = st.form_submit_button(label="Click me to proceed >>")

	if submit_button:
# https://github.com/streamlit/docs/blob/main/content/develop/concepts/app-design/button-behavior-and-examples.md
		st.session_state.file_stats = (
			os.path.getsize(new_file_name)/1024/1024,
			"""Dataset enlarged =)""", 
			required_multiplier * len(rows_original)
			)
		# st.query_params.from_dict({"fileName": new_file_name})
		st.switch_page("pages/p1.py", query_params={"fileName": new_file_name})
	# 
		# if file_status_container.button("""### ✅Done! Click me to proceed >>"""):
			# st.session_state.file_size = os.path.getsize(file_name)/1024/1024, required_multiplier * len(rows_original)
			# st.switch_page("pages/p1.py")
					# 
			# benchmarking_df = pd_df.loc[pd_df.index.repeat(required_total_rows // num_rows_original)]
			# benchmarking_df.to_csv("bench_" + file_name, index = False)
			
if to_proceed:
	proceed()	
st.set_option("client.showSidebarNavigation", False)

