function fetchNotes() {
    fetch('/notes/get_notes/')
        .then(response => response.json())
        .then(data => {
            var dropdown = document.getElementById("notesDropdown");
            dropdown.innerHTML = "";

            if (data.length === 0) {
                dropdown.innerHTML = '<a style="cursor: default">Нет заметок</a>';
            } else {
                data.forEach(note => {
                    var noteLink = document.createElement("a");
                    noteLink.href = `/notes/${note.id}/`;

                    var noteTitle = document.createElement("span");
                    noteTitle.textContent = note.title;
                    noteTitle.classList.add('note-title');
                    noteLink.appendChild(noteTitle);

                    dropdown.appendChild(noteLink);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
}

function deleteNote() {
    const noteId = window.location.pathname.split('/').filter(Boolean).pop();

    fetch(`/notes/${noteId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/notes/';
        } else {
            console.error('Ошибка при удалении заметки');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function toggleNotesDropdown() {
    var dropdown = document.getElementById("notesDropdown");
    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";

    localStorage.setItem('dropdownDisplay', dropdown.style.display);

    if (dropdown.style.display === "block") {
        fetchNotes();
    }
}

function saveNoteOnChange(noteForm) {
    const formData = new FormData(noteForm);
    const noteId = window.location.pathname.split('/').filter(Boolean).pop();

    fetch(`/notes/${noteId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            console.log('Изменения сохранены');
            updateDropdownItem(noteId, formData.get('title'));
        } else {
            console.error('Произошла ошибка при сохранении изменений');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function handleAddNote() {
    document.addEventListener('click', function(event) {
        const addNoteBtn = event.target.closest('.add-note-btn');
        const overlay = document.getElementById('overlay');

        if (addNoteBtn) {
            fetch('/notes/add_note/')
                .then(response => response.text())
                .then(data => {
                    overlay.innerHTML = data;
                    overlay.style.display = 'flex';

                    const noteForm = overlay.querySelector('#note-form');

                    const handleFieldBlur = function(event) {
                        const isNewNote = noteForm.getAttribute('data-is-new-note');
                        if (isNewNote === 'true') {
                            saveNewNoteOnChange(noteForm);
                        }
                    };

                    const inputFields = noteForm.querySelectorAll('input, textarea');

                    inputFields.forEach(field => {
                        field.addEventListener('blur', handleFieldBlur);
                    });

                    overlay.addEventListener('click', function(event) {
                        if (event.target === overlay) {
                            if (noteForm.getAttribute('data-is-new-note') === 'true') {
                                saveNewNoteOnChange(noteForm);
                            }
                            overlay.style.display = 'none';
                        }
                    });
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                });
        } else {
            console.error('Кнопка "Добавить заметку" не найдена');
        }
    });
}


function saveNewNoteOnChange(noteForm) {
    const formData = new FormData(noteForm);

    fetch('/notes/add_note/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            console.log('Новая заметка создана');
            noteForm.setAttribute('data-is-new-note', 'false');
        } else {
            console.error('Ошибка при создании новой заметки');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}


const formFields = document.querySelectorAll('#note-form input, #note-form textarea');

formFields.forEach(field => {
    field.addEventListener('input', () => {
        const formData = new FormData(document.getElementById('note-form'));
        const noteId = window.location.pathname.split('/').filter(Boolean).pop();

        fetch(`/notes/${noteId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('Изменения сохранены');
                fetchNotes();
            } else {
                console.error('Произошла ошибка при сохранении изменений');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    fetchNotes();
    handleAddNote();

    const noteTitleInput = document.getElementById('note-form');

    noteTitleInput.addEventListener('input', function(event) {
        saveNoteOnChange(noteTitleInput.form);
    });

    const textArea = document.getElementById('text');
    const container = document.querySelector('.container');

    textArea.addEventListener('input', function() {
        const containerHeight = container.clientHeight;
        const textAreaScrollHeight = this.scrollHeight;

        if (textAreaScrollHeight > containerHeight) {
            container.style.height = textAreaScrollHeight + 'px';
        } else {
            container.style.height = '100%';
        }

        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});