# Fast API Template

This template is an opinionated config of Fast API.  The intent is to give
developers an option to quickly stand up an api without having to worry about
all the different config options.

# Assumptions
- Postgres is the database. Though you can easily swap the connection string in the config
- Your api requires users and we use email & password with JWT & scopes to authenticate
- Sentry is installed for exception monitoring, though you can easily remove this
- Pytest is installed for testing
- Using Github Actions for Deployment
- Using Docker, AWS ECR, ECS, & EC2 for hosting

# Features
- Extracts out config options to `app.config`
- Generic CRUD APIs.  Define your models & schemas and you'll instantly have APIs for them
- Generic CRUD functions for interacting with the database
- Admins can access all data, but users can only access data they have created
- Background Script runner.  `manage.py` gives you the ability to schedule background tasks in ECS
- JWT Auth already setup & configured
- Base model ensures best practices for data modeling, enabling you to audit data