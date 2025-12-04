import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Carrega tarefas do arquivo JSON"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        """Salva tarefas no arquivo JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)
    
    # CREATE - Criar nova tarefa
    def create_task(self, title, description=''):
        """Cria uma nova tarefa"""
        if not title or title.strip() == '':
            raise ValueError("Título não pode ser vazio")
        
        task = {
            'id': len(self.tasks) + 1,
            'title': title.strip(),
            'description': description.strip(),
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    # READ - Ler tarefas
    def get_all_tasks(self):
        """Retorna todas as tarefas"""
        return self.tasks
    
    def get_task_by_id(self, task_id):
        """Busca uma tarefa pelo ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    # UPDATE - Atualizar tarefa
    def update_task(self, task_id, title=None, description=None, completed=None):
        """Atualiza uma tarefa existente"""
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Tarefa com ID {task_id} não encontrada")
        
        if title is not None:
            if title.strip() == '':
                raise ValueError("Título não pode ser vazio")
            task['title'] = title.strip()
        
        if description is not None:
            task['description'] = description.strip()
        
        if completed is not None:
            task['completed'] = completed
        
        self.save_tasks()
        return task
    
    # DELETE - Deletar tarefa
    def delete_task(self, task_id):
        """Deleta uma tarefa pelo ID"""
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Tarefa com ID {task_id} não encontrada")
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def clear_all_tasks(self):
        """Remove todas as tarefas (útil para testes)"""
        self.tasks = []
        self.save_tasks()


# Interface de linha de comando
def main():
    manager = TaskManager()
    
    while True:
        print("\n=== GERENCIADOR DE TAREFAS ===")
        print("1. Criar tarefa")
        print("2. Listar tarefas")
        print("3. Atualizar tarefa")
        print("4. Deletar tarefa")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == '1':
            title = input("Título da tarefa: ")
            description = input("Descrição (opcional): ")
            try:
                task = manager.create_task(title, description)
                print(f"✓ Tarefa criada com ID: {task['id']}")
            except ValueError as e:
                print(f"✗ Erro: {e}")
        
        elif choice == '2':
            tasks = manager.get_all_tasks()
            if not tasks:
                print("Nenhuma tarefa encontrada.")
            else:
                print("\n--- TAREFAS ---")
                for task in tasks:
                    status = "✓" if task['completed'] else "○"
                    print(f"{status} [{task['id']}] {task['title']}")
                    if task['description']:
                        print(f"    Descrição: {task['description']}")
        
        elif choice == '3':
            task_id = int(input("ID da tarefa: "))
            print("Deixe em branco para não alterar")
            title = input("Novo título: ")
            description = input("Nova descrição: ")
            completed = input("Completada? (s/n): ")
            
            try:
                manager.update_task(
                    task_id,
                    title if title else None,
                    description if description else None,
                    True if completed.lower() == 's' else False if completed.lower() == 'n' else None
                )
                print("✓ Tarefa atualizada!")
            except ValueError as e:
                print(f"✗ Erro: {e}")
        
        elif choice == '4':
            task_id = int(input("ID da tarefa: "))
            try:
                manager.delete_task(task_id)
                print("✓ Tarefa deletada!")
            except ValueError as e:
                print(f"✗ Erro: {e}")
        
        elif choice == '5':
            print("Até logo!")
            break


if __name__ == '__main__':
    main()