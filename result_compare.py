import Levenshtein

def calculate_accuracy(original_text, ocr_text):
   distance = Levenshtein.distance(original_text, ocr_text)
   max_len = max(len(original_text), len(ocr_text))
   accuracy = (1 - distance / max_len) * 100
   return accuracy
