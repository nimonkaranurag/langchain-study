## How to navigate this repository using any LLM client (like Claude Desktop, Windsurf, etc.)

- The repo implements an MCP server which exposes different resources to your LLM application.
- For `Claude Desktop` you can set the style to "Learning" mode and get an enhanced experience!

### Set-up instructions for Claude Desktop

- Download [Claude Desktop](https://www.claude.com/download)
- Create a `claude_config.json` here:
```bash
touch ~/Library/Application\ Support/Claude/claude_desktop_config.json
```
- Activate your virtual environment:
```bash
conda activate <your_virtual_env>
```
- Install the project if you haven't done so:
```bash
cd /path/to/langchain-study/
pip install -e .
```
- Now find get these paths by running these bash commands (you need them for the config!):
```bash
which python

cd /path/to/langchain-study/
pwd

cd langchain-study/mcp/
pwd
```
- Great, now open the config using:
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```
- Copy/Paste this template and replace the paths here with the ones we discovered just now!
```json
{
  "mcpServers": {
    "langchain-study": {
      "command": "/opt/miniconda3/envs/nvidia-foundations/bin/python",
      "args": [
        "/Users/nimo/Desktop/personal-dev/langchain-study/mcp/server.py"
      ],
      "env": {
        "REPO_ROOT": "/Users/nimo/Desktop/personal-dev/langchain-study"
      }
    }
  }
}
```
- That's it! If Claude Desktop is already open -> close it and restart it!
- Now you can directly ask questions directly about how to navigate this repository, see these examples:

![alt text](./output/ex_one.png)
![alt text](./output/ex_two.png)
![alt text](./output/ex_three.png)