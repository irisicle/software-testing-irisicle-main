## Lab Goals
- Unit and Feature Testing: Practice isolated function tests and integration testing across several functions.
- Mocking: Understand how to mock dependencies to create isolated unit tests.
- Performance and Load Testing: Learn how to simulate concurrent users and measure the application's performance under load.
- Security Testing: Identify and test for common security vulnerabilities like input sanitization and password strength.
- Continuous Integration (CI): Set up GitHub Actions to automate testing on code pushes.

## Submission Instructions:
- Push Your Code to the Repository:

  - Include test_unit.py, test_functional.py, test_security.py, and performance_test.py in your repository.
  - Ensure all tests are passing locally before pushing.
- Set Up the GitHub Workflow:

  - Configure your GitHub Actions workflow to run your tests on every push.
  - Verify that the tests pass in the GitHub Actions pipeline.
- Submit Your Repository Link:

  - Submit the link to your repository in the Learning Hub.

## Lab Tasks
### 1. Functional Testing

#### 1.1 Unit Testing:
- Write tests for each function in isolation, using mocks where applicable.
- Example: Mock datetime.now() in the login function to test last_login without relying on the current time.
- Example: Mock the email function smtplib.SMTP in send_reset_email to simulate email sending without an actual email server.

#### 1.2 Feature Testing: 
- Combine signup, login, view_profile, update_profile, and send_reset_email functions to test the full login and profile management flow.

- Test Scenarios:
  - Scenario 1: A new user signs up and immediately logs in.
  - Scenario 2: An existing user updates their profile and then requests a password reset.
  - Scenario 3: A user views their profile after multiple updates to verify all changes are saved.
- Data Consistency Checks: Verify that changes are correctly reflected in user_db and user_profiles after each operation.

### 2. Performance and Load Testing

- Simulate concurrent users to measure response times for login and signup.
- Steps:
  - Use multithreading or asynchronous programming to simulate multiple users interacting with the system simultaneously.
  - Record the start and end times for each login attempt to calculate individual response times.
  - Analyze the average, minimum, and maximum response times.
- Example:
  - Simulate 100 concurrent login attempts using threading.
  - Vary the processing delay in login to simulate different load conditions.

### 3. Security Testing

- SQL Injection Simulation: While this code does not use SQL, input sanitization is still critical. Test the system for vulnerabilities by inputting SQL-like data (e.g., username="john_doe'; DROP TABLE users; --").
- Weak Password Policy: Test is_valid_password to verify it enforces a strong password policy.
Examples: Try weak passwords such as "12345" and "password" to observe the outcome.

### 4. Continuous Integration with GitHub Actions

- Set up GitHub Actions to run unit tests automatically on every push to your repository.
- Steps:
  - Create a .github/workflows directory in your repository.
  - Add a YAML file defining the CI pipeline to run your tests.
  - Ensure that the pipeline runs successfully and reports the test results.
