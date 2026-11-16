'use strict';
const projects = JSON.parse(document.getElementById('project-data').textContent);
const inspector = document.getElementById('project-inspector');
const nodes = [...document.querySelectorAll('[data-project]')];
const edges = [...document.querySelectorAll('[data-from][data-to]')];

function selectProject(id) {
    const project = projects[id];
    if (!project) return;
    // Content is rendered and escaped by the static builder; no remote HTML.
    inspector.innerHTML = project.html;
    nodes.forEach(node => node.setAttribute('aria-current', String(node.dataset.project === id)));
    edges.forEach(edge => {
        const connected = edge.dataset.from === id || edge.dataset.to === id;
        edge.classList.toggle('is-connected', connected);
        edge.classList.toggle('is-muted', !connected);
    });
}
nodes.forEach(node => {
    node.addEventListener('click', event => {
        event.preventDefault();
        selectProject(node.dataset.project);
    });
    node.addEventListener('keydown', event => {
        if (event.key === ' ') {
            event.preventDefault();
            selectProject(node.dataset.project);
        }
    });
});
selectProject('decima');
