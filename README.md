## Quick Run

Download and set-up `Ollama` then:
```bash
ollama pull llama3.1:8b
```

For tracing with `langsmith`, set-up a `.env` file at the project root that has the following keys:
```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your_langsmith_api_key>
LANGSMITH_PROJECT=langchain-study
```

To use the react agent, you must also provide:
```python
TAVILY_API_KEY=<your_tavily_api_key>
```

**Run the following commands in a Python (>=3.12) environment:**

```bash
pip install -e .
python -m assistants.hr_assistant.main
```

## Langchain Notes

- A langchain `chain` is a sequence of operations where the O/P of one step is the I/P to the next step.
    - A "step" in a chain can be anything: an LLM call, some data transformation, a tool call, another chain, etc.

- Most langchain components like `langchain.prompts.PromptTemplate`, etc. implement the `Runnable` interface.
    - All `Runnable` types expose an `invoke(..)` method.
    - `Runnable` types can be piped using `LangChain Expression Language(LCEL)` to define a `RunnableSequence` (this is a "chain"):
        ```python
        prompt_template = PromptTemplate(...)
        llm = ChatOllama(..)

        chain = prompt_template | llm
        response = chain.invoke(input_variables: dict = {...})
        ```
        - In this example, the `Runnable` sequence comprises a `PromptTemplate` in the first step. The `invoke(...)` method implemented for a `PromptTemplate` type accepts a dictionary of `input_variables` to be rendered into the prompt.
        - Alternatively, this rendering of template variables can also be done directly by calling the `format(..)` method:
            ```python
            prompt_template_string = PromptTemplate(...).format(**input_variables: dict)
            ```
        - The `invoke(...)` method implementation for the `PromptTemplate` is defined in one of its parent interfaces called the `BasePromptTemplate` which initializes a `RunnableConfig` and returns a `PromptValue` (the formatted prompt).
        - You can also use the `invoke(...)` method directly:
            ```
            prompt_template_string = PromptTemplate(...).invoke(input: dict = input_variables).to_string()
            ```
    - A `RunnableSequence` type when "invoked" using the `invoke(...)` method:
        - accepts the args expected by the first `Runnable` in the sequence.
        - returns the value of the last `Runnable` type's `invoke(...)`. 
        - In the above example, the first `Runnable` is a `PromptTemplate` type which expects a `dict` of `input_variables` and, the last `Runnable` is a `ChatOllama` type which returns an `AIMessage` response object.
        - Langchain is able to adapt the O/P of one `Runnable` to the expected I/P format of the next in a `RunnableSequence`.

- The langchain `hub` object offers access to community langchain resources like prompts, etc.
    ```python
    from langchain import hub
    ```

- LangChain offers a `create_react_agent(...)` method which provides a clean interface for building LangChain ReAct agents.
    ```python
    from langchain.agents.react.agent import create_react_agent
    ```
    - `create_react_agent(...)` returns a `Runnable` which is referred to as a "LangChain ReAct agent".

- For actual execution of tool calls, langchain provides an `AgentExecutor` as the agent runtime.
    ```python
    from langchain.agents import AgentExecutor
    ```
- For implementing tools in langchain, it offers a `@tool` decorator which can be imported like so:
    ```python
    from langchain_core.tools import tool

    @tool
    def multiply_two_integers(
        a: int,
        b: int,
    ) -> int:
        """
        Returns the result of a*b.
        """
        return a*b
    ```
    - LangChain will extract a schema for this "tool" for agent use:
        - name
        - description
        - expected args
    - The model itself doesn't execute a tool, this is done by the langchain backend. The model only produces the arguments need for the call.
    
## ReAct architecture

- A `ReAct` styled agent implements the following loop for query resolution:
    ```
    Thought -> Action & Action Input(s) -> Observation -> Thought -> (...) -> Final Answer
    ```
- Initially, "tool calling" was implemented through text-based prompting, for example:
    ```
    You have access to the following tools:

    {tools}

    Use the following format:

    Question: the problem you are trying to solve for.
    Thought: your thought on the appropriate action.
    Action: the recommended action, must be one of {tools}
    Action Input: the input to be provided for executing the action
    Observation: the result of the action
    (this pattern can repeat N times)

    When you have resolved the question:
        Thought: I now think I have a final answer
        Final Answer: the final answer to the question
    
    Begin!

    Question: {question}
    Thought: {agent_scratch_pad}
    ```
    - the `Action` and `Action Input` were then parsed by the system backend to finally execute the "tool call".
    - The `agent_scratch_pad` is initially an empty string:
        ```python
        ""
        ```
        - The `agent_scratch_pad` captures the context of the model's recommended `Action`, `Action Input` and `Observation` thus far.
        - It expands like so:
            ```python
            Action: <tool_name>
            Action Input: <tool_args>
            Observation: <tool_output>
            (...)
            Action: <tool_name>
            Action Input: <tool_args>
            Observation: <tool_output>
            Thought:

            # the `Thought:` is always an empty placeholder prompt appended after the last `Observation` (at the end).
            ```
        - So the prompt iself would go from:
            *first iteration*
            ```python
            <aforementioned ReAct instructions>

            (...)

            Begin!

            Question: <user_query>
            Thought:
            ```
            *n-th iteration*
            ```python
            <aforementioned ReAct instructions>

            (...)

            Begin!

            Action: <tool_name>
            Action Input: <tool_args>
            Observation: <tool_output>
            (...)
            Action: <tool_name>
            Action Input: <tool_args>
            Observation: <tool_output>
            Thought:
            ```
- The landscape has evolved now, modern LLMs support **native function calling**.
- "Agents" in the langchain ecosystem have evolved in the following manner:
    ```
    Text-based tool calling through prompt itself ->
    Native function call supported LLMs as agents ->
    LangGraph ReAct agents for production demands.
    ```

## Agentic AI Notes

- Providing links to resources (real and accurate references) for answers is called "grounding".
    - Grounding an agent is important for building trust with the customer.
    - This helps validate that the answer is not a model hallucination.

