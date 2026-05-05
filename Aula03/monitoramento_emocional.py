"""
Sistema de Monitoramento Emocional com Alertas Automáticos
Integração Low Code com Python

Descrição:
- Recebe dados de batimentos cardíacos via webhook
- Armazena em Google Sheets
- Detecta possíveis crises emocionais
- Envia alertas automáticos via email
"""

import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==================== CONFIGURAÇÃO ====================

# Limiar de batimentos para detectar crise
LIMITE_BATIMENTOS_CRITICO = 100
LIMITE_BATIMENTOS_ALERTA = 85

# Configurações de email
EMAIL_REMETENTE = "seu_email@gmail.com"
SENHA_EMAIL = "sua_senha_ou_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Configuração Google Sheets
ARQUIVO_CREDENCIAIS = "credentials.json"
NOME_PLANILHA = "Monitoramento Emocional"
ABAS = {
    "dados": "Dados de Usuários",
    "historico": "Histórico de Alertas"
}

# ==================== CLASSE PRINCIPAL ====================

class MonitoramentoEmocional:
    """Classe para gerenciar o sistema de monitoramento emocional"""
    
    def __init__(self):
        """Inicializa a conexão com Google Sheets"""
        self.sheet_dados = None
        self.sheet_historico = None
        self._conectar_google_sheets()
    
    def _conectar_google_sheets(self):
        """Estabelece conexão com Google Sheets"""
        try:
            escopo = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            credenciais = ServiceAccountCredentials.from_json_keyfile_name(
                ARQUIVO_CREDENCIAIS, 
                escopo
            )
            cliente = gspread.authorize(credenciais)
            planilha = cliente.open(NOME_PLANILHA)
            
            self.sheet_dados = planilha.worksheet(ABAS["dados"])
            self.sheet_historico = planilha.worksheet(ABAS["historico"])
            
            print("✅ Conexão com Google Sheets estabelecida")
        except Exception as e:
            print(f"❌ Erro ao conectar Google Sheets: {e}")
    
    def receber_dados_webhook(self, dados_json: Dict) -> Dict:
        """
        Simula o recebimento de dados via webhook do app/smartwatch
        
        Args:
            dados_json: Dicionário com {nome, email, batimentos}
            
        Returns:
            Resultado do processamento
        """
        try:
            nome = dados_json.get("nome")
            email = dados_json.get("email")
            batimentos = int(dados_json.get("batimentos", 0))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n📊 Dados recebidos do webhook:")
            print(f"   Nome: {nome}")
            print(f"   Email: {email}")
            print(f"   Batimentos: {batimentos} bpm")
            print(f"   Timestamp: {timestamp}")
            
            # Armazenar dados
            self.armazenar_dados(nome, email, batimentos, timestamp)
            
            # Analisar dados
            status = self.analisar_dados(batimentos)
            
            # Se crise detectada, enviar alerta
            if status in ["CRÍTICO", "ALERTA"]:
                self.enviar_alerta(nome, email, batimentos, status, timestamp)
            
            return {
                "sucesso": True,
                "status": status,
                "mensagem": f"Dados processados. Status: {status}"
            }
            
        except Exception as e:
            print(f"❌ Erro ao processar webhook: {e}")
            return {"sucesso": False, "erro": str(e)}
    
    def armazenar_dados(self, nome: str, email: str, batimentos: int, timestamp: str):
        """Armazena os dados na planilha de dados"""
        try:
            if self.sheet_dados:
                self.sheet_dados.append_row([nome, email, batimentos, timestamp])
                print(f"💾 Dados armazenados com sucesso")
        except Exception as e:
            print(f"❌ Erro ao armazenar dados: {e}")
    
    def analisar_dados(self, batimentos: int) -> str:
        """
        Analisa os dados para detectar crise emocional
        
        Args:
            batimentos: Número de batimentos cardíacos por minuto
            
        Returns:
            Status: "NORMAL", "ALERTA" ou "CRÍTICO"
        """
        if batimentos >= LIMITE_BATIMENTOS_CRITICO:
            status = "CRÍTICO"
            print(f"⚠️  STATUS: {status} - Batimentos muito elevados!")
        elif batimentos >= LIMITE_BATIMENTOS_ALERTA:
            status = "ALERTA"
            print(f"⚠️  STATUS: {status} - Batimentos elevados")
        else:
            status = "NORMAL"
            print(f"✅ STATUS: {status} - Batimentos normais")
        
        return status
    
    def enviar_alerta(self, nome: str, email: str, batimentos: int, status: str, timestamp: str):
        """Envia alerta por email ao usuário"""
        try:
            # Composição do email
            assunto = f"🚨 ALERTA: Possível crise emocional detectada - {status}"
            
            corpo_html = self._gerar_corpo_email(nome, batimentos, status)
            
            # Enviar email
            self._enviar_email(email, assunto, corpo_html)
            
            # Registrar no histórico
            self.registrar_historico(nome, email, batimentos, status, timestamp)
            
            print(f"📧 Alerta enviado para {email}")
            
        except Exception as e:
            print(f"❌ Erro ao enviar alerta: {e}")
    
    def _gerar_corpo_email(self, nome: str, batimentos: int, status: str) -> str:
        """Gera o corpo do email em HTML"""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #d32f2f;">🚨 Alerta de Monitoramento Emocional</h2>
                
                <p>Olá <strong>{nome}</strong>,</p>
                
                <p>Detectamos uma alteração significativa nos seus sinais vitais:</p>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Batimentos Cardíacos:</strong> {batimentos} bpm</p>
                    <p><strong>Status:</strong> <span style="color: #d32f2f; font-weight: bold;">{status}</span></p>
                </div>
                
                <h3>💡 Sugestões Imediatas:</h3>
                <ul>
                    <li>✨ Respire profundamente por 1 minuto (in: 4s, hold: 4s, out: 4s)</li>
                    <li>👥 Entre em contato com alguém de confiança</li>
                    <li>🧘 Tente uma técnica de relaxamento</li>
                    <li>🏥 Procure ajuda profissional se necessário</li>
                </ul>
                
                <p><strong>Lembre-se: Você não está sozinho. 💙</strong></p>
                
                <p>Se esta é uma emergência, por favor, ligue para:</p>
                <ul>
                    <li>🚨 SAMU: 192</li>
                    <li>💬 CVV (Centro de Valorização da Vida): 188</li>
                </ul>
                
                <hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;">
                <p style="font-size: 12px; color: #999;">
                    Mensagem automática do Sistema de Monitoramento Emocional.<br>
                    Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </p>
            </body>
        </html>
        """
    
    def _enviar_email(self, destinatario: str, assunto: str, corpo_html: str):
        """Envia email via Gmail SMTP"""
        try:
            mensagem = MIMEMultipart("alternative")
            mensagem["Subject"] = assunto
            mensagem["From"] = EMAIL_REMETENTE
            mensagem["To"] = destinatario
            
            # Adicionar corpo em HTML
            parte_html = MIMEText(corpo_html, "html")
            mensagem.attach(parte_html)
            
            # Conectar ao servidor SMTP e enviar
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
                servidor.starttls()
                servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
                servidor.sendmail(EMAIL_REMETENTE, destinatario, mensagem.as_string())
            
            print(f"✅ Email enviado com sucesso para {destinatario}")
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
    
    def registrar_historico(self, nome: str, email: str, batimentos: int, status: str, timestamp: str):
        """Registra o alerta no histórico da planilha"""
        try:
            if self.sheet_historico:
                self.sheet_historico.append_row([
                    timestamp, 
                    nome, 
                    email, 
                    batimentos, 
                    status
                ])
                print(f"📝 Alerta registrado no histórico")
        except Exception as e:
            print(f"❌ Erro ao registrar histórico: {e}")
    
    def obter_relatorio(self) -> Dict:
        """Obtém relatório geral do monitoramento"""
        try:
            if not self.sheet_dados:
                return {"erro": "Planilha não conectada"}
            
            todos_os_dados = self.sheet_dados.get_all_records()
            
            total_registros = len(todos_os_dados)
            batimentos_medio = sum(int(r.get("Batimentos", 0)) for r in todos_os_dados) / total_registros if total_registros > 0 else 0
            
            return {
                "total_registros": total_registros,
                "batimentos_medio": round(batimentos_medio, 2),
                "ultimos_registros": todos_os_dados[-5:] if total_registros > 0 else []
            }
        except Exception as e:
            return {"erro": str(e)}


# ==================== SIMULAÇÃO DE WEBHOOK ====================

def simular_webhook():
    """Simula o envio de dados via webhook"""
    
    monitor = MonitoramentoEmocional()
    
    # Exemplo de dados que seriam enviados pelo app/smartwatch
    cenarios_teste = [
        {
            "nome": "João Silva",
            "email": "joao@email.com",
            "batimentos": 78
        },
        {
            "nome": "Maria Santos",
            "email": "maria@email.com",
            "batimentos": 105  # Crítico
        },
        {
            "nome": "Pedro Costa",
            "email": "pedro@email.com",
            "batimentos": 90  # Alerta
        },
        {
            "nome": "Ana Oliveira",
            "email": "ana@email.com",
            "batimentos": 72
        },
    ]
    
    print("\n" + "="*60)
    print("SIMULAÇÃO DE MONITORAMENTO EMOCIONAL")
    print("="*60)
    
    for cenario in cenarios_teste:
        resultado = monitor.receber_dados_webhook(cenario)
        print(f"Resultado: {resultado}\n")
    
    # Exibir relatório
    print("\n" + "="*60)
    print("RELATÓRIO GERAL")
    print("="*60)
    relatorio = monitor.obter_relatorio()
    print(json.dumps(relatorio, indent=2, ensure_ascii=False))


# ==================== VERSÃO SEM GOOGLE SHEETS (TESTE LOCAL) ====================

class MonitoramentoEmocionalLocal:
    """Versão local sem dependências externas para testes"""
    
    def __init__(self):
        """Inicializa com banco de dados em memória"""
        self.dados = []
        self.historico_alertas = []
    
    def processar_dados(self, dados_json: Dict) -> Dict:
        """Processa dados do webhook localmente"""
        try:
            nome = dados_json.get("nome")
            email = dados_json.get("email")
            batimentos = int(dados_json.get("batimentos", 0))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n📊 Dados recebidos:")
            print(f"   Nome: {nome}")
            print(f"   Email: {email}")
            print(f"   Batimentos: {batimentos} bpm")
            
            # Armazenar
            self.dados.append({
                "nome": nome,
                "email": email,
                "batimentos": batimentos,
                "timestamp": timestamp
            })
            
            # Analisar
            if batimentos >= LIMITE_BATIMENTOS_CRITICO:
                status = "CRÍTICO"
                print(f"⚠️  ALERTA CRÍTICO!")
                self._gerar_alerta_critico(nome, email, batimentos)
            elif batimentos >= LIMITE_BATIMENTOS_ALERTA:
                status = "ALERTA"
                print(f"⚠️  ALERTA!")
                self._gerar_alerta(nome, email, batimentos)
            else:
                status = "NORMAL"
                print(f"✅ Tudo bem!")
            
            return {"sucesso": True, "status": status}
            
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}
    
    def _gerar_alerta(self, nome: str, email: str, batimentos: int):
        """Gera alerta de batimentos elevados"""
        alerta = f"""
╔════════════════════════════════════════════════════════╗
║         ⚠️  ALERTA: BATIMENTOS ELEVADOS               ║
╚════════════════════════════════════════════════════════╝

Para: {nome} ({email})
Batimentos: {batimentos} bpm
Hora: {datetime.now().strftime('%H:%M:%S')}

💡 SUGESTÕES IMEDIATAS:
  • Respire profundamente (in: 4s, out: 4s)
  • Sente-se em um lugar seguro
  • Beba água
  • Contate alguém de confiança

Você não está sozinho! 💙
"""
        self.historico_alertas.append(alerta)
        print(alerta)
    
    def _gerar_alerta_critico(self, nome: str, email: str, batimentos: int):
        """Gera alerta crítico"""
        alerta = f"""
╔════════════════════════════════════════════════════════╗
║    🚨 ALERTA CRÍTICO: POSSÍVEL CRISE EMOCIONAL        ║
╚════════════════════════════════════════════════════════╝

Para: {nome} ({email})
Batimentos: {batimentos} bpm ⚠️
Hora: {datetime.now().strftime('%H:%M:%S')}

🆘 AÇÕES IMEDIATAS:
  1. Respire lentamente (4-4-4 segundos)
  2. Contate alguém de confiança AGORA
  3. Se for emergência: SAMU - 192
  4. CVV (Valorização da Vida) - 188

💙 Você tem valor. Não está sozinho!
"""
        self.historico_alertas.append(alerta)
        print(alerta)
    
    def obter_relatorio(self) -> Dict:
        """Retorna relatório dos dados coletados"""
        if not self.dados:
            return {"total": 0, "mensagem": "Nenhum dado coletado"}
        
        batimentos_lista = [d["batimentos"] for d in self.dados]
        
        return {
            "total_registros": len(self.dados),
            "batimentos_medio": round(sum(batimentos_lista) / len(batimentos_lista), 2),
            "batimentos_minimo": min(batimentos_lista),
            "batimentos_maximo": max(batimentos_lista),
            "alertas_gerados": len(self.historico_alertas),
            "dados": self.dados
        }


# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n🔬 SISTEMA DE MONITORAMENTO EMOCIONAL COM IA")
    print("=" * 60)
    
    # Usar versão local para testes (sem necessidade de Google Sheets)
    monitor_local = MonitoramentoEmocionalLocal()
    
    # Cenários de teste
    cenarios = [
        {"nome": "João", "email": "joao@email.com", "batimentos": 72},
        {"nome": "Maria", "email": "maria@email.com", "batimentos": 105},
        {"nome": "Pedro", "email": "pedro@email.com", "batimentos": 88},
        {"nome": "Ana", "email": "ana@email.com", "batimentos": 120},
    ]
    
    for cenario in cenarios:
        monitor_local.processar_dados(cenario)
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    relatorio = monitor_local.obter_relatorio()
    print(json.dumps(relatorio, indent=2, ensure_ascii=False))
