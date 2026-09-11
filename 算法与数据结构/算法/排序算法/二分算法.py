def binary_search01(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 5
print(binary_search01(nums, target))
if __name__ == '__main__':
    binary_search01(nums, target)