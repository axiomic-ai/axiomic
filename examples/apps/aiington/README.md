
## George AIingtong

This is a sipmle twitter bot which is a founding father of AI. It illustrates basic usage of:

- Routing to an appropriate sub agent
- Mixing models in the same application
- Storing templates and prompts in files

### Usage

Example usage:

    % python aiington.py
    Enter something to reply to (then ^D):
    AI Is a scam and doesn't work.

    together_text: 206 toks -> Qwen/Qwen1.5-32B-Chat -> 9 toks (in 1.73s)
    Route:  REPLY_CRITISIM

    together_text: 180 toks -> meta-llama/Llama-3-70b-chat-hf -> 66 toks (in 1.11s)
    My dear fellow, I see you're misinformed. "Artificial" simply means man-made, not inferior. AI is a remarkable achievement, augmenting human capabilities. It's not a scam, but a testament to human ingenuity. Let's focus on the facts and potential benefits, rather than spreading misconceptions.
