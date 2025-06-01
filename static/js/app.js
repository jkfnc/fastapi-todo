const API_BASE = '/api/todos';

class TodoApp {
    constructor() {
        this.todos = [];
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadTodos();
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('add-todo-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTodo();
        });

        // Filter buttons
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.setFilter(btn.dataset.filter);
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
    }

    async loadTodos() {
        this.showLoading(true);
        this.hideError();

        try {
            const response = await fetch(API_BASE);
            if (!response.ok) throw new Error('Failed to load todos');
            
            this.todos = await response.json();
            this.renderTodos();
        } catch (error) {
            this.showError('Failed to load todos. Please try again.');
            console.error('Error loading todos:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async addTodo() {
        const titleInput = document.getElementById('todo-title');
        const descriptionInput = document.getElementById('todo-description');
        
        const title = titleInput.value.trim();
        const description = descriptionInput.value.trim();

        if (!title) return;

        try {
            const response = await fetch(API_BASE + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title,
                    description,
                    completed: false
                })
            });

            if (!response.ok) throw new Error('Failed to add todo');

            const newTodo = await response.json();
            this.todos.unshift(newTodo);
            this.renderTodos();

            // Clear form
            titleInput.value = '';
            descriptionInput.value = '';
        } catch (error) {
            this.showError('Failed to add todo. Please try again.');
            console.error('Error adding todo:', error);
        }
    }

    async toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (!todo) return;

        try {
            const response = await fetch(`${API_BASE}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    completed: !todo.completed
                })
            });

            if (!response.ok) throw new Error('Failed to update todo');

            const updatedTodo = await response.json();
            const index = this.todos.findIndex(t => t.id === id);
            this.todos[index] = updatedTodo;
            this.renderTodos();
        } catch (error) {
            this.showError('Failed to update todo. Please try again.');
            console.error('Error updating todo:', error);
        }
    }

    async deleteTodo(id) {
        if (!confirm('Are you sure you want to delete this todo?')) return;

        try {
            const response = await fetch(`${API_BASE}/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) throw new Error('Failed to delete todo');

            this.todos = this.todos.filter(t => t.id !== id);
            this.renderTodos();
        } catch (error) {
            this.showError('Failed to delete todo. Please try again.');
            console.error('Error deleting todo:', error);
        }
    }

    setFilter(filter) {
        this.currentFilter = filter;
        this.renderTodos();
    }

    getFilteredTodos() {
        switch (this.currentFilter) {
            case 'active':
                return this.todos.filter(t => !t.completed);
            case 'completed':
                return this.todos.filter(t => t.completed);
            default:
                return this.todos;
        }
    }

    renderTodos() {
        const todoList = document.getElementById('todo-list');
        const emptyState = document.getElementById('empty-state');
        const filteredTodos = this.getFilteredTodos();

        if (filteredTodos.length === 0) {
            todoList.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';
        todoList.innerHTML = filteredTodos.map(todo => this.createTodoHTML(todo)).join('');

        // Add event listeners to new elements
        todoList.querySelectorAll('.todo-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const id = parseInt(e.target.dataset.id);
                this.toggleTodo(id);
            });
        });

        todoList.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.dataset.id);
                this.deleteTodo(id);
            });
        });
    }

    createTodoHTML(todo) {
        const createdDate = new Date(todo.created_at).toLocaleDateString();
        
        return `
            <li class="todo-item ${todo.completed ? 'completed' : ''}">
                <input 
                    type="checkbox" 
                    class="todo-checkbox" 
                    data-id="${todo.id}"
                    ${todo.completed ? 'checked' : ''}
                >
                <div class="todo-content">
                    <h3 class="todo-title">${this.escapeHtml(todo.title)}</h3>
                    ${todo.description ? `<p class="todo-description">${this.escapeHtml(todo.description)}</p>` : ''}
                    <div class="todo-meta">
                        <span class="todo-date">📅 ${createdDate}</span>
                        ${todo.completed ? '<span class="todo-status">✅ Completed</span>' : ''}
                    </div>
                </div>
                <div class="todo-actions">
                    <button class="btn-delete" data-id="${todo.id}">Delete</button>
                </div>
            </li>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }

    showError(message) {
        const errorElement = document.getElementById('error-message');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    }

    hideError() {
        document.getElementById('error-message').style.display = 'none';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp();
});