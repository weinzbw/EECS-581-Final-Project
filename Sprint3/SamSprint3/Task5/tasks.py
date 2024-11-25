# Tasks
# Code Artifact 8
# The purpose of tasks is to manage the tasks of the game as a class, simplifying a lot of functions needed for them.
# Name: Sam Harrison
# Creation Date: 10/26/24
# Revision Date: 11/24/24 - made tasks easier to read by scaling them to fit and added a gray box
# Preconditions: task list (list), tasks (str), surface (Surface)
# Postconditions: add_task (str and False), complete_task (str and True), toggle_visibility (True and False), render (True)
# Error & Exceptions: There are none so far.
# Side Effects: render's text, the visibility of tasks
# Invariants: the tasks dictionary, the visibility of tasks
# Faults: fonts aren't handled, rendering errors aren't handled
import pygame

class Tasks:
    def __init__(self, font_size=24, tasks=None, padding=10):
        self.font_size = font_size
        self.base_font = pygame.font.SysFont("Courier New", font_size) # sets the font to the same as the one used in main
        # uses an empty list of no tasks are given; when a task is False, it's incomplete (made with the help of ChatGPT)
        self.tasks = {task: False for task in (tasks if tasks else [])}
        self.is_visible = False # when True, the task is displayed
        self.padding = padding

    def add_task(self, task):
        self.tasks[task] = False # this just adds a task

    def complete_task(self, task):
        if task in self.tasks:
            self.tasks[task] = True # this marks a task as complete when it's prompted and available

    def toggle_visibility(self):
        self.is_visible = not self.is_visible # this toggles the visibility of tasks

    def calculate_dimensions(self):
        height = max(len(self.tasks) * (self.font_size + self.padding), 50) + 40 # ensures min size
        return 200, height

    def render(self, surface):
        if not self.is_visible:
            return

        width, height = self.calculate_dimensions()
        tasks_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        tasks_surface.fill((0, 0, 0, 180))

        title_text = self.base_font.render("Tasks:", True, (255, 255, 255))
        tasks_surface.blit(title_text, (10, 10))

        y_offset = 40
        for task, completed in self.tasks.items():
            font_size = self.font_size
            temp_font = pygame.font.SysFont("Courier New", font_size)
            task_text = temp_font.render(task, True, (255, 255, 255))
            while task_text.get_width() > width - 20 and font_size > 8:
                font_size -= 1
                temp_font = pygame.font.SysFont("Courier New", font_size)
                task_text = temp_font.render(task, True, (255, 255, 255))
            tasks_surface.blit(task_text, (10, y_offset))
            y_offset += font_size + self.padding

        surface.blit(tasks_surface, (20, 20))
