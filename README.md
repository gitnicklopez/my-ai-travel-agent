## my-ai-travel-agent
# Restaurant & Hospitality AI Agent

# Overview
This AWS-powered AI agent leverages Bedrock, Lambda, and API Gateway to process user queries related to restaurants, hotels, and Airbnb accommodations. It dynamically retrieves and filters data from an Amazon S3 bucket, delivering real-time responses tailored to user preferences.

# How It Works
1. User Input Processing
-   The agent receives queries via API Gateway (e.g., “Find restaurants in New York” or “List pet-friendly Airbnbs”).
-   User parameters such as location, fine dining preference, or hotel amenities are extracted.
2. Data Retrieval & Filtering
-   The agent pulls relevant CSV data from Amazon S3 using boto3.
-   Pandas processes and cleans the data, applying filters based on user-specified criteria.
3. Response Generation
-   The refined dataset is converted into structured JSON output.
-   The AI agent formats the response, ensuring clarity for API integrations.
4. Conversational AI Interaction
-   When invoked via the Bedrock AI Runtime, the agent responds intelligently using predefined AI models.
-   Dynamic text responses enhance usability for chatbots and voice assistants.

# Key Features
✔ Automated Restaurant & Hotel Search – Retrieves and filters dining & accommodation options.
✔ Customizable Preferences – Supports queries based on fine dining, pet policies, pools, and saunas.
✔ Scalable Serverless Architecture – Optimized with AWS Lambda for efficient processing.
✔ Real-Time JSON Responses – Delivers structured, actionable insights for customer interactions.
✔ Robust Error Handling – Implements logging and exception management to ensure reliability.

# Use Cases
- Restaurant Recommendation Bots
- Hotel & Airbnb Booking Assistants
- Travel Planning Automation
- AI-Powered Customer Support
