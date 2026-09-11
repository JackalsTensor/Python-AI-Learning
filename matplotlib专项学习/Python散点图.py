import matplotlib.pyplot as plt
fig, ax = plt.subplots()
x_data=range(1,1001)
y_data=[x**6 for x in x_data]
ax.scatter(x_data,y_data,s=100)
ax.set_title("Fangtasy's Matplotlib",fontsize=20)
ax.set_xlabel("x",fontsize=20)
ax.set_ylabel("y",fontsize=20)
ax.tick_params(labelsize=20)
ax.axis([0,1100,0,1_100_000000000000000])
plt.show()
