We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

##### LangChain v1.0

* [Release notes](/oss/python/releases/langchain-v1)
* [Migration guide](/oss/python/migrate/langchain-v1)

##### Get started

* [Install](/oss/python/langchain/install)
* [Quickstart](/oss/python/langchain/quickstart)
* [Philosophy](/oss/python/langchain/philosophy)

##### Core components

* [Agents](/oss/python/langchain/agents)
* [Models](/oss/python/langchain/models)
* [Messages](/oss/python/langchain/messages)
* [Tools](/oss/python/langchain/tools)
* [Short-term memory](/oss/python/langchain/short-term-memory)
* [Streaming](/oss/python/langchain/streaming)
* [Middleware](/oss/python/langchain/middleware)
* [Structured output](/oss/python/langchain/structured-output)

##### Advanced usage

* [Guardrails](/oss/python/langchain/guardrails)
* [Runtime](/oss/python/langchain/runtime)
* [Context engineering](/oss/python/langchain/context-engineering)
* [Model Context Protocol (MCP)](/oss/python/langchain/mcp)
* [Human-in-the-loop](/oss/python/langchain/human-in-the-loop)
* [Multi-agent](/oss/python/langchain/multi-agent)
* [Retrieval](/oss/python/langchain/retrieval)
* [Long-term memory](/oss/python/langchain/long-term-memory)

##### Use in production

* [Studio](/oss/python/langchain/studio)
* [Test](/oss/python/langchain/test)
* [Deploy](/oss/python/langchain/deploy)
* [Agent Chat UI](/oss/python/langchain/ui)
* [Observability](/oss/python/langchain/observability)

* [Response Format](#response-format)
* [Provider strategy](#provider-strategy)
* [Tool calling strategy](#tool-calling-strategy)
* [Custom tool message content](#custom-tool-message-content)
* [Error handling](#error-handling)
* [Multiple structured outputs error](#multiple-structured-outputs-error)
* [Schema validation error](#schema-validation-error)
* [Error handling strategies](#error-handling-strategies)

[Core components](/oss/python/langchain/agents)

# Structured output

Structured output allows agents to return data in a specific, predictable format. Instead of parsing natural language responses, you get structured data in the form of JSON objects, Pydantic models, or dataclasses that your application can directly use. LangChain’s [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) handles structured output automatically. The user sets their desired structured output schema, and when the model generates the structured data, it’s captured, validated, and returned in the `'structured_response'` key of the agent’s state.

Copy

Ask AI

```
def create_agent(def  create_agent( ... ... response_format: Union[ response_format: Union[ ToolStrategy[StructuredResponseT], ToolStrategy[StructuredResponseT], ProviderStrategy[StructuredResponseT], ProviderStrategy[StructuredResponseT], type[StructuredResponseT], type[StructuredResponseT], ] ]
```

## [​](#response-format) Response Format

Controls how the agent returns structured data:

* **`ToolStrategy[StructuredResponseT]`**: Uses tool calling for structured output
* **`ProviderStrategy[StructuredResponseT]`**: Uses provider-native structured output
* **`type[StructuredResponseT]`**: Schema type - automatically selects best strategy based on model capabilities
* **`None`**: No structured output

When a schema type is provided directly, LangChain automatically chooses:

* `ProviderStrategy` for models supporting native structured output (e.g. [OpenAI](/oss/python/integrations/providers/openai), [Grok](/oss/python/integrations/providers/xai))
* `ToolStrategy` for all other models

The structured response is returned in the `structured_response` key of the agent’s final state.

## [​](#provider-strategy) Provider strategy

Some model providers support structured output natively through their APIs (currently only OpenAI and Grok). This is the most reliable method when available. To use this strategy, configure a `ProviderStrategy`:

Copy

Ask AI

```
class ProviderStrategy(Generic[SchemaT]): class  ProviderStrategy(Generic[SchemaT]): schema: type[SchemaT] schema: type[SchemaT]
```

[​](#param-schema)

schema

required

The schema defining the structured output format. Supports:

* **Pydantic models**: `BaseModel` subclasses with field validation
* **Dataclasses**: Python dataclasses with type annotations
* **TypedDict**: Typed dictionary classes
* **JSON Schema**: Dictionary with JSON schema specification

LangChain automatically uses `ProviderStrategy` when you pass a schema type directly to [`create_agent.response_format`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent(response_format)) and the model supports native structured output:

Copy

Ask AI

```
from pydantic import BaseModel from  pydantic import  BaseModelfrom langchain.agents import create_agent from langchain.agents import  create_agent class ContactInfo(BaseModel): class  ContactInfo(BaseModel): """Contact information for a person.""" """Contact information for a person.""" name: str = Field(description="The name of the person") name: str = Field(description = "The name of the person") email: str = Field(description="The email address of the person") email: str = Field(description = "The email address of the person") phone: str = Field(description="The phone number of the person") phone: str = Field(description = "The phone number of the person") agent = create_agent(agent = create_agent( model="gpt-5",  model ="gpt-5", tools=tools,  tools =tools, response_format=ContactInfo # Auto-selects ProviderStrategy  response_format = ContactInfo # Auto-selects ProviderStrategy)) result = agent.invoke({result = agent.invoke({ "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]  "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]})}) result["structured_response"]result["structured_response"]# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```

Provider-native structured output provides high reliability and strict validation because the model provider enforces the schema. Use it when available.

If the provider natively supports structured output for your model choice, it is functionally equivalent to write `response_format=ProductReview` instead of `response_format=ToolStrategy(ProductReview)`. In either case, if structured output is not supported, the agent will fall back to a tool calling strategy.

## [​](#tool-calling-strategy) Tool calling strategy

For models that don’t support native structured output, LangChain uses tool calling to achieve the same result. This works with all models that support tool calling, which is most modern models. To use this strategy, configure a `ToolStrategy`:

Copy

Ask AI

```
class ToolStrategy(Generic[SchemaT]): class  ToolStrategy(Generic[SchemaT]): schema: type[SchemaT] schema: type[SchemaT] tool_message_content: str | None tool_message_content: str  |  None handle_errors: Union[ handle_errors: Union[ bool,  bool, str,  str, type[Exception], type[Exception], tuple[type[Exception], ...], tuple[type[Exception], ...], Callable[[Exception], str], Callable[[Exception], str], ] ]
```

[​](#param-schema-1)

schema

required

The schema defining the structured output format. Supports:

* **Pydantic models**: `BaseModel` subclasses with field validation
* **Dataclasses**: Python dataclasses with type annotations
* **TypedDict**: Typed dictionary classes
* **JSON Schema**: Dictionary with JSON schema specification
* **Union types**: Multiple schema options. The model will choose the most appropriate schema based on the context.

[​](#param-tool-message-content)

tool\_message\_content

Custom content for the tool message returned when structured output is generated. If not provided, defaults to a message showing the structured response data.

[​](#param-handle-errors)

handle\_errors

Error handling strategy for structured output validation failures. Defaults to `True`.

* **`True`**: Catch all errors with default error template
* **`str`**: Catch all errors with this custom message
* **`type[Exception]`**: Only catch this exception type with default message
* **`tuple[type[Exception], ...]`**: Only catch these exception types with default message
* **`Callable[[Exception], str]`**: Custom function that returns error message
* **`False`**: No retry, let exceptions propagate

Copy

Ask AI

```
from pydantic import BaseModel, Field from  pydantic import BaseModel, Field from typing import Literal from  typing import  Literalfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.structured_output import ToolStrategy from langchain.agents.structured_output import  ToolStrategy class ProductReview(BaseModel): class  ProductReview(BaseModel): """Analysis of a product review.""" """Analysis of a product review.""" rating: int | None = Field(description="The rating of the product", ge=1, le=5) rating: int  |  None = Field(description = "The rating of the product", ge = 1, le = 5) sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review") sentiment: Literal["positive", "negative"] = Field(description = "The sentiment of the review") key_points: list[str] = Field(description="The key points of the review. Lowercase, 1-3 words each.") key_points: list[str] = Field(description ="The key points of the review. Lowercase, 1-3 words each.") agent = create_agent(agent = create_agent( model="gpt-5",  model ="gpt-5", tools=tools,  tools =tools, response_format=ToolStrategy(ProductReview)  response_format =ToolStrategy(ProductReview))) result = agent.invoke({result = agent.invoke({ "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]  "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]})})result["structured_response"]result["structured_response"]# ProductReview(rating=5, sentiment='positive', key_points=['fast shipping', 'expensive'])# ProductReview(rating=5, sentiment='positive', key_points=['fast shipping', 'expensive'])
```

### [​](#custom-tool-message-content) Custom tool message content

The `tool_message_content` parameter allows you to customize the message that appears in the conversation history when structured output is generated:

Copy

Ask AI

```
from pydantic import BaseModel, Field from  pydantic import BaseModel, Field from typing import Literal from  typing import  Literalfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.structured_output import ToolStrategy from langchain.agents.structured_output import  ToolStrategy class MeetingAction(BaseModel): class  MeetingAction(BaseModel): """Action items extracted from a meeting transcript.""" """Action items extracted from a meeting transcript.""" task: str = Field(description="The specific task to be completed") task: str = Field(description = "The specific task to be completed") assignee: str = Field(description="Person responsible for the task") assignee: str = Field(description = "Person responsible for the task") priority: Literal["low", "medium", "high"] = Field(description="Priority level") priority: Literal["low", "medium", "high"] = Field(description = "Priority level") agent = create_agent(agent = create_agent( model="gpt-5",  model ="gpt-5", tools=[],  tools =[], response_format=ToolStrategy( response_format =ToolStrategy( schema=MeetingAction,  schema =MeetingAction, tool_message_content="Action item captured and added to meeting notes!"  tool_message_content ="Action item captured and added to meeting notes!" ) ))) agent.invoke({agent.invoke({ "messages": [{"role": "user", "content": "From our meeting: Sarah needs to update the project timeline as soon as possible"}]  "messages": [{"role": "user", "content": "From our meeting: Sarah needs to update the project timeline as soon as possible"}]})})
```

Copy

Ask AI

```
================================ Human Message ================================= ================================ Human Message ================================= From our meeting: Sarah needs to update the project timeline as soon as possibleFrom our meeting: Sarah needs to update the project timeline as soon as possible ================================== Ai Message ================================== ================================== Ai Message ==================================Tool Calls:Tool Calls: MeetingAction (call_1) MeetingAction (call_1) Call ID: call_1 Call ID: call_1 Args: Args: task: Update the project timeline task: Update the project timeline assignee: Sarah assignee: Sarah priority: high priority: high ================================= Tool Message ================================= ================================= Tool Message =================================Name: MeetingActionName: MeetingAction Action item captured and added to meeting notes!Action item captured and added to meeting notes! 
```

Without `tool_message_content`, our final [`ToolMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolMessage) would be:

Copy

Ask AI

```
================================= Tool Message ================================= ================================= Tool Message =================================Name: MeetingActionName: MeetingAction Returning structured response: {'task': 'update the project timeline', 'assignee': 'Sarah', 'priority': 'high'}Returning structured response: {'task': 'update the project timeline', 'assignee': 'Sarah', 'priority': 'high'} 
```

### [​](#error-handling) Error handling

Models can make mistakes when generating structured output via tool calling. LangChain provides intelligent retry mechanisms to handle these errors automatically.

#### [​](#multiple-structured-outputs-error) Multiple structured outputs error

When a model incorrectly calls multiple structured output tools, the agent provides error feedback in a [`ToolMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolMessage) and prompts the model to retry:

Copy

Ask AI

```
from pydantic import BaseModel, Field from  pydantic import BaseModel, Field from typing import Union from  typing import  Unionfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.structured_output import ToolStrategy from langchain.agents.structured_output import  ToolStrategy class ContactInfo(BaseModel): class  ContactInfo(BaseModel): name: str = Field(description="Person's name") name: str = Field(description = "Person's name") email: str = Field(description="Email address") email: str = Field(description = "Email address") class EventDetails(BaseModel): class  EventDetails(BaseModel): event_name: str = Field(description="Name of the event") event_name: str = Field(description = "Name of the event") date: str = Field(description="Event date") date: str = Field(description = "Event date") agent = create_agent(agent = create_agent( model="gpt-5",  model ="gpt-5", tools=[],  tools =[], response_format=ToolStrategy(Union[ContactInfo, EventDetails]) # Default: handle_errors=True  response_format =ToolStrategy(Union[ContactInfo, EventDetails]) # Default: handle_errors=True)) agent.invoke({agent.invoke({ "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]  "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]})})
```

Copy

Ask AI

```
================================ Human Message ================================= ================================ Human Message ================================= Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15thExtract info: John Doe (john@email.com) is organizing Tech Conference on March 15th None None ================================== Ai Message ================================== ================================== Ai Message ==================================Tool Calls:Tool Calls: ContactInfo (call_1) ContactInfo (call_1) Call ID: call_1 Call ID: call_1 Args: Args: name: John Doe name: John Doe email: john@email.com email: john@email.com EventDetails (call_2) EventDetails (call_2) Call ID: call_2 Call ID: call_2 Args: Args: event_name: Tech Conference event_name: Tech Conference date: March 15th date: March 15th ================================= Tool Message ================================= ================================= Tool Message =================================Name: ContactInfoName: ContactInfo Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected.Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected. Please fix your mistakes. Please fix your mistakes. ================================= Tool Message ================================= ================================= Tool Message =================================Name: EventDetailsName: EventDetails Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected.Error: Model incorrectly returned multiple structured responses (ContactInfo, EventDetails) when only one is expected. Please fix your mistakes. Please fix your mistakes. ================================== Ai Message ================================== ================================== Ai Message ==================================Tool Calls:Tool Calls: ContactInfo (call_3) ContactInfo (call_3) Call ID: call_3 Call ID: call_3 Args: Args: name: John Doe name: John Doe email: john@email.com email: john@email.com ================================= Tool Message ================================= ================================= Tool Message =================================Name: ContactInfoName: ContactInfo Returning structured response: {'name': 'John Doe', 'email': 'john@email.com'}Returning structured response: {'name': 'John Doe', 'email': 'john@email.com'} 
```

#### [​](#schema-validation-error) Schema validation error

When structured output doesn’t match the expected schema, the agent provides specific error feedback:

Copy

Ask AI

```
from pydantic import BaseModel, Field from  pydantic import BaseModel, Fieldfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.structured_output import ToolStrategy from langchain.agents.structured_output import  ToolStrategy class ProductRating(BaseModel): class  ProductRating(BaseModel): rating: int | None = Field(description="Rating from 1-5", ge=1, le=5) rating: int  |  None = Field(description ="Rating from 1-5", ge = 1, le = 5) comment: str = Field(description="Review comment") comment: str = Field(description = "Review comment") agent = create_agent(agent = create_agent( model="gpt-5",  model ="gpt-5", tools=[],  tools =[], response_format=ToolStrategy(ProductRating), # Default: handle_errors=True  response_format =ToolStrategy(ProductRating), # Default: handle_errors=True system_prompt="You are a helpful assistant that parses product reviews. Do not make any field or value up."  system_prompt ="You are a helpful assistant that parses product reviews. Do not make any field or value up.")) agent.invoke({agent.invoke({ "messages": [{"role": "user", "content": "Parse this: Amazing product, 10/10!"}]  "messages": [{"role": "user", "content": "Parse this: Amazing product, 10/10!"}]})})
```

Copy

Ask AI

```
================================ Human Message ================================= ================================ Human Message ================================= Parse this: Amazing product, 10/10!Parse this: Amazing product, 10/10! ================================== Ai Message ================================== ================================== Ai Message ==================================Tool Calls:Tool Calls: ProductRating (call_1) ProductRating (call_1) Call ID: call_1 Call ID: call_1 Args: Args: rating: 10 rating: 10 comment: Amazing product comment: Amazing product ================================= Tool Message ================================= ================================= Tool Message =================================Name: ProductRatingName: ProductRating Error: Failed to parse structured output for tool 'ProductRating': 1 validation error for ProductRating.ratingError: Failed to parse structured output for tool 'ProductRating': 1 validation error for ProductRating.rating Input should be less than or equal to 5 [type=less_than_equal, input_value=10, input_type=int]. Input should be less than or equal to 5 [type=less_than_equal, input_value=10, input_type=int]. Please fix your mistakes. Please fix your mistakes. ================================== Ai Message ================================== ================================== Ai Message ==================================Tool Calls:Tool Calls: ProductRating (call_2) ProductRating (call_2) Call ID: call_2 Call ID: call_2 Args: Args: rating: 5 rating: 5 comment: Amazing product comment: Amazing product ================================= Tool Message ================================= ================================= Tool Message =================================Name: ProductRatingName: ProductRating Returning structured response: {'rating': 5, 'comment': 'Amazing product'}Returning structured response: {'rating': 5, 'comment': 'Amazing product'} 
```

#### [​](#error-handling-strategies) Error handling strategies

You can customize how errors are handled using the `handle_errors` parameter: **Custom error message:**

Copy

Ask AI

```
ToolStrategy(ToolStrategy( schema=ProductRating,  schema =ProductRating, handle_errors="Please provide a valid rating between 1-5 and include a comment."  handle_errors ="Please provide a valid rating between 1-5 and include a comment."))
```

If `handle_errors` is a string, the agent will *always* prompt the model to re-try with a fixed tool message:

Copy

Ask AI

```
================================= Tool Message ================================= ================================= Tool Message =================================Name: ProductRatingName: ProductRating Please provide a valid rating between 1-5 and include a comment.Please provide a valid rating between 1-5 and include a comment. 
```

**Handle specific exceptions only:**

Copy

Ask AI

```
ToolStrategy(ToolStrategy( schema=ProductRating,  schema =ProductRating, handle_errors=ValueError # Only retry on ValueError, raise others  handle_errors = ValueError # Only retry on ValueError, raise others))
```

If `handle_errors` is an exception type, the agent will only retry (using the default error message) if the exception raised is the specified type. In all other cases, the exception will be raised. **Handle multiple exception types:**

Copy

Ask AI

```
ToolStrategy(ToolStrategy( schema=ProductRating,  schema =ProductRating, handle_errors=(ValueError, TypeError) # Retry on ValueError and TypeError  handle_errors =(ValueError, TypeError) # Retry on ValueError and TypeError))
```

If `handle_errors` is a tuple of exceptions, the agent will only retry (using the default error message) if the exception raised is one of the specified types. In all other cases, the exception will be raised. **Custom error handler function:**

Copy

Ask AI

```
def custom_error_handler(error: Exception) -> str: def  custom_error_handler(error: Exception) -> str: if isinstance(error, StructuredOutputValidationError):  if  isinstance(error, StructuredOutputValidationError): return "There was an issue with the format. Try again.  return "There was an issue with the format. Try again. elif isinstance(error, MultipleStructuredOutputsError):  elif  isinstance(error, MultipleStructuredOutputsError): return "Multiple structured outputs were returned. Pick the most relevant one."  return "Multiple structured outputs were returned. Pick the most relevant one." else:  else: return f"Error: {str(error)}"  return  f"Error: {str(error)} " ToolStrategy(ToolStrategy( schema=ToolStrategy(Union[ContactInfo, EventDetails]),  schema =ToolStrategy(Union[ContactInfo, EventDetails]), handle_errors=custom_error_handler  handle_errors = custom_error_handler))
```

On `StructuredOutputValidationError`:

Copy

Ask AI

```
================================= Tool Message ================================= ================================= Tool Message =================================Name: ToolStrategyName: ToolStrategy There was an issue with the format. Try again.There was an issue with the format. Try again. 
```

On `MultipleStructuredOutputsError`:

Copy

Ask AI

```
================================= Tool Message ================================= ================================= Tool Message =================================Name: ToolStrategyName: ToolStrategy Multiple structured outputs were returned. Pick the most relevant one.Multiple structured outputs were returned. Pick the most relevant one. 
```

On other errors:

Copy

Ask AI

```
================================= Tool Message ================================= ================================= Tool Message =================================Name: ToolStrategyName: ToolStrategy Error: Error:  
```

**No error handling:**

Copy

Ask AI

```
response_format = ToolStrategy(response_format = ToolStrategy( schema=ProductRating,  schema =ProductRating, handle_errors=False # All errors raised  handle_errors = False  # All errors raised))
```

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/structured-output.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Middleware](/oss/python/langchain/middleware)[Guardrails](/oss/python/langchain/guardrails)