import openai
import time
import logging
import argparse

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# To prevent triggering a rate limit
SLEEP_TIME = 0.5
RETRY_COUNT = 3

def main():
    parser = argparse.ArgumentParser(description='Have GPT problem solve using many attempts while reading through a text file for inspiration')
    parser.add_argument('inspiration_file', type=str)
    parser.add_argument('question', type=str)
    parser.add_argument('--safe_mode_off', action=argparse.BooleanOptionalAction)
    parser.add_argument('--snippet_len', default=1000, type=int)
    parser.add_argument('--max_iter', default=100, type=int)
    
    args = parser.parse_args()
    
    input_file_path = args.inspiration_file
    Q = args.question
    safe_mode = not args.safe_mode_off
    snippet_len = args.snippet_len
    max_iter = args.max_iter

    with open(input_file_path, 'r') as input_file:
        content = input_file.read()

    current_best = ''
    i = 0

    while (i+1)*snippet_len < len(content):   
        logging.info(f"Currently at iter={i} out of {min(len(content)//snippet_len+1,max_iter)}")
        if i >= max_iter:
            print(f"Done max_iter iterations, best answer found:\n{current_best}")
            return
        snippet = content[i*snippet_len:min(len(content),(i+1)*snippet_len)]
        logging.debug(f"Snippet: {snippet}")
        if safe_mode:
            input("Press Enter to continue...")
        candidate = generate_answer(Q, snippet)
        logging.debug(f"Generated candidate answer: {candidate}")
        current_best = compare_answers(Q, current_best, candidate)
        i += 1

    print(f"Got to end of inspiration file, best answer found:\n{current_best}")


def generate_answer(Q, snippet):
    query = f"Snippet:\n{snippet}\nAnswer the following question, step by step:\nQuestion: {Q}"
    return get_assistant_response(query)

def compare_answers(Q,A,B):
    '''Checks which of two answers better answer the question Q, and returns the better answer'''
    if A == '':
        logging.info(f"Initial answer: {B}")
        return B

    query = f"""< Snippet Redacted >\nQuestion:\n{Q}\nA:\n{A}\nB:\n{B}\nWhich answer is better? Decide first based on correctness. If they are both correct, decide by explanation quality. If both are explained well, choose the more concise answer. First discuss the merits of both answers, in terms of these qualities. Finish your response with a single char, the letter A or the letter B.
Meaning, respond in the format:
Merits discussion: <Discussion on correctness, explanation quality, and conciseness>
Chosen Answer: A/B
    """
    response = get_assistant_response(query)
    logging.info(f"query: {query}")
    logging.info(f"compare_answers response: {response}")
    org_response = response
    response = response[-2:]
    if (not ("A" in response)) and (not ("B" in response)):
        logging.info(f"Model did not respond in correct format (response=\"{org_response}\"), likely both answers are equally correct. Defaulting to keep current best answer.")
        return A
    if "B" in response:
        logging.info(f"Found new best answer: {B}")
        return B

    logging.info("Keeping current best answer")
    return A

def get_assistant_response(query):
    for i in range(RETRY_COUNT):
        try:
            time.sleep(SLEEP_TIME)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Reply concisely."},
                    {"role": "user", "content": query},
                    ]
                )
            return parse_chat_response(response)
        except:
            continue
    raise Exception("OpenAI API not responding correctly")

def parse_chat_response(response):
    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    main()
