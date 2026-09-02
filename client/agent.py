import os
import time
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    SharepointPreviewTool,
    SharepointGroundingToolParameters,
    ToolProjectConnection,
    MCPTool,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from openai.types.responses.response_input_param import (
    McpApprovalResponse,
)


with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    print(f"✅ Connected to Foundry: {endpoint}")


sharepoint_connection_id = os.environ.get("SHAREPOINT_CONNECTION_ID")
sharepoint_tool = None

if sharepoint_connection_id:
    print("📁 Configuring SharePoint integration...")
    print(f"   Connection ID: {sharepoint_connection_id}")

    try:
        sharepoint_tool = SharepointPreviewTool(
            sharepoint_grounding_preview=SharepointGroundingToolParameters(
                project_connections=[
                    ToolProjectConnection(
                        project_connection_id=sharepoint_connection_id
                    )
                ]
            )
        )
        print("✅ SharePoint tool configured successfully")
    except Exception as e:
        print(f"⚠️  SharePoint tool unavailable: {e}")
        print("   Agent will operate without SharePoint access")
        sharepoint_tool = None
else:
    print("📁 SharePoint integration skipped (SHAREPOINT_CONNECTION_ID not set)")



mcp_server_url = os.environ.get("MCP_SERVER_URL")
mcp_tool = None

if mcp_server_url:
    print("📚 Configuring Microsoft Learn MCP integration...")
    print(f"   Server URL: {mcp_server_url}")

    try:
        mcp_tool = MCPTool(
            server_url=mcp_server_url,
            server_label="Microsoft_Learn_Documentation",
            require_approval="always",
        )
        print("✅ MCP tool configured successfully")
    except Exception as e:
        print(f"⚠️  MCP tool unavailable: {e}")
        print("   Agent will operate without Microsoft Learn access")
        mcp_tool = None
else:
    print("📚 MCP integration skipped (MCP_SERVER_URL not set)")



print(f"🛠️  Creating agent with model: {os.environ['FOUNDRY_MODEL_NAME']}")

tools = []
if sharepoint_tool:
    tools.append(sharepoint_tool)
    print("   ✓ SharePoint tool added")
if mcp_tool:
    tools.append(mcp_tool)
    print("   ✓ MCP tool added")

print(f"   Total tools: {len(tools)}")

agent = project_client.agents.create_version(
    agent_name="Modern Workplace Assistant",
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL_NAME"],
        instructions=instructions,
        tools=tools if tools else None,
    ),
)

print(f"✅ Agent created successfully (name: {agent.name}, version: {agent.version})")


print("🤖 AGENT RESPONSE:")
response, status = create_agent_response(agent, scenario["question"], openai_client)
