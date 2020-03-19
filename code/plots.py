from matplotlib import pyplot as plt

fig1 = plt.figure()
x_axis1 = ["DFS","BFS","Genetic Alg.","Hill Climb.","Simulated Anneal.","MIMIC"]
y_axis1 = [1.0657520033419133e-07,2.421780955046415e-07,0.3557590821059421,0.004113932698965072,0.001007028785534203,2.3405914925038815]
plt.plot(x_axis1,y_axis1)
plt.title("Convergence Time for Large Map with Low Number of Obstacles")
plt.xlabel("Different Optimization Methods")
plt.ylabel("Convergence Time (seconds)")
plt.show()
plt.close()

fig2 = plt.figure()
x_axis2 = ["DFS","BFS","Genetic Alg.","Hill Climb.","Simulated Anneal.","MIMIC"]
y_axis2 = [426.1296889251098,479.8831956561189,525.7637033849023,507.004113932698965072,425.98983178683557,412.74928567186]
plt.plot(x_axis2,y_axis)
plt.title("Total Coverage Time for Large Map with Low Number of Obstacles")
plt.xlabel("Different Optimization Methods")
plt.ylabel("Total Coverage Time (seconds)")
plt.show()
plt.close()




