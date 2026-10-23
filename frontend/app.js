// ==============================================================================
// O MOTOR DO FRONTEND (frontend/app.js)
// ==============================================================================
// EXPLICAÇÃO GERAL PARA A APRESENTAÇÃO:
// "Professor, este arquivo é o nosso 'Garçom'. O HTML é só a cara do sistema, 
// mas é este Javascript puro que escuta os cliques do usuário e faz as requisições
// HTTP para o nosso Backend usando a função nativa 'fetch()'."
// ==============================================================================

const API_URL = "http://localhost:8000/api";

const loginSection = document.getElementById("login-section");
const dashboardSection = document.getElementById("dashboard-section");

window.onload = () => {
    // Quando a página carrega, procuramos o "Crachá" (Token JWT) no navegador
    const token = localStorage.getItem("checkmate_token");
    if (token) showDashboard(); // Se achou o crachá, pula direto pro Dashboard
};

// ==============================================================================
// 1. SISTEMA DE LOGIN E REGISTRO (O RECEPCIONISTA)
// ==============================================================================
// EXPLICAÇÃO PARA A APRESENTAÇÃO:
// "Aqui é onde capturamos o email e senha da tela e enviamos para a API.
// Se o login for um sucesso, a API nos devolve um Token JWT (Cartão Magnético).
// Nós guardamos esse token no 'localStorage' (memória do navegador) para usar depois."
let isLoginMode = true;

function toggleAuthMode(event) {
    event.preventDefault();
    isLoginMode = !isLoginMode;
    const nameGroup = document.getElementById("name-group");
    const authBtn = document.getElementById("auth-btn");
    const toggleLink = document.getElementById("toggle-mode");
    const formSubtitle = document.querySelector(".logo p");

    if (isLoginMode) {
        nameGroup.classList.add("hidden");
        authBtn.innerHTML = '<i class="fa-solid fa-right-to-bracket"></i> Entrar no Sistema';
        toggleLink.innerText = "Não tem conta? Cadastre-se";
        formSubtitle.innerText = "O seu espaço de produtividade focado.";
    } else {
        nameGroup.classList.remove("hidden");
        authBtn.innerHTML = '<i class="fa-solid fa-user-plus"></i> Criar Conta';
        toggleLink.innerText = "Já tem conta? Faça Login";
        formSubtitle.innerText = "Crie sua conta grátis para começar.";
    }
}

document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Impede que a tela pisque e recarregue
    
    // Capturamos o que o usuário digitou nas caixinhas do HTML
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorP = document.getElementById("login-error");
    const submitBtn = document.getElementById("auth-btn");

    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processando...';
    errorP.innerText = "";

    try {
        // Se estiver na aba "Cadastre-se", primeiro cria a conta no Backend!
        if (!isLoginMode) {
            const regResponse = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });

            if (!regResponse.ok) {
                const err = await regResponse.json();
                errorP.innerText = err.detail || "Erro ao criar conta!";
                submitBtn.innerHTML = '<i class="fa-solid fa-user-plus"></i> Criar Conta';
                return; // Para tudo e não faz o login
            }
        }

        // ROTA DE LOGIN (Roda sempre. Se acabou de criar conta, ele loga automaticamente!)
        const formData = new URLSearchParams();
        formData.append("username", email); 
        formData.append("password", password);

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST', body: formData, headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        if (response.ok) {
            const data = await response.json();
            // A API nos devolveu o "Crachá" de acesso (Token). Nós o guardamos no navegador!
            localStorage.setItem("checkmate_token", data.access_token);
            
            // Limpa o nome para uma próxima vez
            document.getElementById("name").value = "";
            showDashboard();
        } else {
            errorP.innerText = "E-mail ou senha incorretos!";
            submitBtn.innerHTML = '<i class="fa-solid fa-right-to-bracket"></i> Entrar no Sistema';
        }
    } catch (error) { 
        errorP.innerText = "Erro ao conectar com o servidor."; 
        submitBtn.innerHTML = isLoginMode ? '<i class="fa-solid fa-right-to-bracket"></i> Entrar no Sistema' : '<i class="fa-solid fa-user-plus"></i> Criar Conta';
    } 
});

// ==============================================================================
// 2. BUSCAR CHECKLISTS E MOSTRAR NA TELA (Apresentando o Crachá JWT)
// ==============================================================================
// EXPLICAÇÃO PARA A APRESENTAÇÃO:
// "Veja a linha do 'headers: { Authorization: Bearer token }'. É aqui que a mágica 
// acontece. Nós pegamos o Token JWT e enviamos anexado ao pedido. Se não fizermos 
// isso, o backend nos expulsa com o Erro 401 Unauthorized."
async function loadChecklists() {
    const token = localStorage.getItem("checkmate_token");
    const grid = document.getElementById("checklist-grid");
    grid.innerHTML = '<div style="color: gray;"><i class="fa-solid fa-spinner fa-spin"></i> Carregando...</div>';

    try {
        const response = await fetch(`${API_URL}/checklists/`, {
            method: 'GET', headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.status === 401) return logout();

        const checklists = await response.json();
        grid.innerHTML = ""; 

        if (checklists.length === 0) {
            grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: #94a3b8; padding: 40px; border: 1px dashed rgba(255,255,255,0.1); border-radius: 16px;"><i class="fa-solid fa-folder-open" style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;"></i><p>Nenhum checklist criado ainda.</p></div>`;
            return;
        }

        // Renderiza cada Checklist na tela
        checklists.forEach(list => {
            const card = document.createElement("div");
            card.className = "check-card";
            
            card.innerHTML = `
                <div class="check-header">
                    <h3>${list.name}</h3>
                    <div class="card-actions">
                        <button onclick="deleteChecklist(${list.id})" class="btn-delete" title="Apagar Checklist"><i class="fa-solid fa-trash"></i> Checklist</button>
                    </div>
                </div>
                
                <!-- Formulário para Criar TAREFAS dentro do checklist -->
                <div class="task-creator">
                    <input type="text" id="task-title-${list.id}" placeholder="Nome da tarefa...">
                    <div class="row">
                        <select id="task-priority-${list.id}">
                            <option value="LOW">🐢 Urgência: Baixa</option>
                            <option value="MED" selected>🚶 Urgência: Média</option>
                            <option value="HIGH">🔥 Urgência: Alta</option>
                        </select>
                        <input type="date" id="task-date-${list.id}" title="Data de Entrega">
                    </div>
                    <button onclick="createTask(${list.id})" class="btn-add-task"><i class="fa-solid fa-plus"></i> Adicionar Tarefa</button>
                </div>

                <!-- Lista de Tarefas -->
                <ul id="task-list-${list.id}" class="task-list">
                    <div style="text-align: center; font-size: 0.8rem; color: #94a3b8;"><i class="fa-solid fa-spinner fa-spin"></i></div>
                </ul>
            `;
            grid.appendChild(card);
            
            // Assim que desenha o Cartão, busca as tarefas dele no banco!
            loadTasksForChecklist(list.id);
        });
    } catch (error) { console.error("Erro", error); }
}

async function createChecklist() {
    const titleInput = document.getElementById("new-checklist-title");
    const name = titleInput.value.trim();
    if (!name) return alert("Digite o nome da lista!");

    const response = await fetch(`${API_URL}/checklists/`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem("checkmate_token")}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name })
    });

    if (response.ok) { titleInput.value = ""; loadChecklists(); } 
    else { alert("Erro ao criar checklist"); }
}

async function deleteChecklist(id) {
    if (!confirm("Deletar permanentemente este Checklist e TODAS as suas tarefas?")) return;
    
    const response = await fetch(`${API_URL}/checklists/${id}`, {
        method: 'DELETE', headers: { 'Authorization': `Bearer ${localStorage.getItem("checkmate_token")}` }
    });
    
    if (response.ok) {
        loadChecklists(); 
    } else {
        const error = await response.json();
        alert("Bloqueado pela Regra de Negócios:\n\n" + error.detail);
    }
}

// ==========================================
// 3. SISTEMA DE TAREFAS (Tasks)
// ==========================================

// Busca as tarefas daquele checklist no Banco de Dados
async function loadTasksForChecklist(checklistId) {
    const token = localStorage.getItem("checkmate_token");
    const taskContainer = document.getElementById(`task-list-${checklistId}`);

    try {
        const response = await fetch(`${API_URL}/tasks/checklist/${checklistId}`, {
            method: 'GET', headers: { 'Authorization': `Bearer ${token}` }
        });
        const tasks = await response.json();
        taskContainer.innerHTML = "";

        if (tasks.length === 0) {
            taskContainer.innerHTML = "<p style='font-size: 0.8rem; text-align:center; color:gray;'>Nenhuma tarefa ainda.</p>";
            return;
        }

        // Ordena para exibir as Não concluídas primeiro
        tasks.sort((a, b) => a.status === "DONE" ? 1 : -1);

        tasks.forEach(task => {
            const li = document.createElement("li");
            li.className = `task-item status-${task.status}`;
            
            // Pega a data (se houver) e formata para aparecer bonitinho (ex: 25/12/2026)
            let dateText = "Sem data";
            if(task.dueDate) {
                const d = new Date(task.dueDate);
                dateText = `<i class="fa-regular fa-calendar"></i> ${d.toLocaleDateString()}`;
            }

            // Pinta as prioridades
            let priorityBadge = "";
            if(task.priority === "HIGH") priorityBadge = `<span class="badge badge-HIGH">ALTA</span>`;
            else if(task.priority === "MED") priorityBadge = `<span class="badge badge-MED">MÉDIA</span>`;
            else priorityBadge = `<span class="badge badge-LOW">BAIXA</span>`;

            li.innerHTML = `
                <div class="task-info">
                    <span class="task-title">${task.title}</span>
                    <div class="task-meta">
                        ${priorityBadge}
                        <span style="color: ${task.status === 'LATE' ? 'red' : 'inherit'}">${dateText}</span>
                    </div>
                </div>
                <div class="task-actions">
                    ${task.status !== 'DONE' ? `<button onclick="completeTask(${task.id}, ${checklistId})" class="btn-check" title="Concluir"><i class="fa-solid fa-check"></i></button>` : ''}
                    <button onclick="deleteTask(${task.id}, ${checklistId})" class="btn-del-task" title="Apagar"><i class="fa-solid fa-trash"></i></button>
                </div>
            `;
            taskContainer.appendChild(li);
        });
    } catch (error) { console.error("Erro ao carregar tarefas", error); }
}

// ==============================================================================
// 4. CRIANDO DADOS (Conversando com o Escudo Pydantic)
// ==============================================================================
// EXPLICAÇÃO PARA A APRESENTAÇÃO:
// "Na hora de criar uma tarefa, nós montamos um JSON (requestBody). 
// Esse JSON tem que estar exatamente no formato que o nosso escudo de segurança 
// (Pydantic) exige no Backend. Se faltar um campo, o servidor nos barra!"
async function createTask(checklistId) {
    const title = document.getElementById(`task-title-${checklistId}`).value.trim();
    const priority = document.getElementById(`task-priority-${checklistId}`).value;
    const dateRaw = document.getElementById(`task-date-${checklistId}`).value; // Formato YYYY-MM-DD
    
    if(!title) return alert("A tarefa precisa ter um título!");

    // O Pydantic (Backend) quer a data num formato específico (ISO) ou null
    let isoDate = null;
    if(dateRaw) {
        // Pega a data do formulário e joga pro formato ISO pro Banco entender
        isoDate = new Date(dateRaw).toISOString(); 
    }

    const requestBody = {
        title: title,
        checklistId: checklistId,
        priority: priority,
        dueDate: isoDate
    };

    const token = localStorage.getItem("checkmate_token");
    const response = await fetch(`${API_URL}/tasks/`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    });

    if (response.ok) {
        document.getElementById(`task-title-${checklistId}`).value = ""; // Limpa a caixa
        document.getElementById(`task-date-${checklistId}`).value = "";
        loadTasksForChecklist(checklistId); // Atualiza só as tarefas daquele cartão!
    } else {
        const error = await response.json();
        alert("Erro: " + error.detail);
    }
}

// Atualiza a tarefa como CONCLUÍDA
async function completeTask(taskId, checklistId) {
    const requestBody = { status: "DONE" };
    const response = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${localStorage.getItem("checkmate_token")}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    });
    if (response.ok) loadTasksForChecklist(checklistId);
}

// Apaga a tarefa
async function deleteTask(taskId, checklistId) {
    if (!confirm("Deletar tarefa?")) return;
    const response = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'DELETE', headers: { 'Authorization': `Bearer ${localStorage.getItem("checkmate_token")}` }
    });
    if (response.ok) loadTasksForChecklist(checklistId);
}

// ==========================================
// FUNÇÕES AUXILIARES E NAVEGAÇÃO DE ABAS
// ==========================================
function showDashboard() {
    loginSection.classList.add("hidden");
    loginSection.classList.remove("active");
    dashboardSection.classList.remove("hidden");
    dashboardSection.classList.add("active");
    switchTab('checklists'); // Força abrir na aba certa
}

function logout() {
    localStorage.removeItem("checkmate_token");
    dashboardSection.classList.add("hidden");
    dashboardSection.classList.remove("active");
    loginSection.classList.remove("hidden");
    loginSection.classList.add("active");
}

function switchTab(tabName) {
    // Esconde tudo
    document.getElementById("view-checklists").classList.add("hidden");
    document.getElementById("view-reports").classList.add("hidden");
    
    // Tira a cor "ativa" dos menus
    document.getElementById("menu-checklists").classList.remove("active");
    document.getElementById("menu-reports").classList.remove("active");

    // Mostra só a aba que clicou
    document.getElementById(`view-${tabName}`).classList.remove("hidden");
    document.getElementById(`menu-${tabName}`).classList.add("active");

    // Se for checklist carrega eles, se for relatórios carrega a API de relatórios
    if(tabName === 'checklists') {
        loadChecklists();
        document.querySelector(".creator-card").classList.remove("hidden"); // Mostra o criador de checklist
    } else if(tabName === 'reports') {
        document.querySelector(".creator-card").classList.add("hidden"); // Esconde na aba relatórios
        loadReports();
    }
}

// Consome a API de Relatórios
async function loadReports() {
    const token = localStorage.getItem("checkmate_token");
    const response = await fetch(`${API_URL}/dashboard/`, {
        method: 'GET', headers: { 'Authorization': `Bearer ${token}` }
    });

    if(response.ok) {
        const data = await response.json();
        // Atualiza os painéis na tela!
        document.getElementById("kpi-total").innerText = data.total_tasks;
        document.getElementById("kpi-completed").innerText = data.completed_tasks;
        document.getElementById("kpi-pending").innerText = data.pending_tasks;
        document.getElementById("kpi-late").innerText = data.late_tasks;
    }
}
