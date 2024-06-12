import json
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import argparse
import numpy
import evaluate

parser = argparse.ArgumentParser()
parser.add_argument("--mode",  type=str, choices=["detect", "rationale"], default="detect", help="Whether to evaluate the hallucination detection or rationale generation")
parser.add_argument("--prediciton_path", type=str, default="meta-evaluation_result/Llama-2-13b-chat-hf_detect.json", help="Path to the prediction file")

args = parser.parse_args()

data_list = json.load(open(args.prediciton_path, 'r', encoding='utf8'))

if args.mode == "detect":

    preds = []
    labels = []
    err_cnt = 0
    for data in data_list:
        
        if data['judgement'].startswith('Yes'):
            preds.append(1)
        elif data['judgement'].startswith('No'):
            preds.append(0)
        else:
            err_cnt += 1
            continue
        
        if data['target'].startswith('Yes'):
            labels.append(1)
        else:
            labels.append(0)
                
    hallu_p = precision_score(labels, preds, pos_label=1, average='binary')
    hallu_r = recall_score(labels, preds, pos_label=1, average='binary')
    hallu_f1 = f1_score(labels, preds, pos_label=1, average='binary')

    non_hallu_p = precision_score(labels, preds, pos_label=0, average='binary')
    non_hallu_r = recall_score(labels, preds, pos_label=0, average='binary')
    non_hallu_f1 = f1_score(labels, preds, pos_label=0, average='binary')

    avg_acc = accuracy_score(labels, preds)
    avg_p = (hallu_p + non_hallu_p) / 2
    avg_r = (hallu_r + non_hallu_r) / 2
    macro_f1 = f1_score(labels, preds, average='macro')

    print(f"hallu_p: {hallu_p*100:.2f}\thallu_r: {hallu_r*100:.2f}\thallu_f1: {hallu_f1*100:.2f}\tnon_hallu_p: {non_hallu_p*100:.2f}\tnon_hallu_r: {non_hallu_r*100:.2f}\tnon_hallu_f1: {non_hallu_f1*100:.2f}\tavg_acc: {avg_acc*100:.2f}\tavg_p: {avg_p*100:.2f}\tavg_r: {avg_r*100:.2f}\tmacro_f1: {macro_f1*100:.2f}")

else:
    
    rouge = evaluate.load('rouge')
    bleu = evaluate.load("bleu")
    bertscore = evaluate.load("bertscore")

    predictions = []
    references = []
    for data in data_list:
        
        predictions.append(data['judgement'])
        references.append(data['target'])
            
    rouge_results = rouge.compute(predictions=predictions, references=references)
    bleu_results = bleu.compute(predictions=predictions, references=references, max_order=4)
    bertscore_results = bertscore.compute(predictions=predictions, references=references, lang="en")
    
    print(f"rougeL: {rouge_results['rougeL']*100:.2f}\tbleu: {bleu_results['bleu']*100:.2f}\tbertscore: {numpy.mean(bertscore_results['f1'])*100:.2f}")