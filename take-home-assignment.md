# Blink labs take-home assignment

## Overview
You are to implement a simple fullstack app for a coding tutor, where the user is able to ask simple questions of how to write some javascript functions, and the AI assistant will reply with a solution and a simple explanation too, in order to help the user learn coding. The frontend should allow the user to use the function.
The platform should reject answering any irrelevant question.

## Tech requirements
The frontend is to be written in NextJS/typescript, and the AI functions are to written in a separate backend written in python.
The frontend should make an API call to this backend, to generate a short javascript function, and a one-line explanation of the function, to teach the user how to code.

You have flexibility on the specific packages you want to use.
Please include as much comments as possible, to explain what you are trying to achieve.

## Evaluation criteria
Since this is an open-ended question, besides the basic functionality of the end-to-end, try to demonstrate your skills and knowledge in writing 
- ways to improve performance of AI code generation,
- good code structure, quality and conformance to best practices, 
- considerations for completeness of use-case, 
- production-readiness, and 
- security. 
You will not be evaluated on the aesthetic of the frontend, but on having a good code structure that is in-line with modern nextjs/react best-practices.

## Some example input/output between the frontend and AI could be:

input: add 2 numbers
output:
```
{
  "code":"function add(num1, num2) {\n return num1 + num2;\n}\n",
  "explanation": "This function takes two parameters and returns their sum."
}
```

input: are you a boy
output: returns a 400 HTTP error for invalid input

input: calculate factorial
output:
```
{
  "code":"function factorial(n) {\nreturn (n === 0 || n === 1) ? 1 : n * factorial(n - 1);\n}",
  "explanation": "The function uses a ternary operator to check if n is 0 or 1 (base case), returning 1 in that case, otherwise, it returns n multiplied by the factorial of n - 1, working recursively."
}
```

## Submission

Please send us a github repo of your completed assignment by the dateline(30 June).
We will schedule a quick session for you to present your code.
