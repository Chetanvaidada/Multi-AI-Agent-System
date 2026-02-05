from dotenv import load_dotenv
load_dotenv()
from graph import app

if __name__ == "__main__":
    user_input = input("Enter your task: ")

    result = app.invoke({"input": user_input})

    print("\nFinal Answer:\n")
    print(result["final_output"])