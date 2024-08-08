
import re

# txt to text
class TextExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.questions = []
        self.answers = []

    def extract(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        q = False
        a = False
        current_answer_lines = []
        current_question_lines = []
        for line in lines:
            line = line.strip() 
            if line.startswith('Q'):
                q = True
                a = False
                if current_answer_lines:
                    self.answers.append(' '.join(current_answer_lines))
                    current_answer_lines = []
                current_question_lines.append(line[3:])
            elif line.startswith('A'):
                a = True
                q = False
                if current_question_lines:
                    self.questions.append(' '.join(current_question_lines))
                    current_question_lines = []
                current_answer_lines.append(line[3:])
            elif q:
                current_question_lines.append(line)
            elif a:
                current_answer_lines.append(line)

        if current_question_lines:
            self.questions.append(' '.join(current_question_lines))
        if current_answer_lines:
            self.answers.append(' '.join(current_answer_lines))
        return self.questions,self.answers



# file_path = 'media/answer_keys/text.txt'  # Replace with your file path
# qa_extractor = TextExtractor(file_path)
# qa_extractor.extract()

# # Access questions and answers
# print("Questions:")
# for question in qa_extractor.questions:
#     print(question)

# print("\nAnswers:")
# for answer in qa_extractor.answers:
#     print(answer)



# Print or use the extracted questions and answers
# print("Questions:")
# for question in questions:
#     print(f"{question}")

# print("\nAnswers:")
# for answer in answers:
#     print(f" {answer}")

# print(answers[7])



def extract_answers_key(file_path):
    try:
        # Read the answer key from the text file
        with open(file_path, 'r') as file:
            answer_key = file.readlines()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return {}

    # Initialize a dictionary to store the answers
    answers_dict = {}

    # Process each line in the answer key
    current_question = None
    current_answer = None
    current_marks = None
    for line in answer_key:
        line = line.strip()
        if line.startswith('Q'):
            # Extract question number
            current_question = line.split(':')[0].strip()[1:]
        elif line.startswith('A'):
            print('thatfkingline: ',line)
            # Extract answer
            current_answer = line.split(':')[1].split('[')[0].strip()
            # Extract marks
            
            current_marks = int(line.split('[')[-1].split('=')[-1].split(']')[0].strip())
            # Store the answer and marks in the dictionary
            answers_dict[current_question] = [current_answer, current_marks]
            # Reset variables for the next question
            current_question = None
            current_answer = None
            current_marks = None

    return answers_dict
# Example usage:
# file_path = 'papergrading/utils/keytest.txt'
# answers = extract_answers(file_path)
# print(answers)
