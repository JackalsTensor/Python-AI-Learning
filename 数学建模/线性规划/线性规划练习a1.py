from scipy.optimize import linprog
c=[-4,2,-3]
A_ub=[[-3,4,-2],[1,2,3]]
b_ub=[-8,10]
A_eq=[[2,1,-1]]
b_eq=[5]
bounds=[(0,None),(0,None),(0,None)]
result=linprog(c,A_ub=A_ub,b_ub=b_ub,A_eq=A_eq,b_eq=b_eq,bounds=bounds,method='highs')
print("求解状态：","最优解"if result.success else "无可行解")
print("x1的最优值:",result.x[0])
print("x2的最优值:",result.x[1])
print("x3的最优值:",result.x[2])
print("目标函数z的最大值",-result.fun)