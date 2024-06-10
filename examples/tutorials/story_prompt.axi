nodes {
  immediate_node {
    value: "Write a story about a dog finding a cookie."
  }
  name: "_immediate1"
}
nodes {
  history_complete_node {
    user_message {
      name: "_immediate1"
    }
    complete_params {
      llm_provider_name: "together_text"
      llm_model_name: "meta-llama/Llama-3-8b-chat-hf"
      llm_temperature: 0.5
      llm_max_tokens: 1024
    }
    system_prompt {
      name: "_immediate2"
    }
  }
  name: "_history_complete3"
}
