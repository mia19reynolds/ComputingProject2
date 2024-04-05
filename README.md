# Recipe Finder Web Application

This is a web application built with Flask, a Python web framework, which allows users to search for recipes based on various criteria such as cuisine, dish type, dietary preferences, and ingredients. The application also provides features for user authentication, allowing registered users to save their favorite recipes and customize their dietary preferences.

## Features

- **Recipe Search**: Users can search for recipes using keywords, cuisine types, dish types, and dietary preferences.
- **Recipe Details**: Detailed information about each recipe, including ingredients, instructions, and nutritional facts, is displayed.
- **User Authentication**: Users can sign up, log in, and log out of the application. Authenticated users can save recipes to their account and customize their dietary preferences.
- **User Dashboard**: Authenticated users have access to a personalized dashboard where they can view their saved recipes and update their account settings.
- **Intolerances and Diets**: Users can specify dietary intolerances and preferences such as gluten-free, vegetarian, or dairy-free, which are taken into account when searching for recipes.
- **Password Management**: Users can reset their passwords securely through the application.

## Installation

1. Clone the repository:

```bash
    git clone https://github.com/your_username/recipe-finder-app.git
```

2. Install dependencies:

```bash
    pip install -r requirements.txt
```

3. Configure MySQL database:

- Update the database configuration in `app.py` with your MySQL host, username, password, and database name.

4. Run the application:

```bash
    python app.py
```

5. Access the application in your web browser locally:

    <http://localhost:5000>

Alternatively it can be depoyed on AWS EC2

## Hosting on AWS EC2

This application can be deployed and hosted on Amazon Web Services (AWS) EC2 instances. Follow the steps below to deploy your Flask application on AWS EC2:

1. **Create EC2 Instance**: Launch an EC2 instance using the AWS Management Console. Choose an appropriate instance type, configure security groups, and optionally assign an Elastic IP address for a static public IP.

2. **Set Up MySQL Database**: If your application uses a MySQL database, you can install and configure MySQL on the EC2 instance itself or consider using Amazon RDS for managed MySQL database hosting.

3. **Configure Security Groups**: Ensure that your EC2 instance's security group allows inbound traffic on the necessary ports (e.g., port 80 for HTTP, port 443 for HTTPS) and restricts access to only trusted IP addresses.

4. **Deploy Application Code**: Transfer your Flask application code to the EC2 instance using secure file transfer methods like SCP or SFTP. Alternatively, you can set up a version control system like Git and clone your repository directly onto the instance.

5. **Install Dependencies**: Install the required Python dependencies for your Flask application using pip. You may also need to install additional software or packages depending on your application's requirements.

6. **Configure Environment**: Update the configuration settings in your Flask application (e.g., database connection details, API keys) to reflect the environment variables and resources available on the EC2 instance.

7. **Start Application**: Run your Flask application on the EC2 instance using a command like `python app.py`. You may choose to run the application as a background process or set it up to automatically start on system boot.

8. **Set Up HTTPS (Optional)**: Configure SSL/TLS certificates for your domain using AWS Certificate Manager (ACM) or third-party certificate providers to enable secure HTTPS communication between clients and your application.

9. **Monitor and Maintain**: Regularly monitor the health and performance of your EC2 instance using AWS CloudWatch. Perform routine maintenance tasks such as security updates, backups, and performance optimization to ensure smooth operation.

By following these steps, you can deploy and host your Flask application on AWS EC2, taking advantage of AWS's scalability, reliability, and flexibility for web hosting.

## Usage

1. **Home Page**: Users are greeted with the home page where they find out more about the application or log in/sign up for an account.
2. **Search for Recipes**: Users can search for recipes using keywords, cuisine types and dish types on the search page.
3. **View Recipe Details**: Clicking on a recipe from the search results displays detailed information about the selected recipe.
4. **User Authentication**: Users can sign up for a new account or log in with their existing credentials.
5. **User Dashboard**: Authenticated users have access to a personalized dashboard where they can view their saved recipes and update their account settings, including dietary preferences and intolerances.
6. **Save Recipes**: Authenticated users can save their favorite recipes to their account for future reference.

## Contributors

- [Your Name](https://github.com/your_username)
- [Contributor 1](https://github.com/contributor1)
- [Contributor 2](https://github.com/contributor2)