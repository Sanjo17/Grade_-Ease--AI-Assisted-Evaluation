

# GradeEase

## Overview

GradeEase is a web-based application developed as a final year project designed to automate the evaluation of students' answers and assign grades. The system assesses both online tests and handwritten answer sheets using semantic similarity, keywords, and word count. It employs a pre-trained BERT model for semantic similarity calculations and utilizes the Gemini API to extract text from handwritten papers.

## Features

- **Automated Grading:** Evaluates answers based on semantic similarity with the pre-trained BERT model.
- **Versatile Input:** Supports online tests and handwritten answer sheets.
- **Text Extraction:** Uses Gemini API for converting handwritten answers into text.
- **Front-End:** Built with HTML, CSS, and JavaScript.
- **Back-End:** Powered by Django Framework.
- **Manual Adjustment:** Teachers can manually edit grades if needed.
- **Productivity Enhancement:** Speeds up the grading process and increases efficiency.

## Technical Details

- **Semantic Similarity:** Uses BERT model for accurate grading.
- **Text Retrieval:** Gemini API for text extraction from handwritten papers.
- **Web Technologies:** HTML, CSS, JavaScript for front-end; Django for back-end.
- **Machine Learning & NLP:** Incorporates machine learning models and Natural Language Processing.

## Learning Outcomes

- Gained experience with the Django Framework and web development.
- Deepened understanding of machine learning models and NLP.
- Explored generative AI and integrated ML models from Hugging Face.
- Learned to combine machine learning with Django for practical applications.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Install Dependencies:**
   ```bash
   cd gradeease
   pip install -r requirements.txt
   ```

3. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the Application:**
   Open `http://127.0.0.1:8000/` in your web browser.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [your-email@example.com](mailto:your-email@example.com).

---

Replace `<repository-url>` with the actual URL of your repository and `[your-email@example.com]` with your email address. This README provides an overview, features, technical details, and setup instructions for your project.
