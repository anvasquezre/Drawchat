# Chatbot Dashboard

Welcome to the Chatbot Dashboard! This Streamlit dashboard provides an analytics view of chatbot interactions, chatlogs, and user feedback. You can analyze data for different date ranges and resampling frequencies. Here's how to use it:

## Getting Started

To run this Streamlit dashboard locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Create a `.env` file in the root directory of the project and add the following environment variables:

   ```dotenv
   API_TOKEN=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.zlukokly5KU_vILNKLxTaCU_itZvA640KXafFZPa3lG3DAgVkgqGM47w6O9Lu-h9A3VosPfTXsvf-fjrdOAO4w
   API_URI=http://172.17.0.1:3000/api/v1
   ```

3. Install the required dependencies. You can create a virtual environment and use `pip` to install the dependencies listed in `requirements.txt`:
   ```bash
   cd <repository_directory>
   python -m venv venv  # Create a virtual environment (optional but recommended)
   source venv/bin/activate  # Activate the virtual environment
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

Once you have the Streamlit app running, you can interact with the Chatbot Dashboard:

### Main Menu

- **Dashboard**: View analytics data for chatbot interactions.
- **Chatlogs**: Explore chatlogs for specific date ranges.
- **Feedback**: Analyze user feedback.

### Dashboard

On the Dashboard page, you can:

- Select a date range using either a calendar or predefined time periods.
- Choose a resampling frequency for data visualization.
- Explore analytics graphs and charts.

### Chatlogs

On the Chatlogs page, you can:

- Select a date range using either a calendar or predefined time periods.
- View chatlogs for the selected date range.

### Feedback

On the Feedback page, you can:

- Select a date range using either a calendar or predefined time periods.
- Analyze user feedback data.

## Docker Deployment

This Streamlit dashboard can be deployed using Docker. A Dockerfile is provided to simplify deployment. To deploy the app with Docker, follow these steps:

1. Build the Docker image:

   ```bash
   docker build -t chatbot-dashboard .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 8501:8501 --env-file .env chatbot-dashboard
   ```

The dashboard will be accessible at [http://localhost:8501](http://localhost:8501) in your web browser.

## Project Structure

```
.
├── Dockerfile
├── Documentation.pdf
├── __init__.py
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── resources
│   └── logo.png
├── src
│   ├── Chatlog.py
│   ├── components.py
│   ├── __init__.py
│   ├── plots.py
│   ├── settings.py
│   └── utils.py
├── style.css
├── tree.txt
└── views
    ├── chatlog.py
    ├── feedback.py
    ├── graphs.py
    ├── home.py
    ├── __init__.py
```


## Credits

This Chatbot Dashboard was developed and is maintained by Tenant Evaluation.

![Tenant Evaluation Logo](resources/logo.png)

---

Feel free to explore the different pages of the dashboard and analyze the chatbot's performance and user feedback. If you have any questions or need assistance, please contact Tenant Evaluation.