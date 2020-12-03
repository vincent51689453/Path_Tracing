# Path_Tracing
A path tracing application for hygiene procedure monitoring

1. single_id_analyzer.py: It is a script for reconstructing the path. Meanwhile, it is able to plot distance measurments from self to other zones.

![image](https://github.com/vincent51689453/Path_Tracing/blob/main/output/single_id_trace.JPG)

![image](https://github.com/vincent51689453/Path_Tracing/blob/main/output/single_id_plot_LPF.JPG)

2. single_id_overlay.py: It is a script to overlay all the results from different log file (same id) and visualize it. You need to set **i and j** to indicate the starting log_file and the ending log_file to overlay.

![image](https://github.com/vincent51689453/Path_Tracing/blob/main/output/sinlge_id_overlay_2_files.JPG)

3. single_id_counter.py: It is a script to count all the data inside a log file and generate visualized result. Meanwhile, it helps to produce cumulative statistical results from result_buffer.csv and publish it to node red dash board through mqtt.

Some parameters can be adjusted to improve the accuracy:

- single_id_counter.py -> contact_diff -> It helps to compare the difference of time for two contact records.

- single_id_counter.py -> Plotting_enable -> It helps to ENABLE/DISABLE the graph plotting analysis.

- single_id_counter.py -> patient_thresh -> It is the threshold distance between staff and patient

- single_id_counter.py -> MQTT_Enable -> It helps to ENABLE/DISABLE the MQTT process

- statistic.py -> theta_1 & theta_2 -> They are the orientation limitations of filtering patient contacts.


![image](https://github.com/vincent51689453/Path_Tracing/blob/main/output/Text_output.PNG)
