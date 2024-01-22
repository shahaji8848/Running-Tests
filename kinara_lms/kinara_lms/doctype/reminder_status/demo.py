def breck_function():
    print("Inside breck_function")
    # Some code here

# Main part of the program
for i in range(5):
    print("Iteration:", i)
    if i == 2:
        breck_function()
        break

print("After the loop")
