# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 17:53:34 2026

Transpiling DAX into SQL-like execution through Python frameworks for EDA.

@author: omarn
"""
# from app import file_name
import timeit,	tracemalloc
import pandas as pd
pd_df = dict()
import polars as pl

pl_df = dict()


# file_name = "Databel - Data.csv"


import logging

# csv_format = "%(asctime)s,%(message)s"
# formatter = logging.Formatter(csv_format)
# log_file = "bench_log.csv"
# with open(log_file, "w", encoding="utf-8") as f:
    # f.write("timestamp,framework,time(ms),current_ram(MB),ram_peak(MB),memo_diff(MB)\n")


import logging
import json
import sys

# Configure a custom JSON formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            # "level": record.levelname,
            # "logger": record.name,
            # "message": record.getMessage(),
            # "path": record.pathname,
            # "line": record.lineno
            "function":record.funcName #Name of function containing the logging call.
        }
        # Include any custom fields passed via the `extra` parameter
        if hasattr(record, "duration_ms"):
            log_record["duration_ms"] = record.duration_ms
        if hasattr(record, "current_ram_MB"):
            log_record["current_ram_MB"] = record.current_ram_MB
        if hasattr(record, "ram_peak_MB"):
            log_record["ram_peak_MB"] = record.ram_peak_MB
        if hasattr(record, "memo_diff_MB"):
            log_record["memo_diff_MB"] = record.memo_diff_MB
        if hasattr(record, "framework"):
        	log_record["framework"] = record.framework          
                
        return json.dumps(log_record)



df_map = dict()
log_file_name = 'log.jsonl'
def prep_dataset(file_name):	
	global pd_df, pl_df, df_map 	
	tracemalloc.start()
	pd_df = pd.read_csv(file_name)
	memory_usage = tracemalloc.get_traced_memory()
	tracemalloc.stop()

#• Unlike Polars (which crashes immediately when it hits an unexpected type), 
#	Pandas will seamlessly upcast the column on the fly mid-parse [pydata.org].

	pl_df = pl.read_csv(file_name, infer_schema_length=None)


	type_mapping = {
    'int64': pl.Int64,
    'float64': pl.Float64,
    'object': pl.String,
    'bool': pl.Boolean
}#for custom schema overriding method*
	df_map = {"pandas": pd_df, "polars": pl_df}
	 
	return pl_df.glimpse(return_type="frame")


# Setup file handler
logger = logging.getLogger("StructuredApp")
def init_log(usr_name):
	global log_file_name, logger
	if log_file_name == 'log.jsonl':
		log_file_name = "bench_" + usr_name + log_file_name
		handler = logging.FileHandler(log_file_name, mode="a", encoding="utf-8")
		handler.setFormatter(JSONFormatter())
		
		logger.setLevel(logging.INFO)
		logger.addHandler(handler)
	return log_file_name
# Simulate log events
# logger.warning("High memory usage detected", extra={"user_id": "admin", "duration_ms": 450.1})

	
				#infer_schema_length=pl.scan_csv(file_name).select(pl.len()).collect().item())
				#infer_schema_length=pd_df.shape[0])
	#pl.from_pandas(pd_df)
#https://pola.rs/posts/schema-evolution/
#[ENCOUNTERED!] polars.exceptions.ComputeError: ```invalid primitive value found during CSV parsing```
# "https://raw.githubusercontent.com/keitazoumana/Experimentation-Data/main/diabetes.csv" such URLs are supported by both!


# t1 = timeit.default_timer()
# fun()
# t2 = timeit.default_timer()
#We manually measure the start and end time of a code block. This is helpful when you want more control over what you're timing.
# Explanation: timeit.default_timer() records start and end times around the fun function and their difference gives the time taken for a single execution.

class Matistical:
	def __init__(self,column = None, expression = None, table = None):
		"""
			the object will be instantiated once the single DAX is entred, 
			even other attributes were N/R.
		"""
		self.column = column
		self.expression = expression
		self.table = table
	#misc. vars
	NUMERATOR = None
	DENOMINATOR = None

	def SUM(self):
		"""single summation -  Adds all the numbers in a column
"""
		
		for fm_wrk, _df in df_map.items():
			start = timeit.default_timer()
			tracemalloc.start()
			req = sum(list(_df[self.column]))
			memory_usage = tracemalloc.get_traced_memory()
			tracemalloc.stop()
			end = timeit.default_timer()
			current, peak, diff = memory_usage[0]/ (1024**2), memory_usage[1]/ (1024**2), (memory_usage[1] - memory_usage[0]) / (1024**2) 
			fmt_stats = {#Could use the unpack method at the LHS as follows: (duration, value), (current,value), (peak,value), (diff,value)
			#... then repack them using: dict([(duration, value), (current,value), (peak,value), (diff,value)])
			#>> validated through interactive REPL.
			"framework": fm_wrk,
			"duration_ms": f"{(end - start)*1000:.3f}"	,
			"current_ram_MB": f"{current:.6f}"			,
			"ram_peak_MB": f"{peak:.3f}"				,
			"memo_diff_MB": f"{diff:.6f}"  
			}
			
			# logger.info(f"{fm_wrk},{fmt_time},{fmt_current},{fmt_peak},{fmt_diff}")
			logger.info(None, extra=fmt_stats)
			yield req, f"{fmt_stats["duration_ms"]} milliseconds", \
						f"Current: {fmt_stats["current_ram_MB"]} MB", \
						f"Peak: {fmt_stats["ram_peak_MB"]} MB", \
						f"Peak - Current: {fmt_stats["memo_diff_MB"]} MB" 
	
	def AVG(self):
		"""   Returns the average (arithmetic mean) of all the numbers in a column
"""
		for fm_wrk, _df in df_map.items():
			start = timeit.default_timer()
			tracemalloc.start()
			req = sum(list(_df[self.column])) / len(list(_df[self.column]))
			memory_usage = tracemalloc.get_traced_memory()
			tracemalloc.stop()
			end = timeit.default_timer()
			current, peak, diff = memory_usage[0]/ (1024**2), memory_usage[1]/ (1024**2), (memory_usage[1] - memory_usage[0]) / (1024**2) 
			fmt_stats = {#Could use the unpack method at the LHS as follows: (duration, value), (current,value), (peak,value), (diff,value)
			#... then repack them using: dict([(duration, value), (current,value), (peak,value), (diff,value)])
			#>> validated through interactive REPL.
			"framework": fm_wrk,
			"duration_ms": f"{(end - start)*1000:.3f}"	,
			"current_ram_MB": f"{current:.6f}"			,
			"ram_peak_MB": f"{peak:.3f}"				,
			"memo_diff_MB": f"{diff:.6f}"  
			}
			
			# logger.info(f"{fm_wrk},{fmt_time},{fmt_current},{fmt_peak},{fmt_diff}")
			logger.info(None, extra=fmt_stats)
			yield req, f"{fmt_stats["duration_ms"]} milliseconds", \
						f"Current: {fmt_stats["current_ram_MB"]} MB", \
						f"Peak: {fmt_stats["ram_peak_MB"]} MB", \
						f"Peak - Current: {fmt_stats["memo_diff_MB"]} MB"
		return 1
	def MxMn(self):
		"""   Returns the sum of an expression evaluated for each row in a table
"""
		for fm_wrk, _df in df_map.items():
			start = timeit.default_timer()
			tracemalloc.start()
			req = f"""max_value = {max(list(_df[self.column]))} , 
					  min_value = {min(list(_df[self.column]))}"""
			memory_usage = tracemalloc.get_traced_memory()
			tracemalloc.stop()
			end = timeit.default_timer()
			current, peak, diff = memory_usage[0]/ (1024**2), memory_usage[1]/ (1024**2), (memory_usage[1] - memory_usage[0]) / (1024**2) 
			fmt_stats = {#Could use the unpack method at the LHS as follows: (duration, value), (current,value), (peak,value), (diff,value)
			#... then repack them using: dict([(duration, value), (current,value), (peak,value), (diff,value)])
			#>> validated through interactive REPL.
			"framework": fm_wrk,
			"duration_ms": f"{(end - start)*1000:.3f}"	,
			"current_ram_MB": f"{current:.6f}"			,
			"ram_peak_MB": f"{peak:.3f}"				,
			"memo_diff_MB": f"{diff:.6f}"  
			}
			
			# logger.info(f"{fm_wrk},{fmt_time},{fmt_current},{fmt_peak},{fmt_diff}")
			logger.info(None, extra=fmt_stats)
			yield req, f"{fmt_stats["duration_ms"]} milliseconds", \
						f"Current: {fmt_stats["current_ram_MB"]} MB", \
						f"Peak: {fmt_stats["ram_peak_MB"]} MB", \
						f"Peak - Current: {fmt_stats["memo_diff_MB"]} MB"
		return 1
	# return expression+conditional_sum(expression)

	def DISTINCTCOUNT(self):
		"""   Counts the number of rows from an expression that evaluates to a non-blank value
"""
	#table
		for fm_wrk, _df in df_map.items():
			start = timeit.default_timer()
			tracemalloc.start()
			req = len(set(_df[self.column]))
			memory_usage = tracemalloc.get_traced_memory()
			tracemalloc.stop()
			end = timeit.default_timer()
			current, peak, diff = memory_usage[0]/ (1024**2), memory_usage[1]/ (1024**2), (memory_usage[1] - memory_usage[0]) / (1024**2) 
			fmt_stats = {#Could use the unpack method at the LHS as follows: (duration, value), (current,value), (peak,value), (diff,value)
			#... then repack them using: dict([(duration, value), (current,value), (peak,value), (diff,value)])
			#>> validated through interactive REPL.
			"framework": fm_wrk,
			"duration_ms": f"{(end - start)*1000:.3f}"	,
			"current_ram_MB": f"{current:.6f}"			,
			"ram_peak_MB": f"{peak:.3f}"				,
			"memo_diff_MB": f"{diff:.6f}"  
			}
			
			# logger.info(f"{fm_wrk},{fmt_time},{fmt_current},{fmt_peak},{fmt_diff}")
			logger.info(None, extra=fmt_stats)
			yield req, f"{fmt_stats["duration_ms"]} milliseconds", \
						f"Current: {fmt_stats["current_ram_MB"]} MB", \
						f"Peak: {fmt_stats["ram_peak_MB"]} MB", \
						f"Peak - Current: {fmt_stats["memo_diff_MB"]} MB"
		return 1
#NOTE: moving Python UDF-heavy Pandas logic into Python callbacks inside Polars can throw away a large part of the optimizer's advantage.
if __name__ == "__main__":
	import psutil, os 
	import gc #We would better implement the project in R/C++*
	def benchmark_memory():
		process = psutil.Process(os.getpid())
    	
    	# 2. Capture baseline RSS memory (in MB)
		mem_before = process.memory_info().rss / (1024 * 1024)
		req = sum(list(pl_df["Age"]))
		mem_after = process.memory_info().rss / (1024 * 1024)

		mem_freed = process.memory_info().rss / (1024 * 1024)
		print(f"Memory Before : {mem_before:.2f} MB")
		print(f"Memory After  : {mem_after:.2f} MB")
		print(f"Net Memory Delta: {mem_after - mem_before:.2f} MB")
		print(f"Memory After Cleanup: {mem_freed:.2f} MB")
	test_obj = Matistical("Age")
	stats = list(test_obj.SUM())
	# if stats[0][0] != stats[1][0]:
		# print("diff!")
	# print(f"Pandas: {stats[0]}",'\n',f"Polars: {stats[1]}")


	# 2. Estimate average size per row in CSV format
# To do this accurately, we can serialize a single row (or a small sample) to a string 
# and measure its length in bytes (including commas and the newline character '\n').
	# sample_csv_row = pd_df.iloc[0].to_csv(index=False, header=False)
	# avg_bytes_per_row = len(sample_csv_row.encode('utf-8'))
	# header_bytes = len(",".join(pd_df.columns).encode('utf-8')) + 1
	target_size_mb = 800 # Imported

# Calculate how many total rows you need based on the sample row size
	target_size_bytes = target_size_mb * 1024 * 1024
	# required_total_rows = (target_size_bytes - header_bytes) // avg_bytes_per_row
	# num_rows_original = len(pd_df)
	# required_multiplier = required_total_rows // num_rows_original

# print(f"To reach ~{target_size_mb} MB, you need a duplication factor of approximately: {required_multiplier:,}")
	# while os.path.getsize("bench_" + file_name)/(1024**2) < 800.0:
		# benchmarking_df = pd_df.loc[pd_df.index.repeat(rep)]		
		# benchmarking_df.to_csv("bench_" + file_name, index = False)
	# benchmarking_df = pd_df.loc[pd_df.index.repeat(required_multiplier)]
	# print(required_multiplier)

		
	