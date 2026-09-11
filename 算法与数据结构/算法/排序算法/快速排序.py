def quick_sort(nums):
    # 递归终止条件
    if len(nums) <= 1:
        return nums
    # 选基准值（选第一个元素）
    pivot = nums[0]
    # 分治：小于基准、等于基准、大于基准
    left = [x for x in nums[1:] if x <= pivot]
    right = [x for x in nums[1:] if x > pivot]
    # 递归排序+合并
    return quick_sort(left) + [pivot] + quick_sort(right)

# 测试
print(quick_sort([3,1,4,2,5]))  # [1,2,3,4,5]