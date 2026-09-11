def bubble_sort(nums):
    n = len(nums)
    # 外层循环：控制排序轮数
    for i in range(n-1):
        # 标记是否提前有序（优化）
        swapped = False
        # 内层循环：每轮比较到n-1-i（后面已排好）
        for j in range(n-1-i):
            if nums[j] > nums[j+1]:
                # 交换元素（解包赋值超简洁）
                nums[j], nums[j+1] = nums[j+1], nums[j]
                swapped = True
        # 没有交换说明已有序，提前退出
        if not swapped:
            break
    return nums

# 测试
print(bubble_sort([3,1,4,2,5]))  # [1,2,3,4,5]