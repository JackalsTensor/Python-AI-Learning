import matplotlib.pyplot as plt
x_data=[1,3,9,11,13,17,19]
y_data=[1,3,9,11,13,17,19]
fig, ax = plt.subplots()
ax.set_title("Fangtasy's Matplotlib",fontsize=20)
ax.set_xlabel("x",fontsize=20)
ax.set_ylabel("y",fontsize=20)
ax.tick_params(labelsize=20)
ax.plot(x_data,y_data,color='blue',linewidth=2)
plt.show()