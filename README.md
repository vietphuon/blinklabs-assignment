# blinklabs-assignment
## AI Coding Tutor

AI Coding Tutor is a fullstack application that helps users learn JavaScript by generating code snippets and explanations based on user prompts. The application uses an AI model to create JavaScript functions and provide brief explanations, making it an interactive learning tool for coding enthusiasts.

## Features

- Interactive UI for submitting coding questions
- AI-powered code generation for JavaScript functions
- Brief explanations of generated code
- Responsive design using Chakra UI
- Error handling and loading states
- Separate backend and frontend architecture

## Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- OpenAI GPT-3.5

### Frontend
- Next.js 14
- TypeScript
- Chakra UI
- Axios

## Project Main Structure
ai-coding-tutor/
├── backend/
│   ├── main.py
│   ├── ai_helper.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── services/
│   ├── package.json
│   └── tsconfig.json
└── README.md

## Setup and Installation

### Backend

1. Navigate to the `backend` directory:
cd backend

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Set up your OpenAI API key:
export OPENAI_API_KEY=your_api_key_here

5. Run the backend server:
uvicorn app:app --reload

### Frontend

1. Navigate to the `frontend` directory:
cd frontend

2. Install dependencies:
npm install

3. Run the development server:
npm run dev

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Enter a coding question or prompt in the input field
3. Click "Generate Code" or press Enter
4. View the generated JavaScript function and its explanation

## API Endpoints

- `POST /generate_code`: Generates code based on the provided prompt
- Request body: `{ "prompt": "your coding question here" }`
- Response: `{ "code": "generated JavaScript code", "explanation": "brief explanation" }`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- OpenAI for providing the GPT-3.5 model
- LangChain for simplifying AI interactions
- Chakra UI for the responsive design components
- Next.js team for the amazing React framework
This README provides a comprehensive overview of your project, including its features, tech stack, setup instructions, usage guide, and other relevant information. You can customize it further based on your specific project details or any additional information you'd like to include.
To use this README, simply create a new file named README.md in the root directory of your GitHub repository and paste this content into it. Make sure to replace any placeholder information (like "your_api_key_here") with your actual project details.
