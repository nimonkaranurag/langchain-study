https://blog.langchain.com/https://blog.langchain.com/favicon.pngLangChain Bloghttps://blog.langchain.com/Ghost 6.6Wed, 05 Nov 2025 23:48:59 GMT60*By Liam Bush*

## Background

Every successful platform needs reliable support, but we realized our own team was spending hours tracking down answers to technical questions. This friction wasn't just slowing down our engineers—it was a critical **bottleneck** for our users.

We set out to solve this

]]>https://blog.langchain.com/rebuilding-chat-langchain/690adc85eab788000153a26bWed, 05 Nov 2025 16:28:53 GMT

*By Liam Bush*

## Background

Every successful platform needs reliable support, but we realized our own team was spending hours tracking down answers to technical questions. This friction wasn't just slowing down our engineers—it was a critical **bottleneck** for our users.

We set out to solve this using the very tools we champion: **LangChain, LangGraph** and **LangSmith**. We originally built [**chat.langchain.com**](http://chat.langchain.com/?ref=blog.langchain.com) as a prototype, explicitly designed to serve two functions:

1. **Product Q&A:** Help users—and our own team—get instant, authoritative answers to product questions.
2. **Customer Prototype:** Serve as a living example demonstrating how customers could build sophisticated, reliable agents using the LangChain stack.

We had a strong intent and a functional product. But we have a confession: our support engineers weren't actively using the LangChain Chatbot. That's where our real learning began. This is the story of **how we fixed our own agent**—and what we learned about building truly reliable, production-grade applications that our customers can adapt and use.

Our team was not actively using Chat LangChain not because it was broken and not because they didn't believe in it. But because when someone asked *"Why isn't streaming working in production?"* they needed something more thorough than just using docs as it’s only resource. We all know there’s never enough documentation.

So they built their own workflow:

* **Step 1:** Search our docs ([docs.langchain.com](http://docs.langchain.com/?ref=blog.langchain.com)) to understand what the feature is supposed to do.
* **Step 2:** Check our knowledge base ([support.langchain.com](http://support.langchain.com/?ref=blog.langchain.com)) to see if other users hit the same issue and how it was resolved.
* **Step 3:** Open `Claude Code`, search the actual implementation, and verify what the code actually does.

**Docs for the official story. Knowledge base for real-world issues. Codebase for ground truth.**

---

## We Decided to Automate It

This three-step ritual worked incredibly well. We watched them do it dozens of times a day and thought: *what if we just automated this exact workflow?*

So we built an internal [`Deep Agent`](https://docs.langchain.com/oss/python/deepagents/overview?ref=blog.langchain.com) (a library for building agents that can tackle complex, multi-step tasks) with three specialized subagents — one for docs, one for knowledge base, one for codebase search — each one asking follow-up questions and filtering results before passing insights to a main orchestrator agent.

The main agent would synthesize everything and deliver answers like this:

> Example output:  
>   
> *"To stream from subgraphs, set subgraphs: true in your stream config according to the* [*LangGraph streaming docs.*](https://docs.langchain.com/oss/python/langgraph/use-subgraphs?ref=blog.langchain.com#stream-subgraph-outputs) *There's a support article titled ['Why is token streaming not working after upgrade](*[*https://support.langchain.com/articles/7150806184-Why-is-token-by-token-streaming-not-working-after-upgrading-LangGraph?)[?](https://www.notion.so/263808527b1780db9f26fa75aed5e7e3?pvs=21)*](https://support.langchain.com/articles/7150806184-Why-is-token-by-token-streaming-not-working-after-upgrading-LangGraph?%29%5B%3F%5D%28https%3A%2F%2Fwww.notion.so%2F263808527b1780db9f26fa75aed5e7e3%3Fpvs=21%29&ref=blog.langchain.com)*' that explains this exact issue — you need to enable subgraph streaming to get token-level updates from nested agents. The implementation is in* [pregel/main.py lines 3373-3279,](https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/pregel/main.py?ref=blog.langchain.com#L3273-L3279) *where the subgraphs flag controls whether nested graph outputs are included in the stream."*

Our engineers loved it.

It saved them hours every week on complex debugging. They'd describe a production issue and get back a comprehensive answer that cited documentation, referenced known solutions, and pointed to the exact lines of code that mattered.

---

## Then We Had a Realization

Then someone asked the obvious question: **if this works so well for us, why doesn't our public Chat LangChain work this way?**

It was a fair point. Our public tool was chunking documents into fragments, generating embeddings, storing them in a vector database. We had to reindex constantly as docs updated. Users got answers, but the citations needed love and the context was fragmented.

We'd accidentally built something better internally just by copying what worked. It was time to bring that same approach to the public product.

When we started rebuilding, we quickly realized we needed to combine two different architectures driven by two broad categories of questions. Most questions could be answered using docs and knowledge base. The remainder would require analysis of foundation of code.

---

## How We Built The New Agent

### For Simple Docs: Create Agent

We chose [`createAgent`](https://docs.langchain.com/oss/javascript/releases/langchain-v1?ref=blog.langchain.com#createagent) (Agent abstraction in [`langchain`](https://docs.langchain.com/oss/javascript/langchain/overview?ref=blog.langchain.com)) for [chat.langchain.com](https://chat.langchain.com/?ref=blog.langchain.com) as the default mode because it's best for **speed**.

There's no planning phase, no orchestration overhead — just immediate tool calls and answers. The agent searches the docs, checks the knowledge base if needed, refines its query if the results are unclear, and returns an answer. Most documentation questions can be handled with **3-6 tool calls**, and Create Agent executes those in seconds.

**Model options:**

We give end-users access to multiple models — `Claude Haiku 4.5`, `GPT-4o Mini`, and `GPT-4o-nano` — and we've found that **Haiku 4.5 is exceptionally fast at tool calling** while maintaining strong accuracy. The combination of createAgent and Haiku 4.5 delivers **sub-15-second responses** for most queries, which is exactly what documentation Q&A demands.

**How we optimized it:**

We used [`LangSmith`](https://smith.langchain.com/?ref=blog.langchain.com) to trace every conversation, identify where the agent was making unnecessary tool calls, and refine our prompts. The data showed us that most questions could be answered with 3-6 tool calls if we taught the agent to ask better follow-up questions. LangSmith's evaluation suite let us A/B test different prompting strategies and measure improvements in both speed and accuracy.

### For answering using code: Deep Agent with Subgraphs

A lot of questions needed searching diving into our codebases to verify implementation details in addition to leveraging documentation, knowledge bases and cross-referencing known issues as resources.

**The architecture:**

For these tasks, we built a `Deep Agent` with **specialized subgraphs**: one for **documentation search**, one for **knowledge base search**, and one for **codebase search**.

Each subagent operates independently, asking follow-up questions, filtering through information, and extracting only the most relevant insights before passing them up to a main orchestrator agent. This prevents the main agent from drowning in context while allowing each domain expert to dig as deep as necessary.

**The codebase search advantage:**

The codebase search subagent is particularly powerful. It can search our private repositories using pattern matching, navigate file structures to understand context, and read specific implementations with line-number precision.

**The tradeoff:**

This deep agent architecture takes longer to run — sometimes **1-3 minutes** for complex queries — but the thoroughness is worth it. We leverage DeepAgent when the initial response is not addressing the core question.

Disclaimer: This mode is only enabled for a subset of users at launch and will be made generally available in a few days.

---

## Why We Got Moved Away from Vector Embeddings

The standard approach to documentation search — chunk docs into pieces, generate embeddings, store in a vector database, retrieve by similarity — works fine for unstructured content like PDFs. But for structured product documentation, we kept hitting three problems.

**Chunking breaks structure.** When you chop documentation into 500-token fragments, you lose headers, subsections, and context. The agent would cite `"set streaming=True"` without explaining why or when. Users had to hunt through pages to find what they needed.

**Constant reindexing.** Our docs update multiple times daily. Every change meant re-chunking, re-embedding, and re-uploading. It slowed us down.

**Vague citations.** Users couldn't verify answers or trace where information came from.

The breakthrough was realizing we were solving the wrong problem. Documentation is already organized. Knowledge bases are already categorized. Codebases are already navigable. We didn't need smarter retrieval — we needed to give the agent direct access to that existing structure.

---

## The Better Approach: Direct API Access and Smart Prompting

Instead of chunking and embedding, we gave the agent direct access to the real thing. For documentation, we use `Mintlify's API`, which returns **full pages** with all their headers, subsections, and code examples intact. For the knowledge base, we query our support articles by title first, then read the most promising ones in full. For codebase search, **we uploaded our codebase to our LangGraph Cloud deployment** and use `ripgrep`for pattern matching, directory traversal to understand structure, and file reading to extract specific implementations.

The agent doesn't retrieve based on similarity scores. It **searches like a human would** — with keywords, refinement, and follow-up questions.

This is where the magic happens. We don't just tell the agent to search once and return whatever it finds. We prompt it to **think critically** about whether it has enough information. If the results are ambiguous or incomplete, the agent refines its query and searches again. If documentation mentions a concept without explaining it, the agent searches for that concept specifically. If multiple interpretations are possible, the agent narrows down to the most relevant one.

---

## Tool Design: Building for Human Workflows

We designed our tools to mirror how humans actually search, not how retrieval algorithms work.

### Documentation Search: Full Pages, Not Fragments

The documentation search tool queries `Mintlify's API` and returns **complete pages**. When someone asks about streaming, the agent doesn't get three disjointed paragraphs from different sections — it gets the entire streaming documentation page, structured exactly as a human would read it.

```
@tool def SearchDocsByLangChain(query: str, page_size: int = 5, language: Optional[str] = None) -> str: """Search LangChain documentation via Mintlify API""" params = {"query": query, "page_size": page_size} if language: params["language"] = language response = requests.get(MINTLIFY_API_URL, params=params) return _format_search_results(response.json()) 
```

But we don't stop there. We prompt the agent to evaluate whether the initial results actually answer the question. *Is this the right section? Are there related concepts that need clarification? Would a more specific search term be better?*

The agent has a budget of **4-6 tool calls**, and we encourage it to use them strategically to refine its understanding before responding.

**Here's what that looks like in practice:**

A user asks, *"How do I add memory to my agent?"*

The agent searches for `"memory"` and gets results that cover checkpointing, conversation history, and the Store API. Instead of picking one at random, the agent realizes the question is ambiguous — memory could mean persisting conversation state within a thread or storing facts across multiple conversations.

It searches again with `"checkpointing"` to narrow down thread-level persistence, fetches the support article *"How do I configure checkpointing in LangGraph?"* and recognizes it doesn't cover cross-thread memory.

So it searches for `"store API"` to fill the gap.

The final answer covers both checkpointing for conversation history and the Store API for long-term memory, with precise citations to the support article and documentation used.

---

This iterative search process happens in seconds with Create Agent, but it fundamentally changes the quality of responses. The agent isn't just retrieving — it's reasoning about what the user actually needs.

### Knowledge Base Search: Scan, Then Read

We built the knowledge base (powered by Pylon) search as a **two-step process** because that's how humans use knowledge bases.

First, the agent retrieves article titles — sometimes dozens of them — and scans them to identify which ones seem relevant. Then it reads only those articles in full.

```
@tool def search_support_articles(collections: str = "all", limit: int = 50) -> str: """Step 1: Get article titles to scan""" articles = pylon_client.list_articles(collections=collections, limit=limit) return json.dumps([{ "id": a["id"], "title": a["title"], "url": a["url"] } for a in articles]) @tool def get_article_content(article_ids: List[str]) -> str: """Step 2: Read the most relevant articles""" articles = pylon_client.get_articles(article_ids) return "\\n\\n---\\n\\n".join([ f"# {a['title']}\\n\\n{a['content']}\\n\\nSource: {a['url']}" for a in articles ]) 
```

**Why this works:**

This prevents the agent from drowning in information. Instead of passing 30 full articles to the context window, the agent filters down to the 2-3 that actually matter, reads them thoroughly, and extracts the key insights.

The prompting reinforces this: *focus on quality over quantity, narrow your search if needed, and return only the information that directly answers the question.*

---

### Codebase Search: Search, Navigate, Verify

This is where our `Deep Agent` shines.

We gave the agent three tools that mirror the workflow from the opening — the same pattern our engineers follow when using `Claude Code`:

```
@tool def search_public_code(pattern: str, path: Optional[str] = None) -> str: """Step 1: Find code matching a pattern""" cmd = ["rg", pattern, str(path or search_path)] return subprocess.run(cmd, capture_output=True, text=True).stdout @tool def list_public_directory(path: str, max_depth: int = 2) -> str: """Step 2: Understand the file structure""" cmd = ["tree", "-L", str(max_depth), str(path)] return subprocess.run(cmd, capture_output=True, text=True).stdout @tool def read_public_file(file_path: str, start_line: int = 1, num_lines: int = 100) -> str: """Step 3: Read the actual implementation""" with open(file_path, "r") as f: lines = f.readlines() return "\\n".join(lines[start_line-1:start_line-1+num_lines]) 
```

**How it works:**

First, it searches the codebase for a pattern using `ripgrep`. Then it lists the directory structure to understand how files are organized. Finally, it reads the specific file, focusing on the relevant section, and returns the implementation with line numbers.

**Real-world example:**

A user reports that streaming tokens hang in production. The docs subagent finds that streaming configuration involves buffer settings. The knowledge base subagent surfaces a support article about token streaming issues after upgrades.

But the codebase subagent is the one that finds the actual implementation — it searches for `"streaming buffer"`, navigates to `callbacks/streaming.py`, and returns **lines 47-83** where the default buffer size is hardcoded.

That's the kind of deep investigation that solves real problems.

**The difference?** The `Deep Agent` can work in parallel across all three domains, and summarize the interim findings into one coherent answer.

---

## How Deep Agent and Subgraphs Solve Context Overload

When we first built the deep agent as a single system with access to all three tools, it would return everything it found. The main agent would get five documentation pages, twelve knowledge base articles, and twenty code snippets — all at once.

The context window would explode, and the final response would either be bloated with irrelevant details or miss the key insight entirely.

That's when we restructured it with specialized subgraphs.

**How it works:**

Each subagent operates independently. It searches its domain, asks follow-up questions to clarify ambiguity, filters through the results, and extracts only the **golden data**: the essential facts, citations, and context needed to answer the question.

The main orchestrator agent never sees the raw search results. It only receives the refined insights from each domain expert. Look at a full trace along with prompts \*\*[here](https://smith.langchain.com/public/c1059a52-d045-4013-a17f-3bdc07ef3f0d/r/67669d45-0065-47de-b0ee-0b4ca2687060?ref=blog.langchain.com).

**Why this matters:**

The docs subagent might read five full pages but return only two key paragraphs. The knowledge base subagent might scan twenty article titles but return only three relevant summaries. The codebase subagent might search fifty files but return only the specific implementation with line numbers.

The main agent gets clean, curated information that it can synthesize into a comprehensive answer.

---

## **Making It Production-Ready**

Even elegant agent designs need production infrastructure to survive contact with real users. We built modular [middleware](https://docs.langchain.com/oss/javascript/langchain/middleware?ref=blog.langchain.com#middleware) to handle the operational concerns that would otherwise clutter our prompts.

```
middleware = [ guardrails_middleware, # Filter off-topic queries model_retry_middleware, # Retry on API failures model_fallback_middleware, # Switch models if needed anthropic_cache_middleware # Cache expensive calls ] 
```

**What each layer does:**

**Guardrails** filter out off-topic queries so the agent stays focused on LangChain questions.

**Retry middleware** handles temporary API failures gracefully, so users never see cryptic error messages.

**Fallback middleware** switches between Haiku, GPT-4o Mini, and Gemini Nano if a model is unavailable.

**Caching** reduces costs by reusing results for identical queries.

These layers are invisible to users, but they're essential for reliability. They let the agent focus on reasoning while the infrastructure handles failure modes, cost optimization, and quality control.

---

## Getting the Agent to Users

Building a great agent is only half the battle. The other half? Getting it to users in a way that feels fast and intelligent.

We use the **LangGraph SDK** to handle all the complexity of streaming and state management.

### **Loading User Threads:**

When someone opens Chat LangChain, we fetch their conversation history using the LangGraph SDK:

```
const userThreads = await client.threads.search({ metadata: { user_id: userId }, limit: THREAD_FETCH_LIMIT, }) 
```

Every thread stores the user's ID in metadata, so conversations stay private and persistent across sessions. The LangGraph SDK handles the filtering automatically.

### S**treaming Responses in Real Time:**

When a user sends a message, the LangGraph SDK streams the response as it generates:

typescript

```
const streamResponse = client.runs.stream(threadId, "docs_agent", { input: { messages: [{ role: "user", content: userMessage }] }, streamMode: ["values", "updates", "messages"], streamSubgraphs: true, }) for await (const chunk of streamResponse) { if (chunk.event === "messages/partial") { setMessages(prev => updateWithPartialContent(chunk.data.content)) } } 
```

**What users see:**

Three stream modes show the agent's entire thought process:

* **`messages`** — Tokens appear progressively as the agent writes
* **`updates`** — Tool calls reveal what the agent is searching
* **`values`** — Final complete state after processing

Users watch the agent think, search docs, check the knowledge base, and build the response token-by-token. No loading spinners.

### Conversation Memory

Pass the same `thread_id` across messages and LangGraph's checkpointer handles the rest. It stores conversation history, retrieves context for each turn, and maintains state across sessions. We set a 7-day TTL. That's it.

---

## The Results

Since launching the new systems, we've seen dramatic improvements.

For public Chat LangChain, users get **sub-15-second responses** with precise citations. They can verify answers immediately because we link directly to the relevant documentation page or knowledge base article. And we no longer spend hours reindexing — the documentation updates automatically.

Internally, our support engineers use the `Deep Agent` to handle the most complex tickets. It searches documentation, cross-references known issues, and dives into our private codebase to find the implementation details that actually explain what's happening. **The agent doesn't replace our engineers — it amplifies them**, handling the research so they can focus on solving the problem.

---

## Key Takeaways

* **Follow the user's workflow:** Don't reinvent the wheel; automate the successful workflow your best users (or internal experts) already use. For LangChain, this meant replicating the three-step ritual of checking **docs,** the **knowledge base,** and the **codebase**.
* **Evaluate if vector embeddings are appropriate:** For structured content like product documentation and code, using vector embeddings could break the document structure, leads to vague citations, and requires constant reindexing. Vector embeddings are fantastic for unstructured content or shorter blocks or clustering use cases.
* **Give the agent direct access to structure:** This approach allows the agent direct API access to the content's existing structure. This allows the agent to search like a human, with keywords and refinement.
* **Prioritize reasoning over retrieval:** Design tools to mirror human workflows: scan article titles then read content, and use pattern matching and directory navigation for code. Prompt the agent to ask follow-up questions and refine its query if initial results are ambiguous, ensuring the final answer covers the user's real need.
* **Use Deep Agents and subgraphs to manage context:** For complex, multi-domain questions, using a **Deep Agent** with specialized **subgraphs** prevents the main orchestrator agent from drowning in raw search results. Each subagent filters and extracts only the "golden data" from its domain before passing the refined insights up.
* **The need for production middleware:** Even an elegant agent design needs robust infrastructure to be reliable. Implementing modular middleware for **guardrails** (filtering off-topic queries), **retries** (on API failures), **fallbacks** (switching models), and **caching** is essential for production-grade reliability, cost-optimization, and quality control.

---

## What's Next

**Public codebase search** (launching in the next few days) — When docs and knowledge base aren't sufficient, the agent will search our public repositories to verify implementations and cite exact line numbers

---

## Try It Yourself

Chat LangChain is live at [chat.langchain.com](https://chat.langchain.com/?ref=blog.langchain.com). Try it with `Claude Haiku 4.5` for the fastest responses, or experiment with `GPT-5 Mini` and `GPT-5 Nano` to see how different models perform.

---

## Join the Conversation

Building agents that balance speed and depth is hard, and we're still learning. If you're working on similar problems, we'd love to hear what you're discovering.

Join the LangChain community on our [forum](https://forum.langchain.com/?ref=blog.langchain.com) or follow us on [Twitter](https://twitter.com/LangChainAI?ref=blog.langchain.com).

Subscribe to our newsletter for updates from the team and community.

]]>*By* [*Vivek Trivedy*](https://www.linkedin.com/in/vivek-trivedy-433509134/?ref=blog.langchain.com)

We're excited to introduce **DeepAgents CLI** for coding, research, and building agents with persistent memory. Now you can easily create and run custom DeepAgents directly from the terminal. It supports:

* **Read, write, and edit files** in your project
* **Execute shell commands** with human approval
* **Search**

]]>https://blog.langchain.com/introducing-deepagents-cli/69039825eab78800015398d9Thu, 30 Oct 2025 16:55:35 GMT

*By* [*Vivek Trivedy*](https://www.linkedin.com/in/vivek-trivedy-433509134/?ref=blog.langchain.com)

We're excited to introduce **DeepAgents CLI** for coding, research, and building agents with persistent memory. Now you can easily create and run custom DeepAgents directly from the terminal. It supports:

* **Read, write, and edit files** in your project
* **Execute shell commands** with human approval
* **Search the web** for current information
* **Make HTTP requests** to APIs
* **Learn and remember** information across sessions
* **Plan tasks** with visual todo lists

## Installation

Install DeepAgents with CLI support:

```
 pip install deepagents-cli 
```

Or if you're using `uv`:

```
 uv pip install deepagents-cli 
```

## Quick Start

### 1. Set Up Your API Keys

DeepAgents CLI supports both Anthropic (Claude) and OpenAI models. **Anthropic Claude Sonnet 4 is the default** model and Tavily is used for web search. Add these to your `.env` file in your project root, and DeepAgents will automatically load them:

```
 export ANTHROPIC_API_KEY=your_api_key_here export OPENAI_API_KEY=your_api_key_here export TAVILY_API_KEY=your_tavily_key_here 
```

### 2. Launch the CLI

Start DeepAgents in your project directory:

```
 deepagents 
```

Or, if you’re using `uv`:

```
uv run deepagents 
```

### 3. Your First Task

Try asking the agent to help with a simple task:

```
 You: Add type hints to all functions in src/utils.py 
```

The agent will:

1. Read the file
2. Analyze the functions
3. Show you a diff of proposed changes
4. Ask for your approval before writing

There's also an option to Auto-Accept Edits to speed up development

## Learning Through Memory

One of DeepAgents' most powerful features is its **persistent memory system**. The agent can learn information and recall it across sessions. Each agent stores its knowledge in `~/.deepagents/AGENT_NAME/memories/`:

By default, if you spin up DeepAgents it will create an agent with the name `agent` and use that by default. You can change the agent used (and therefor what memories are used) by specifying an agent name, eg `deepagents --agent foo`. See next section for more details.

The agent automatically follows a **Memory-First Protocol**:

1. **During Research** - Checks `/memories/` for relevant knowledge
2. **Before answering** - Searches memory files in case of uncertainty
3. **When learning** - Saves new information to `/memories/`

### Example: Teaching API Patterns

```
 You: Remember that our API endpoints follow this pattern: - Use /api/v1/ prefix - All POST requests return 201 on success - Error responses include a "code" and "message" field Save this as our API conventions. Agent: I'll save these API conventions to memory. ⚙ write_file(/memories/api-conventions.md) 
```

Because this memory is persistent, the agent can use this information across future conversations.

```
You: Create a new endpoint for user registration Agent: Based on our API conventions, I'll create an endpoint at /api/v1/users that returns 201 on success and follows our error format. ⚙ read_file(/memories/api-conventions.md) ⚙ write_file(src/routes/users.py) 
```

### Memory Best Practices

**1. Use descriptive filenames** ✓ /memories/deployment-checklist.md ✗ /memories/notes.md

**2. Organize by topic**

```
/memories/ ├── backend/ │ ├── tools_to_use.md │ └── api-design.md ├── frontend/ │ ├── component-patterns.md └── security-setup.md 
```

**3. Verify saved knowledge** Because memory is just a set of files, you can always inspect and validate its content manually or with the agent.

```
You: Check what you know about our database Agent: Let me check my memories... ⚙ ls /memories/ ⚙ read_file(/memories/backend/database-schema.md) Based on my memory, we use PostgreSQL with these tables... 
```

You can also inspect the memory files manually by just looking at `~/.deepagents/AGENT_NAME/memories/`

### Managing Multiple Agents

You can create specialized agents for different projects or roles: From the DeepAgents CLI you can list existing agents, create new agents, or reset an agent to its default state (system prompts, memories, etc).

```
deepagents list 
```

```
deepagents agent backend-dev 
```

```
deepagents reset backend-dev 
```

## Get Started Today

Get started with DeepAgents and the DeepAgent CLI today! We're excited to see what you build.

Join the community and contribute:

* **GitHub**: [https://github.com/langchain-ai/deepagents](https://github.com/langchain-ai/deepagents?ref=blog.langchain.com)
* **Documentation**: [docs.langchain.com/oss/python/deepagents](https://docs.langchain.com/oss/python/deepagents/overview?ref=blog.langchain.com)
* **YouTube:** [https://youtu.be/IrnacLa9PJc](https://youtu.be/IrnacLa9PJc?ref=blog.langchain.com)

]]>*By Brace Sproul and Sam Crowder*

Today, we’re expanding who can build agents beyond developers. While a lot of the highest volume, customer-facing agents will be built by technical teams, nearly every business user has use cases for agentic applications in their daily routines. Our new **LangSmith Agent**

]]>https://blog.langchain.com/langsmith-agent-builder/690164caeab7880001539265Wed, 29 Oct 2025 14:38:43 GMT

*By Brace Sproul and Sam Crowder*

Today, we’re expanding who can build agents beyond developers. While a lot of the highest volume, customer-facing agents will be built by technical teams, nearly every business user has use cases for agentic applications in their daily routines. Our new **LangSmith Agent Builder** provides a no code agent-building experience — complete with memory and guided prompt creation — that lowers the barrier to building agents.

Sign up for [the waitlist today](http://langchain.com/langsmith-agent-builder-waitlist?ref=blog.langchain.com), and learn more about our approach below.

## What’s different

We’ve spent the past three years building agents alongside millions of developers. We hear from engineering teams how much their colleagues want to build their own agents. Even technical users have asked for faster ways to get started with agents that doesn't always involve writing and deploying code.

That’s why we’re launching **LangSmith** **Agent Builder** in private preview. It empowers everyone in an organization to build agents in a safe and accessible way. Unlike other solutions out there, LangSmith Agent Builder is an agent builder, [not a visual workflow builder](https://blog.langchain.com/not-another-workflow-builder/). Visual workflows builders have two major pitfalls:

1. **A visual workflow builder is not “low” barrier to entry.**
2. **Complex tasks quickly get too complicated to manage in a visual builder.**

Rather than follow a predetermined path, agents can delegate more decision-making to an LLM, allowing for more dynamic responses. By focusing on letting users build agents, we make agent building accessible to a broader audience while enabling users to tackle more complicated and complex tasks, rather than simple workflows.

## What an agent consists of

Every agent in LangSmith is built from four core components that work together:

* **Prompt:** This is the brain of your agent containing the logic to describe what the agent should do. With LangSmith agents, all the complexity of the agent is pushed into the prompt (rather than into a complex visual workflow). Writing good prompts is hard but really important, which is why we've built tools to make it easier (learn more in the next section).
* **Tools:** In order to interact with the world, agents need to call tools. LangSmith uses MCP to connect your agent to external services and data. We provide built-in tools, but you can also easily bring your own MCP servers. With LangSmith’s new Agent Authorization functionality, you can securely connect to tools your team has approved such as Gmail, Slack, LinkedIn, or Linear – all within the agent building flow.
* **Triggers:** Agents don't just respond to chat messages – they can also act automatically on background events. Set up triggers to launch your agent when you receive an email, get a Slack message in a particular channel, or on a time-based schedule.
* **Subagents:** We recommend starting out by putting most complexity in the prompt. But as complexity grows, you may want to keep the system manageable by creating smaller, more focused subagents for specific tasks.

## How we make it easier to build your agent

We've consistently seen that the hardest part of building agents is **writing effective prompts**. Two challenges make this difficult:

1. Good prompts require detail and specificity, but most people lack prompt engineering experience.
2. Prompts need to evolve or be updated as you discover edge cases and new requirements.

We've set out to make these things easier:

* **Start with a conversation** **instead of a blank canvas**. First, start with your request and describe what you want your agent to do in plain language. The system then asks you follow up questions to get the details right, auto-generates your agent's system prompt, connects tools, and sets triggers based on your answers. This guided conversation makes it easy to create detailed, effective prompts without prompt engineering expertise.
* **Have your agent remember over time.** LangSmith agents have built-in memory for not only their prompt but also the tools that they (and any subagents) have access to. At any point, the agent can update its memory. If you correct the agent, it will now remember that correction so you don't have to prompt it to do so again in the future.

LangSmith Agent Builder is great for internal productivity use cases like email, chat, and Salesforce assistants. For instance, you can build an agent to send you a summary of your schedule with meeting prep every day. You could build an email agent that dynamically creates next steps based on the message, from creating Linear tickets, to drafting responses, or sending a Slack message. And, you can make sure to approve any messages before they get sent.

We'll continue to expand what's possible with Agent Builder based on community feedback — [join the waitlist](http://langchain.com/langsmith-agent-builder-waitlist?ref=blog.langchain.com) to help shape what comes next.

## Under the hood

We’ve incorporated learnings from the last three years building open source agent frameworks LangChain and LangGraph, as well as our early iteration of this product Open Agent Platform, to inform our design decisions.

Today, LangSmith Agent Builder is built on top of our `deepagents` package. Deep Agents gives your agents access to planning capabilities, persistent memory, and the ability to break down complex tasks into manageable subtasks. This means your agent can handle complex, multi-step workflows without you needing to map out every possible scenario; they problem-solve in real time.

For folks already using the LangChain ecosystem of tools, here's a table with some tips on when to use LangSmith Agent Builder vs. our open source frameworks.

## Sign up for the Agent Builder waitlist

If you’re interested in checking out the new experience, [sign up for our private preview waitlist](http://langchain.com/langsmith-agent-builder-waitlist?ref=blog.langchain.com) today! We can’t wait to hear input from the community to continue to improve the experience for everyone.

]]>Two months ago [we wrote about Deep Agents](https://blog.langchain.com/deep-agents/) - a term we coined for agents that are able to do complex, open ended tasks over longer time horizons. We hypothesized that there were four key elements to those agents: a planning tool, access to a filesystem, subagents, and detailed prompts.]]>https://blog.langchain.com/doubling-down-on-deepagents/68fd1e03eab7880001538d59Tue, 28 Oct 2025 17:02:22 GMT

Two months ago [we wrote about Deep Agents](https://blog.langchain.com/deep-agents/) - a term we coined for agents that are able to do complex, open ended tasks over longer time horizons. We hypothesized that there were four key elements to those agents: a planning tool, access to a filesystem, subagents, and detailed prompts.

We launched [`deepagents`](https://github.com/hwchase17/deepagents?ref=blog.langchain.com) as an Python package that had a base of all these elements, so that you would only have to bring your custom tools and a custom prompt and you could build a Deep Agent easily.

We've seen strong interest and adoption, and today we're excited to double down with a 0.2 release. In this blog we want to talk about whats new in 0.2 release compared to the launch, as well as when to use [`deepagents`](https://docs.langchain.com/oss/python/deepagents/overview?ref=blog.langchain.com) (vs [`langchain`](https://docs.langchain.com/oss/python/langchain/overview?ref=blog.langchain.com) or [`langgraph`](https://docs.langchain.com/oss/python/langgraph/overview?ref=blog.langchain.com))

## **Pluggable Backends**

The main new addition in 0.2 release comes in the form of pluggable backends. Previously, the "filesystem" that `deepagents` had access to was a "virtual filesystem". It would use LangGraph state to store files.

In 0.2, we have a new `Backend` abstraction, which allows you to plug in anything as the "filesystem". Built in implementations include:

* LangGraph State
* LangGraph Store (cross thread persistence)
* The actual local filesystem

We've also introduced the idea of a "composite backend". This allows you to have a base backend (eg local filesystem) but then map on top of it other backends at certain subdirectories. An example use case of this is to empower long term memory. You could have a local filesystem as a base backend, but then map all file operations in `/memories/` directory to an s3 backed "virtual filesystem", allowing your agent to add things there and have them persist beyond your computer.

You can write your own backend to create a "virtual filesystem" over any database or any data store you want.

You can also subclass an existing backend and add in guardrails around which files can be written to, format checking for these files, etc.

## Other things in 0.2

We also added a number of other improvements making their way to `deepagents` in the 0.2 release:

* [Large tool result eviction](https://docs.langchain.com/oss/python/deepagents/harness?ref=blog.langchain.com#large-tool-result-eviction): automatically dump large tool results to the filesystem when they exceed a certain token limit.
* [Conversation history summarization](https://docs.langchain.com/oss/python/deepagents/harness?ref=blog.langchain.com#conversation-history-summarization): automatically compress old conversation history when token usage becomes large.
* [Dangling tool call repair](https://docs.langchain.com/oss/python/deepagents/harness?ref=blog.langchain.com#dangling-tool-call-repair): fix message history when tool calls are interrupted or cancelled before execution.

## When to use deepagents vs LangChain, LangGraph

This is now our third open source library we are investing in, but we believe that all three serve different purposes. In order to distinguish these purposes, we will likely refer `deepagents` as an "agent harness", `langchain` as an "agent framework", and `langgraph` as an agent runtime.

LangGraph is great if you want to build things that are combinations of workflows and agents.

LangChain is great if you want to use the core agent loop without anything built in, and built all prompts/tools from scratch.

DeepAgents is great for building more autonomous, long running agents where you want to take advantage of built in things like planning tools, filesystem, etc.

They built on top of each other - `deepagents` is built on top of `langchain`'s agent abstraction, which is turn is built on top of `langgraph`'s agent runtime.

]]>There are few different open source packages we maintain: [LangChain](https://docs.langchain.com/oss/python/langchain/quickstart?ref=blog.langchain.com) and [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview?ref=blog.langchain.com) being the biggest ones, but [DeepAgents](https://docs.langchain.com/oss/python/deepagents/overview?ref=blog.langchain.com) being an increasingly popular one. I’ve started using different terms to describe them: LangChain is an agent framework, LangGraph is an agent runtime, DeepAgents is an [agent harness](https://www.vtrivedy.com/posts/claude-code-sdk-haas-harness-as-a-service?ref=blog.langchain.com). Other folks]]>https://blog.langchain.com/agent-frameworks-runtimes-and-harnesses-oh-my/68fcf4a3eab7880001538d0cSat, 25 Oct 2025 16:14:35 GMT

There are few different open source packages we maintain: [LangChain](https://docs.langchain.com/oss/python/langchain/quickstart?ref=blog.langchain.com) and [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview?ref=blog.langchain.com) being the biggest ones, but [DeepAgents](https://docs.langchain.com/oss/python/deepagents/overview?ref=blog.langchain.com) being an increasingly popular one. I’ve started using different terms to describe them: LangChain is an agent framework, LangGraph is an agent runtime, DeepAgents is an [agent harness](https://www.vtrivedy.com/posts/claude-code-sdk-haas-harness-as-a-service?ref=blog.langchain.com). Other folks are using these terms as well - but I don’t think there is a clear definition of framework vs runtime vs harness. This is my attempt to do try to define things. I will readily admit that there is still murkiness and overlap so I would love any feedback!

## Agent Frameworks (LangChain)

Most packages out there that help build with LLMs I would classify as agent frameworks. The main value add they provide is abstractions. These abstractions represent a mental model of the world. These abstractions should ideally make it easier to get started. They also provide a standard way to build applications which makes it easy for developers to onboard and jump between projects. Complaints against abstractions are that if done poorly they can obfuscate the inner workings of things and not provide the flexibility needed for advanced use cases.

We think of [LangChain](https://docs.langchain.com/oss/python/langchain/overview?ref=blog.langchain.com) as an agent framework. As part of the 1.0 we spent a lot of time thinking about the abstractions - for structured content blocks, for the agent loop, for middleware (which we think adds flexibility to the standard agent loop). Other examples of what I would consider agent frameworks are Vercel’s AI SDK, CrewAI, OpenAI Agents SDK, Google ADK, LlamaIndex, and lot more.

## Agent Runtimes (LangGraph)

When you need to run agents in production, you will want some sort of runtime for agents. This runtime should provide more infrastructure level considerations. The main one that comes to mind is [durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution?ref=blog.langchain.com), but I would also put considerations like support for streaming, [human-in-the-loop support](https://docs.langchain.com/oss/python/langgraph/interrupts?ref=blog.langchain.com), thread level persistence and [cross-thread persistence](https://docs.langchain.com/oss/python/langgraph/add-memory?ref=blog.langchain.com) here.

When we build [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview?ref=blog.langchain.com), we wanted to build in a production ready agent runtime from scratch. You can read more about our thought process behind building LangGraph [here](https://blog.langchain.com/building-langgraph/). The other projects we think are closest to this are Temporal, Inngest, and other durable execution engines.

Agent runtimes are generally lower level than agent frameworks and can power agent frameworks. For example, LangChain 1.0 is built on top of LangGraph to take advantage of the agent runtime it provides.

## Agent Harnesses (DeepAgents)

[DeepAgents](https://docs.langchain.com/oss/python/deepagents/overview?ref=blog.langchain.com) is the newest project we’re working on. It is higher level than agent frameworks - it builds on top of LangChain. It adds in default prompts, opinionated handling for tool calls, tools for planning, has access to a filesystem, and more. It’s more than a framework - it comes with batteries included.

Another way that we’ve used to describe DeepAgents is as a “general purpose version of Claude Code”. To be fair, Claude Code is also trying to be an agent harness - they’ve released things like Claude Agent SDK as a step in that direction. Besides Claude Agent SDK, I don’t think there are many other general purpose agent harnesses out there today. One could argue, however, that ALL the coding CLI's are in a way agent harnesses, and may be general purpose.

## When to use each one

Let’s summarize the differences and talk about when to each one:

Now, I will readily admit that the lines are blurry. LangGraph is probably best described as both a runtime and a framework, for example. “Agent Harness” is a term I’m just starting to see be used more ([I didn’t come up with it](https://www.vtrivedy.com/posts/claude-code-sdk-haas-harness-as-a-service?ref=blog.langchain.com)). I don’t think there is yet a super clear definition of any of these.

Part of the fun of developing in an early space is coming up with the mental models for how to talk about things. We know LangChain is different from LangGraph, and DeepAgents is different from both of them. We think describing them as a framework, runtime, and harness respectively is a helpful distinction - but as always, we would love your feedback!

]]>https://blog.langchain.com/insights-agent-multiturn-evals-langsmith/68f2aa54eab7880001538304Thu, 23 Oct 2025 14:23:55 GMT

**TL;DR:** We’re releasing new capabilities in **LangSmith** to help monitor agents in production. We’re making the concept of “threads” - representing a multi-turn agent interaction - a first-party concept, and we’re adding two new tools to monitor threads: **Insights Agent** for automatically categorizing agent usage patterns, and **Multi-turn Evals** for scoring complete agent conversations.

---

More and more agents are moving to production. As they do so, AI teams find themselves needing better visibility into what’s happening across all user interactions. But, traditional observability and testing that focus on uptime can't tell whether your agent is actually accomplishing users’ goals. And testing your agent before it goes into production (what we call offline evals) only covers what you had in mind to start.

Today, we’re releasing new features to help you understand what’s happening inside your agent *while it’s in production*, so you can prioritize improvements:

* **Insight Agent**: automatically categorizes agent behavior patterns
* **Multi-turn Evals**: helps you evaluate the complete agent trajectory in each conversation

## **Discover patterns in production traces with the Insights Agent**

Today's popular agents produce millions of traces per day—soon to be billions. These traces contain valuable signal about an agent's capabilities and how real users engage with it. If you could review each interaction, you would gain deep insight into how to improve your agent. Manual review is time-consuming and impossible at scale, so how can we automate this insight generation process?

**Insights Agent** is our first step towards helping LangSmith users find signal in their production traces. Insights Agent analyzes traces to discover and surface common usage patterns, agent behaviors, and failure modes.

In agent engineering, you need to iterate rapidly to build reliable experiences. This new feature helps you answer questions like “What are users asking my agent?”, so you can determine where to focus your next set of tests based on real interactions your agent is having.

Once you [trace your data](https://docs.langchain.com/langsmith/observability-quickstart?ref=blog.langchain.com) to LangSmith, you have a few options for how to categorize usage insights.

* **Group by usage patterns:** Cluster based on common usage patterns. This helps you understand how users are actually using your agent. When you put a chatbot in front of people, they can ask it anything. Now you can find out what they are asking.
* **Group by poor interactions:** Cluster based on how your agent is messing up. We will look for signals in each conversation that indicate a negative interaction (user getting frustrated, etc), and then group the root causes. This helps you understand common ways your agent fails, so you can prioritize improvements.
* **Customize configurations:** Insights Agent is highly configurable. You can specify which categories it should group by, filter on existing attributes (like traces from a particular time period or keywords in a chat), define new attributes, and save configs for future use.

Generating insights can take up to 15 minutes depending on how much data the agent is crunching. Once the report is ready, you’ll see traces organized into categories and subcategories based on your initial request. You can click into any category to explore the underlying traces and add them to datasets or annotation queues. You can also see other LangSmith metrics split by category, like latency, number of runs, and any evals you have set up.

Our goal in building this feature was to help you kick off exploration and ideas for improvements as quickly as possible.

**Insights Agent is now generally available** for LangSmith Plus and Enterprise cloud customers. [Sign up for LangSmith](https://smith.langchain.com/?ref=blog.langchain.com) and [check out our docs](https://docs.langchain.com/langsmith/insights?ref=blog.langchain.com) to get started.

## Evaluate end-to-end agent interactions with Multi-turn Evals

Once you have a good sense of the top usage patterns your agent is handling, you can start to drill into how each complete conversation is performing. Until now, that’s been tricky — most other evaluation platforms only focus on individual traces or steps, making it hard to understand whether the overall interaction achieved the user’s goal.

Today, we're launching **Multi-turn Evals** to help you measure whether your agent accomplished the user’s goal across an *entire* interaction. You can do still evaluate at the trace level in LangSmith, but now you can also but also evaluate the whole interaction.

Multi-turn evals are online evaluations that let you measure things like:

* **Semantic intent**: What the user was actually trying to do.
* **Semantic outcomes:** Whether the task was completed (and if not, why).
* **Agent trajectory:** How the interaction unfolded, including tool calls and decisions made along the way.

In LangSmith, we represent these multi-turn exchanges between users and agents as [**threads**](https://docs.langchain.com/langsmith/threads?ref=blog.langchain.com). If you’re already using threads, getting started is simple. Multi-turn evals run automatically once a conversation is complete, and you define the LLM-as-a-judge prompt to guide scoring.

Insights Agent and Multi-turn evals are the first of several thread-level features we’re working on. Stay tuned for thread-level metrics and dashboards, automations to add threads to an annotation queue and datasets, and SDK support so you can programmatically pull and analyze threads.

**Multi-turn evals are live today for all LangSmith users.** [Visit our docs](https://docs.langchain.com/langsmith/online-evaluations?ref=blog.langchain.com#configure-multi-turn-online-evaluators) to get started.

## **Iterate faster with LangSmith**

Our latest LangSmith updates work together to address tough challenges when engineering reliable agents. Now, you can understand what's happening in production (Insights Agent) and measure whether agents accomplish user goals (Multi-turn Evals). These features provide new levels of visibility to help you figure out what’s the best next step to improving your agent.

Ready to ship reliable agents? Get started with [LangSmith](https://smith.langchain.com/?ref=blog.langchain.com) today.

]]>*By Sydney Runkle and the LangChain OSS team* 

We're releasing LangChain 1.0 and LangGraph 1.0 — our first major versions of our open source frameworks! After years of feedback, we've updated `langchain` to focus on the core agent loop, provide flexibility with a new

]]>https://blog.langchain.com/langchain-langgraph-1dot0/68f50b74eab78800015383f5Wed, 22 Oct 2025 14:58:46 GMT

*By Sydney Runkle and the LangChain OSS team*

We're releasing LangChain 1.0 and LangGraph 1.0 — our first major versions of our open source frameworks! After years of feedback, we've updated `langchain` to focus on the core agent loop, provide flexibility with a new concept of middleware, and upgrade model integrations with the latest content types.

These two frameworks serve different purposes:

* **LangChain** is the fastest way to build an AI agent — with a standard tool calling architecture, provider agnostic design, and middleware for customization.
* **LangGraph** is a lower level framework and runtime, useful for highly custom and controllable agents, designed to support production-grade, long running agents

These 1.0 releases mark our commitment to stability for our open source libraries and no breaking changes until 2.0. Alongside these releases, we're launching a completely redesigned [docs site](https://docs.langchain.com/oss/python/langchain/overview?ref=blog.langchain.com).

Learn more about the changes below, and check our [behind-the-scenes](https://youtu.be/r5Z_gYZb4Ns?ref=blog.langchain.com) [conversation](https://youtu.be/r5Z_gYZb4Ns?ref=blog.langchain.com) with our engineers for more commentary.

## LangChain 1.0

LangChain has always offered high-level interfaces for interacting with LLMs and building agents. With standardized model abstractions and prebuilt agent patterns, it helps developers ship AI features fast and build sophisticated applications without vendor lock-in. This is essential in a space where the best model for any given task changes regularly.

**We've been listening.** Over the past three years, we've heard consistent feedback: LangChain's abstractions were sometimes too heavy, the package surface area had grown unwieldy, and developers wanted more control over the agent loop without dropping down to raw LLM calls. Some struggled with customization when their use cases diverged from our prebuilt patterns. We took this feedback seriously. LangChain 1.0 is our response— a thoughtful refinement that preserves what works while fixing what didn't.

> "We rely heavily on the durable runtime that LangGraph provides under the hood to support our agent developments, and the new agent prebuilt and middleware in LangChain 1.0 makes it far more flexible than before. We're excited about 1.0 and are already building with the new features at Rippling." – **Ankur Bhatt, Head of AI at Rippling**

We’re leaning hard into three things for LangChain 1.0:

1. **Our new `create_agent` abstraction:** the fastest way to build an agent with any model provider
   1. Built on the LangGraph runtime, helping to power reliable agents
   2. Prebuilt and user defined middleware enable step by step control and customization
2. **Standard content blocks:** a provider agnostic spec for model outputs.
3. **Streamlined surface area:** we’re trimming down our namespace to focus on what developers use to build agents.

### 1. `create_agent`

The `create_agent` abstraction is built around the core agent loop, making it easy to get started quickly. Here's how the loop works:

**Setup:** select a model and give it some tools and a prompt.

**Execution:**

1. Send a request to the model
2. The model responds with either:
   1. Tool calls → execute the tool and add results to the conversation
   2. Final answer → return the result
3. Repeat from step 1

The new `create_agent` function uses LangGraph under the hood to run this loop. It has a very similar feel to the `create_react_agent` function from `langgraph.prebuilts`, which has been used in production for a year.

Getting started with an agent in `langchain` is easy:

```
from langchain.agents import create_agent weather_agent = create_agent( model="openai:gpt-5", tools=[get_weather], system_prompt="Help the user by fetching the weather in their city.", ) result = agent.invoke({"role": "user", "what's the weather in SF?"}) 
```

Most agent builders are highly restrictive in that they don’t permit customization outside of this core loop. That’s where `create_agent` stands out with our introduction of `middleware`.

**Middleware:**

Middleware defines a set of hooks that allow you to customize behavior in the agent loop, enabling fine grained control at every step an agent takes.

We’re including a few built-in middlewares for common use cases:

* **Human-in-the-loop:** Pause agent execution to let users approve, edit, or reject tool calls before they execute. This is essential for agents that interact with external systems, send communications, or make sensitive transactions.
* **Summarization:** Condense message history when it approaches context limits, keeping recent messages intact while summarizing older context. This prevents token overflow errors and keeps long-running agent sessions performant.
* **PII redaction:** Use pattern matching to identify and redact sensitive information like email addresses, phone numbers, and social security numbers before content is passed to the model. This helps maintain compliance with privacy regulations and prevents accidental exposure of user data.

LangChain also supports **custom** **middleware** that hook into various of points in the agent loop. The following diagram showcases these hooks:

**Structured Output Generation:**

We’ve also improved structured output generation in the agent loop by incorporating it into the main model <–> tools loop. This reduces both latency and cost by eliminating an extra LLM call that used to happen in addition to the main loop.

Developers now have fine grained control over how structured output is generated, either via tool calling or provider-native structured output.

```
from langchain.agents import create_agent from langchain.agents.structured_output import ToolStrategy from pydantic import BaseModel class WeatherReport(BaseModel): temperature: float condition: str agent = create_agent( "openai:gpt-4o-mini", tools=[weather_tool], response_format=ToolStrategy(WeatherReport), prompt="Help the user by fetching the weather in their city.", ) 
```

### Standard Content Blocks

LangChain’s hundreds of provider integrations (OpenAI, Anthropic, etc.) are largely unchanged in 1.0. The interfaces used by these abstractions live in `langchain-core`, which we’re promoting to 1.0 with one key addition: **standardized content blocks**.

Much of LangChain’s value comes from its provider-agnostic interfaces, allowing developers to use a common protocol across multiple providers in a single application. Without standard content blocks, switching models or providers often breaks streams, UIs and frontends, and memory stores. The new `.content_blocks` property on messages provides:

* Consistent content types across providers
* Support for reasoning traces, citations, and tool calls – including server-side tool calls
* Typed interfaces for complex response structures
* Full backward compatibility

This keeps LangChain’s abstractions current with modern LLM capabilities like reasoning, citations, and server side tool execution, while minimizing breaking changes.

### Simplifying the package

LangChain 1.0 reduces package scope to essential abstractions. Legacy functionality moves to `langchain-classic` for backwards compatibility. As the framework has matured, we've learned what patterns matter most. This streamlined package cuts through years of accumulated features to make LangChain simple *and* powerful.

**Key Changes:**

* `create_agent` introduced in LangChain, with `create_react_agent` deprecated in `langgraph.prebuilt`
* Python 3.9 support dropped due to October 2025 EOL, v1.0 requires Python 3.10+
  + Python 3.14 support is coming soon!
* Package surface area reduced to focus on core abstractions with old functionality moved to `langchain-classic`

### Installation

```
# Python uv pip install --upgrade langchain uv pip install langchain-classic # JavaScript npm install @langchain/langchain@latest npm install @langchain/langchain-classic 
```

### Migration

If you're upgrading from a previous version of LangChain, we've created detailed resources to guide you through the changes.

**Release overviews:** [Python](https://docs.langchain.com/oss/python/releases/langchain-v1?ref=blog.langchain.com), [JavaScript](https://docs.langchain.com/oss/javascript/releases/langchain-v1?ref=blog.langchain.com)

**Migration guides**: [Python](https://docs.langchain.com/oss/python/migrate/langchain-v1?ref=blog.langchain.com), [JavaScript](https://docs.langchain.com/oss/javascript/migrate/langchain-v1?ref=blog.langchain.com)

## LangGraph 1.0

AI agents are moving from prototype to production, but core features like persistence, observability, and human-in-the-loop control have remained underserved.

LangGraph 1.0 addresses these gaps with a powerful graph-based execution model, and it provides production-ready features for reliable agentic systems:

* **Durable state** - Your agent's execution state persists automatically, so if your server restarts mid-conversation or a long-running workflow gets interrupted, it picks up exactly where it left off without losing context or forcing users to start over.
* **Built-in persistence** - Save and resume agent workflows at any point without writing custom database logic, enabling use cases like multi-day approval processes or background jobs that run across multiple sessions.
* **Human-in-the-loop patterns** - Pause agent execution for human review, modification, or approval with first-class API support, making it trivial to build systems where humans stay in control of high-stakes decisions.

For a deeper dive into our design philosophy, check out our [blog post](https://blog.langchain.com/building-langgraph/) on building LangGraph from first principles.

This is the first stable major release in the durable agent framework space — a major milestone for production-ready AI systems. After more than a year of iteration and widespread adoption by companies like Uber, LinkedIn, and Klarna, LangGraph is officially v1.

### Breaking Changes & Migration

The only notable change is deprecation of the `langgraph.prebuilt` module, with enhanced functionality moved to `langchain.agents`.

LangGraph 1.0 maintains full backward compatibility.

### Installation

```
# Python uv pip install --upgrade langgraph # JavaScript npm install @langchain/langgraph@latest 
```

## When to Use Each Framework

LangChain lets you build and ship agents fast with high-level abstractions for common patterns, while LangGraph gives you fine-grained control for complex workflows that require customization.

The best part? LangChain agents are built on LangGraph, so you're not locked in. Start with LangChain's high-level APIs and seamlessly drop down to LangGraph when you need more control. Since graphs are composable, you can mix both approaches—using agents created with `create_agent` inside custom LangGraph workflows as your needs evolve.

### Choose LangChain 1.0 for:

* Shipping quickly with standard agent patterns
* Agents that fit the default loop (model → tools → response)
* Middleware-based customization
* Higher-level abstractions over low-level control

### Choose LangGraph 1.0 for:

* Workflows with a mixture of deterministic and agentic components
* Long running business process automation
* Sensitive workflows which necessitate more oversight / human in the loop
* Highly custom or complex workflows
* Applications where latency and / or cost need to be carefully controlled

## Documentation & Resources

We're launching a much improved documentation site at [docs.langchain.com](https://docs.langchain.com/?ref=blog.langchain.com). For the first time, all LangChain and LangGraph docs—across Python and JavaScript—live in one unified site with parallel examples, shared conceptual guides, and consolidated API references.

The new docs feature more intuitive navigation, thoughtful guides, and in depth tutorials for common agent architectures.

## Thank You & Feedback

We hope you love these 1.0 releases. We are incredibly grateful for the community that has pressure tested LangChain and LangGraph over the years to make them what they are today. With 90M monthly downloads and powering production applications at Uber, JP Morgan, Blackrock, Cisco, and more, we have a duty to you all to keep innovating but also be the most dependable framework for building agents.

While this is a major milestone, we are still at the beginning of a major change in software. We want to hear from you: [post on the LangChain Forum](https://forum.langchain.com/t/launch-week-is-here-oss-1-0s-insights-agent-and-no-code-agent-builder/1890?ref=blog.langchain.com) and tell us what you think of our 1.0 release and what you're building.

]]>https://blog.langchain.com/series-b/68f179b9eab7880001538274Mon, 20 Oct 2025 14:36:50 GMT

Today, we’re announcing we’ve raised $125M at a $1.25B valuation to build the **platform for agent engineering.** We’re also releasing new capabilities to accelerate the path to reliable agents, including LangChain and LangGraph 1.0 releases, a new Insights Agent, and a no code agent builder. IVP led the round alongside existing investors Sequoia, Benchmark, and Amplify, as well as new investors CapitalG and Sapphire Ventures.

From AI-native startups to global enterprises, builders trust LangChain's products to engineer reliable agents. Today, we’re grateful to power AI teams at Replit, Clay, Harvey, Rippling, Cloudflare, Workday, Cisco, and more.

The core ideas we had when we made the first commit to the `langchain` package three years ago still hold true today: LLMs will change what applications can do, but the real power comes from turning LLM applications into **agents** with access to data and APIs. Agents will function as complex systems that require new tooling and infrastructure to harness the power of generative AI.

Today’s reality is that agents are easy to prototype but hard to ship to production. That’s because any input or change to an agent can create a host of unknown outcomes. Building reliable agents requires a new approach, one that combines product, engineering, and data science thinking. We call this discipline **agent engineering** - the iterative process of refining non-deterministic LLM systems into reliable experiences.

**We are building the platform for agent engineering.**

We’ve evolved our offerings from the original `langchain` library based on feedback from millions of developers and thousands of customers in our community. We’ve always let you choose the best model for the job, no matter the vendor. Today, we are launching an expanded platform for the complete lifecycle of agent engineering.

The LangChain community can build agents with our **open source frameworks – LangChain and LangGraph**.

* **LangChain** helps you get started building agents quickly with any model provider of your choice. We’ve completely rewritten `langchain` in its 1.0 release to be opinionated, focused, and powered by `langgraph`’s runtime.
* **LangGraph** allows you to control every step of your custom agent with low-level orchestration, memory, and human-in-the-loop support. You can manage long-running tasks with durable execution.

Previously, LangSmith helped you understand and test your agent. Now, **LangSmith** is a comprehensive platform for agent engineering that helps AI teams use live production data for continuous testing and improvement. LangSmith provides:

* **Observability** to see exactly how your agent thinks and acts with detailed tracing and aggregate trend metrics.
* **Evaluation** to test and score agent behavior on production data and offline datasets for continuous improvement.
* **Deployment** (formerly LangGraph Platform) to ship your agent in one click, using scalable infrastructure built for long-running tasks.
* **Agent Builder** (now in private preview) to reduce the barrier to building agents with a no code text-to-agent experience.

Open is part of our ethos, so you can use LangSmith whether you build your agent with our open source frameworks or not. If you do use our stack together, you’ll be able to iterate faster towards reliable agents.

The space evolves rapidly, and so do we. Today we’re announcing:

* [**Major 1.0 releases**](https://docs.langchain.com/oss/python/langchain/overview?ref=blog.langchain.com) **of LangChain and LangGraph** marking stability, with a completely revamped `langchain` package focused on pre-built architectures for common agent patterns, improved model integrations, and no breaking changes until 2.0. Plus, new docs!
* [**Insights Agent**](https://youtu.be/9aX8ETgSp0w?ref=blog.langchain.com), a new agent in LangSmith Observability that automatically categorizes agent behavior patterns.
* [**Agent Builder**](http://langchain.com/langsmith-agent-builder-waitlist?ref=blog.langchain.com) **(in private preview)** to lower the barrier to entry for building agents with a no code text-to-agent builder experience for business users.

The momentum we’ve seen is just the beginning. Today, `langchain` and `langgraph` have a combined 90M monthly downloads, and 35 percent of the Fortune 500 use our services. Monthly trace volume for our commercial LangSmith platform has 12x’d year over year.

We’d love you to be a part of the story. Head on over to the [docs](http://docs.langchain.com/?ref=blog.langchain.com) to see what’s available, stay tuned on [our blog](https://blog.langchain.com/) for deep dives on every launch this week and next, take a [course](http://academy.langchain.com/?ref=blog.langchain.com) to uplevel your skills, and if building the future of agent engineering sounds fun, come join us. [We're hiring.](http://langchain.com/careers?ref=blog.langchain.com)

*Thank you to our new investors, many of whom are already customers or partners, that help make this journey possible – ServiceNow Ventures, Workday Ventures, Cisco Investments, Datadog Ventures, Databricks Ventures, and Frontline.*

]]>*by Harrison Chase*

Almost exactly 3 years ago, I pushed the first lines of code to `langchain` as an open source package. There was no company at the time, and no grand plan for what the project would become.

A month later, ChatGPT launched, and everything for `langchain` changed. It

]]>https://blog.langchain.com/three-years-langchain/68f45df6eab788000153839cMon, 20 Oct 2025 14:34:32 GMT

*by Harrison Chase*

Almost exactly 3 years ago, I pushed the first lines of code to `langchain` as an open source package. There was no company at the time, and no grand plan for what the project would become.

A month later, ChatGPT launched, and everything for `langchain` changed. It quickly gained steam as the default way to build your own LLM-powered apps. Over the past three years the industry has matured past prototyping chatbots toward productionizing agents that do things, and `langchain` has evolved into LangChain, the company.

Our product offerings have expanded, too: from a single Python open source package to a multi-language agent ecosystem consisting of multiple popular open source packages and a separate commercial platform (LangSmith). Our technologies power leading companies' agents like Rippling, Vanta, Cloudflare, Replit, Harvey, and thousands more.

Today, we’re announcing a $125 million funding round at a $1.25 billion valuation to continue that trajectory, expand LangSmith, the platform for agent engineering, and grow our open source contributions. We wrote more about our vision for LangSmith and what else we’re launching today in our [announcement blog](https://blog.langchain.com/series-b).

With such a large funding announcement (and on the eve of the third anniversary of the initial `langchain` launch), I also want to take the time to share my perspective on how agents have evolved over the past three years, how we’ve kept pace, worked to address fair feedback on the original `langchain`, and where the company is headed.

## **Starting as a side project**

`langchain` was launched as a single (800 line long?) python package in fall of 2022 out of my personal github `hwchase17`. It was a side project. I was inspired by going to meetups and running into a few folks on the bleeding edge, building some experimental stuff with language models. I was instantly fascinated by the technology but cannot claim to have had any idea how big LLMs would become. I saw a few common patterns in terms of how people were building and put those patterns into `langchain`.

After the initial launch, I kept on iterating on it, adding mainly two things: (1) more integrations to various LLMs, vector DBs, etc; (2) more high-level “templates” for getting started with RAG, SQL question answering, extraction, etc in 5 lines of code. A lot of `langchain` in the early days was experimenting with prompting techniques, and we were figuring things out alongside everyone else building in the space.

In addition to needing lots of integrations, it was clear from the beginning that there would be lots of options for LLMs. Especially in a dynamic industry, helping users pick a model and later change that decision was incredibly important. Model neutrality still remains one the main benefits of our products.

## **Forming a company**

As the space (and `langchain`) exploded, I started working more closely with Ankush, my cofounder (and a much better engineer than me). We started to get the inklings of what would drive us to start a company and that early inspiration is still what we're focused on today:

LLMs are this great, transformational new technology. They are even more powerful when connected to external data and APIs. We call these systems agents. And it turns out building *reliable* agents is quite hard! When there is so much promise, but it’s difficult to realize the vision, there's a massive opportunity to help. We were (and still are) determined to build the best tools to help others build reliable agents. We know what some of the needed tools are, and we don’t yet know what others will be. Our goal is to figure out what the agents of the future look like, and then build tools to help make them real.

We started the company in February 2023 knowing that `langchain` was just the first tool we would build.

## **Launching LangSmith**

The biggest problem we saw facing developers was that these LLM systems had quality problems. LLM calls kept on messing up, largely because they had the wrong context. In order to make them more reliable, you needed observability into the context going into the LLMs, and a way to test that once you modified that context it actually led to improvements.

LangSmith was our answer to this problem – observability and evals for LLM systems, and we went live with a beta in summer of 2023. Notably, we made LangSmith completely separate from `langchain`. We recognized that the space was very early and that a tool like LangSmith was much needed, so we committed to building LangSmith to be best-in-class, regardless of the framework (or lack of framework) that a developer used. LangSmith is neutral to the LLM and neutral to the underlying framework, adding to our open and composable philosophy of tooling.

## **Launching LangGraph**

Around the summer of 2023, we started to get a lot of negative feedback about `langchain`. Some problems we could fix: like preventing breaking changes, making hidden prompts explicit, package bloat, dependency conflicts, outdated documentation. But one piece of feedback was harder to address – people wanted more control. While `langchain` was the fastest place to get started, we traded power for ease of use. The same high level interfaces in `langchain` that made it easy to get started were now getting in the way when people tried to customize them to go to production.

We started developing LangGraph that summer, and launched it in early 2024. There were two main pillars we focused on:

1. Controllability: no hidden prompts, no hidden context engineering. You had full control over your system - whether it was a workflow or agent or anything in between.
2. Runtime: we took everything we learned about what was needed for a production runtime (streaming, statefulness, human-in-the-loop, durable execution) and built it into LangGraph in a first-party way.

LangGraph was inspired by the limitations of the initial `langchain`. The production validation from companies like LinkedIn, Uber, J.P. Morgan, and BlackRock gave us confidence we were building in the right direction.

## **Revisiting LangChain**

A few months ago, we decided to revisit `langchain` from the ground up. While we were seeing tremendous adoption of LangGraph, it did have a higher learning curve, and the incredible, persistent enthusiasm for `langchain` encouraged us that there was still a need in the industry that `langchain` was fulfilling. We had three goals for reimagined `langchain`:

1. Make it as easy as possible to get started building agents
2. Allow for more customization than we had previously
3. Give it a production-ready runtime

We knew this approach would require massive breaking changes to `langchain`. We decided it would be best to do this in 1.0 release. We accomplished our goals by:

1. Focusing on the core tool-calling loop that is now synonymous with "agents".
2. Adding in a new concept of middleware, which is uniquely designed to give developers control over the “context engineering” lifecycle exactly where they need it.
3. Building upon LangGraph, a runtime that supported streaming, durable execution, human-in-the loop, and more.

We believe `langchain` 1.0, released today, solves the goals we had for it, and importantly gives the community of over a million developers a clearer view of what we stand behind. The best patterns for an agent architecture are far better understood today than when we started the project, and 1.0 is far more curated than anything you’ve seen from our team before. Plus, we shipped a [new centralized docs site](https://docs.langchain.com/?ref=blog.langchain.com) which has been a long time coming! We hear you.

For the millions of developers (80 million monthly downloads!) using `langchain` today, we’re also keeping around `langchain` 0.x as `langchain-classic`, and are committed to supporting it for an extended period of time.

## **Evolving LangSmith into the Agent Engineering Platform**

The bread and butter of LangSmith has been observability and evaluations, but that’s not the only tooling needed to build reliable agents. We started experimenting with bringing more functionality into the platform with “LangGraph Platform,” which was focused on deployments. As we look to the future, we see a number of new ways that we can help customers, and we want to make LangSmith a single place where you can get most of your tooling to build reliable agents. Today we’re bringing deployments into LangSmith, and are setting LangSmith up to be the comprehensive agent engineering platform. We will add other product lines in LangSmith in the future and aim to make each new product independent of the existing ones but well integrated into the platform.

## **Agents of the future**

Our goal is to figure out what the agents of the future look like and build tools to facilitate that. We know what some of those pieces are (an agent runtime like LangGraph, observability, evals). We have some hunches about what the other pieces are that we are actively exploring. We also fully expect that there will be other components that, at this moment in time, we can't imagine what they'll look like – which makes this journey incredibly fun and rewarding for what we expect to be a long time.

If you have feedback on how our tools can adapt to better build the agents of the future, [let me know on X](https://x.com/hwchase17?ref=blog.langchain.com). I appreciate every piece of feedback because we know our products will have to evolve.

If you need a partner when building the agents of the future - [get in touch](https://www.langchain.com/contact-sales?ref=blog.langchain.com). We are lucky enough to work with wonderful companies like Vanta, Rippling, Replit, Clay, Cisco, Workday, and many more, and would love to work with more teams pushing what's possible.

If you want to help us on our mission in building the agents of the future - [we’re hiring](http://langchain.com/careers?ref=blog.langchain.com) for basically all roles.

]]>https://blog.langchain.com/agent-authorization-explainer/68e9a604eab7880001537cfbMon, 13 Oct 2025 21:12:15 GMT

Lately, every company has been rushing to build agents. And unlike the AI applications of years before, agents aren’t limited to chat. Agents are notable because they can take action; they can fetch files, send messages, call tools and update records — which makes the stakes higher and warrants a more thoughtful approach to securing them.

### Access Control Primer

To access sensitive data and use tools, agents need to be authenticated and authorized. While often used interchangeably, the two terms have distinct meanings:

* Authentication (AuthN): verifies *who* you are. When accessing data, your agent needs to have a distinct identity from all the other users or applications that also want access.
* Authorization (AuthZ): determines *what you can do*. Your agent should have limits on what data it can access or what actions it can take.

Authentication and authorization (collectively referred to as “auth”) are relevant to all types of applications, not just agents. To that end, there are existing frameworks like OAuth 2.0 to facilitate AuthN/Z. Many identity providers today have built extensive services on top of OAuth 2.0 to allow developers to implement access control in their applications. However, compared to the applications served by existing solutions, agents have some unique attributes that make it useful to create additional constructs for access.

### What Makes Agents Different?

The biggest distinctions between agents and traditional applications are:

1. Compared to most applications, agents will need to access an extremely large number of services and tools.
2. Agents are dynamic, and have significantly more fluid access needs.
3. Agents are more complex to audit than traditional applications.

Each of these new attributes comes with new considerations for agent authentication and authorization. We break them down below.

**1. Agents will need to access an extremely large number of services and tools:**

* Common constructs will be useful to standardize tool access from agents
* A standardized interface abstracting common OAuth 2.0 flows will simplify giving agents access to the data they need

**2. Agents having significantly more fluid access needs:**

* Traditional applications have structured access needs, where the scope of the application’s behavior is well defined. This means access controls can afford to be simpler, mainly checking if a user is allowed to consent to whatever permissions the app is requesting.
* Agent behavior is nondeterministic, not well-defined. The correct level of access may be heavily context dependent, which can make it useful to set rules like “Agent A is never allowed to request consent for permission A” or “Agent B must request consent each time permission C is needed”

**3. Agents are more complex to audit than traditional applications:**

* Due to the number of services agents can access, audit logs may be spread across many providers
* Each call to an agent may involve many services and actions, which makes individual access trajectories more difficult to interpret
* Agents benefit more from a centralized location to track audit events and analyze access patterns

Taken together, these considerations form the shape of a centralized framework to manage agent authentication and authorization. It should consolidate auditable events and allow flexible rule configurations to match the dynamic access needs of agents. In essence, an auth server for agents.

### An Agent Auth Server

What might such an auth server look like? We could draw inspiration from existing paradigms for human access, such as Role Based Access Control (RBAC) or Just in Time (JIT) access.

RBAC is an access control mechanism that grants humans access to resources based on their role. Instead of tying permissions to a particular user’s identity, the permission is tied to the role the user holds (i.e. administrator). Roles can be granted and removed from users to dynamically adjust their access based on changing conditions, which can help fulfill the fluid access needs of agents.

JIT access is a security principle where users are granted temporary, privileged access to systems or resources only when needed, for a limited time. For agents, JIT access could be an effective method to allow agents to do powerful things while minimizing potential security risks.

By consolidating agent auth through a single service, access to tools and resources can be centralized and standardized. The server could consolidate disparate audit events, and organize them for easier review.

While some of these components are still being built, that doesn’t mean you, as a developer, cannot build authentication and authorization into your agents today. The foundational frameworks of auth, like OAuth 2.0, can still be used to secure your individual agentic applications.

### Agent AuthN and AuthZ Today

Though agents bring new challenges, at a high level they share many similarities with traditional applications. At their core, they’re pieces of software that want access to resources. Most modern applications today use the OAuth 2.0 framework for authorization and the OIDC framework built on top of OAuth 2.0 for authentication. Agents can also effectively use these standards.

However, OAuth 2.0 covers a lot of ground, and not all flows will be relevant for the agents you build. Access patterns can be broadly broken into two categories: Delegated Access and Direct Access

| Delegated Access | Direct Access |
| --- | --- |
| Definition | The agent needs to access a resource on behalf of a user | The agent needs to access a resource without user involvement |
| Agent Types | Useful for agents dedicated to fulfilling human requests OR agents reliant on human oversight | Useful for ambient agents, which can trigger off events, or agents conducting autonomous processes |
| Benefits | Delegated access allows you to limit your agent’s permissions to what the human is allowed to do. It also lets you associate agent actions with human approvers | Direct Access access allows your agents to operate independently of humans, and identify when agents are conducting fully autonomous flows |
| Examples | An email assistant needing access to your emails would need you to delegate access to read your emails | A security agent triaging large amounts of incidents might need access to system logs independent of a human |

In practice, most agents will have some tasks where they need delegated access, and some where they want direct access. Most of these access scenarios can be covered by a few particular OAuth flows, which we’ll break down in this next section.

### Delegated Access

Let’s list some common requirements for tasks in which agents need delegated access.

1. The agent needs to fulfill human requests, and is available to users as a service
2. Users should not be able to view the requests of other users without explicit permission. This means you need to…
   1. Identify who the user accessing your agent is — meaning you need to authenticate users
   2. Control whether users have access to view a particular request to your agent — meaning you need to authorize your users
3. The Agent needs to access data across several platforms (Microsoft, Slack, Jira, Google, Datadog, etc.) to do useful work. This means…
   1. Your agent needs to obtain access to other services — meaning your agent needs authorization from these other services
   2. While handling user requests, your agent should be limited to what the user is allowed to do. If the user can’t view a top secret Microsoft document, the agent shouldn’t use that document when answering their question.

The most common OAuth 2.0 flow used to fulfill Requirement 2 is [**Auth Code Flow**](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow?ref=blog.langchain.com)**.**

The OAuth 2.0 flow used to fulfill Requirement 3 is the [**OBO (On-Behalf-Of) Token Flow.**](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-on-behalf-of-flow?ref=blog.langchain.com)

**In most delegated access scenarios, Auth Code Flow and OBO Token Flow are all you need for your agent.**

### Direct Access

We can take the same approach for Direct access, and list some requirements:

1. Your agent needs to access one or more services without human involvement. This means…
   1. Other services need to be able to identify your agent and distinguish it from other applications — meaning your agent needs to be authenticated to these services
   2. Your agent needs access to other services — these services need to authorize your agent to control what it has access to

**The OAuth flow used to accomplish the Direct Access scenario above is the** [**Client Credentials Flow**](https://auth0.com/docs/get-started/authentication-and-authorization-flow/client-credentials-flow?ref=blog.langchain.com)

* Client Credentials flow requires that your agent is running in a private environment where its source code is not exposed to third parties - so no mobile apps or Single Page Apps (SPAs)
* In production, it’s good practice to use a credential management mechanism to avoid long-lived credentials (which are vulnerable to compromise).

To recap, if you’re looking to set up access for your agent, there’s likely 3 flows you’ll need:

| Type of Access | OAuth 2.0 Flows |
| --- | --- |
| Delegated Access | 1. Auth Code Flow 2. OBO Token Flow |
| Direct Access | 3. Client Credentials Flow |

### Conclusion

As agents become more capable, more autonomous, and more useful, the need for a good authentication and authorization story increases.

Part of that story is a continuation of what’s already been built: the existing standards of OAuth 2.0 and OIDC. If you need to implement auth for your agent, you’ll likely find yourself implementing Auth Code Flow, OBO Token Flow, or Client Credentials Flow.

However, agents *do* bring new challenges to the table. Agents will routinely span dozens of services, request access in fluid ways, and trigger chains of actions that are harder to audit. We believe there’ll be a need for new tooling to centralize control and standardize agent access.

We’ve written about [agent access control](https://blog.arcade.dev/agent-authorization-langgraph-guide?ref=blog.langchain.com) before with our friends at [Arcade](https://www.arcade.dev/?ref=blog.langchain.com), in case you’re interested in diving deeper.

]]>*By Harrison Chase*

One of the most common requests we’ve gotten from day zero of LangChain has been a visual workflow builder. We never pursued it and instead let others (LangFlow, Flowise, n8n) build on top of us. With OpenAI launching a [workflow builder](https://openai.com/index/introducing-agentkit/?ref=blog.langchain.com) at Dev Day yesterday,

]]>https://blog.langchain.com/not-another-workflow-builder/68e51ba99024b70001afe265Tue, 07 Oct 2025 16:38:16 GMT

*By Harrison Chase*

One of the most common requests we’ve gotten from day zero of LangChain has been a visual workflow builder. We never pursued it and instead let others (LangFlow, Flowise, n8n) build on top of us. With OpenAI launching a [workflow builder](https://openai.com/index/introducing-agentkit/?ref=blog.langchain.com) at Dev Day yesterday, I thought it would be interesting to write about why we haven’t built one to date, and what different (but related) directions we are more interested in.

## The problem statement

First of all, it’s worth aligning on the problem statement these no-code workflow builders solve. The main motivation is to allow non-technical users to build agents. There’s two main reasons people are interested in this:

1. Many companies are more resource constrained on engineering talent than others
2. Non-technical users are the ones who know what agents to build / what they should do

We occasionally see other motivations, like allowing technical users to quickly prototype agents that will get ported into code later. But for the purpose of this blog let’s assume that the motivation is to enable everyone in an organization to build their own apps and widgets without support from engineering.

## Workflows vs agents

Two words which I’ve used intentionally above are “workflows” and “agents”. We’ve written about this before - actually in a blog post [arguing for workflows](https://blog.langchain.com/how-to-think-about-agent-frameworks/) (ironically, in response to an OpenAI article arguing against workflows).

The developer community has largely settled on the [following definition of an agent](https://simonwillison.net/2025/Sep/18/agents/?ref=blog.langchain.com):

💡

An LLM agent runs tools in a loop to achieve a goal.

Workflows give you more predictability at the expense of autonomy, while agents give you more autonomy at the expense of predictability. **Notably, when building agentic systems we are in pursuit of *reliably good* outcomes, which neither predictability or autonomy alone guarantee.**

Workflows are often complicated - branching logic, parallel edges, many different paths. This complexity is represented in the “graph” of the workflow, which is represented in some DSL.

Agents can also contain complicated logic, but by contrast all that logic is abstracted away into natural language, which goes into the prompt. So the overall structure of an agent is simple (just a prompt + tools), though that “prompt” can often times be pretty complex.

OpenAI’s AgentKit - and n8n, Flowise, LangFlow - are all visual **workflow** builders - not *agent* builders.

## The issue with visual workflow builders

So, with all that context, what is the problem with workflow builders:

**1.Visual workflow builders are not “low” barrier to entry.**

Despite being built for a mass audience, it is still not easy for the average non-technical user to use them.

**2.Complex tasks quickly get too complicated to manage in a visual builder.**

As soon as they pass a certain level of complexity (which happens pretty quickly) you end up with a mess of nodes and edges that you need to manage in the UI.

## Other alternatives

The goal is to create LLM powered systems (whether workflows or agents) that are *reliably good*. There are different types of problems that people may want to solve with LLM powered systems - ranging anywhere from low complexity to high complexity. The best alternative may depend on the level of complexity.

**High Complexity: Workflows in Code**

For high complexity problems, we’ve found that in order to achieve a certain level of reliability the systems are not just pure agents, but rather involve some aspect of a workflow. These high complexity problems often require complex workflows. In these scenarios, where you want lots of branching, parallelism and modularity, code is the best option ([LangGraph](https://github.com/langchain-ai/langgraph?ref=blog.langchain.com) is designed for this).

Traditionally this would mean that these types of problems just aren’t actually solvable by a non-technical builder. As the cost of code generation goes to zero, however, we expect that more and builders will find themselves capable of building these solutions.

**Low Complexity: No-Code Agents**

For lower complexity use cases, I would assert that simple agents (prompt + tools) are getting reliably good enough to solve these use cases. Building these agents in a no-code way should be simpler than building a workflow in a no-code way.

As models get better and better, I would expect the ceiling of the type of problems these agents can solve to get higher and higher.

## The squeeze

The issue with no code workflow builders are that I think they are getting squeezed from both directions.

| Complexity Level | Best Solution |
| --- | --- |
| Low | No-Code Agent |
| Medium | No-Code Workflow |
| High | Workflow in Code |

I think agents (prompt + tools) should be strictly easier to create in a no-code way than workflows. I expect models, agent harnesses, and our interfaces for creating, modifying, and *teaching* these agents to get better. This means that these agents will be *reliably good* at more and more tasks.

In the other direction, visual workflow builders become unmanageable for a certain level of complexity. The only real alternative to that is code. Writing code has historically been limited to a small set of people, with the barrier to entry being pretty high. As models get better and better at code generation, and the cost of code generation goes to zero, I expect the decision to go to code becomes easier and easier.

## The interesting problems

To be very clear - there are companies that have done a fantastic job at democratizing LLM powered workflow builders (n8n, Flowise, LangFlow, Gumloop, etc). Many of them have found product-market fit - they solve a real problem that exists today and empower non-technical users to build fantastic things.

I do not think the world needs yet another workflow builder. Rather, I think the interesting problems to solve next are:

* How can we make it easier to create *reliably good* agents in a no-code way. These should be agents! Not low code workflows.
* How can we make code generation models better at writing LLM powered workflows/agents

]]>Authored by: [Aliyan Ishfaq](https://www.linkedin.com/in/aliyan-ishfaq/?ref=blog.langchain.com)

Coding agents are great at writing code that uses popular libraries on which LLMs have been heavily trained on. But point them to a custom library, a new version of a library, an internal API, or a niche framework – and they’re not so

]]>https://blog.langchain.com/how-to-turn-claude-code-into-a-domain-specific-coding-agent/68bf37c0c3c55900012a78cdThu, 11 Sep 2025 16:54:37 GMT

Authored by: [Aliyan Ishfaq](https://www.linkedin.com/in/aliyan-ishfaq/?ref=blog.langchain.com)

Coding agents are great at writing code that uses popular libraries on which LLMs have been heavily trained on. But point them to a custom library, a new version of a library, an internal API, or a niche framework – and they’re not so great. That’s a problem for teams working with domain specific libraries or enterprise code.

As developers of libraries (LangGraph, LangChain) we are really interested in how to get these coding agents to be really good at writing LangGraph and LangChain code. We tried a bunch of context engineering techniques. Some worked, some didn’t. In this blog post we will share the experiments we ran and learnings we had. Our biggest takeaway:

**High quality, condensed information combined with tools to access more details as needed produced the best results**

Giving the agent raw documentation access didn’t improve performance as much as we hoped. In fact, the context window filled up faster. A concise, structured guide in the form of `Claude.md` always outperformed simply wiring in documentation tools. The best results came from combining the two, where the agent has some base knowledge (via `Claude.md`) but can also access specific parts of the docs if it needs more info.

In this post, we’ll share:

* The different Claude Code configurations we tested
* The evaluation framework we used to to assess the generated code (a template you can reuse for your own libraries)
* Results and key takeaways

## **Claude Code Setups**

We tested four different configurations, using Claude 4 Sonnet as the model for consistency:

**Claude Vanilla:** Out-of-the-box Claude Code with no modifications.

**Claude + MCP:** Claude Code connected to our [MCPDoc](https://github.com/langchain-ai/mcpdoc?ref=blog.langchain.com) server for documentation access.

**Claude + Claude.md:** Claude Code with a detailed `Claude.md` file containing LangGraph-specific guidance.

**Claude + MCP + Claude.md:** Claude with access to detailed `Claude.md` and MCPDoc server.

### MCP tool for documentation

We built the MCPDoc server because we wanted to provide coding agents with access to any library’s documentation. It is an open-source MCP server that exposes two tools: `list_doc_sources` and `fetch_docs`. The first shares the URLs of available `llms.txt` files, and the latter reads a specific `llms.txt` file. In our setup, we provided access to LangGraph and LangChain Python and JavaScript documentation. You can easily adapt this for your use case by passing in the URLs of your library's `llms.txt` files in the MCP config.

### Claude.md

For `Claude.md`, we created a LangGraph library guide. It included detailed instructions for common LangGraph project structure requirements, like mandatory codebase searching before creating files, proper export patterns, and deployment best practices. It included sample code for primitives required for building both single and multi-agent systems, things like `create_react_agent`, supervisor patterns, and swarm patterns for dynamic handoffs. There were certain implementations that LLMs were struggling with like streaming and human-in-the-loop for user-facing agents. We added extensive guidelines for these.

We found it particularly valuable to include comprehensive sections on common pitfalls and anti-patterns. This covered common mistakes like incorrect `interrupt()` usage, wrong state update patterns, type assumption errors, and overly complex implementations. These were mistakes we frequently saw LLMs make, either due to deprecated libraries or confusion with patterns from other frameworks.

We also included LangGraph-specific coding standards like structured output validation, proper message handling, and other framework integration debugging patterns. Since Claude has access to web tools, we added specific documentation URLs at the end of each section for further reference and navigation guidelines.

The way this file differs from `llms.txt` is that the former is a plain text file of all the content of a page with URLs while this includes condensed information that is most important when starting from scratch. As we'll see in the results, when `llms.txt` is passed alone, it is not most effective as it sometimes confuses LLMs with more context and no instructions on how to navigate and discern what's important.

Before going into how our Claude Code configurations performed across different tasks, we want to share our evaluation framework that we used to determine task fulfillment and code quality.

## **Evaluations**

Our goal was to measure what contributes most to code quality, not just functionality. Popular metrics like Pass@k capture functionality and not best practices, which varies by context.

We built a task-specific evaluation harness that checks both technical requirements and subjective aspects such as code quality, design choices, and adherence to preferred methods.

We define three categories for our evaluation:

**Smoke Tests**

These verify basic functionality. Tests confirm that the code compiles, exposes the `.invoke()` method, handles expected input states, and returns expected output structures like `AIMessage` objects with required state properties.

We calculate scores using weighted summation:

Score = Σᵢ wᵢ × cᵢ

 where *wi* is the weight of of test *i* and *ci* is the binary result of a test.

**Task Requirement Tests**

These verify task specific functionality. Tests include validation of deployment configuration files, verification of HTTP requests to external APIs such as web search or LLM providers, and unit tests specific to each coding task. Scoring is done through weighted summation of each test result, same as smoke tests.

**Code Quality & Implementation Evaluation**

For this category, we use LLM-as-a-Judge to capture what binary tests miss. Implementations that follow better approaches should score higher than those that simply compile and run. Code quality, design choices, and use of LangGraph abstractions all require nuanced evaluation.

We reviewed expert written code for each task and built task specific rubrics. Using Claude Sonnet 4 (`claude-sonnet-4-20250514`) at temperature 0, we evaluated generated code against these rubrics, using expert-written code as the reference and human annotations to log compilation and runtime errors.

Our rubric had two types of criteria:

**Objective Checks:** These are binary facts about the code (e.g. presence of specific nodes, correct graph structure, module separation, absence of test files). The LLM judge returned a boolean response for each check and we used weighted summation, same as smoke tests, to get a score for objective checks.

**Subjective Assessment:** This is qualitative evaluation of the code using expert-written code as reference and human annotation for passing in logs of compilation and runtime errors. LLM judge identified issues and categorized them by severity (critical, major, minor) across two dimensions: correctness violations and quality concerns.

We use penalty-based scoring for this:

Score = Scoreₘₐₓ - Σₛ (nₛ × pₛ)

where Score*max* is the maximum possible score, *ns* is the number of violations at severity *s* and *ps* is the penalty weight for that severity.

The overall score, combining both objective and subjective results, is given as:

Score = Σᵢ wᵢ × cᵢ + Σₛ (Scoreₘₐₓ,ₛ - Σₛ (nₛ × pₛ))

where the first term represents objective checks and the second term represents assessments across all subjective categories.

We ran each Claude Code configuration three times per task to account for variance. For consistency, all scores are reported as percentages of total possible points and then averaged across tasks.

You can replicate this approach for your own libraries using the [LangSmith](https://www.langchain.com/langsmith?ref=blog.langchain.com) platform to compare coding agent configurations.

## **Results**

We average scores across three different LangGraph tasks to compare Claude Code configurations. The chart below shows overall scores:

The most interesting finding for us is that Claude + `Claude.md` outperformed Claude + MCP, even though `Claude.md` only included a subset of what the MCP server could provide. Traces explained why: Claude didn’t invoke MCP tools as much as we’d expected. Even when a task required following two or three linked pages, it typically called MCP once and stopped at the main page,  which only gave surface-level descriptions, not the details needed.

By contrast, Claude + `Claude.md` + MCP used the docs more effectively. We observed in traces that it called MCP tools more frequently and even triggered web search tool when required. This behavior was driven by `Claude.md` that included reference URLs at the end of each section to look for further information.

This doesn’t mean MCP tools didn’t help on their own. They improved scores by ~10 percentage points, mainly by grounding the agent in basic syntax and concepts. But for task completion and code quality, `Claude.md` was more important. The guide included pitfalls to avoid and principles to follow, which helped Claude Code think better and explore different parts of the library rather than stopping at high-level descriptions.

These results point to a few broader lessons for anyone configuring coding agents.

## **Key Takeaways**

The results leave us with a few takeaways. If you’re thinking about customizing coding agents for your own libraries, the following can be useful:

**Context Overload:** Dumping large `llms.txt` files from documentation can crowd the context window. This can lead to poor performance and higher cost. Our MCP server has a naive implementation of fetching page contents completely. Even invoking it once flagged Claude Code warnings of context window filling up. If your documentation is extensive enough that you need tooling to retrieve specific docs, it’s worth building smarter retrieval tooling that pulls only the relevant snippets.

**Claude.md has the highest payoff:** It’s easier to set up than an MCP server or specific tooling and cheaper to run. On task #2, Claude + `Claude.md` was ~2.5x cheaper than Claude MCP and Claude + `Claude.md` + MCP. It’s cheaper than Claude MCP and performs better. This is a great starting point when thinking of customizing Claude Code and may just be good enough for some use cases.

**Write good instructions**.  A `Claude.md` (or `Agents.md`) should highlight core concepts, unique functionality, and common primitives in your library. Review failed runs manually to find recurring pitfalls and add guidance for them. For us, that meant covering async tasks in LangGraph with Streamlit, where agents often failed on `asyncio` integration. We also added debugging steps for spinning up dev servers, which fixed import errors and let Claude Code send requests to the server to verify outputs. Popular code-gen tools often use long system prompts (7–10k tokens). Putting effort into instructions pays off pretty well.

**Claude +** [**Claude.md**](http://claude.md/?ref=blog.langchain.com) **+ MCP wins**: While `Claude.md` provides the most mileage per token, the strongest results came from pairing it with an MCP server that allows it to read documentation in detail. The guide provided orientation with concepts and the docs helped go in-depth. Together, they can produce best results on domain specific libraries.

In the Appendix, we include per-task results and category-level graphs for readers who want to dig into per task performance.

## **Appendix**

**Task #1: Text-to-SQL Agent**

We asked each configuration to build a LangGraph-based text-to-SQL agent that could generate SQL query from natural language, execute it against a database, and return a natural language response. This task required fetching the Chinook SQLite database from a remote URL and setting up an in-memory database. You can read the prompt that we passed to Claude Code instances [here](https://github.com/langchain-ai/claude-code-evals/blob/main/task_1/input_prompt.py?ref=blog.langchain.com).

For this task, our smoke tests verified basic LangGraph functionality. Task requirements checked database setup; SQL query handling for simple queries, join queries, date range queries; and LLM-as-a-Judge evaluated code design choices such as remote URL fetching, separate nodes for SQL generation, execution, and response. The LLM-as-a-Judge prompt is available [here](https://github.com/langchain-ai/claude-code-evals/blob/main/task_1/llm_as_a_judge.py?ref=blog.langchain.com).

The results show performance difference across Claude Code configurations and categories:

Poor implementations typically struggled with connecting in-memory database across threads, downloaded and hardcoded schemas in LLM prompts instead of using remote URLs with runtime schema reading, and failed to properly parse LLM output for SQL execution (breaking when LLM would generate slightly different formatted results).

**Task #2: Company Researcher**

For this task, we asked each Claude configuration to build a multi-node LangGraph agent that researches companies using web search through [Tavily API](https://www.tavily.com/?ref=blog.langchain.com). The agent needed to handle structured data collection, implement parallel search execution, and add a reflection step that ensures all requested information is gathered. You can read the prompt [here](https://github.com/langchain-ai/claude-code-evals/blob/main/task_2/input_prompt.py?ref=blog.langchain.com).

Our tests verified basic functionality, Tavily API integration, and presence of all requested properties in the structured object class. [LLM-as-a-Judge](https://github.com/langchain-ai/claude-code-evals/blob/main/task_2/llm_as_a_judge.py?ref=blog.langchain.com) checked for implementation of features like reflection logic, minimum search query limits, and parallel web search execution.

 The following are the results for this task:

Most implementation failures were related to structuring information in an object in state and reflection step. Poor implementations either didn’t have functional reflection nodes or failed to trigger additional searches.

**Task #3: Categories of Memories**

This was an editing task where we provided each Claude Code configuration with an existing memory agent as base code. We asked them to extend the memory storage method to categorize memory by type (personal, professional, other) in addition to user ID, implement selective memory retrieval based on message category instead of just user ID, and add human in the loop confirmation step before saving memories. We deliberately added syntax errors as well. The full prompt is available [here](https://github.com/langchain-ai/claude-code-evals/blob/main/task_3/input_prompt.py?ref=blog.langchain.com).

With tests we verified that implementations correctly added the interrupt functionality before memory storage, implemented category-wise storage and retrieval, used three specific categories (personal, professional, other), and maintained functional interrupt logic that saves memories only when users accept. [LLM-as-a-Judge](https://github.com/langchain-ai/claude-code-evals/blob/main/task_3/llm_as_a_judge.py?ref=blog.langchain.com) evaluated whether implementations used LLM-based categorization rather than brittle keyword matching and unnecessary files.

For an editing task, we see following results:

Most implementations struggled with correctly implementing interrupt functionality. Wrong implementations either added simple `input()` calls to get terminal input or overcomplicated the solution by creating separate nodes instead of using a few lines of proper interrupt logic. Poor implementations also relied on keyword matching for categorization instead of LLM-based classification, and almost all failed to catch the deliberate syntax errors we included.

]]>https://blog.langchain.com/customers-monte-carlo/68c1959f2cb313000119b048Thu, 11 Sep 2025 04:30:49 GMT

A high-level overview of Monte Carlo’s [Troubleshooting Agent](https://www.montecarlodata.com/platform/observability-agents?ref=blog.langchain.com) architecture

[**Monte Carlo**](https://www.montecarlodata.com/?ref=blog.langchain.com) is a leading data + AI observability platform for enterprises, helping organizations monitor data and AI reliability issues, and trace them back to their root causes. After years of building sophisticated data monitoring and troubleshooting tools, Monte Carlo realized they had been unknowingly building the foundation for what would become their flagship AI agent— a system that can launch hundreds of sub-agents to investigate data issues and accelerate root cause analysis in a compelling, actionable way.

## **Automating data pipeline troubleshooting at enterprise scale**

Data engineers at enterprise organizations spend countless hours manually troubleshooting data alerts—investigating failed jobs, tracking down code changes, and determining whether issues require immediate resolution or can be deprioritized. This manual process forces engineers to follow single investigation paths sequentially, often missing parallel issues or taking too long to identify root causes in complex, interconnected data systems.

Monte Carlo's customers are primarily large enterprises where data drives significant revenue. For these customers, **data that remains incorrect or unavailable can affect millions of dollars of business**. While Monte Carlo had built comprehensive troubleshooting tools, they identified an opportunity to further reduce this “data downtime:” have AI agents process and reason through hundreds of hypotheses concurrently to accelerate data + AI team’s ability to quickly spot and fix the root cause behind specific data quality incidents.

## **Troubleshooting multi-paths with LangGraph**

Monte Carlo chose **LangGraph** as the foundation for their AI Troubleshooting Agent because their investigation process naturally mapped to a graph-based decision-making flow. When an alert is triggered, their system follows a structured troubleshooting methodology that mirrors how experienced data engineers approach problems, but at scale.

Alert → Check Code Changes → Analyze Timeline → Investigate Dependencies → Report Findings

Their LangGraph implementation starts with an alert and creates a dynamic graph of investigation nodes. Each node can spawn sub-nodes based on findings, allowing the agent to:

* Check for code changes in the past 7 days
* Narrow down to changes affecting the specific data pipeline
* Look at events occurring hours before the issue
* Investigate multiple potential root causes simultaneously

**The key advantage**: While human troubleshooters follow one path at a time, Monte Carlo's agent can explore multiple investigation branches in parallel, checking significantly more scenarios than any individual data engineer could handle manually.

Monte Carlo's Product Manager, Bryce Heltzel, notes that LangGraph's value was in achieving speed to market. With a tight 4-week deadline ahead of major industry summits, the team felt confident demonstrating their agent to customers— something that wouldn't have been possible with a custom-built solution.

## **Debugging with LangSmith**

Monte Carlo started debugging using LangSmith on day one of development. As Heltzel explains, "LangSmith was a natural choice as we started building our agent in LangGraph. We wanted LangSmith to visualize what we were developing for our graph-based workflows."

As a product manager, Heltzel is very involved in the process of prompt engineering for their agents. With his deep context about customer use cases, he can now iterate quickly on prompts directly rather than going through engineering cycles.

The Monte Carlo team has been able to focus on agent logic and solving data issues for customers rather than tooling setup due to the minimal configuration LangSmith required to get up and running.

## **Monte Carlo's architecture**

This architecture leverages several AWS services to build a scalable, secure, and decoupled system that connects Monte Carlo’s existing monolithic platform with its new AI Agent stack. We use **Amazon Bedrock** to empower our agents with the latest foundational models without the need to manage any infrastructure. The **Auth Gateway Lambda** handles authentication as a lightweight, serverless entry point, ensuring secure access without maintaining dedicated servers. The **Monolith Service**continues to serve core APIs (GraphQL and REST) and persists application data in **Amazon RDS**, a managed relational database that provides reliability and automated maintenance.

On the AI side, the **AI Agent Service** runs on **Amazon ECS Fargate**, which enables containerized microservices to scale automatically without managing underlying infrastructure. Incoming traffic to the AI Agent Service is distributed through a network load balancer (NLB), providing high-performance, low-latency routing across Fargate tasks. Together, these AWS components create a robust system where the legacy monolith and modern AI microservices interoperate efficiently, with secure authentication, resilient data storage, and elastic compute scaling.

## **What's next**

Monte Carlo is currently focused on visibility and validation — understanding where bugs occur in their traces and building robust feedback mechanisms to ensure their agent consistently delivers value to customers. They're working on validation scenarios to measure whether the agent successfully identifies root causes in each investigation.

Looking ahead, Monte Carlo plans to expand their agent's capabilities while maintaining the core value proposition: **enabling data teams to resolve issues faster and more comprehensively than ever before**. Their head start in building data + AI observability tools, combined with LangGraph's flexible architecture and LangSmith's debugging capabilities, positions them to continue leading the data + AI observability space.

]]>*LangChain has had agent abstractions for nearly three years. There are now probably 100s of agent frameworks with the same core abstraction. They all suffer from the same downsides that the original LangChain agents suffered from: they do not give the developer enough control over context engineering when needed, leading*]]>https://blog.langchain.com/agent-middleware/68bf2a69c3c55900012a789dMon, 08 Sep 2025 21:11:12 GMT

*LangChain has had agent abstractions for nearly three years. There are now probably 100s of agent frameworks with the same core abstraction. They all suffer from the same downsides that the original LangChain agents suffered from: they do not give the developer enough control over context engineering when needed, leading to developers graduating off of the abstraction for any non-trivial use case. In LangChain 1.0 we are introducing a new agent abstraction (*[*`Middleware`*](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com)*) which we think solves this.*

The core agent components are quite simple:

* A model
* A prompt
* A list of tools

The core agent algorithm is equally simple. The user first invokes the agent with some input message, and the agent then runs in a loop, calling tools, adding AI and tool messages to its state, until it decides to not call any tools and ultimately finish.

We had a version of this agent in LangChain in November of 2022, and over the past 3 years 100s of frameworks have popped up with similar abstractions.

At the same time, while it is simple to get a basic agent abstraction up and running, it is hard to make this abstraction flexible enough to bring to production.

In this blog we will cover:

1. Why it is hard to get this abstraction to be reliable enough to bring to production
2. Our journey to make it more reliable over the past year or so
3. A new [`Middleware`](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com) abstraction we are introducing in LangChain 1.0 which we think makes it the most flexible and composable agent abstraction out there

## Why it is hard to bring this abstraction to production

So why is it still so hard to build reliable agents with these frameworks? Why do many people, when they hit a certain level of complexity, go away from frameworks in favor of custom code?

The answer is [*context engineering*](https://blog.langchain.com/the-rise-of-context-engineering/). The context that goes into the model determines what comes out of it. In order to make the model (and therefore, the agent) more reliable, you want to have full control over what goes into the model. And while this simple agent state and simple agent loop are great for getting started, as you push the boundaries of your agent’s performance you will likely want to modify part of that.

There are a number of things you may want to have more control over as complexity increases:

1. You may want to adjust the “state” of the agent to contain more than just messages
2. You may want to have more control over what exactly goes into the model
3. You may want to have more control over the sequence of steps run

## Our journey to make it more reliable

Over the past two years we worked to make our agent abstraction better support context engineering. Some things we did (roughly in order):

* Allowed the user to specify runtime configuration, to pass in things like connection strings and read only user info
* Allowed the user to specify arbitrary state schemas, that either the user or the agent could update
* Allowed the user to specify a function to return a prompt, rather than a string, allowing for dynamic prompts
* Allowed the user to specify a function to return a list of messages, to have full control over the whole message list that was sent to the model
* Allowed the user to specify a “pre model hook”, to run a step BEFORE the model was called, that could update state or jump to a different node. This allows for things like summarization of long conversations.
* Allowed the user to specify a “post model hook”, to run a step AFTER the model was called, that could update state or jump to a different node. This allows for things like human-in-the-loop and guardrails.
* Allowed the user to specify a function that returned the model to use at each call, making it possible to do dynamic model switching and dynamic tool calling.

This allowed for high level of customization and control over the context engineering that gets done.

But it also resulted in a large number of parameters to the agent. Furthermore, these parameters often had dependencies on each other, which made it tough to coordinate. And it was tough to combine multiple versions of these parameters, or provide off-the-shelf variants to try.

## What we’re doing in LangChain 1.0

For LangChain 1.0 we are leaning to this idea of modifying this core agent loop by introducing a concept of [`Middleware`](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com).

The core agent loop will still consist of a model node and a tool node. But Middleware can now specify:

* [`before_model`](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com#before-model): will run before model calls, can update state or jump to other nodes.
* [`after_model`](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com#after-model): will run after model calls, can update state or jump to other nodes.
* [`modify_model_request`](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com#modify-model-request): will run before model calls, allows user to modify (only for that model request) the tools, prompt, message list, model, model settings, output format, and tool choice.

You can provide multiple middleware to an agent. They will run as middleware runs in web servers: sequentially on the way in to the model call (`before_model`, `modify_model_request`), and in reverse sequential order on the way back (`after_model`).

Middleware can also specify custom state schemas and tools as well.

We will provide off-the-shelf middleware for developers to get started with. We will also maintain a list of community middleware for easy access. For a while, developers have asked for collections of nodes to plug into LangGraph agents. This is exactly that.

Middleware will also help us unify our different agent abstractions. We currently have separate LangGraph agents for supervisor, swarm, bigtool, deepagents, reflection, and more. We’ve already verified that we will be able replicate these architectures using Middleware.

## Try it in LangChain 1.0 alpha

You can try out Middleware in the most recent LangChain 1.0 alpha releases (Python and JavaScript). This is the biggest new part of LangChain 1.0 so we would LOVE feedback on Middleware.

As part of this alpha release, we are also releasing three different middleware implementations (all of which we are using in internal agents already):

1. [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com#human-in-the-loop): uses `Middleware.after_model` to provide an off-the-shelf way to add interrupts to get human-in-the-loop feedback on tool calls.
2. [Summarization](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com#summarization): uses `Middleware.before_model` to summarize messages once they accumulate past a certain threshold
3. [Anthropic Prompt Caching](https://docs.langchain.com/oss/python/langchain/middleware?ref=blog.langchain.com#anthropic-prompt-caching): uses `Middleware.modify_model_request` to add special prompt caching tags to messages.

Try it in Python: `pip install --pre -U langchain`

Try it in JavaScript: `npm install langchain@next`

]]>https://blog.langchain.com/building-langgraph/68b68295c3c55900012a702cThu, 04 Sep 2025 16:26:16 GMT

*By Nuno Campos*

**Summary:** We launched LangGraph as a low level agent framework nearly two years ago, and have already seen companies like LinkedIn, Uber, and Klarna use it to build production ready agents. LangGraph builds upon feedback from the super popular LangChain framework, and rethinks how agent frameworks should work for production. We aimed to find the right abstraction for AI agents, and decided that was little to no abstraction at all. Instead, we focused on control and durability. This post shares our design principles and approach to designing LangGraph based on what we’ve learned about building reliable agents.

LangGraph ALPHA

We just launched an alpha version of LangGraph 1.0!

 [Try it out now](https://docs.langchain.com/oss/python/langgraph/overview?ref=blog.langchain.com)

We started [LangGraph](https://github.com/langchain-ai/langgraph?ref=blog.langchain.com) as a reboot of LangChain’s super popular chains and agents more than two years ago. We decided that starting fresh would give us the most leeway to address all the feedback we had received since the launch of the original `langchain` open source library (in countless GitHub issues, discussions, Discord, Slack and Twitter posts). The main thing we heard was that `langchain` was easy to get started but hard to customize and scale.  
This time around, our top goal was to make LangGraph what you’d use to run your agents in production. When we had to make tradeoffs, we prioritized production-readiness over how easy it would be for people to get started.  
In this post, we’ll share our process for scoping and designing LangGraph.

* First: we cover what’s different about building agents compared to traditional software.
* Next: we discuss how we turned these differences into required features.
* Finally: we show how we designed and tested our framework for these requirements.

The result is a low-level, production ready agent framework that scales with both the size and throughput of your agents.

## 1. What do agents need?

The first two questions we asked were, “Do we actually need to build LangGraph?” And, “Why can’t we use an existing framework to put agents in production?” To answer these questions, we had to define what makes an agent different (or similar) to previous software. By building many agents ourselves and working with [teams like Uber, LinkedIn, Klarna, and Elastic](https://blog.langchain.com/top-5-langgraph-agents-in-production-2024/), we boiled these down to 3 key differences.

* More latency makes it harder to keep users engaged
* Retrying long-running tasks when they fail is expensive and time-consuming
* The non-deterministic nature of AI requires checkpoints, approvals, and testing

### Managing latency

The first defining quality and challenge of LLM-based agents is **latency**. We used to measure the latency of our backend endpoints in milliseconds. Now, we need to measure agent run times in seconds, minutes, or soon hours.

This is because LLMs themselves are slow and are becoming slower with test-time compute. It’s also because we often need multiple LLM calls to achieve our desired results, with looping agents, and chaining LLM prompts to fix earlier output. And, we usually need to add non-LLM steps before and after the LLM call. For instance, you might need to get database rows into the context or create guardrails and verifiers to check the LLM call for accuracy.

All this latency enables building new things, but you do still need to keep end users engaged throughout. So, we identified two features that would come in handy when building agents:

* **Parallelization.** Whenever there were multiple steps to your agent, when the next step doesn’t need the output of the previous one, then you could run them in parallel. But to do this reliably in production you want to avoid data races between your parallel steps.
* **Streaming.** When you can’t reduce the actual latency of your agent any further without making it produce worse results, then you turn to perceived latency. Here the key unlock comes from showing useful information to the user while the agent is running, which can go all the way from a progress bar, or key actions taken by the agent, all the way to streaming LLM messages token-by-token in real-time to the end-user.

### **Managing reliability**

The slowness of LLM agents had other implications, too. As we all know all too well, inevitably all software bugs out. Long-running agents fail more often because, the longer they run, the more opportunity there is for something to go wrong.

When traditional software bugs out, you usually want to retry. With AI agents? That may not be the best approach. If your agent fails on minute 9 of 10, going back to the beginning is pretty time consuming and also expensive.

So we knew we had to add two more features to the list:

* **Task queue.** Queues eliminate one common source of failure by disconnecting the running of the agent from the request that triggered it. They provide the primitives to retry the agent reliably and fairly when needed.
* **Checkpointing.** This saves snapshots of the computation state at intermediate stages and makes it a lot cheaper to retry when it does fail.

### Managing non-deterministic LLMs

Next, the non-deterministic nature of LLMs creates two more challenges. When you write traditional software, you at least know what the code is supposed to do and what should result if you built it as you hoped. Generative AI obviously changes this.

With LLMs, both input and their output is open-ended. You can imagine when you’ve used ChatGPT, and the same prompt you used a day before produces a different result, or, how easy it is to ask your question in many different ways and get back similar results.

This is a very big part of what makes LLM agents so powerful compared other previous software, but it also introduces challenges when taking them to production.

The testing you do while developing will almost certainly miss many surprising ways in which your users will use your agent. You truly can’t plan for all the ways users will interact with your agent or how the LLM will respond. And so, two more features then become very useful when going to production:

* **Human-in-the-loop.** Having the tools to interrupt and resume the agent at any point, without having to redo work done until then, enables many essential UX patterns for AI agents. For example, you can approve or reject actions, edit the next action, ask clarifying questions, or even time travel to re-do things from a previous step.
* **Tracing.** To build for scale, developers need clear visibility into what's happening within the details of their agent loops. You need to see inputs, trajectories, and outputs of the agent, otherwise you won’t know what users are asking of it, how the agent is handling it, and if users are happy with the outcome.

### What developers need to build agents

This is how we built our shortlist of the six features most developers need when taking agents to production.

* Parallelization – to save actual latency
* Streaming – to save perceived latency
* Task queue – to reduce number of retries
* Checkpointing – to reduce the cost of each retry
* Human-in-the-loop - to collaborate with the user
* Tracing - to learn how users use it

If the agent you’re building doesn’t need most of these features (eg. because it’s a very short agent without tools and a single prompt), then you might not need LangGraph, or any other framework.

As we thought about building for each of these features, we also realized that developers wouldn’t adopt a framework that that provided all those features at the cost of making their LLM app perceivably slower to end users. Especially for agents deployed as chatbots. That made **low latency** our final overarching requirement.

Next, we'll cover how we built these capabilities into LangGraph.

## 2. Why build LangGraph at all?

Back to our existential question, should we build something new, or adopt one of the existing open source frameworks built before LLMs? Armed with our feature shortlist, it became pretty easy to make that decision.

### Why was a new framework needed?

Existing frameworks were mostly split between two categories:

**DAG frameworks (made popular by Apache Airflow and many others)**

These we had to exclude just based on the name, as LLM agents really benefit from looping, ie. the computation graph for an LLM agent is cyclical, and thus cannot be handled by DAG algorithms.

**Durable execution engines (made popular by Temporal and others)**

These options were closer, but in the end, as they were designed before LLM agents, so they were lacking some of those specific features — namely streaming. In addition, these engines introduced latency between steps which would have been noticeable to chatbot developers. Lastly, due to their design, the performance degrades the more steps there are in the history, which sounded like a bad bet to make as LLM agents get longer and more complicated.

So in the end our answer was, yes LLMs are different enough that previous production infrastructure needed some new ideas injected into it to become relevant for the new era. And so we embarked on building LangGraph.

## 3. Our design philosophy

We designed LangGraph with two leading principles.

* **We don’t know what the future holds for AI.** The fewer assumptions we make about the future the better. No one really knows what it will look like to build with LLMs one, two, three years from now, so the fewer assumptions we bake into the design of the framework, the more relevant it will be in the future. The only assumptions we wanted to bake into it were the realizations we talked about above, i.e. that **LLMs are slow, flaky, and open-ended.**
* **It should feel like writing code.** The public API for the framework should be as close as possible to writing regular framework-less code. Every requirement we place on the developer’s code needs to be justified by enabling a really high-value feature. Otherwise the pull of skipping the framework altogether is just too strong. The biggest competitor to any code framework is always no framework.

These principles impacted a few key design decisions that have stayed with us ever since.

* **First, the runtime of the library is independent from the developer SDKs.** The SDKs are the public interfaces (classes, functions, methods, constants, etc) that developers use when building their agents. We currently offer two – **StateGraph** and the **imperative/functional API**. The runtime (which we call PregelLoop) implements each of the features listed earlier, plans the computation graph for each agent invocation, and executes it. This design enables us to evolve the developer APIs and the runtime independently. For instance, on the SDK side, it has allowed us to introduce the imperative SDK, and deprecate the very first SDK we offered, a Graph interface without shared state. On the runtime side, it has enabled us to implement many performance improvements over the last 2 years without any impact to the public APIs, and enabled experimentation with more radical changes to the runtime – more about this later when we get to distributed execution.
* **Second, we wanted to provide each of the 6 features as building blocks, with the developer free to pick which to use in their agent at any point in time.** For instance, the ability to interrupt/resume for human-in-the-loop scenarios doesn’t get in your way until you reach for it (which is as easy as adding a call to the `interrupt()` function in one of your nodes). So LangGraph ended up as a uniquely low-level framework in a sea of other frameworks trying to convince developers to bet everything on the high-level abstraction du jour. We have seen these come and go, and LangGraph remaining relevant, so we’re happy with our approach so far.

## 4. The LangGraph runtime

With all this in mind, let’s look at how LangGraph implements each of the 6 features we wanted to have (as a reminder, these are parallelization, streaming, checkpointing, human-in-the-loop, tracing and a task queue).

### **Structured agents with discrete steps**

If there is one idea that informs every other architectural decision we’ve made, it is the idea of structured agents. There’s a long tradition of adding more structure to computer programs, trading some amount of flexibility for a host of new features. Once upon a time, basic constructs like [if statements and while loops](https://en.wikipedia.org/wiki/Structured_programming?ref=blog.langchain.com) were the new kid on the block. Agents too can be written directly as a single function with one big while loop. But when you do that, you lose the ability to implement features like checkpointing or human-in-the-loop. (Note: While it may technically be possible to interrupt execution of some kinds of subroutines, like generators, that execution state can’t be saved in a portable format that can be resumed from a different machine at a different time.)

### **Execution algorithm**

Once you make the choice to structure agents into multiple discrete steps, you need to choose some algorithm to organize its execution. Even if it’s a naive one that feels like “no algorithm,” which is where LangGraph started before launch. The problem with using “no algorithm” is, while it may seem simpler, you’re making it up as you go along, and end up with unexpected results. (For instance, an early version of a precursor to LangGraph suffered from non-deterministic behavior with concurrent nodes). The usual DAG algorithms (topological sort and friends) are out of the picture, given we need loops. We ended up building on top of the [BSP](https://en.wikipedia.org/wiki/Bulk_synchronous_parallel?ref=blog.langchain.com)/ [Pregel](https://dl.acm.org/doi/10.1145/1807167.1807184?ref=blog.langchain.com) algorithm, because it provides deterministic concurrency, with full support for loops (cycles).

Our execution algorithm works like this:

* **Channels** contain data (any Python/JS data type), and have a name and current version (a monotonically increasing string)
* **Nodes** are functions to run, which subscribe to one or more channels, and run whenever they change
* One or more channels are mapped to **input**, ie. the starting input to the agent is written to those channels, and therefore triggers any nodes subscribed to them
* One or more channels are mapped to **output**, ie. the return value of the agent is the value of those channels when execution halts

The execution proceeds in a loop, where each iteration

* Selects the 1 or more nodes to run, by comparing current channel versions and the last versions seen by each of their subscribers
* Executes those nodes in parallel, with independent copies of the channel values (ie. the state, so they don’t affect each other while running)
* Nodes modify their local copy of the state while running
* Once all nodes finish, the updates from each copy of the state are applied to their respective channels, in a deterministic order (this is what guarantees no data races), and the channel versions are bumped

The execution loop stops when there are no more nodes to run (ie. after comparing channels with their subscriptions we find all nodes have seen the most recent version of their subscribed channels), or when we run out of iteration steps (a constant the developer can set).

### **Validating framework features**

Let’s see how this maps to the 6 features we wanted to implement.

* **Parallelization**. This algorithm is designed for safe parallelization without data races, it automatically selects parallel execution whenever the dependencies between the nodes allow, it executes parallel nodes with isolated state copies, and it applies updates from nodes in an order which doesn’t depend on which one started or finished first (as that can change between executions). This ensures that the execution order and latency of each node never influences the final output of the agent. Given LLMs are non-deterministic, we felt this was an important property, to ensure that variability in your outputs is never the fault of the agent framework, making it a lot easier to debug issues.
* **Streaming**. Structured execution models (ie. where the computation is split into discrete steps and/or nodes) offer many more opportunities for emitting intermediate output and updates throughout. Our execution engine collects streaming output from inside nodes while they are running, as well as at the step boundaries, without requiring any custom developer code. This has enabled us to offer 6 distinct stream modes in LangGraph, values, updates, messages, tasks, checkpoints and custom. A streaming chatbot might use messages stream mode, while a longer running agent might use updates mode.
* **Checkpointing**. Again, structured execution is what makes this feasible. We want to save checkpoints that can be resumed on any machine, an arbitrary amount of time after they were saved – ie. checkpoints that don’t rely on keeping a process running in a specific machine, or keeping any live data in memory. To enable this we record serialised channel values (by default serialised to MsgPack, optionally encrypted), their version strings, and a record of which channel versions each node has most recently seen.
* **Human-in-the-loop**. The same checkpointing that enables fault tolerance can also be used to power “expected interruptions” of the agent, ie. giving the agent the ability to interrupt itself to ask the user or developer for input before continuing. Usually this capability is implemented by leaving the agent running while it waits for the input to arrive, but sadly that scales neither in time nor in volume. If you have many agents interrupted simultaneously, or if you want to wait several days (or months!) before replying, then actual interruption (powered by checkpointing to resume again from the same point) is the only way to go.
* **Tracing**. Another nice property of using structured execution is you get very clear steps to inspect the progress of your agent, while it runs and after the fact. We had previously built [LangSmith](https://docs.langchain.com/langsmith/home?ref=blog.langchain.com) as the first LLM observability platform, so naturally LangGraph integrates natively with it. Today we have also LangGraph Studio, where you can debug your agent while it’s running, and LangGraph can also emit OTEL traces for wider compatibility.
* **Task queue**. This was out of scope for a Python library such as LangGraph, so we ended up creating LangGraph Platform to answer this need.

All in all, this architecture delivers the 6 key features needed for agents. At the same time, it makes creating and debugging agents faster, thanks to the structured approach, and the tools to explore it. And finally, it does so with an excellent performance profile, which scales with the size of your agent, and the throughput you need in production –  more on this in the next section.

## 5. Performance characteristics

Like we mentioned earlier, developers want reliability, but not at the expense of latency. So we need to look at how our approach is working against these tradeoffs. LangGraph scales very gracefully with all size measures of the agents you build with it. This is a great place to be in for a future where agents are becoming ever longer, with more steps, more interruptions, larger state, etc.

How is the execution of a LangGraph agent affected by the key variables that control its size?

First, let’s list the key **size variables** in StateGraph, the most common LangGraph developer SDK:

* The number of nodes (individual steps, usually functions)
* The number of edges (or the connections between nodes, which can be fixed or conditional)
* The number of channels (or the keys in your state object)
* The number of active nodes (to be executed in parallel in a given step)
* The length of invocation history (previous steps of the current invocation)
* The number of threads (independent invocations on different inputs and context)

Now, let’s list the key **moments in an invocation** of a LangGraph agent, and see how each scales with each variable:

* Starting or resuming invocation, which consists of transferring from storage the most recent checkpoint for that thread, and deserializing it
* Planning the next invocation step, where we decide which nodes to execute next, and prepare their inputs
* Running the active nodes for a step, where we execute the code for each node, producing writes to channels and edges
* Finishing an invocation step, which consists of applying updates to each channel (running channel reducers and bumping channel versions) and saving the latest checkpoint (serializing and transferring to storage)

Note there is no ‘finishing invocation’ action as execution simply stops when the planning action returns no nodes to execute next.

In summary, this is how each action scales with agent size:

| Metric / Action | Starting invocation | Planning a step | Running a step | Finishing a step |
| --- | --- | --- | --- | --- |
| Number of nodes | O(n) | O(1) | O(1) | O(n) |
| Number of edges | O(1) | O(1) | O(n) | O(1) |
| Number of channels | O(n) | O(n) | O(n) | O(n) |
| Active nodes | O(1) | O(n) | O(n) | O(n) |
| Length of history | O(1) | O(1) | O(1) | O(1) |
| Number of threads | O(1) | O(1) | O(1) | O(1) |

Now, let’s look more in detail at some of these. First, starting an invocation:

* Scales **linearly with number of nodes**, for each node there is one hidden control channel holding the current state of its incoming edges
* **Constant on the number of edges** as the state of all edges for each destination node is collapsed into a single control channel
* Scales **linearly with number of channels**, for each channel there is a serialized representation of its current value
* **Constant on the number of active nodes**, there is no relation to this variable
* **Constant on the length of history**, as we only fetch the latest checkpoint, and don’t need to replay steps before it
* **Constant on number of threads**, as threads are completely independent, and each invocation only touches a single one

Second, planning the next step:

* **Constant on the number of nodes**, when finishing the previous step we store the list of updated channels, which lets us avoid iterating over all nodes when planning the next one
* **Constant on the number of edges**, as all edges are collapsed into a single trigger channel per node
* Scales **linearly with the number of channels**, when assembling the input for each node we loop over channels to check which are currently set
* Scales **linearly with number of active nodes**, for each node to execute in this step we assemble the input and configuration to use for its invocation
* **Constant on the length of history**, as we only deal with the latest checkpoint, which aggregates all previous writes
* **Constant on number of threads**, as threads are completely independent, and each invocation only touches a single one

Third, running a step:

* **Constant on the number of nodes**, only nodes active in a step influence the running of that step
* Scales **linearly on the number of edges** of the nodes active in this step, each active node publishes to each of its outgoing edges
* Scales **linearly on the number of channels**, for each active node we check if the node returned an update to its value (when using a dictionary return value we optimize this to be constant on the number of channels, and just iterate over the keys of the return value)
* Scales **linearly with the number of active nodes**, each active node is executed concurrently
* **Constant on the length of history**, we don’t deal with history at this time
* **Constant on number of threads**, as threads are completely independent, and each invocation only touches a single one

Lastly, finishing a step:

* Scales **linearly with number of nodes**, for each node there is one hidden control channel holding the current state of its incoming edges
* **Constant on the number of edges** as the state of all edges for each destination node is collapsed into a single control channel
* Scales **linearly with number of channels**, each channel is updated with the writes from the active nodes, and its version is bumped
* Scales **linearly with number of active nodes**, as we collect writes from each active node
* **Constant on the length of history**, as we only deal with the latest checkpoint, which aggregates all previous writes
* **Constant on number of threads**, as threads are completely independent, and each invocation only touches a single one

These performance characteristics have been the result of both our choice of design for the library, as well as numerous performance optimizations we have made over the past two years.

## Getting started

In summary, we thought deeply about what is different about building with LLMs and what it takes your agent to run in production. These ideas led us to build and iterate on LangGraph. LangGraph focuses on control and durability, so you have the best chance of your agent doing what you intended.

If you want to learn more about LangGraph and test it out for your own projects, head on over to the [docs](https://langchain-ai.github.io/langgraph/?ref=blog.langchain.com) to get started.

]]>