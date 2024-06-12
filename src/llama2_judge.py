import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import argparse
from utils import PROMPT_DICT


parser = argparse.ArgumentParser()
parser.add_argument("--mode",  type=str, choices=["detect", "rationale"], default="detect", help="Whether to run the hallucination detection or rationale generation task")
parser.add_argument("--data_path", type=str, default="data/induced/induced_train.json", help="Path to the data file")
parser.add_argument("--model_path", type=str, default="meta-llama/Llama-2-13b-chat-hf", help="Path to the judge model")

args = parser.parse_args()

prompt_template = PROMPT_DICT[f'llama2_{args.mode}']

data_list = json.load(open(args.data_path, 'r', encoding='utf8'))

# Set the maximum number of tokens to generate based on the task
if args.mode == "detect":
    max_new_tokens = 2
else:
    max_new_tokens = 300

model = AutoModelForCausalLM.from_pretrained(
    args.model_path,
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto'
).half().eval() 
    
tokenizer = AutoTokenizer.from_pretrained(args.model_path)

result_list = []
for data in data_list:

    prompt = prompt_template.format_map(data)
        
    inputs = tokenizer(prompt, return_tensors='pt').to("cuda")
        
    tokens = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
    )
    completion_tokens = tokens[0][inputs['input_ids'].size(1):]
    completion = tokenizer.decode(completion_tokens, skip_special_tokens=True).strip()
    
    data['judgement'] = completion
    
    result_list.append(data)
    
json.dump(result_list, open(f"meta-evaluation_result/{args.model_path.split('/')[-1]}_{args.mode}.json", 'w', encoding='utf8'), indent=4)