document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('users')) localStorage.setItem('users', JSON.stringify([]));
    if (!localStorage.getItem('todos')) localStorage.setItem('todos', JSON.stringify([]));

    const screens = {
        login: document.getElementById('login-screen'),
        register: document.getElementById('register-screen'),
        dashboard: document.getElementById('dashboard-screen')
    };
    
    const forms = {
        login: document.getElementById('login-form'),
        register: document.getElementById('register-form'),
        todo: document.getElementById('todo-form')
    };
    
    const errors = {
        login: document.getElementById('login-error'),
        register: document.getElementById('register-error')
    };
    
    const elements = {
        greeting: document.getElementById('user-greeting'),
        todoList: document.getElementById('todo-list'),
        emptyState: document.getElementById('empty-state')
    };

    let currentUser = null;

    const showError = (element, message) => {
        element.textContent = message;
        element.classList.remove('hidden');
    };

    const hideErrors = () => {
        Object.values(errors).forEach(el => el.classList.add('hidden'));
    };

    const switchScreen = (screenName) => {
        Object.values(screens).forEach(screen => {
            screen.classList.add('hidden');
            if(screenName !== 'dashboard') {
                screen.classList.remove('self-center');
            }
        });
        hideErrors();
        
        screens[screenName].classList.remove('hidden');
        if(screenName !== 'dashboard') {
            screens[screenName].classList.add('self-center');
        }
    };

    const checkAuthStatus = () => {
        const userData = localStorage.getItem('currentUser');
        if (userData) {
            currentUser = JSON.parse(userData);
            elements.greeting.textContent = `Olá, ${currentUser.name}`;
            switchScreen('dashboard');
            renderTodos();
        } else {
            currentUser = null;
            switchScreen('login');
        }
    };

    document.getElementById('show-register').addEventListener('click', () => switchScreen('register'));
    document.getElementById('show-login').addEventListener('click', () => switchScreen('login'));
    document.getElementById('logout-btn').addEventListener('click', () => {
        localStorage.removeItem('currentUser');
        checkAuthStatus();
    });

    forms.register.addEventListener('submit', (e) => {
        e.preventDefault();
        hideErrors();
        const name = document.getElementById('register-name').value.trim();
        const email = document.getElementById('register-email').value.trim();
        const password = document.getElementById('register-password').value.trim();

        if (!name || !email || !password) return showError(errors.register, 'Preencha todos os campos.');

        const users = JSON.parse(localStorage.getItem('users'));
        if (users.some(u => u.email === email)) return showError(errors.register, 'E-mail já está em uso.');

        const newUser = { id: Date.now().toString(), name, email, password };
        users.push(newUser);
        localStorage.setItem('users', JSON.stringify(users));

        localStorage.setItem('currentUser', JSON.stringify({ id: newUser.id, name: newUser.name, email: newUser.email }));
        forms.register.reset();
        checkAuthStatus();
    });

    forms.login.addEventListener('submit', (e) => {
        e.preventDefault();
        hideErrors();
        const email = document.getElementById('login-email').value.trim();
        const password = document.getElementById('login-password').value.trim();

        if (!email || !password) return showError(errors.login, 'Informe e-mail e senha.');

        const users = JSON.parse(localStorage.getItem('users'));
        const user = users.find(u => u.email === email);

        if (!user) return showError(errors.login, 'E-mail não cadastrado.');
        if (user.password !== password) return showError(errors.login, 'Senha incorreta.');

        localStorage.setItem('currentUser', JSON.stringify({ id: user.id, name: user.name, email: user.email }));
        forms.login.reset();
        checkAuthStatus();
    });

    const getTodos = () => JSON.parse(localStorage.getItem('todos')) || [];
    const saveTodos = (todos) => localStorage.setItem('todos', JSON.stringify(todos));

    const getBadgeColor = (type) => {
        switch(type) {
            case 'Trabalho': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
            case 'Pessoal': return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
            case 'Estudos': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
            default: return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
        }
    };

    const renderTodos = () => {
        const allTodos = getTodos();
        const userTodos = allTodos.filter(t => t.userId === currentUser.email);
        
        elements.todoList.innerHTML = '';
        
        if (userTodos.length === 0) {
            elements.emptyState.classList.remove('hidden');
            return;
        }
        
        elements.emptyState.classList.add('hidden');

        userTodos.sort((a, b) => {
            if (a.done === b.done) return b.id - a.id; 
            return a.done ? 1 : -1;
        });

        userTodos.forEach(todo => {
            const card = document.createElement('div');
            card.className = `bg-slate-800/50 border border-slate-700/50 rounded-xl p-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 transition-all duration-300 hover:bg-slate-800 ${todo.done ? 'task-done' : ''}`;
            
            const badgeClass = getBadgeColor(todo.type);
            
            card.innerHTML = `
                <div class="flex-1">
                    <div class="flex items-center gap-3 mb-1">
                        <h3 class="text-lg font-medium text-white ${todo.done ? 'line-through text-slate-400' : ''}">${todo.title}</h3>
                        <span class="text-xs px-2.5 py-0.5 rounded-full border font-medium ${badgeClass}">${todo.type}</span>
                    </div>
                    ${todo.description ? `<p class="text-slate-400 text-sm mt-2 ${todo.done ? 'line-through text-slate-500' : ''}">${todo.description}</p>` : ''}
                </div>
                ${!todo.done ? `
                    <button onclick="window.completeTodo(${todo.id})" class="shrink-0 bg-slate-700 hover:bg-emerald-600/90 text-white p-2 rounded-lg transition-colors border border-slate-600 hover:border-emerald-500" title="Concluir tarefa">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                    </button>
                ` : `
                    <span class="shrink-0 text-emerald-500 flex items-center gap-1 font-medium text-sm">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                        Concluída
                    </span>
                `}
            `;
            
            elements.todoList.appendChild(card);
        });
    };

    forms.todo.addEventListener('submit', (e) => {
        e.preventDefault();
        const titleInput = document.getElementById('todo-title');
        const typeInput = document.getElementById('todo-type');
        const descInput = document.getElementById('todo-desc');

        const title = titleInput.value.trim();
        const type = typeInput.value;
        const description = descInput.value.trim();

        if (!title) return;

        const newTodo = {
            id: Date.now(),
            userId: currentUser.email,
            title,
            type,
            description,
            done: false
        };

        const todos = getTodos();
        todos.push(newTodo);
        saveTodos(todos);

        forms.todo.reset();
        renderTodos();
    });

    window.completeTodo = (id) => {
        const todos = getTodos();
        const index = todos.findIndex(t => t.id === id);
        if (index > -1) {
            todos[index].done = true;
            saveTodos(todos);
            renderTodos();
        }
    };

    checkAuthStatus();
});
