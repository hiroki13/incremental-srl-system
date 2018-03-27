# incremental-srl-system

## Install
```
git clone https://github.com/hiroki13/incremental-srl-system.git
```

## Getting Started
### Prerequisites:
* python 2
* numpy
* theano

### Example Comand
- Command Prompt Mode

```
python main.py
```
```
SYSTEM START

	Loading Embeddings...

	Vocab Size: 130000

Model configuration
	SHIFT: EmbCorpus -> EmbInit -> BiRNNLayer-1:(100x128):gru -> Dense(256x1,sigmoid)
	  - Params: 1197479
	LABEL: EmbCorpus -> EmbInit -> EmbMark -> BiRNNLayer-2:(105x128):gru -> Dense(256x54,softmax)
	  - Params: 1510630

Building a predict func...

Input a tokenized sentence.
>>>  She
She

>>>  likes
She likes
PRD:likes  She/A0 likes/_

>>>  cats
She likes cats
PRD:likes  She/A0 likes/_ cats/A1
```

- Server/Client Mode
```
python server.py
```

```
python client.py
```
