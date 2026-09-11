from scipy.optimize import linprog
c=[-2,-3,5]         #第一步：填目标函数
A_ub=[[-2,5,-1],[1,3,1]]            #第二步：填《=函数
b_ub=[-10,22]
A_eq=[[1,1,1]]          #第三步：填=约束函数
b_eq=[7]
bounds=[(0,None),(0,None),(0,None)]         #第四步：填变量约束函数
result=linprog(c,A_ub=A_ub,b_ub=b_ub,A_eq=A_eq,b_eq=b_eq,bounds=bounds,method='highs')          #第五步：运行求解（套模板）
print("求解状态：","最优解"if result.success else "无可行解")
print("x1的最优值:",result.x[0])            #第六步：写运算或者输出结果
print("x2的最优值:",result.x[1])
print("x3的最优值:",result.x[2])
print("目标函数z的最大值",-result.fun)