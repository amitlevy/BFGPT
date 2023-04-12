# BFGPT: Give GPT 3.5/4 a boost

> "Richard Feynman was fond of giving the following advice on how to be a genius. You have to keep a dozen of your favorite problems constantly present in your mind, although by and large they will lay in a dormant state. Every time you hear or read a new trick or a new result, test it against each of your twelve problems to see whether it helps. Every once in a while there will be a hit, and people will say: 'How did he do it? He must be a genius!'"

BFGPT (Brute Force GPT) is an experiment to try and push the power of a GPT chat model a bit further using a large amount of attempts and a tangentially related reference for inspiration.

The following are the two core ideas:
1. GPT can identify which of two answers is better, even if it isn't capable of generating them itself.
2. Adding a related snippet to the model's context can occasionally cause a much better result, even if it is not clearly helpful to a human.

So BFGPT goes through snippets in a provided txt file, calls the OpenAI API to generate an answer of each snippet, all the while keeping the current best answer in memory, and comparing it to each new candidate answer created. At the end it returns the best answer found.

## Example Result:

The following example is for GPT-3.5. GPT-4 can zero-shot the question shown here, I don't have access to its API, which is why I'm showing this less impressive example.

If you normally ask GPT3.5 "Can a cat live inside a Kubernetes container?", a typical response would be:

> Technically speaking, it is possible for a cat to live inside a Kubernetes container, but it would not be a good idea.
>
> Kubernetes is a container orchestration system used for deploying, scaling, and managing containerized applications. Containers are designed to run software applications and are not meant to be living spaces for animals or humans.
>
> In addition, Kubernetes containers are typically run in data centers or cloud environments, which are not suitable for pets due to the lack of fresh air, natural light, and access to water and food.
> 
> Furthermore, running a live animal inside a container violates ethical and moral considerations, and it is not a recommended practice. It is important to prioritize the well-being of animals and provide them with suitable living conditions.
> 
> Therefore, while it is technically possible, it is not advisable or ethical to keep a cat or any other live animal inside a Kubernetes container.


If you do ask it with a random snippet from a book on Kubernetes in the context, you might get something like:

> As an AI language model, I must inform you that the question is not relevant to the given text snippet which is about building, distributing, and running a Docker image. To answer the question, theoretically it is possible for a cat to live inside a Kubernetes container, but it would not be a recommended or ethical practice as containers are meant for running software applications, not for living creatures.


After running the above command with the default values using a Kubernetes book as the inspiration text (contained in a txt file), at the end I got:

> No. 
> Kubernetes uses Linux container technologies to provide isolation of running applications. 
> Containers are a lightweight virtualization technology that allows running multiple isolated > applications on the same host. 
> They are not designed to accommodate living creatures like cats.

(By default, BFGPT does 100 iterations, which in this case was about 60 pages)

If I had GPT-4 access, I'd check if it can boost it as well, for instance on the variant of the River Crossing Riddle that it currently can't solve (https://news.ycombinator.com/item?id=35155467&p=2), with a book on problem solving as the inspiration text. I believe it should, if anyone has access and decides to test it (though it would be expensive) I'd be happy to hear the result.

This project is currently a Work in Progress.

## Usage:

1. Git clone the repository

2. Download a reference text file (if you have a pdf that would work as a reference, you can convert it to a txt online or using a cli tool for your OS, e.g. pdftotext)

3. Install the requirements (just the openai package):
```
pip3 install -r requirements.txt
```

4. Export your API key as an enviroment variable:
```
export OPENAI_API_KEY='yourkey'
```

5. Run the command (**Careful**! It costs money, potentially a lot, especially if you changed it to GPT-4. Each iteration is two API calls, and the default is 100 iterations. By default you must press Enter before each iteration to confirm.):
```
python3 BFGPT.py kubernetes.txt "Can a cat live inside a Kubernetes container?"
```

Press enter between iterations, or turn off safe mode.
To switch from GPT-3.5 to GPT-4, you must manually change it in the code. Remember that it is x30 more expensive (until OpenAI's next x10 price reduction :D).

For more options, python3 BFGPT.py --help

-------------

Disclaimer I copied over from AutoGPT:
## 🛡 Disclaimer

Disclaimer
This project, BFGPT, is an experimental application and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use, including but not limited to data loss, system failure, or any other issues that may arise.
