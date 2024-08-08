def calculate_total_marks(semantic_similarity, keyword_similarity, word_count_student, word_count_key, total_marks):
    # Define the maximum score for each criterion
    max_score = 10
    
    # Calculate normalized scores
    normalized_semantic_similarity = (semantic_similarity / max_score) * max_score
    normalized_keyword_similarity = (keyword_similarity / max_score) * max_score
    
    # Calculate word count score (adjustment based on percentage of key answer)
    word_count_percentage = min(word_count_student / word_count_key, 1)  # Cap at 1 to avoid penalty for longer answers
    word_count_score = (word_count_percentage * max_score)
    
    # Calculate total weighted score
    total_score = normalized_semantic_similarity + normalized_keyword_similarity + word_count_score
    
    # Normalize total score to out of total_marks
    normalized_total_score = (total_score / (max_score * 3)) * total_marks
    
    return round(normalized_total_score)

def calculate_keyword_similarity(student_keywords, key_keywords):
    # Convert keyword lists to sets for easier comparison
    student_set = set(student_keywords)
    key_set = set(key_keywords)
    
    # Calculate the number of common keywords
    common_keywords_count = len(student_set.intersection(key_set))
    
    # Calculate the similarity score as a percentage
    similarity_score = (common_keywords_count / len(key_set)) * 100
    
    return similarity_score

# Example usage:
# semantic_similarity_score = 5
# keyword_similarity_score = 4
# word_count_student = 60
# word_count_key = 100
# total_marks = 50

# total_marks_result = calculate_total_marks(semantic_similarity_score, keyword_similarity_score, word_count_student, word_count_key, total_marks)
# print("Total marks:", total_marks_result)
