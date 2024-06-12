python src/llama2_judge.py --mode detect --data_path data/induced/induced_train.json --model_path meta-llama/Llama-2-13b-chat-hf

python src/eval.py --mode detect --prediciton_path meta-evaluation_result/Llama-2-13b-chat-hf_detect.json