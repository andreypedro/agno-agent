import os
import random
from agno.agent import Agent, Team
from agno.tools import Tool

# ==============================
# CONFIG OPENROUTER
# ==============================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ==============================
# MOCK TOOLS
# ==============================
class MockCRMTool(Tool):
    """Simula um CRM para checar estágio do cliente"""

    def get_stage(self, client_id: str) -> str:
        stages = ["prospect", "pre-contrato", "cliente ativo", "suporte"]
        return random.choice(stages)  # mock: retorna aleatório

    def register_client(self, name: str, phone: str):
        return {"status": "ok", "client_id": f"cli_{random.randint(1000,9999)}"}


class MockBillingTool(Tool):
    """Simula sistema financeiro"""
    def list_invoices(self, client_id: str):
        return [
            {"id": "NF001", "valor": 200.50, "status": "pago"},
            {"id": "NF002", "valor": 450.00, "status": "em aberto"},
        ]


class MockContractTool(Tool):
    """Simula assinatura de contrato"""
    def create_contract(self, client_id: str, plano: str):
        return {"status": "assinado", "plano": plano, "client_id": client_id}


class MockSupportTool(Tool):
    """Simula abertura de chamados"""
    def open_ticket(self, client_id: str, issue: str):
        return {"ticket_id": f"T{random.randint(1000,9999)}", "issue": issue, "status": "aberto"}


# ==============================
# AGENTS
# ==============================
faq_agent = Agent(
    name="FAQ Agent",
    # model="openrouter/mistralai/mistral-7b-instruct",  # rápido/barato
    model="meituan/longcat-flash-chat",
    tools=[MockCRMTool()]
)

sales_agent = Agent(
    name="Sales Agent",
    # model="openrouter/openai/gpt-4",  # persuasivo/detalhado
    model="meituan/longcat-flash-chat",
    tools=[MockCRMTool(), MockContractTool()]
)

billing_agent = Agent(
    name="Billing Agent",
    # model="openrouter/meta-llama/llama-3-70b",  # bom para relatórios
    model="meituan/longcat-flash-chat",
    tools=[MockBillingTool()]
)

support_agent = Agent(
    name="Support Agent",
    # model="openrouter/openai/gpt-4-turbo",  # bom para instruções
    model="meituan/longcat-flash-chat",
    tools=[MockSupportTool()]
)

# ==============================
# TEAMS
# ==============================
atendimento_team = Team(
    name="Atendimento Inicial",
    agents=[faq_agent, sales_agent]
)

onboarding_team = Team(
    name="Onboarding",
    agents=[sales_agent]
)

customer_team = Team(
    name="Customer",
    agents=[billing_agent, support_agent]
)

# Mapeamento
teams = {
    "prospect": atendimento_team,
    "pre-contrato": onboarding_team,
    "cliente ativo": customer_team,
    "suporte": customer_team
}


# ==============================
# ROUTER
# ==============================
def route_message(client_id: str, mensagem: str):
    crm = MockCRMTool()
    stage = crm.get_stage(client_id)
    print(f"🧭 Cliente {client_id} identificado como estágio: {stage}")

    team = teams.get(stage, atendimento_team)
    response = team.run(mensagem)

    return response


# ==============================
# MAIN (Simulação de WhatsApp)
# ==============================
if __name__ == "__main__":
    print("🤖 Bot WhatsApp iniciado com Agno + OpenRouter (Mock)...\n")

    mensagens = [
        "Oi, gostaria de saber preços",
        "Quero assinar um plano",
        "Me envie minhas últimas notas fiscais",
        "Preciso abrir um chamado de suporte",
    ]

    for i, msg in enumerate(mensagens, start=1):
        client_id = f"cli_{i}"
        print(f"\n📩 Mensagem recebida de {client_id}: {msg}")
        resposta = route_message(client_id, msg)
        print(f"💬 Resposta: {resposta}")
