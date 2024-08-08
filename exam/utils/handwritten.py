import os
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path

# google vision api for img text to raw text
class GeminiHandler:
    def __init__(self):
        load_dotenv()
        api_key = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.0-pro-vision-latest",
            generation_config=self.get_model_config(),
            safety_settings=self.get_safety_settings()
        )

    def get_model_config(self):
        return {
            "temperature": 0.2,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }

    def get_safety_settings(self):
        return [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]

    def image_format(self, image_path):
        img = Path(image_path)
        if not img.exists():
            raise FileNotFoundError(f"Could not find image: {img}")
        image_parts = [{"mime_type": "image/png", "data": img.read_bytes()}]
        return image_parts

    def gemini_output(self, image_path):
        system_prompt = """
                   You are a specialist in handwritten text extraction .
               Input images  will be provided to you,
               and your task is to respond to questions based on the content of the input image.
                   """
        # user_prompt = """Given an image containing a student's answer paper, extract the text and structure the questions and answers in a 
        #            clear and organized format. The image may contain various types of questions, such as short answer, 
        #            and essay questions. Account for the possibility of answers spanning multiple paragraphs.
        #            Output the extracted questions and their corresponding answers in a structured manner for further processing or analysis.
        #            only extract the text in the image dont make new text. """
        user_prompt= ''' extract the text from the image '''
        image_info = self.image_format(image_path)
        input_prompt = [system_prompt, image_info[0], user_prompt]
        response = self.model.generate_content(input_prompt)
        return response.text

# Example usage:


# image_path = "exam/utils/a4.png"

# gemini_handler = GeminiHandler()
# result = gemini_handler.gemini_output(image_path)
# print(result)
