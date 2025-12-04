import unittest
import os
from task_manager import TaskManager

class TestTaskManagerIntegration(unittest.TestCase):
    """Testes de Integração - Testam fluxos completos do sistema"""
    
    def setUp(self):
        """Executado antes de cada teste"""
        self.test_file = 'test_integration_tasks.json'
        self.manager = TaskManager(self.test_file)
        self.manager.clear_all_tasks()
    
    def tearDown(self):
        """Executado após cada teste"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_complete_crud_workflow(self):
        """Teste: Fluxo completo de CRUD em sequência"""
        # CREATE: Criar uma tarefa
        task = self.manager.create_task("Estudar para prova", "Matemática")
        self.assertEqual(task['id'], 1)
        
        # READ: Ler a tarefa criada
        found = self.manager.get_task_by_id(1)
        self.assertIsNotNone(found)
        self.assertEqual(found['title'], "Estudar para prova")
        
        # UPDATE: Atualizar a tarefa
        updated = self.manager.update_task(1, completed=True)
        self.assertTrue(updated['completed'])
        
        # READ novamente: Verificar se mudança persistiu
        found_again = self.manager.get_task_by_id(1)
        self.assertTrue(found_again['completed'])
        
        # DELETE: Deletar a tarefa
        self.manager.delete_task(1)
        
        # READ final: Verificar se foi deletada
        deleted = self.manager.get_task_by_id(1)
        self.assertIsNone(deleted)
    
    def test_persistence_across_instances(self):
        """Teste: Dados persistem entre diferentes instâncias"""
        # Criar tarefa na primeira instância
        manager1 = TaskManager(self.test_file)
        manager1.clear_all_tasks()
        task = manager1.create_task("Tarefa Persistente")
        task_id = task['id']
        
        # Criar segunda instância e verificar se dados existem
        manager2 = TaskManager(self.test_file)
        loaded_task = manager2.get_task_by_id(task_id)
        
        self.assertIsNotNone(loaded_task)
        self.assertEqual(loaded_task['title'], "Tarefa Persistente")
    
    def test_multiple_operations_sequence(self):
        """Teste: Múltiplas operações em sequência"""
        # Criar várias tarefas
        task1 = self.manager.create_task("Tarefa 1", "Descrição 1")
        task2 = self.manager.create_task("Tarefa 2", "Descrição 2")
        task3 = self.manager.create_task("Tarefa 3", "Descrição 3")
        
        # Verificar que todas foram criadas
        all_tasks = self.manager.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)
        
        # Atualizar uma tarefa
        self.manager.update_task(task2['id'], completed=True)
        
        # Deletar outra tarefa
        self.manager.delete_task(task1['id'])
        
        # Verificar estado final
        remaining = self.manager.get_all_tasks()
        self.assertEqual(len(remaining), 2)
        
        # Verificar que task2 foi completada
        task2_updated = self.manager.get_task_by_id(task2['id'])
        self.assertTrue(task2_updated['completed'])
        
        # Verificar que task1 foi deletada
        task1_deleted = self.manager.get_task_by_id(task1['id'])
        self.assertIsNone(task1_deleted)
        
        # Verificar que task3 ainda existe
        task3_exists = self.manager.get_task_by_id(task3['id'])
        self.assertIsNotNone(task3_exists)
    
    def test_update_after_multiple_creates(self):
        """Teste: Atualizar tarefa correta após criar várias"""
        # Criar 5 tarefas
        tasks = []
        for i in range(1, 6):
            task = self.manager.create_task(f"Tarefa {i}")
            tasks.append(task)
        
        # Atualizar apenas a tarefa do meio
        self.manager.update_task(tasks[2]['id'], title="Tarefa ATUALIZADA")
        
        # Verificar que apenas a tarefa correta foi atualizada
        for i, task in enumerate(tasks):
            current = self.manager.get_task_by_id(task['id'])
            if i == 2:
                self.assertEqual(current['title'], "Tarefa ATUALIZADA")
            else:
                self.assertEqual(current['title'], f"Tarefa {i+1}")
    
    def test_error_handling_in_workflow(self):
        """Teste: Sistema se recupera de erros durante fluxo"""
        # Criar tarefa válida
        task = self.manager.create_task("Tarefa Válida")
        
        # Tentar criar tarefa inválida
        try:
            self.manager.create_task("")
        except ValueError:
            pass  # Erro esperado
        
        # Verificar que sistema ainda funciona
        all_tasks = self.manager.get_all_tasks()
        self.assertEqual(len(all_tasks), 1)
        
        # Tentar atualizar tarefa inexistente
        try:
            self.manager.update_task(999, title="Teste")
        except ValueError:
            pass  # Erro esperado
        
        # Verificar que tarefa original não foi afetada
        original = self.manager.get_task_by_id(task['id'])
        self.assertEqual(original['title'], "Tarefa Válida")
    
    def test_json_file_creation_and_format(self):
        """Teste: Arquivo JSON é criado corretamente"""
        # Criar tarefa
        self.manager.create_task("Teste JSON", "Descrição teste")
        
        # Verificar que arquivo existe
        self.assertTrue(os.path.exists(self.test_file))
        
        # Verificar que pode ser lido como JSON válido
        import json
        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn('id', data[0])
        self.assertIn('title', data[0])
        self.assertIn('description', data[0])
        self.assertIn('completed', data[0])


if __name__ == '__main__':
    unittest.main(verbosity=2)