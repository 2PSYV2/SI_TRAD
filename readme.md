  

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/2PSYV2/SI_TRAD/blob/main/LICENSE.txt)

[![Release](https://img.shields.io/github/v/release/2PSYV2/SI_TRAD)](https://github.com/2PSYV2/SI_TRAD/releases)

  

# OpenRouter Langer

## LLM Translation Testing Tool

### Use of "Langer"

1. First download the latest release from GitHub or pull the main branch: https://github.com/2PSYV2/SI_TRAD/releases. You will need 7zip/rar/other compatible software to unpack the release.

2. Ensure you have downloaded python **3.11** or newer: Run "python --version" in CMD | Powershell | etc.

3. Run the main.py: "python main.py" from the source folder

4. If it's your first launch, Langer will attempt to download any and all libraries and dependencies you might lack, so BE NOT AFRAID of the terminal and text in it, it's 99,9% probability just pip installing packets

5. If it's your first launch, you will be asked to create your own API key to access the functionality of the program:

1. Access this webpage and register: https://openrouter.ai/

2. Generate API key following the instructions and set you spending limit (by default every model included with the program is set to be free, but you can/should/might/etc. add another model which might be paid. You can be sure you are using a paid version if you follow the model's link)

6. Once you enter the API key you may use the software to either translate individual queries -> "Translate" or multi-queries via JSON -> "Translate from JSON".  The multi-queries results are to be saved in JSON format in the **/sets/output** folder while the initial queries should be saved in **/sets/input**. The format of the afformentioned JSONs will be discussed later.

7. All the multi-queries outputs are saved in JSON format and can be analyzed by the evaluate.py. To invoke the Evaluator use the appropriate interface button "Compare Outputs". Besides, the multi-queries WILL override the language chosen in the menu but will comply with the model selection, as the first is hard-coded into the JSON and the second one must be provided during execution.

### Use of "Langer - Evaluator"
1. Ensure you have performed at least one multi-queue translation so you have something to analyze.
2. Once in the Evaluator select "File" -> "Load JSON Files...". By default the opened window will point to /sets/output.
3. Select one or more JSON files with output results.
4. Now you can select any of the loaded JSONs from the menu box and see it's content.
5. After loading and checking if the files are the desired one, you may parse the files through the evaluation algorithms. To do so go to "Tools" and select either "Evaluate Automatically..." for an auto evaluation with ALL available algorithms, or select the desired algorithm from "Evaluate..."


  ### Plugins
  The Evaluator allows to add any number of new evaluation algorithms as long as it complies with few rules:
  1. The new algorithm MUST be inside the /evaluation/ folder and be of the .py format
  2. The algorithm MUST include name parameter such as:

    name = "BLEU"

6. The algorithm must expose as the main function a function by the name "evaluate" and be of the next format:

    evaluate(reference: str, hypothesis: str) -> float:

7. If your algorithm MUST include a new library which is not part of the standard set nor is downloaded automatically by the Langer (see: data/requirements.txt) you should either implement an auto downloader/installer like in the Langer's main.py or add the name of the library to the data/requirements.txt. In the latter case if the lib's name and the download link name are different you might see warning when launching as it is not included in the dictionary by default and as such, should be added.

The Evaluator WILL Parse EVERY single .py file in the folder so do NOT include non compliant algorithms as it will ignore them.

### FAQ

<details>  
<summary>

> Why shouldn't I share my API with friends/relatives/~~my local spy/concubines/vassals~~/etc.?
</summary>
  

Your API key is yours and only yours. If you decide to share the API key bare in mind that ANYONE with access to it might and WILL use it to burn through tokens. If you ever wish to share an API key with someone, you should generate a new one with expiration date and spending limit if it is decided to be a paid key. Even free personal key should not be shared as they usually won't have expiration date and will become time bombs.

  </details>
<details>  
<summary>

> How do I switch the API key?
</summary>
  

Go to the "File" --> "Set API Key"

  </details>  
  <details>  
<summary>

>Where is my API key stored?
  </summary>

/Data/ folder houses miscellaneous data like settings and your personal API key. To be precise the key is inside ".env" file. Beware about the file as it is not encrypted and thus anyone with the access to the file might compromise your API key, thus I recommend to create a new API key to use exclusively for Langer and set it's expiration date to anything but "never".

  </details>  
<details>  
<summary>

>What's the difference between "Translate" and "Translate from JSON"?
</summary>
  

Plain translate just sends the API request to the model appending the translation segment, it allows you to send literally anything with minor tweaks. "Translate from JSON" is a tool to translate multiple texts simultaneously and store additional processing data. File valid for "Translate from JSON" must include origin language, target language, phrase in the original language and reference translation in target language. The output file from this operation will include additionally the LLM's translation, model's reference and time employed in the process.

  </details>  
 <details> 
<summary>

> I constantly receive: "[ERROR] Request limit reached, try again later." How to fix it?
</summary>
  

You can not "fix it", the error means you have exhausted your API's calls and thus must wait a bit. Usually you see it if you use a free model as their bandwidth and tokens are limited and thus you can run dry fast. If you MUST use specific model you should either wait or switch to a paid version. Meanwhile if you just need SOME translation you may switch to other model which may or may not be less congested at the time.

   </details> 
   <details> 
   <summary>

> How to add more languages or models?
</summary>
  

In the boxes where you can select ether of them, you can find the option "+ Add new...".

  

- Languages: Just type the language's name in English as it is the language used for LLM prompting and thus will integrate in calls, better than others.

- Models: Access OpenRouter's https://openrouter.ai/models page and choose freely which you want to use in the app. I would recommend applying these filters to narrow the selection to the most optimal LLMs for translation. (https://openrouter.ai/models?fmt=cards&input_modalities=text&output_modalities=text&categories=translation)

  </details> 
  <details> 
  <summary>

> Can I use the program for other prompts rather than translation?
</summary>
  

Yes and No. Langer is no more than a relay and a wrapper to your API calls. By default the behavior of the LLM is set to: "You are a translation assistant. Provide exclusively the translation of the requested text." and thus it's responses will tend to be in this awe. You can change the systems role in preferences to be anything and thus virtually convert Langer into your personal API Wrapper.

  </details> 
  <details> 
  <summary>

> Do you plan on implementing calls on locally instantiated LLMs?
</summary>
  

By default Langer redirects it's API calls and requests to: "https://openrouter.ai/api/v1/chat/completions" but it is not forced nor hard-coded to do so, furthermore, you can change the URL to be whatever you wish.

The method to send the API calls is "r = requests.post(API_URL, headers=headers, json=data)" with OpenAI API scheme and thus any locally instantiated LLM with exposed HTTP and compatible API will work.

  

- Work out of the box:

- LM Studio should work out of the box as it uses OpenAI style API - (`http://localhost:1234/v1/chat/completions`) As for API key, you can fill it with anything like 'lmstudio'

- Fastchat is supposedly using OpenAI style API thus should work out of the box as well - (`http://127.0.0.1:8000/v1/chat/completions`)

- Should work with minor tweaks to schema:

- Ollama: Uses slightly different API thus might need minor tweaks to the schema. Either wait untill I decide to implement schema editing and selection, or edit the code segment relevant to the payload construction.

  </details> 
  <details>
  <summary>

> Can I edit/fork/sell/etc. Langer?
</summary>
  

Langer is licensed under MIT license. All the information regarding the legal status of such actions must be referred to at LICENSE.txt

  

### Technical details

 #### Json formating
 ##### Input for batch translation
 The format of the JSON you will receive once it is translated and parsed is as follows:
The format of the JSON to be used as the input for the multi-query must be as follows:
 

    {
	    "source_language": "ORIGINAL LANGUAGE",
	    "target_language": "THE TRANLATION LANGUAGE",
	    "pairs": [
			    {
				    "id": NUMBER VALUE OF THE PAIR,
				    "original": "STRING IN THE ORIGINAL LANGUAGE",
				    "reference": "REFERENCE TRANSLATION DEEMED AS THE MOST ACCURATE"
			    },
			    {
				    "id": NUMBER VALUE OF THE PAIR,
				    "original": "STRING IN THE ORIGINAL LANGUAGE",
				    "reference": "REFERENCE TRANSLATION DEEMED AS THE MOST ACCURATE"
			    },
			    ...
		    ]
    }
 ##### Output of batch translation

    {
  	    "model": "NAME OF THE MODEL USED WHEN TRANSLATING",
  	    "source_language": "ORIGINAL LANGUAGE",
  	    "target_language": "THE TRANSLATION LANGUAGE",
  	    "results": [
	  		    {
	  			    "id": NUMBER VALUE OF THE PAIR,
	  				  "original": "STRING IN THE ORIGINAL LANGUAGE",
	  				  "reference": "REFERENCE TRANSLATION DEEMED AS THE MOST ACCURATE",
	  				  "llm_translation": "THE TRANSLATION GIVEN BY THE CHOSEN LLM"
	  		    },
	  		    {
	  			    "id": NUMBER VALUE OF THE PAIR,
	  				  "original": "STRING IN THE ORIGINAL LANGUAGE",
	  				  "reference": "REFERENCE TRANSLATION DEEMED AS THE MOST ACCURATE",
	  				  "llm_translation": "THE TRANSLATION GIVEN BY THE CHOSEN LLM"
	  		    },
	  		    ...
	  	    ]
  	  }

 ##### Evaluated outputs
The JSON formatting of the evaluation output is as follows:

    {
	    "timestamp": "TIME AT WHICH THE EVALUATION WAS PERFORMED"
	    "metrics_used": [
		    "NAME OF METRIC 1",
		    "NAME OF METRIC 2",
		    ...
	    ],
	    "models": {
		    "NAME OF THE MODEL 1": [
			    "NAME OF METRIC 1": [
				    {
					    "id": NUMBER ID OF THE PAIR AND IT'S EVALUATION,
					    "reference": "REFERENCE TRANSLATION DEEMED AS THE MOST ACCURATE",
					    "hypothesis": "THE TRANSLATION GIVEN BY THE CHOSEN LLM",
					    "SCORE": NUMBER VALUE OF THE SCORE GIVEN BY THE ALGORITHM
				    },
				    {
					    "id": NUMBER ID OF THE PAIR AND IT'S EVALUATION,
					    "reference": "REFERENCE TRANSLATION DEEMED AS THE MOST ACCURATE",
					    "hypothesis": "THE TRANSLATION GIVEN BY THE CHOSEN LLM",
					    "SCORE": NUMBER VALUE OF THE SCORE GIVEN BY THE ALGORITHM
				    },
				    ...
			    ]
			    "NAME OF METRIC 2": [
				   ...
			    ],
			    
		    "NAME OF MODEL 2:"[
			    "NAME OF METRIC 1": [
				   ...
				]
			]
	    {
	  }

  

### Authors

- Eugene Edelshteyn Kylymnyk
