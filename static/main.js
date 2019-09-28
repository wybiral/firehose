// WebSocket connection
let socket;

function createUpdate(data) {
    const article = document.createElement('article');
    const header = document.createElement('header');
    if (data.thumb) {
        const thumb = document.createElement('img');
        thumb.src = data.thumb;
        header.appendChild(thumb);
    }
    article.appendChild(header);
    const title = document.createElement('a');
    title.className = 'title';
    title.href = data.url;
    title.target = '_blank';
    title.innerText = data.title;
    header.appendChild(title);
    const source = document.createElement('div');
    header.appendChild(source);
    source.className = 'source';
    const sourceLink = document.createElement('a');
    sourceLink.href = data.source.url;
    sourceLink.target = '_blank';
    let sourceName = data.source.name;
    if (data.source.category) {
        sourceName += ' (' + data.source.category + ')';
    }
    sourceLink.innerText = sourceName;
    source.appendChild(sourceLink);
    const clear = document.createElement('div');
    clear.style.clear = 'both';
    header.appendChild(clear);
    const body = document.createElement('p');
    if (typeof data.body != 'undefined') {
        body.appendChild(document.createTextNode(data.body));
    }
    article.appendChild(body);
    return article;
}

function connect(updates) {
    let url = 'ws://localhost:8000/socket';
    socket = new WebSocket(url);
    socket.onmessage = evt => {
        const data = JSON.parse(evt.data);
        updates.appendChild(createUpdate(data));
    };
    // if WebSocket closes keep trying to connect
    socket.onclose = evt => setTimeout(() => connect(updates), 1000);
}

window.onload = () => {
    const updates = document.querySelector('main');
    connect(updates);
};