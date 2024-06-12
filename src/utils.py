# choose the right prompt format for chat models
PROMPT_DICT = {
    
    "llama2_detect": '''[INST]<<SYS>>
You are are a helpful assistant.
<</SYS>>

As an assistant, your task is to serve as a response judge. Provided with the related knowledge, a dialogue history and a generated response, your objective is to determine if the generated response contains any hallucinated information that (1) directly contradicts the given knowledge, or (2) cannot be verified from the provided knowledge and dialogue context.

You SHOULD carefully evaluate each segment of the generated response and determine if the response contains any hallucinated information. If such content is detected, your output should be "Yes"; otherwise, it should be "No".

###Knowledge###: {knowledge}
###Dialogue History###: {dialogue_history}
###Response###: {response}
###Judgement###: [/INST]''',

    "llama2_rationale": '''[INST]<<SYS>>
You are are a helpful assistant.
<</SYS>>

As an assistant, your task is to serve as a response judge. Provided with the related knowledge, a dialogue history and a generated response, your objective is to determine if the generated response contains any hallucinated information that (1) directly contradicts the given knowledge, or (2) cannot be verified from the provided knowledge and dialogue context.

You SHOULD follow the following examples:

Example 1:
###Knowledge###: Use by a wider audience only came in 1995 when restrictions on the use of the Internet to carry commercial traffic were lifted.
###Dialogue History###: [Human]: Can you imagine the world without internet access? [Assistant]: Yeah, but once the access to the internet was a rare thing. do you remember? [Human]: I do. What else can you tell me ?
###Response###: Well, I know that the internet was primarily available to the public in the early 1980s, with no restrictions on commercial traffic from the very beginning. 
###Judgement###: Yes. The hallucinated part of the response is the claim that "the internet was primarily available to the public in the early 1980s, with no restrictions on commercial traffic from the very beginning." In reality, widespread use of the internet only began after restrictions on carrying commercial traffic were lifted in 1995.

Example 2:
###Knowledge###: Women brewers dominated alcohol production on every occupied continent until commercialization and industrialization of brewing occurred.
###Dialogue History###: [Human]: I have homebrewed before. Beer can be fun to craft. [Assistant]: That's interesting, so you just brew enough for yourself? [Human]: Yes, that is correct. And it can be used to make some really cool concoctions. [Assistant]: That's cool! Did you know that beer has been made by home brewers long before commercial companies made it? [Human]: Home brewers have been around for centuries if not thousands of years. [Assistant]: Yes, and the first beers were thick! Have you ever made a mead or a rice wine? [Human]: I have made mead, but that info about rice wine is interesting. Rice is also very versatile. What else do you know about home brewing?
###Response###: Absolutely, in fact, in ancient times, women brewers not only dominated alcohol production but also creatively used local ingredients like fruits, herbs, and spices to enhance the flavor of the brews.
###Judgement###: Yes. The hallucinated part of the response is the claim that "women brewers creatively used local ingredients like fruits, herbs, and spices to enhance the flavor of the brews." This specific information is not verifiable from the given knowledge, which only mentions that women dominated alcohol production before the commercialization and industrialization of brewing. There's no mention of the specific ingredients used by these early women brewers.

Example 3:
###Knowledge###: Imagine Dragons is an American rock band from Las Vegas, Nevada, consisting of lead vocalist Dan Reynolds, lead guitarist Wayne Sermon, bassist and keyboardist Ben McKee, and drummer Daniel Platzman.
###Dialogue History###: [Human]: I really like Imagine Dragons.  Are you familiar with them at all?
###Response###: I've heard of them. They're an American rock band, right?
###Judgement###: No.

You SHOULD first carefully evaluate each segment of the generated response and determine if the response contains any hallucinated information. If any such content is found, your next step is to identify the specific hallucinated segment and explain why it qualifies as such. Your judgement MUST strictly follow the format demonstrated in the examples above and be well-organized, clear and concise.

###Knowledge###: {knowledge}
###Dialogue History###: {dialogue_history}
###Response###: {response}
###Judgement###: [/INST]'''

}