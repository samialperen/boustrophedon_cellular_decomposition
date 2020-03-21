from matplotlib import pyplot as plt



#x_axis1 = ["DFS","BFS","Genetic Alg.","Hill Climb.","Simulated Anneal.","MIMIC"]
#y_axis1 = [1.0657520033419133e-07,2.421780955046415e-07,0.34132279418408873,0.004113932698965072,
#            0.001007028785534203,2.3405914925038815]
x_axis1 = ["DFS","BFS","Hill Climb.","Simulated Anneal."]
y_axis1 = [10.657520033419133,24.21780955046415,4113.932698965072,
            1007.028785534203]
x_axis2 = ["Genetic Alg.","MIMIC"]
y_axis2 = [0.34132279418408873,2.3405914925038815]

bar_width = 1

f, axes = plt.subplots(2, 1)
f.suptitle('Convergence Time for Large Map with Low Number of Obstacles')


axes[0].bar(x_axis1, y_axis1, color='#7f6d5f', width=bar_width, edgecolor='white')
axes[0].set_xlabel('Different Optimization Methods')
axes[0].set_ylabel('Convergence Time (micro seconds)')


axes[1].bar(x_axis2, y_axis2, color='#557f2d', width=bar_width, edgecolor='white')
axes[1].set_xlabel('Different Optimization Methods')
axes[1].set_ylabel('Convergence Time (seconds)')


######################################################################33



#x_axis1 = ["DFS","BFS","Genetic Alg.","Hill Climb.","Simulated Anneal.","MIMIC"]
#y_axis1 = [1.306990161538124e-07,2.7898396365344526e-07,0.4721514669014141,0.023594312206842005,
#            0.0013403398916125298,5.412915337597951]
x_axis3 = ["DFS","BFS","Simulated Anneal."] ##Hill climbing diverges
y_axis3 = [13.06990161538124,27.898396365344526,1340.3398916125298]
x_axis4 = ["Genetic Alg.","MIMIC"]
y_axis4 = [0.4721514669014141,5.412915337597951]

bar_width = 1

f2, axes2 = plt.subplots(2, 1)
f2.suptitle('Convergence Time for Large Map with High Number of Obstacles')


axes2[0].bar(x_axis3, y_axis3, color='#7f6d5f', width=bar_width, edgecolor='white')
axes2[0].set_xlabel('Different OptiAmization Methods')
axes2[0].set_ylabel('Convergence Time (micro seconds)')


axes2[1].bar(x_axis4, y_axis4, color='#557f2d', width=bar_width, edgecolor='white')
axes2[1].set_xlabel('Different Optimization Methods')
axes2[1].set_ylabel('Convergence Time (seconds)')


######################################################################33

x_axis5 = ["DFS","BFS","Hill Climb.","Simulated Anneal."]
y_axis5 = [8.780485950410367,29.729492962360384,443.33459809422495,584.6634041517973]
x_axis6 = ["Genetic Alg.","MIMIC"]
y_axis6 = [0.23870504209771753,0.9090649277204648]

bar_width = 1

f3, axes3 = plt.subplots(2, 1)
f3.suptitle('Convergence Time for Small Map with Low Number of Obstacles')


axes3[0].bar(x_axis5, y_axis5, color='#7f6d5f', width=bar_width, edgecolor='white')
axes3[0].set_xlabel('Different Optimization Methods')
axes3[0].set_ylabel('Convergence Time (micro seconds)')


axes3[1].bar(x_axis6, y_axis6, color='#557f2d', width=bar_width, edgecolor='white')
axes3[1].set_xlabel('Different Optimization Methods')
axes3[1].set_ylabel('Convergence Time (seconds)')


######################################################################33

x_axis7 = ["DFS","BFS","Hill Climb.","Simulated Anneal."]
y_axis7 = [12.20970007125288,31.45319988107076,8778.156200060038,1200.5476999547681]
x_axis8 = ["Genetic Alg.","MIMIC"]
y_axis8 = [0.4501033263000863,4.34933532740015]

bar_width = 1

f4, axes4 = plt.subplots(2, 1)
f4.suptitle('Convergence Time for Small Map with High Number of Obstacles')


axes4[0].bar(x_axis7, y_axis7, color='#7f6d5f', width=bar_width, edgecolor='white')
axes4[0].set_xlabel('Different Optimization Methods')
axes4[0].set_ylabel('Convergence Time (micro seconds)')


axes4[1].bar(x_axis8, y_axis8, color='#557f2d', width=bar_width, edgecolor='white')
axes4[1].set_xlabel('Different Optimization Methods')
axes4[1].set_ylabel('Convergence Time (seconds)')


################################################################

# Large map low number of objects
xaxis1 = ["DFS","BFS","Genetic Alg.","Hill Climb.","Simulated Anneal.","MIMIC"]
coverage_times1 = [476.129, 479.883, 510.237, 525.763, 425.989, 489.749 ]
# Large map high number of objects
xaxis2 = ["DFS","BFS","Genetic Alg.","Simulated Anneal.","MIMIC"]
coverage_times2 = [663.802, 672.442, 591.547, 598.305, 507.125]
# Small map low number of objects
xaxis3 = ["DFS","BFS","Genetic Alg.","Hill Climb.","Simulated Anneal.","MIMIC"]
coverage_times3 = [127.438, 126.197, 124.357, 131.483, 133.576, 138.142]
# Small map high number of objects
xaxis4 = ["DFS","BFS","Genetic Alg.","Hill Climb.","Simulated Anneal.","MIMIC"]
coverage_times4 = [213.596, 269.609, 193.117, 191.323, 194.862, 193.583]

f5 = plt.figure()
plt.bar(xaxis1, coverage_times1, color='#557f2d', width=bar_width, edgecolor='white')
plt.title("Total Coverage Time for Large Map with Low Number of Obstacles")
plt.xlabel("Different Optimization Methods")
plt.ylabel("Total Coverage Time (seconds)")

f6 = plt.figure()
plt.bar(xaxis2, coverage_times2, color='#557f2d', width=bar_width, edgecolor='white')
plt.title("Total Coverage Time for Large Map with High Number of Obstacles")
plt.xlabel("Different Optimization Methods")
plt.ylabel("Total Coverage Time (seconds)")

f7 = plt.figure()
plt.bar(xaxis3, coverage_times3, color='#557f2d', width=bar_width, edgecolor='white')
plt.title("Total Coverage Time for Small Map with Low Number of Obstacles")
plt.xlabel("Different Optimization Methods")
plt.ylabel("Total Coverage Time (seconds)")

f8 = plt.figure()
plt.bar(xaxis4, coverage_times4, color='#557f2d', width=bar_width, edgecolor='white')
plt.title("Total Coverage Time for Small Map with High Number of Obstacles")
plt.xlabel("Different Optimization Methods")
plt.ylabel("Total Coverage Time (seconds)")





plt.show()



