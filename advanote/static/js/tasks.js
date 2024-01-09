function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function updatePageWithNewTask(task) {
    const taskListContainer = document.querySelector('.task-list');

    const newTaskElement = document.createElement('div');
    newTaskElement.classList.add('task');
    newTaskElement.textContent = task.title;

    newTaskElement.setAttribute('data-id', task.id);

    newTaskElement.addEventListener('click', function(event) {
        const taskId = event.currentTarget.getAttribute('data-id');
    });

    taskListContainer.appendChild(newTaskElement);
}

function handleAddTask() {
    const overlay = document.getElementById('overlay');
    const addTaskBtn = document.querySelector('.add-task-btn');

    if (addTaskBtn) {
        addTaskBtn.addEventListener('click', function() {
            fetch('/tasks/add_task/')
                .then(response => response.text())
                .then(data => {
                    overlay.innerHTML = data;
                    overlay.style.display = 'flex';

                    const taskForm = overlay.querySelector('#task-form');
                    taskForm.addEventListener('submit', function(event) {
                        event.preventDefault();

                        const formData = new FormData(taskForm);

                        fetch(taskForm.action, {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        })
                        .then(response => {
                            if (response.ok) {
                                overlay.style.display = 'none';
                                taskForm.reset();
                                location.reload();
                            }
                        })
                        .catch(error => {
                            console.error('Fetch error:', error);
                        });
                    });
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                });
        });
    } else {
        console.error('Кнопка "Добавить задачу" не найдена');
    }
}

function openEditForm(taskId) {
    fetch(`/tasks/edit_task/${taskId}/`)
        .then(response => response.text())
        .then(data => {
            const overlay = document.getElementById('overlay');
            overlay.innerHTML = data;
            overlay.style.display = 'flex';

            const taskForm = overlay.querySelector('#task-form');
            taskForm.addEventListener('submit', function(event) {
                event.preventDefault();
                saveTask(taskForm, overlay);
            });
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
}

function saveTask(taskForm, overlay) {
    const formData = new FormData(taskForm);

    fetch(taskForm.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            overlay.style.display = 'none';
            taskForm.reset();
            location.reload();
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}

function handleDeleteTask(taskId) {
    if (confirm('Вы уверены, что хотите удалить эту задачу?')) {
        fetch(`/tasks/delete_task/${taskId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Ошибка при удалении задачи:', error);
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    handleAddTask();

    const tasks = document.querySelectorAll('.task');
    const circles = document.querySelectorAll('.circle');

    circles.forEach(circle => {
        circle.addEventListener('click', function(event) {
            event.stopPropagation();
            circle.classList.toggle('checked');
            const taskText = circle.nextElementSibling;
            taskText.classList.toggle('checked-text');

            const taskId = circle.getAttribute('data-task-id');
            const isDone = circle.classList.contains('checked');

            fetch(`/tasks/update_task_status/${taskId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ isDone: isDone })
            })
            .then(response => {
                if (response.ok) {
                    console.log('Статус обновлен успешно!');
                } else {
                    console.error('Ошибка при обновлении статуса:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке запроса:', error);
            });
        });
    });

    tasks.forEach(task => {
        const taskId = task.getAttribute('data-task-id');
        const deleteIcon = task.querySelector('.delete-icon');

        if (deleteIcon !== null){
        deleteIcon.addEventListener('click', function(event) {
                event.stopPropagation();
                handleDeleteTask(taskId);
            });
        }

        task.addEventListener('click', function() {
            openEditForm(taskId);
        });
    });
});

document.addEventListener('click', function(event) {
    const overlay = document.getElementById('overlay');
    const taskForm = overlay.querySelector('#task-form');

    if (!taskForm.contains(event.target)) {
        overlay.style.display = 'none';
    }
});