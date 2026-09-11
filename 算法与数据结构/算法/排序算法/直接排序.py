#直接用 Python 内置排序
nums=[2,1, 3, 4, 5, 21, 7, 8, 9, 10]
nums.sort()
print(nums)
nums.sort(reverse=True)
print(nums)

#对二维数组排序(按某一列)
nums=[[2,1],[3,4],[5,21],[7,8],[9,10]]
nums.sort(key=lambda x:x[1])
print(nums)