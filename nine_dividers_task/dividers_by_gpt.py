def count_numbers_with_nine_divisors(N):
    def count_divisors(n):
        count = 0
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                count += 1
                if i != n // i:
                    count += 1
        return count

    count = 0
    for number in range(1, N + 1):
        if count_divisors(number) == 9:
            count += 1
    return count

# Example usage:
N = 100
result = count_numbers_with_nine_divisors(N)
print(result)
