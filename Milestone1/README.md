
# User Authentication System Using Streamlit and JWT

## Infosys Springboard Internship 7.0 – Batch 4 | Milestone 1

## 1. Project Overview

The application provides essential authentication and account management features, including user registration, login, password recovery, email-based OTP verification, session management, and an administrative dashboard.

The application is developed using Python and Streamlit, with JSON Web Tokens (JWT) for session management and Gmail SMTP for sending OTP verification emails. Google Colab is used as the execution environment, while ngrok provides a public URL to access the application.

## 2. Project Objectives

The main objectives of this project are:

- To develop a functional user authentication system.
- To implement user registration with input validation.
- To authenticate users through a login interface.
- To manage authenticated sessions using JWT.
- To provide a password recovery mechanism.
- To implement email-based OTP verification.
- To create user and administrator dashboards.
- To provide logout functionality.
- To demonstrate the integration of Python, Streamlit, email services, and authentication technologies.

## 3. Features

### 3.1 User Signup

The signup module allows new users to create an account.

Features include:
- User registration through a form.
- Input validation for required fields.
- Email address validation.
- Password validation.
- Collection of security-question information, if configured.
- Storage of registered user information for subsequent authentication.

### 3.2 User Login

The login module authenticates registered users.

Features include:
- Email or username-based login, depending on the implementation.
- Password verification.
- Validation of user credentials.
- JWT-based session management.
- Access to the user dashboard after successful authentication.
- Appropriate error messages for invalid credentials.

### 3.3 Forgot Password

The forgot-password module helps users recover access to their accounts.

Depending on the configured recovery method, users can recover their accounts through:

- Security-question verification.
- Email-based OTP verification.

The recovery process is designed to verify the user's identity before allowing a password reset.

### 3.4 Email OTP Verification

The application integrates Gmail SMTP to send one-time passwords (OTPs) to registered email addresses.

Features include:
- OTP generation.
- Delivery of OTPs through email.
- User input for OTP verification.
- Verification before proceeding with the recovery process.

*Note: OTP expiry, retry limits, and rate limiting should be implemented and tested if they are required for production-level security.*

### 3.5 User Dashboard

After successful login, users can access their dashboard.

The dashboard may include:
- A personalized welcome message.
- Confirmation of successful authentication.
- Access to available user features.
- A logout option.

### 3.6 Admin Dashboard

The administrator dashboard provides access to registered-user information.

Features include:
- Viewing registered users.
- Displaying relevant user details.
- Separating administrative access from regular user access.

Administrative credentials should be stored securely and must not be exposed in the source code or public repository.

### 3.7 Logout Functionality

The logout feature allows authenticated users to end their sessions.

It should:
- Clear the application's authentication state.
- Remove or invalidate the active session token where applicable.
- Return the user to the login interface.
- Prevent access to protected pages without authentication.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application programming language |
| Streamlit | User interface and web application framework |
| JSON Web Tokens (JWT) | Authentication and session management |
| Gmail SMTP | Sending OTP verification emails |
| Google Colab | Development and execution environment |
| pyngrok | Integration with the ngrok tunnelling service |
| ngrok | Public access to the locally running Streamlit application |
| Environment Variables | Passing configuration and sensitive credentials to the application |
| Google Colab Secrets | Managing sensitive configuration values |

## 5. System Architecture

The application follows a client-server authentication workflow.

```text
                 User
                  |
                  v
          Streamlit Interface
                  |
          +-------+-------+
          |               |
          v               v
      Signup/Login    Forgot Password
          |               |
          v               v
    Input Validation   Identity Verification
          |               |
          v               v
   Credential Check    Email OTP / Security
          |               Question
          v
     JWT Generation
          |
          v
     User Dashboard
          |
          v
        Logout

     Admin Authentication
             |
             v
      Admin Dashboard
             |
             v
     Registered Users
```

Gmail SMTP is used for email-based OTP delivery. The application is executed in Google Colab, and ngrok exposes the Streamlit server through a public URL.

## 6. Application Workflow

### Step 1: User Registration

1. The user opens the application.
2. The user navigates to the signup page.
3. The user enters the required registration details.
4. The application validates the submitted information.
5. Valid registration details are stored using the application's configured storage mechanism.

### Step 2: User Login

1. The registered user opens the login page.
2. The user enters their login credentials.
3. The application validates the credentials.
4. Upon successful authentication, the application creates or establishes the authenticated session.
5. The user is redirected to the dashboard.

### Step 3: Password Recovery

1. The user selects the Forgot Password option.
2. The application requests the information required to identify the account.
3. The user completes the configured recovery method.
4. For email OTP recovery, the application sends an OTP to the registered email address.
5. The user enters the received OTP.
6. After successful verification, the application permits the password-reset process.

### Step 4: Dashboard Access

1. The authenticated user accesses the dashboard.
2. The application checks the authentication state.
3. Protected functionality is made available to the authenticated user.
4. The user can log out when finished.

### Step 5: Administrator Access

1. The administrator enters the configured administrator credentials.
2. The application verifies the credentials.
3. Authorized administrators can access the admin dashboard.
4. The administrator can view registered-user information.

## 7. Project Setup and Execution

### Prerequisites

Ensure that you have:

- A Google account with access to Google Colab.
- A valid ngrok account and authentication token.
- A Gmail account configured for SMTP access.
- The project authentication notebook.
- Python dependencies required by the application.

### Step 1: Open Google Colab

Open the authentication notebook in Google Colab.

Upload the project files or ensure that `app.py` is available in the current working directory.

### Step 2: Install Dependencies

If the required packages are not already installed, execute:

```python
!pip install streamlit pyngrok PyJWT
```

Install any additional dependencies imported by your application.

### Step 3: Configure Colab Secrets

Open the **Secrets** panel in Google Colab and configure the variables used by the application.

| Secret Name | Purpose |
|---|---|
| `NGROK_AUTHTOKEN` | Authentication token for ngrok |
| `JWT_SECRET` | Secret key used to sign JWTs |
| `EMAIL_ADDRESS` | Gmail account used for sending emails |
| `EMAIL_PASSWORD` | Gmail App Password used for SMTP authentication |
| `ADMIN_USERNAME` | Configured administrator username |
| `ADMIN_PASSWORD` | Configured administrator password |

Enable notebook access to the required secrets.

**Important:** Do not publish real credentials, JWT signing keys, Gmail App Passwords, or administrator passwords in the README, screenshots, or public GitHub repository.

For Gmail SMTP, use an App Password where supported and required, rather than your regular Google account password.

### Step 4: Run the Notebook

Execute the notebook cells in the correct order:

1. Install the required dependencies.
2. Import the necessary libraries.
3. Load the configured secrets.
4. Initialize the application environment.
5. Start the Streamlit server.
6. Establish the ngrok tunnel.
7. Open the generated public URL.

### Step 5: Access the Application

Once Streamlit and ngrok start successfully, the notebook displays a public URL.

Open the URL in your browser to access the authentication application.

Keep the Google Colab runtime active while using the application. The public URL may change after restarting the tunnel or runtime.

## 8. Screenshots

Add screenshots of the actual running application to document the main features.

Create a folder named `screenshots` in the project repository and save the screenshots using the suggested filenames below.

### 8.1 Login Page

**File:** `screenshots/login.png`

The login page allows registered users to enter their credentials and access their accounts.

Include a screenshot showing:
- Login form fields.
- Login button.
- Signup navigation option.
- Forgot Password option.

![Login Page](screenshots/login.png)

### 8.2 Signup Page

**File:** `screenshots/signup.png`

The signup page allows new users to register with the application.

Include a screenshot showing:
- Registration form fields.
- Email and password fields.
- Input validation messages, if available.
- Signup or registration button.

![Signup Page](screenshots/signup.png)

### 8.3 Forgot Password Page

**File:** `screenshots/forgot_password.png`

The forgot-password page provides the interface for account recovery.

Include a screenshot showing:
- The password recovery option.
- Account identification field.
- Security-question or email OTP recovery option, as implemented.

![Forgot Password Page](screenshots/forgot_password.png)

### 8.4 OTP Email

**File:** `screenshots/otp_email.png`

This screenshot demonstrates the email delivered through Gmail SMTP during OTP-based account recovery.

Include a screenshot showing:
- The OTP email subject.
- The application's sender or recognizable project identity.
- The OTP delivery message.

**Security note:** Use a demonstration OTP or redact the actual OTP, email address, and other sensitive information before publishing the screenshot.

![OTP Email](screenshots/otp_email.png)

### 8.5 User Dashboard

**File:** `screenshots/user_dashboard.png`

The user dashboard demonstrates successful authentication.

Include a screenshot showing:
- The dashboard interface.
- The welcome message or authenticated-user details.
- The logout button.

![User Dashboard](screenshots/user_dashboard.png)

### 8.6 Admin Dashboard

**File:** `screenshots/admin_dashboard.png`

The administrator dashboard demonstrates authorized administrative access.

Include a screenshot showing:
- The admin dashboard.
- The registered-user listing.
- Relevant user information, with personal details redacted where necessary.

![Admin Dashboard](screenshots/admin_dashboard.png)

### Adding Screenshots to GitHub

Place the screenshot files inside the `screenshots` folder using the filenames specified above.

For example:

```text
screenshots/
├── login.png
├── signup.png
├── forgot_password.png
├── otp_email.png
├── user_dashboard.png
└── admin_dashboard.png
```

The README image references will display the screenshots automatically once the files are committed to the repository at those paths.

Replace the screenshot placeholders with actual application screenshots. Do not include screenshots of pages that have not been implemented.

## 9. Security Considerations

The following security practices are recommended:

- Store sensitive configuration values in Colab Secrets or an appropriate secret manager.
- Use a strong, randomly generated JWT signing key.
- Set an appropriate JWT expiration time.
- Validate user inputs on the server side.
- Store passwords using a suitable password-hashing algorithm, such as Argon2id or bcrypt, rather than plaintext.
- Use cryptographically secure OTP generation.
- Set OTP expiry and attempt limits.
- Avoid revealing whether an email address is registered through password-recovery error messages.
- Restrict admin functionality to authenticated and authorized administrators.
- Protect private user information in logs and screenshots.
- Avoid committing credentials, environment files, or tokens to version control.
- Use HTTPS for production deployment.
- Ensure logout and token-expiration checks are enforced by the application.

These are security recommendations; the actual level of protection depends on the implementation.

## 10. Testing

The following test cases can be used to evaluate the application.

| Test Case | Expected Result |
|---|---|
| Register with valid information | Account is registered successfully |
| Submit invalid registration data | Validation message is displayed |
| Log in with valid credentials | User dashboard opens |
| Log in with invalid credentials | Access is denied |
| Request password recovery | Recovery workflow begins |
| Submit a valid OTP | OTP verification succeeds |
| Submit an invalid OTP | Verification fails |
| Log out | Authenticated session is cleared |
| Access admin dashboard as an authorized administrator | Admin dashboard opens |
| Access admin functionality as an ordinary user | Access is denied |

Record the actual results after running each test. Do not mark a test as passed unless it has been verified.

## 11. Challenges and Learning Outcomes

This project provides practical experience in:

- Developing web interfaces using Streamlit.
- Implementing user authentication workflows.
- Understanding JWT-based session management.
- Integrating Gmail SMTP for email communication.
- Configuring application secrets and environment variables.
- Running Python applications in Google Colab.
- Exposing a development server through ngrok.
- Testing login, registration, and account-recovery functionality.
- Understanding basic web application security practices.

## 12. Limitations and Future Enhancements

Possible future improvements include:

- Database integration using SQLite, PostgreSQL, or MySQL.
- Improved password policies and secure password hashing.
- OTP expiration, retry limits, and rate limiting.
- Email verification during signup.
- Stronger administrator role management.
- Audit logging for security-related events.
- Automated authentication tests.
- Deployment to a persistent hosting platform.
- Enhanced user interface and mobile responsiveness.

These enhancements can improve reliability, maintainability, and suitability for real-world use.

