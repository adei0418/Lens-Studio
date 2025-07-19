#!/usr/bin/env python3
"""Simple command line calculator."""

import sys


def main():
    if len(sys.argv) != 4:
        print("Usage: calculator.py <num1> <operator> <num2>")
        print("Example: calculator.py 5 + 3")
        return

    num1 = float(sys.argv[1])
    op = sys.argv[2]
    num2 = float(sys.argv[3])

    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
    elif op == '*':
        result = num1 * num2
    elif op == '/':
        if num2 == 0:
            print("Error: Division by zero")
            return
        result = num1 / num2
    else:
        print(f"Unknown operator: {op}")
        return

    print(result)

if __name__ == "__main__":
    main()
