import os

PATH = "C:\\Users\\Anita Agyepong\\Documents\\Daquiver's Quivers\\Python\\past_questions_bot\\past_questions"

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    
    return max(paths, key=os.path.getctime)

newest(PATH)
print(newest(PATH))