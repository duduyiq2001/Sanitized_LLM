    Securing Large language models against prompt injection

### Background and Context:

The security issues of today’s LLM systems are not the same as the security issues of other technologies we have faced before. Because instead of users interacting with the system through a predefined and rigid interface such as web applications and mobile devices, here users use a much more ambigious interface, which is natural language. One of the most harmful attacks is prompt injection, in which an attacker crafts specially designed input to manipulate an AI system into bypassing its built-in safeguards or restrictions, potentially causing it to perform unintended actions or reveal sensitive information. Jailbreaking is a type of prompt injection.

The consequences of allowing those vulnerabilities introduced by natural language goes beyond simply fulfilling unethical requests. As LLM becomes more and more integrated into the rest of the tech ecosystems, the attack surface will become much broader. For example, businesses and organizations started using RAG to enhance their internal LLM, and vulnerabilities such as prompt injection can expose or even manipulate their sensitive data.

Nowadays, most LLM systems contain system prompts for aligning the model with its appropriate role and responsibilities. Some task-specific LLM applications might embed COT prompting or few-shot examples to further enhance Models’ abilities. However, this allows attackers to exploit them to make the model perform mal-intended actions. A simple example would be asking the model to ignore all previous system prompts and inject a new malicious system prompt into the model, or they can craft their evil requests into a seemingly legitimate chain of thought step. However, there are patterns to those “disguised system prompts” that allow evil requests to be fulfilled. For example, The PAIR attack mentions three categories : “role-playing, logical appeal, and authority endorsement.”

### Our proposed approach to tackle this problem

We took inspiration from an important security principle which is called “data/code” separation. Code aims to alter a system, while data does not. Likewise, the key distinction between “system prompt” and “user prompt” is one’s purpose is to “program the LLM system” to some extent, while the other is simply asking to fulfill a task. Nowadays, most language models are trained with ethical awareness so that if the user simply requests an unethical task, the system will reject it by default. Therefore, if we can separate the malicious system prompt from the user prompt, we will achieve the same isolation effect and model will be capable of rejecting malicious user requests![img](https://lh7-rt.googleusercontent.com/docsz/AD_4nXccYnSRyKCAMn7DFPz8LSlVlDLPaGeSqSf8wOgUtmoTNwaA2escS8VERBd8RqbMgbPn0IXqmvkJ3qaty_1EEtF1rj9FIVDaXPakih7Mm-zpLtNPY_Xq93iWHSKzIdcWrS4wKy81rAo5EjG1hEcPoZqkw7UO?key=uLgYCDSbrgwpMlhHhGTBEA)

Our approach will first instruct the model to summarize the user input through either zero-shot or few-shot prompting, and then we will instruct tune the LLM (or use few shot prompting as well) to further rewrite the prompt so that “system prompt like” language is separated from user prompts. Thus, the model can simply judge the true user request (untampered by those malicious system prompts) based on its own ethical awareness. The accepted user input cam be changed back to the original input to preserve intent.

### The experiment

For the experiment we will not be rerunning raw user input and will only be measuring the effectiveness of the model in rejecting malicious prompts. While most LLM security experiments only measure the ASR(aka the attack success rate), meaning the rate of successfully jail breaking the LLM with a malicious prompt, we measure both ASR and false positive rate, since we believe that successful security meaures should not only protect the system but also allow legitimate user requests.

Due to budget and resource constraints, we will only be experiementing with open source large language models, from which we have selected the 7 billion parameter vicuna model and 7 billion parameter meta llama2 model.

##### The dataset

We collected and compiled a labled dataset of prompt injection of **Mixed techniques** from five different sources in huggingface (for details [https://colab.research.google.com/drive/15ZfYB71qx6sLIwzlfEpws9UADJ4B5G0c?usp=sharing]()), with the label 1 being true malicious prompt injections and 0 being genuine user requests. We think that for a 7B parameter model, 100k samples are needed for fine tuniing. This dataset is comprised of around 330k samples which are divided into 5 csv files.

We noticed several issues that exists in the source datasets from huggingface:

* Very short prompts that provide little to zero relevance to our training

  * Solution: prune out samples by size (less than 7 words)
* Labels are different in different datasets: some use numbers, some use words(benign/evil)

  * Solution: need to convert them all to 0 and 1
* Some datasets only contain certain domain of prompt injection(get pwnd, get password)

  * We disregarded those for lack of generalization

Therefore we preprocessed them before adding them to our dataset.

###### The experiment setup

The most pressing and challenging issues is the lack of free cloud gpu resources where we can conduct our expeirment given the amount of computation to run LLMs over large datasets, as a single Vicuna inference would take at least two minutes on my local desktop equipped with RTX2070 SUPER, let alone the amount of storage needed to install all the tool to run the LLMs. Since google collab charge by the comput unit, we figured that the most cost effective way is to rent cloud gpu servers that charge by the hours. We ended up using a H100 instance on lambada labs.

###### How to run the experiment

In this repository we built a configurable benchmarking tool to test both ASR and false positives of prompt injection attacks on different LLM models. To run the experiment, you will need to :

1. make sure you git clone this repo on a gpu instance capable of running 7b parameter LLMs.
2. configure setup.sh so that it has execute priviledges(sudo chmod 700 setup.sh), the setup script only works for ubuntu Linux
3. run setup.sh
4. python3 run.py to start the experiment
5. follow prompts to enter the desired configurations (max token, the model to run, etc.)
6. the result will be downloaded into result.csv
