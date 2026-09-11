def selection_sort(nums):
    n = len(nums)
    for i in range(n-1):
        # 找[i, n-1]范围内最小元素的索引
        min_idx = i
        for j in range(i+1, n):
            if nums[j] < nums[min_idx]:
                min_idx = j
        # 交换到已排序区
        nums[i], nums[min_idx] = nums[min_idx], nums[i]
    return nums

# 测试
print(selection_sort([3,1,4,2,5]))  # [1,2,3,4,5]