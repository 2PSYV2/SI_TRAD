
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/2PSYV2/SI_TRAD)](https://github.com/2PSYV2/SI_TRAD/releases)

# OpenRouter Langer
## LLM Translation Testing Tool
### Use
 1. First download the latest release from GitHub or pull the main branch: https://github.com/2PSYV2/SI_TRAD/releases. You will  need 7zip/rar/other compatible software to unpack the release.
 2. Ensure you have downloaded python 3.11 or later: Run "python --version" in CMD | Powershell | etc.
3. Run the main.py: "python main.py" from the source folder
4. If it's your first launch, Langer will attempt to download any and all libraries and dependencies you might lack, so BE NOT AFRAID of the terminal and text in it, it's 99,9% probability just pip installing packets
5. If it's your first launch, you will be asked to create your own API key to access the functionality of the program:
	1. Access this webpage and register: https://openrouter.ai/ 
	2. Generate API key following the instructions and set you spending limit (by default every model included with the program is set to be free, but you can/should/might/etc. add another model which might be paid. You can be sure you are using a paid version if you follow the model's link)
6. Once you enter the API key you may use the software to either translate individual queries or multi-queries via JSON.
7. All the multi-queries are saved in JSON format and can be analyzed by the evaluate.py. To invoke the Evaluator use the appropriate interface button.

### FAQ

> Why shouldn't I share my API with friends/relatives/my local spy/concubines/vassals/etc.?

Your API key is yours and only yours. If you decide to share the API key bare in mind that ANYONE with access to it might and WILL use it to burn through tokens. If you ever wish to share an API key with someone, you should generate a new one with expiration date and spending limit if it is decided to be a paid key. Even free personal key should not be shared as they usually won't have expiration date and will become time bombs.

> How do I switch the API key?

Go to the "File" --> "Set API Key"

>Where is my API key stored?

/Data/ folder houses miscellaneous data like settings and your personal API key. To be precise the key is inside ".env" file. Beware about the file as it is not encrypted and thus anyone with the access to the file might compromise your API key, thus I recommend to create a new API key to use exclusively for Langer and set it's  expiration date to anything but "never".

>What's the difference between "Translate" and "Translate from JSON"?

Plain translate just sends the API request  to  the model appending the translation segment, it allows you to send literally anything with minor tweaks. "Translate from JSON" is a tool to translate multiple texts simultaneously and store additional processing data. File valid for "Translate from JSON" must include origin language, target language, phrase in the original language and reference translation in target language. The output file from this operation will include additionally the LLM's translation, model's reference and time employed in the process.

> I constantly receive: "[ERROR] Request limit reached, try again later." How to fix it?

You can not "fix it", the error means you have exhausted your API's calls and thus must wait a bit. Usually you see it if you use a free model as their bandwidth and tokens are limited and thus you can run dry fast. If you MUST use specific model you should either wait or switch to a paid version. Meanwhile if you just need SOME translation you may switch to other model which may or may not be less congested at the time.

> How to add more languages or models?

In the boxes where you can select ether of them, you can find  the option "+ Add new...".

- Languages: Just type the language's name in English as it is the language used for LLM prompting  and thus will integrate in calls, better than others.
- Models: Access OpenRouter's https://openrouter.ai/models page and choose freely which you want to use in the app. I would recommend applying these filters to narrow the selection to the most optimal LLMs for translation. (https://openrouter.ai/models?fmt=cards&input_modalities=text&output_modalities=text&categories=translation)

> Can I use the program for other prompts  rather than translation?

Yes and No. Langer is no more than a relay and a wrapper to your API calls. By default the behavior of the LLM is set to: "You are a translation assistant. Provide exclusively the translation of the requested text." and thus it's responses will tend to be in this awe. You can change the systems role in preferences to be anything and thus virtually convert Langer into your personal API Wrapper.

> Do you plan on implementing calls on locally instantiated LLMs?

By default Langer redirects it's API calls and requests to: "https://openrouter.ai/api/v1/chat/completions" but it is not forced nor hard-coded to do so, furthermore, you can change the URL to be whatever you wish.
The method to send the API calls is "r = requests.post(API_URL, headers=headers, json=data)" with OpenAI API scheme and thus any locally instantiated LLM with exposed HTTP and compatible API will work.

- Work out of the box:
	- LM Studio should work out of the box as it uses OpenAI style API - (`http://localhost:1234/v1/chat/completions`)  As for API key, you can fill it with anything like 'lmstudio'
	- Fastchat is supposedly using OpenAI style API thus should work out of the box as well - (`http://127.0.0.1:8000/v1/chat/completions`)
- Should work with minor tweaks to schema:
	- Ollama: Uses slightly different API thus might need minor tweaks to the schema. Either wait untill I decide to implement schema editing and selection, or edit the code segment relevant to the payload construction.

> Can I edit/fork/sell/etc. Langer?

Langer is licensed under MIT license. All the information regarding the legal status of such actions must be referred to at LICENSE.txt

### Technical details


### Authors
-	Eugene Edelshteyn Kylymnyk



