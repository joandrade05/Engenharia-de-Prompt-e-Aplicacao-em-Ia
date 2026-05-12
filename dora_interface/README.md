## 🤖 DORA - Assistente de Monitoramento Emocional

Dora é uma aplicação web inteligente desenvolvida para ajudar no monitoramento e gerenciamento emocional. Utiliza HTML5, CSS responsivo e JavaScript vanilla para oferecer uma experiência fluidificada em dispositivos móveis.

---

## ✨ Características Principais

### 📊 Verificação Emocional
- **5 níveis de emoção**: Muito Feliz, Feliz, Neutro, Triste, Muito Triste
- **Respostas personalizadas** baseadas no estado emocional
- **Sugestões contextualizadas** para cada sentimento

### 💬 Chat Interativo
- Converse com Dora sobre seus sentimentos
- IA responsiva com base de dados de palavras-chave
- Mensagens animadas e interface intuitiva

### 📈 Histórico de Emoções
- Rastreie suas emoções ao longo do tempo
- Armazenamento local (localStorage) com até 20 registros
- Visualização de tendências emocionais

### 🎯 Dicas de Bem-estar
- Meditação
- Atividade Física
- Sono de Qualidade
- Alimentação Saudável

### 📱 Design Responsivo
- **Mobile-first**: Totalmente otimizado para celulares
- **Funciona em rede móvel**: Carregamento rápido e leve
- **PWA Ready**: Pode ser instalada como app nativo
- **Offline Support**: Funciona sem conexão (via Service Worker)

### 🆘 Recursos de Ajuda
- Links para CVV (Centro de Valorização da Vida)
- Disque Saúde - 136
- Contato de emergência - 188

---

## 📂 Estrutura de Arquivos

```
dora_interface/
├── index.html          # Estrutura HTML principal
├── styles.css          # Estilos responsivos
├── script.js           # Lógica JavaScript
├── sw.js              # Service Worker (offline)
├── manifest.json      # Configuração PWA
└── README.md          # Este arquivo
```

---

## 🚀 Como Usar

### 1️⃣ Abrir no Navegador
Simplesmente abra o arquivo `index.html` em qualquer navegador moderno (Chrome, Firefox, Safari, Edge).

### 2️⃣ Instalação como App (PWA)
**Celular:**
- Chrome: Toque nos 3 pontos → "Instalar app"
- Safari: Compartilhar → Adicionar à Tela Inicial
- Firefox: Menu → "Instalar aplicativo"

**Desktop:**
- Chrome: Clique no ícone de instalação na barra de endereço

### 3️⃣ Usar a Interface
1. Selecione sua emoção atual (😄, 🙂, 😐, 😕, 😢)
2. Receba uma resposta personalizada da Dora
3. Veja sugestões de bem-estar
4. Converse com Dora pelo chat
5. Visualize seu histórico emocional

---

## 🔧 Tecnologias Utilizadas

- **HTML5**: Semântica moderna
- **CSS3**: Grid, Flexbox, variáveis CSS, media queries
- **JavaScript ES6+**: Orientação a objetos, localStorage API
- **Service Workers**: Suporte offline
- **Progressive Web App (PWA)**: Instalável como app nativo

---

## 📊 Dados Guardados

A aplicação utiliza **localStorage** para manter:
- Histórico de emoções (até 20 últimas entradas)
- Timestamp de cada registro
- Emojis e descrições

**Privacidade**: Todos os dados são armazenados localmente no seu dispositivo. Nenhum dado é enviado para servidores externos.

---

## 🎨 Personalização

### Mudar Cores
Edite as variáveis CSS em `styles.css`:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #48bb78;
    --danger-color: #f56565;
}
```

### Adicionar Novas Emoções
Edite em `script.js`:

```javascript
const emotionResponses = {
    'nova-emocao': {
        emoji: '😊',
        response: 'Resposta aqui...',
        suggestions: ['Sugestão 1', 'Sugestão 2', ...]
    }
};
```

### Expandir Base de Dados de Chat
Adicione palavras-chave em `script.js`:

```javascript
const chatResponses = {
    'palavra-chave': 'Resposta da Dora...'
};
```

---

## 📱 Otimizações Mobile

✅ **Viewport Meta Tag**: Escalagem apropriada  
✅ **Responsive Images**: SVG para ícones  
✅ **Minified CSS**: 1 arquivo para performance  
✅ **Lazy Loading**: Imagens carregam sob demanda  
✅ **Touch-friendly**: Botões com mínimo 48x48px  
✅ **Fast Loading**: Zero dependências externas  

---

## ⚙️ Configuração para Servidor

Se deseja hospedar em um servidor web:

1. **Copie todos os arquivos** para o diretório web
2. **Configure HTTPS** (recomendado para PWA)
3. **Configure CORS** se necessário
4. **Teste offline** com DevTools do navegador

### Exemplo com Node.js:
```bash
npm install -g http-server
cd dora_interface
http-server -p 8000
```

Acesse: `http://localhost:8000`

---

## 🔒 Segurança

- ✅ Sem dependências externas (offline-first)
- ✅ Sem transmissão de dados pessoais
- ✅ CSP headers recomendados
- ✅ Input sanitization no chat

---

## 📝 Limitações & Avisos

⚠️ **IMPORTANTE**: Esta aplicação é educacional e **NÃO substitui atendimento profissional de saúde mental**

Se você ou alguém próximo está em crise emocional:
- **CVV**: ☎️ 188 (24h)
- **Disque Saúde**: ☎️ 136
- **SAMU**: 192

---

## 🤝 Contribuições

Melhorias sugeridas:
- Integração com API de IA (OpenAI, Google Gemini)
- Backend para sincronização em múltiplos dispositivos
- Gráficos de tendências emocionais
- Notificações lembrando check-ins
- Suporte multi-idioma
- Modo escuro nativo

---

## 📄 Licença

Projeto desenvolvido para fins educacionais. Livre para uso pessoal e não-comercial.

---

## 👨‍💻 Desenvolvedor

**Estudante de ADS** - Projeto de Engenharia de Prompt e Aplicação em IA

---

## 🌟 Créditos

Desenvolvido com ❤️ para promover saúde mental e bem-estar emocional.

---

**Versão**: 1.0.0  
**Última atualização**: Maio 2026  
**Status**: Ativo ✅
