
# text to questions and answers
class TextStruct:
    def __init__(self, text):
        self.text = text
        self.questions = []
        self.answers = []

    def extract(self):
        lines = self.text.split('\n')

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
        return self.questions, self.answers

# # Example usage:
# text = """
# Q1. What is your name?
# A1. My name is John.

# Q2. Where are you from?
# A2. I am from New York.
# """
# data = [
#     "A1: Multiple inheritance is a way of passing on multiple copies of a particular class or inheritance to a child's class. This can be useful when you want to make sure that some code is always available to your child's class. One way is to create a subclass of the parent class and provide child with a copy of the parent class.",
#     "A2: A cache is a temporary storage location for frequently accessed data. Caches are useful for organizations that need to store large amounts of data in a short amount of time.",
#     "A3: Access modifiers are a way of specifying which users have access to a resource. Access modifiers are often used to control access to data, files, or other resources. For example, a database might allow only certain users to see the data. Or a file might be locked down so that only the owner can see it.",
#     "A. deadlock is a situation where two or more processes are waiting for each other's to finish. The process that is waiting will not finish until the other process finishes. This can be a problem if you need to wait for a long time, as this can lead to your system becoming unresponsive.",
#     "A5: A critical section is a section of code that is crucial to the operation of a program. By accessing critical sections, a program can make changes to the overall functionality of the program without affecting other sections of the code."
# ]

def answer_struct_fn(data):
    answers = []

# Iterate over each item in the list
    for item in data:
        parts = item.split(':')  # Split the item by ":"
        if len(parts) == 2:  # Ensure that there are two parts
            answer_number = parts[0].strip()  # Extract the answer number
            answer_text = parts[1].strip()  # Extract the answer text
            answers.append([answer_number, answer_text])  # Append to the answers list
    return answers
# Print the extracted answers
# d= answer_struct_fn(data=data)
# for answer in d:
#     print(answer[0])
#     print(answer[1])

# extractor = TextStruct(text)
# questions, answers = extractor.extract()
# print("Questions:", questions)
# print("Answers:", answers)


