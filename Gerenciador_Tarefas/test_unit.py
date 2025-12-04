import unittest
import os
from task_manager import TaskManager

class TestTaskManagerUnit(unittest.TestCase):
    """Testes Unitários - Testam cada função individualmente"""
    
    def setUp(self):
        """Executado antes de cada teste"""
        self.test_file = 'test_tasks.json'
        self.manager = TaskManager(self.test_file)
        self.manager.clear_all_tasks()
    
    def tearDown(self):
        """Executado após cada teste"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    # Testes da função CREATE
    def test_create_task_success(self):
        """Teste: Criar tarefa com sucesso"""
        task = self.manager.create_task("Estudar Python", "Revisar testes")
        
        self.assertEqual(task['title'], "Estudar Python")
        self.assertEqual(task['description'], "Revisar testes")
        self.assertEqual(task['completed'], False)
        self.assertEqual(task['id'], 1)
    
    def test_create_task_empty_title(self):
        """Teste: Não pode criar tarefa sem título"""
        with self.assertRaises(ValueError):
            self.manager.create_task("")
    
    def test_create_task_whitespace_title(self):
        """Teste: Não pode criar tarefa com apenas espaços"""
        with self.assertRaises(ValueError):
            self.manager.create_task("   ")
    
    # Testes da função READ
    def test_get_all_tasks_empty(self):
        """Teste: Lista vazia quando não há tarefas"""
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_get_all_tasks_multiple(self):
        """Teste: Retorna todas as tarefas criadas"""
        self.manager.create_task("Tarefa 1")
        self.manager.create_task("Tarefa 2")
        self.manager.create_task("Tarefa 3")
        
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 3)
    
    def test_get_task_by_id_success(self):
        """Teste: Buscar tarefa por ID existente"""
        created = self.manager.create_task("Minha Tarefa")
        found = self.manager.get_task_by_id(created['id'])
        
        self.assertIsNotNone(found)
        self.assertEqual(found['title'], "Minha Tarefa")
    
    def test_get_task_by_id_not_found(self):
        """Teste: Buscar tarefa com ID inexistente"""
        task = self.manager.get_task_by_id(999)
        self.assertIsNone(task)
    
    # Testes da função UPDATE
    def test_update_task_title(self):
        """Teste: Atualizar título da tarefa"""
        task = self.manager.create_task("Título Original")
        updated = self.manager.update_task(task['id'], title="Título Novo")
        
        self.assertEqual(updated['title'], "Título Novo")
    
    def test_update_task_completed(self):
        """Teste: Marcar tarefa como completada"""
        task = self.manager.create_task("Fazer exercício")
        updated = self.manager.update_task(task['id'], completed=True)
        
        self.assertTrue(updated['completed'])
    
    def test_update_task_not_found(self):
        """Teste: Erro ao atualizar tarefa inexistente"""
        with self.assertRaises(ValueError):
            self.manager.update_task(999, title="Novo título")
    
    def test_update_task_empty_title(self):
        """Teste: Não pode atualizar com título vazio"""
        task = self.manager.create_task("Tarefa")
        
        with self.assertRaises(ValueError):
            self.manager.update_task(task['id'], title="")
    
    # Testes da função DELETE
    def test_delete_task_success(self):
        """Teste: Deletar tarefa com sucesso"""
        task = self.manager.create_task("Tarefa temporária")
        result = self.manager.delete_task(task['id'])
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_all_tasks()), 0)
    
    def test_delete_task_not_found(self):
        """Teste: Erro ao deletar tarefa inexistente"""
        with self.assertRaises(ValueError):
            self.manager.delete_task(999)
    
    def test_delete_task_multiple(self):
        """Teste: Deletar uma tarefa não afeta outras"""
        task1 = self.manager.create_task("Tarefa 1")
        task2 = self.manager.create_task("Tarefa 2")
        task3 = self.manager.create_task("Tarefa 3")
        
        self.manager.delete_task(task2['id'])
        
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertIsNotNone(self.manager.get_task_by_id(task1['id']))
        self.assertIsNotNone(self.manager.get_task_by_id(task3['id']))
        self.assertIsNone(self.manager.get_task_by_id(task2['id']))


if __name__ == '__main__':
    unittest.main(verbosity=2)