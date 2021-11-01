# Python Backend home assignment

**General instructions**
- This exercise is meant to check your skills, ability to adopt to our stack, handling unknown code, research and asking questions
- Before your begin, clone this repo and save your changes on the cloned repo
- Exercise 1 (make the code work) is mandatory, the other exercises you can provide general coding instructions and guidelines, you can save those answers in the readme or in a new document
- There are no wrong answers and you are not expected to know all areas in-depth
- Reach out to us if you are confused or need clarifications
- Recommendation: don't spend more than 6 hours
- Complete this exercise within 4 days


**Code background**
- This [aws_prefix.py](aws_prefix.py) code was created quickly as a POC by some engineer who left the company
- We are not sure it’s efficient, reliable or designed correctly 

**Exercise 1 - make the code work:**
- The [aws_prefix.py](aws_prefix.py) code fails on some exception
- Find the bug in the code and fix it:
  - What code changes need to be made? provide a working version of the file
  - What tools and steps did you use to debug the code?

**Exercise 2 - error handling:**

- On what areas would you add try-except to avoid unhandled exception?
- We want structured logging (time, level, message, etc..) to a file and later to CloudWatch, What kind of framework \ module would you recommend for logging?
- **Bonus**: add logging configuration to the file, replace the print statements

**Exercise 3 - expose the API:**

- We want to expose the code as REST API on Linux (ubuntu), i.e. http://127.0.0.1:8080/get_prefix
- What frameworks would you recommend? We are looking for something simple, reliable and fast
- **Bonus**: provide the code to run the API

**Exercise 4 - sending response to SNS:**
- We want to publish each region 100 prefix to SNS for further processing, no limitation on the number of messages, but should be efficient
- What is the SNS message size limit?
- Should we reduce the 100 limit? Is there a better way to ensure we meet the size criteria?

**Exercise 5 - running as a lambda:**
- Can we run this code as an AWS lambda?
- What general changes need to be made?
- **Bonus**: provide the lambda python file

**Exercise 6 -  running as container:**
- We want to run this code in AWS ECS or in EC2 container
- What steps need to made to create a container?

