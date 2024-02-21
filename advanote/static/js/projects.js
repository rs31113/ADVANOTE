document.addEventListener('DOMContentLoaded', function() {
    const projectElements = document.querySelectorAll('.task');

    projectElements.forEach(function(element) {
        const projectId = element.dataset.projectId;

        const deleteButton = element.querySelector('.delete-icon');
        const editButton = element.querySelector('.edit-icon');

        deleteButton.addEventListener('click', function(event) {
            event.preventDefault();

            fetch(`/projects/delete_project/${projectId}/`, {
                method: 'DELETE',
                headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Ошибка удаления проекта');
                }
            })
            .catch(error => {
                console.error('Произошла ошибка:', error);
            });

            event.stopPropagation();
        });

        editButton.addEventListener('click', function(event) {
            event.preventDefault();

            window.location.href = `/projects/edit/${projectId}/`;

            event.stopPropagation();
        });

        element.addEventListener('click', function() {
            window.location.href = `/projects/${projectId}/`;
        });
    });
});
