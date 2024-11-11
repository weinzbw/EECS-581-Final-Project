# Tasks
# Code Artifact 8
# The purpose of tasks is to manage the tasks of the game as a class, simplifying a lot of functions needed for them.
# Name: Sam Harrison
# Creation Date: 10/26/24
# Revision Date: N/A
# Preconditions: task list (list), tasks (str), surface (Surface)
# Postconditions: add_task (str and False), complete_task (str and True), toggle_visibility (True and False), render (True)
# Error & Exceptions: There are none so far.
# Side Effects: render's text, the visibility of tasks
# Invariants: the tasks dictionary, the visibility of tasks
# Faults: fonts aren't handled, rendering errors aren't handled
import pygame

class Tasks:
    def __init__(self, font_size=24, tasks=None):
        self.font = pygame.font.SysFont("Courier New", font_size) # sets the font to the same as the one used in main
        # uses an empty list of no tasks are given; when a task is False, it's incomplete (made with the help of ChatGPT)
        self.tasks = {task: False for task in (tasks if tasks else [])}
        self.is_visible = False # when True, the task is needed to be done

    def add_task(self, task):
        self.tasks[task] = False # this just adds a task

    def complete_task(self, task):
        if task in self.tasks:
            self.tasks[task] = True # this marks a task as complete when it's prompted and available

    def toggle_visibility(self):
        self.is_visible = not self.is_visible # this sets a task to the opposite

    def render(self, surface):
        if not self.is_visible: # the rest is ignored if the task is complete
            return

        # this draws the task list starting at (20, 20); the task list is iterated over until all are displayed
        x, y = 20, 20
        for task, completed in self.tasks.items():
            if not completed:
                task_text = self.font.render(f"- {task}", True, (0, 0, 0))
                surface.blit(task_text, (x, y))
                y += 25 
