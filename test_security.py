from model_security import *

model_names = ['lmsys/vicuna-7b-v1.5', 'meta-llama/Llama-2-7b']
dataset_names = ['./datasets/combined.csv','./datasets/combined_1.csv', './datasets/combined_2.csv', './datasets/combined_3.csv', './datasets/combined_4.csv' ,'./datasets/combined_5.csv','./datasets/test.csv']
devices = ['gpu','cpu']

def get_user_choice(prompt_text, options):
    """
    Prompts the user to select an option from a list of choices.

    Args:
        prompt_text (str): The prompt text to display.
        options (list): A list of valid options to choose from.

    Returns:
        str: The user's selected option.
    """
    print(prompt_text)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():


    # Prompt the user to select a model, dataset, and device
    model_name = get_user_choice("Please choose a model:", model_names)
    dataset_name = get_user_choice("Please choose a dataset:", dataset_names)
    device = get_user_choice("Please choose a device (gpu/cpu):", devices)

    # Ask for max_length and debug flag
    max_length = int(input("Enter the maximum length for generation (e.g., 50): "))
    debug_input = input("Enable debug mode? (yes/no): ").strip().lower()
    debug = debug_input == 'yes'
    user_input = input ("Now provide a test input: ")

    # Print the selected options for confirmation
    print(f"\nYou have selected:\nModel: {model_name}\nDataset: {dataset_name}\nDevice: {device}\nMax Length: {max_length}\nDebug Mode: {debug}")

    print(isolate_user_requests(model_name,device,user_input,max_length,debug,2,1))
