
# CopyProducts

**Developer**: Abderrahim Chadli

CopyProducts is a Python-based application designed to facilitate the copying and management of product data. It provides functionalities for user authentication, product importation, and efficient handling of product information.

## Features

- **User Authentication**: Secure user registration and login system.
- **Product Importation**: Tools to import and manage product data.
- **Logging**: Comprehensive logging of application requests and errors.

## Project Structure

The repository is organized as follows:

- `auth_app/`: Contains modules related to user authentication.
- `importproduct/`: Manages product importation functionalities.
- `project/`: Core project configurations and settings.
- `static/`: Stores static files like images, CSS, and JavaScript.
- `Copyproductsenv/`: Virtual environment directory for dependencies.
- `manage.py`: Django's command-line utility for administrative tasks.
- `requirements.txt`: Lists the Python dependencies for the project.
- `APPNAME.log` and `debug.log`: Log files for application debugging and request logging.

## Installation

To set up the project locally:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/abderrahimchadli/copyproducts.git
   cd copyproducts
   ```

2. **Set up a virtual environment**:

   ```bash
   python3 -m venv Copyproductsenv
   source Copyproductsenv/bin/activate  # On Windows, use `Copyproductsenv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## Usage

- **User Registration**: Navigate to the registration page to create a new account.
- **Product Importation**: Use the provided tools to import product data into the system.
- **Logging**: Monitor `APPNAME.log` and `debug.log` for application activity and debugging information.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

Abderrahim Chadli
