from scipy.optimize import linprog
c=[1,-5,-2]
A_ub=[[-4,1,-1],[2,5,4]]
b_ub=[-12,15]
A_eq=[[1,3,-2]]
b_eq=[6]
bounds=[(0,None),(0,None),(0,None)]
result=linprog(c,A_ub=A_ub,b_ub=b_ub,A_eq=A_eq,b_eq=b_eq,bounds=bounds,method='highs')
print("求解状态：","最优解"if result.success else "无可行解")
print("x1的最优值:",result.x[0])
print("x2的最优值:",result.x[1])
print("x3的最优值:",result.x[2])
print("目标函数z的最大值",-result.fun)