def insertion_sort(nums):
    n = len(nums)
    for i in range(1, n):
        # 待插入元素
        temp = nums[i]
        j = i - 1
        # 已排序区后移，找到插入位置
        while j >= 0 and nums[j] > temp:
            nums[j+1] = nums[j]
            j -= 1
        nums[j+1] = temp
    return nums

# 测试
print(insertion_sort([3,1,4,2,5]))  # [1,2,3,4,5]