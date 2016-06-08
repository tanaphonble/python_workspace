from sys import argv

script, input_file , write_or_read, nodes, threads = argv
data = open(input_file).readlines()
output = open('inject.txt', 'w')

def normalize_data(line):
	ln_1 = line.split(":")[1]
	ln_2 = ln_1.split("[")[0]
	return ln_2

hr = data[16].split(":")[1]
mn = data[16].split(":")[2]
sc = data[16].split(":")[3]	
time = "%s:%s:%s" % (hr, mn, sc)

op_rate = normalize_data(data[0])
partition_rate = normalize_data(data[1])
row_rate = normalize_data(data[2])
latency_mean = normalize_data(data[3])
latency_median = normalize_data(data[4])
p950 = normalize_data(data[5])
p990 = normalize_data(data[6])
p999 = normalize_data(data[7])
latency_max = normalize_data(data[8])
total_partitions = normalize_data(data[9])
total_errors = normalize_data(data[10])
total_gc_count = normalize_data(data[11])
total_gc_mb = normalize_data(data[12])
total_gc_time = normalize_data(data[13])
avg_gc_time = normalize_data(data[14])
stdev_gc_time = normalize_data(data[15])
total_operation_time = time.strip()

query_insert = """
USE [Cassandra]
GO

INSERT INTO [dbo].[cassandra-stress]
           ([op_rate]
           ,[partition_rate]
           ,[row_rate]
           ,[latency_mean]
           ,[latency_median]
           ,[latency_95th_percentile]
           ,[latency_99th_percentile]
           ,[latency_99.9th_percentile]
           ,[latency_max]
           ,[Total_partitions]
           ,[Total_errors]
           ,[total_gc_count]
           ,[total_gc_mb]
           ,[total_gc_time_s]
           ,[avg_gc_time_ms]
           ,[stdev_gc_time_ms]
           ,[Total_operation_time]
           ,[w_or_r]
           ,[nodes]
           ,[threads])
     VALUES
           (%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,%s
           ,'%s'
           ,'%s'
           ,%s
           ,%s)
GO
""" % (op_rate, partition_rate, row_rate, latency_mean, latency_median, p950, p990, p999, latency_max, total_partitions, total_errors, total_gc_count, total_gc_mb, total_gc_time, avg_gc_time, stdev_gc_time, total_operation_time, write_or_read, nodes, threads)

# print query_insert
output.write(query_insert)