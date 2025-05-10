# Financial Assistant

A financial assistant that simulates Amazon Bedrock's multi-agent collaboration framework for portfolio creation and financial insights.


## 🛠️ Requirements

- Python 3.11+
- Streamlit
- Boto3 (for AWS integration)

### Installation

1. Clone the repository:-
    ```bash
git clone https://github.com/JaiInfowayPvtLtd/FinancialInsightEngine.git
cd FinancialInsightEngine
```

2. Create requirements.txt (If Not Present)

This project uses dependencies declared in pyproject.toml. If requirements.txt is missing, create it manually by copying the dependencies:

    📌 From pyproject.toml   
    ###  Like these dependencies can be there:---for example

        [project]
         dependencies = [
            "boto3>=1.38.12",
            "streamlit>=1.45.0",
                        ]


   📝 Create requirements.txt in the project root:
   ### all dependencies should be copied from pyproject.toml and paste in requirements.txt like below:----for example

            boto3>=1.38.12
            streamlit>=1.45.0

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:

  ```bash
   streamlit run app.py
  ```

  ## By running the above command, the application will launch in your web browser
 You can now view your Streamlit app in your browser.

  URL: http://0.0.0.0:5000
  access it via: http://localhost:5000

### AWS Integration (Optional)

For full functionality with AWS services, set the following environment variables:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
USE_SES=true
SENDER_EMAIL=your-verified-email@example.com
```

## Usage

1. Open the application in your browser at http://localhost:5000
2. Enter your email address in the sidebar (optional, for portfolio delivery)
3. Use the chat interface to:
   - Create investment portfolios (e.g., "Create a portfolio of 5 technology companies")
   - Get financial insights (e.g., "Tell me about inflation trends")
   - View FOMC report summaries (e.g., "What's in the latest FOMC report?")
4. Alternatively, use the quick action buttons at the bottom of the page



