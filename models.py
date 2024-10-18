import torch
print(torch.cuda.is_available())  # Should return True if CUDA is available



# from transformers import pipeline

# # Set device to GPU (T4 in your case, which will be device 0)
# torch.cuda.empty_cache()


# pipe = pipeline("question_answering", model="lmsys/vicuna-7b-v1.5", device = 0)
# # Test the generator
# output = generator("what is love", max_length=50, context= "be helpful")
# print(output)


from transformers import AutoTokenizer, AutoModelForCausalLM, RobertaModel, RobertaTokenizer
from sentence_transformers import SentenceTransformer
import torch


def ask_model(model_name, device, question, system_prompt, max_length=50, debug=False) -> str:
    """
    Queries the model with a given question and system prompt.

    Args:
        model_name (str): The name or path of the model to load.
        device (int): The device to use (e.g., 0 for GPU, -1 for CPU).
        question (str): The question to ask the model.
        system_prompt (str): The system prompt to guide the model's response.
        max_length (int): The maximum length of the generated response.
        debug (bool): If True, print the generated output.

    Returns:
        str: The generated response from the model.
    """
    # Clear GPU cache if using GPU
    if device == 'gpu':
        torch.cuda.empty_cache()

    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Move model to specified device (GPU or CPU)
    if device == 'gpu':
            # Use DataParallel to utilize all available GPUs
        if torch.cuda.device_count() > 1:
            print(f"Using {torch.cuda.device_count()} GPUs")
            model = torch.nn.DataParallel(model)

        # Move the model to GPU (will automatically use all GPUs)
        model.to('cuda')
    else:
        model.to('cpu')

    # Combine system prompt and question
    full_prompt = system_prompt + "\n\n" + "User: " + question + "\nYour response:"

    # Tokenize the input text
    inputs = tokenizer(full_prompt, return_tensors="pt").to(f'cuda' if device == 'gpu' else 'cpu')

    # Generate the output
    outputs = model.generate(inputs['input_ids'], max_length=max_length)

    # Decode the generated output
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    result = result.split("Your response: ")[1]

    # Print output if debug is True
    if debug:
        print(result)

    return result



def judge_output(model_output, sample_refuse, threshold):

    '''
    return true if the model rejects the user request
    '''


    # Load pre-trained SBERT model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')

    # Convert sentences to embeddings
    sentences = [model_output, sample_refuse]
    embeddings = model.encode(sentences)

    # Cosine similarity can be calculated between these embeddings
    similarities = model.similarity(embeddings, embeddings)

    return similarities >= threshold