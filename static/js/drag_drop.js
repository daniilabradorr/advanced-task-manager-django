// Función para extraer el token CSRF de las cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
  console.log('🔧 drag_drop.js cargado, inicializando drag & drop…');
  let dragged = null;

  // 1. Configurar cada .task-list como zona draggable
  document.querySelectorAll('.task-list').forEach(listEl => {
    console.log('– Registrando lista drag&drop:', listEl.dataset.listId);
    listEl.draggable = true;

    // Cuando empezamos a arrastrar la lista…
    listEl.addEventListener('dragstart', e => {
      // ▶️ CAMBIO: Solo iniciar drag de lista si el target es la propia lista,
      // evitando que al arrastrar una tarea anidada se dispare este handler.
      if (e.target !== listEl) return;
      dragged = { type: 'list', id: listEl.dataset.listId };
      console.log('⚙️ dragstart lista:', dragged);
      e.dataTransfer.effectAllowed = 'move';
    });

    // Permitir drop sobre otras listas
    listEl.addEventListener('dragover', e => {
      e.preventDefault();
    });

    // Al soltar la lista sobre otra…
    listEl.addEventListener('drop', async e => {
      e.preventDefault();
      console.log('⏬ drop lista sobre:', listEl.dataset.listId, 'con dragged=', dragged);
      if (dragged?.type === 'list') {
        const newPos = parseInt(listEl.dataset.position, 10);
        console.log(`→ PATCH /api/tasklists/${dragged.id}/move/ position=${newPos}`);
        const res = await fetch(
          `/api/tasklists/${dragged.id}/move/`,
          {
            method: 'PATCH',
            credentials: 'same-origin',          // enviar cookies de sesión
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken          // incluir token CSRF
            },
            body: JSON.stringify({ position: newPos })
          }
        );
        console.log('← Respuesta PATCH lista:', res.status);
        if (res.ok) location.reload();
      }
    });

    // 2. Dentro de cada lista, configurar sus tareas
    const ul = listEl.querySelector('ul');
    ul.querySelectorAll('li').forEach(taskEl => {
      console.log('– Registrando tarea drag&drop:', taskEl.dataset.taskId);
      taskEl.draggable = true;
      taskEl.addEventListener('dragstart', e => {
        dragged = { type: 'task', id: taskEl.dataset.taskId };
        console.log('⚙️ dragstart tarea:', dragged);
        e.dataTransfer.effectAllowed = 'move';
      });
    });

    // Permitir drop sobre la lista para tareas
    ul.addEventListener('dragover', e => e.preventDefault());

    // Al soltar una tarea en esta lista…
    ul.addEventListener('drop', async e => {
      e.preventDefault();
      console.log('⏬ drop tarea sobre lista:', listEl.dataset.listId, 'con dragged=', dragged);
      if (dragged?.type === 'task') {
        const newListId = parseInt(listEl.dataset.listId, 10);
        const items = Array.from(ul.children);
        const dropTargetLi = e.target.closest('li');
        const newPos = dropTargetLi
          ? items.indexOf(dropTargetLi) + 1
          : items.length + 1;
        console.log(`→ PATCH /api/tasks/${dragged.id}/move/ task_list=${newListId}, position=${newPos}`);
        const res = await fetch(
          `/api/tasks/${dragged.id}/move/`,
          {
            method: 'PATCH',
            credentials: 'same-origin',          // enviar cookies de sesión
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken          // incluir token CSRF
            },
            body: JSON.stringify({ task_list: newListId, position: newPos })
          }
        );
        console.log('← Respuesta PATCH tarea:', res.status);
        if (res.ok) location.reload();
      }
    });
  });
});