
import argparse
import gear_chat
from typing import Dict
import rich
import dataclasses
import utils
import axiomic.models as models
import yaml

from concurrent.futures import ThreadPoolExecutor, as_completed
import axiomic
import axiomic.core_config 

axiomic.core_config.global_config.thought_crime_retry_count = 1


@dataclasses.dataclass
class CaseResult:
    f1: float
    true_positives: int
    false_positives: int
    false_negatives: int

@dataclasses.dataclass
class EvalResults:
    cases: Dict[str, CaseResult]
    macro_f1: float


def set_f1s(results: EvalResults):
    for case in results.cases.values():
        if case.true_positives == 0:
            case.f1 = 0.0
        else:
            precision = case.true_positives / (case.true_positives + case.false_positives)
            recall = case.true_positives / (case.true_positives + case.false_negatives)
            case.f1 = 2 * (precision * recall) / (precision + recall)
    
    results.macro_f1 = sum([case.f1 for case in results.cases.values()]) / len(results.cases)
    return results


def evaluate_elect_agent(gear_chat, eval_examples, results: EvalResults = None):
    # Get pairs of (example, switch without that example)
    if results is None:
        results = EvalResults(cases={}, macro_f1=0.0)

    for example in eval_examples:
        if example.agent not in results.cases:
            results.cases[example.agent] = CaseResult(f1=0.0, true_positives=0, false_positives=0, false_negatives=0)
    
    for example in eval_examples:
        example_user = example.user
        example_agent = example.agent

        # gathered_info = gear_chat.gather.infer(example_user)
        experimental_result, _ = gear_chat.elect.infer(example_user)
        
        if experimental_result == example_agent:
            results.cases[example_agent].true_positives += 1
        else:
            results.cases[example_agent].false_positives += 1
            results.cases[experimental_result].false_negatives += 1
        
        print(f"Example: {example}")
        print(f"Evaluated: {experimental_result}")
        print(f"Expected: {example_agent}")
        print("")
    
    results = set_f1s(results)
    return results


def print_results_table(results, broken_list=[], timeout_list=[]):
    table = rich.table.Table(title="Evaluation Results")
    table.add_column("Model Name")
    table.add_column("Macro F1 Score")
    # table.add_column("True Positives")
    # table.add_column("False Positives")
    # table.add_column("False Negatives")

    results = list(sorted(results, key=lambda x: x[1].macro_f1, reverse=True))
    
    for name, result in results:
        table.add_row(
            name,
            f"{result.macro_f1:.2f}",
        )
    
    console = rich.console.Console()
    console.print(table)
    table2 = rich.table.Table(title="Not Following Prompt Models")
    table2.add_column("Model Name")
    for name in broken_list:
        table2.add_row(name)
    console.print(table2)

    table3 = rich.table.Table(title="Timeout Models")
    table3.add_column("Model Name")
    for name in timeout_list:
        table3.add_row(name)

    console.print(table3)



'''
                     Evaluation Results                      
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Model                                          ┃ Macro F1 ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Qwen/Qwen1.5-32B-Chat                          │ 1.00     │
│ Qwen/Qwen1.5-72B-Chat                          │ 1.00     │
│ garage-bAInd/Platypus2-70B-instruct            │ 1.00     │
│ mistralai/Mixtral-8x22B-Instruct-v0.1          │ 1.00     │
│ deepseek-ai/deepseek-coder-33b-instruct        │ 1.00     │
│ meta-llama/Llama-3-8b-chat-hf                  │ 1.00     │
│ meta-llama/Llama-3-70b-chat-hf                 │ 1.00     │
│ NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO    │ 0.73     │
│ NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT    │ 0.73     │
│ NousResearch/Nous-Hermes-2-Yi-34B              │ 0.73     │
│ Qwen/Qwen1.5-14B-Chat                          │ 0.73     │
│ mistralai/Mixtral-8x7B-Instruct-v0.1           │ 0.73     │
│ teknium/OpenHermes-2-Mistral-7B                │ 0.73     │
│ Snowflake/snowflake-arctic-instruct            │ 0.73     │
│ databricks/dbrx-instruct                       │ 0.73     │
│ NousResearch/Nous-Hermes-Llama2-13b            │ 0.50     │
│ openchat/openchat-3.5-1210                     │ 0.50     │
│ Austism/chronos-hermes-13b                     │ 0.47     │
│ NousResearch/Nous-Hermes-llama-2-7b            │ 0.47     │
│ Qwen/Qwen1.5-4B-Chat                           │ 0.47     │
│ mistralai/Mistral-7B-Instruct-v0.1             │ 0.47     │
│ allenai/OLMo-7B-Instruct                       │ 0.30     │
│ Qwen/Qwen1.5-7B-Chat                           │ 0.27     │
│ NousResearch/Nous-Capybara-7B-V1p9             │ 0.23     │
│ NousResearch/Nous-Hermes-2-Mistral-7B-DPO      │ 0.23     │
│ teknium/OpenHermes-2p5-Mistral-7B              │ 0.23     │
│ togethercomputer/StripedHyena-Nous-7B          │ 0.23     │
│ cognitivecomputations/dolphin-2.5-mixtral-8x7b │ 0.23     │
│ Open-Orca/Mistral-7B-OpenOrca                  │ 0.07     │
└────────────────────────────────────────────────┴──────────┘
'''

NOT_WORKING = '''
│ Nexusflow/NexusRaven-V2-13B │
│ Phind/Phind-CodeLlama-34B-v2              │
│ Qwen/Qwen1.5-0.5B-Chat                    │
│ deepseek-ai/deepseek-llm-67b-chat         │
│ google/gemma-2b-it                        │
│ google/gemma-7b                           │
│ microsoft/WizardLM-2-8x22B                │
│ microsoft/phi-2                           │
│ mistralai/Mistral-7B-Instruct-v0.2        │
│ mistralai/Mistral-7B-v0.1                 │
│ mistralai/Mixtral-8x22B                   │
│ mistralai/Mixtral-8x7B-v0.1               │
│ snorkelai/Snorkel-Mistral-PairRM-DPO      │
│ togethercomputer/GPT-JT-Moderation-6B     │
│ togethercomputer/LLaMA-2-7B-32K           │
│ togethercomputer/RedPajama-INCITE-7B-Base │
│ togethercomputer/StripedHyena-Hessian-7B  │
│ zero-one-ai/Yi-34B                        │
│ zero-one-ai/Yi-6B                         │
│ codellama/CodeLlama-13b-Instruct-hf       │
│ codellama/CodeLlama-34b-Instruct-hf       │
│ codellama/CodeLlama-70b-Instruct-hf       │
│ codellama/CodeLlama-70b-Python-hf         │
│ codellama/CodeLlama-7b-Instruct-hf        │
│ codellama/CodeLlama-70b-hf                │
│ codellama/CodeLlama-13b-Python-hf         │
│ codellama/CodeLlama-34b-Python-hf         │
│ meta-llama/Llama-3-8b-hf                  │
│ meta-llama/Meta-Llama-3-70B               │
│ meta-llama/Llama-2-13b-hf                 │
│ meta-llama/Llama-2-70b-hf                 │
│ meta-llama/Llama-2-7b-chat-hf             │
│ meta-llama/Llama-2-13b-chat-hf            │
│ meta-llama/Llama-2-70b-chat-hf            │
│ meta-llama/Llama-2-7b-hf                  │
│ Meta-Llama/Llama-Guard-7b                 │
│ meta-llama/LlamaGuard-2-8b                │
│ prompthero/openjourney                    │
│ togethercomputer/Llama-2-7B-32K-Instruct  │
'''


def evaluate_model(model, chat, gear_dir):
    elect_eval_examples = utils.load_elect_eval_examples(gear_dir)
    try:
        # Some models will break by generating a lot of tokens. We never need more than 32 in a response.
        with model & models.MaxTokens32:
            result = (model.context.llm_model_name, evaluate_elect_agent(chat, elect_eval_examples))
        return 'success', result
    except axiomic.ThoughtCrime:
        return 'broken', model.context.llm_model_name
    except KeyboardInterrupt:
        return 'timeout', model.context.llm_model_name


def run_evaluation_with_thread_pool(eval_list, chat, gear_dir):
    results = []
    broken_models = []
    timeout_list = []

    for model in eval_list:
        try:
            status, result = evaluate_model(model, chat, gear_dir)
            if status == 'success':
                results.append(result)
            elif status == 'broken':
                broken_models.append(result)
            elif status == 'timeout':
                timeout_list.append(result)
        except Exception as e:
            print(f"Model {model.context.llm_model_name} generated an exception: {e}")

        print_results_table(results, broken_models, timeout_list=timeout_list)


def list_together_models():
    eval_list = [
        # models.Together.Text.Google.gemma_7b,
        # models.Together.Text.MistralAI.mistral_7b_instruct_v0_2,
        # models.Together.Text.Llama2.llama_2_13b_hf,
        # models.Together.Text.Llama3.llama_3_8b_hf,
        # models.Together.Text.MistralAI.mistral_7b_instruct_v0_2,
        # models.Together.Text.CodeLlama.codellama_34b_instruct_hf,
        # models.Together.Text.CodeLlama.codellama_70b_instruct_hf,
        # models.Together.Text.Llama3.llama_3_70b_chat_hf,
        # models.OpenAI.MultiModal.GPT4o,
        # models.Anthropic.Text.Cluade3.Opus,
    ]

    # List all the together models.
    for cl in models.Together.Text.__dict__:
        if cl.startswith("_"):
            continue
        model_container = models.Together.Text.__dict__[cl]

        for model_name in model_container.__dict__:
            if model_name.startswith("_"):
                continue
            model = model_container.__dict__[model_name]

            eval_list.append(model)

    return eval_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('gear_dir', metavar='DIR', help='the directory name which defines the GEAR agents.')
    args = parser.parse_args()
    chat = gear_chat.GEARChat(args.gear_dir)
    
    eval_list = list_together_models()
    run_evaluation_with_thread_pool(eval_list, chat, args.gear_dir)



if __name__ == '__main__':
    main()
