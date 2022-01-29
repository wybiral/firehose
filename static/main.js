// WebSocket connection
let socket;

function createUpdate(data) {
    const article = document.createElement('article');
    const header = document.createElement('header');
    if (data.thumb) {
        const thumb = document.createElement('div');
        header.appendChild(thumb);
        thumb.className = 'thumb'
        const img = document.createElement('img');
        thumb.appendChild(img);
        img.src = data.thumb;
    }
    article.appendChild(header);
    const info = document.createElement('div');
    header.appendChild(info);
    info.className = 'info';
    const title = document.createElement('a');
    info.appendChild(title);
    title.className = 'title';
    title.href = data.url;
    title.target = '_blank';
    title.innerText = data.title;
    const source = document.createElement('div');
    info.appendChild(source);
    source.className = 'source';
    const sourceLink = document.createElement('a');
    sourceLink.href = data.source_url;
    sourceLink.target = '_blank';
    let sourceName = data.source_name;
    if (data.category) {
        sourceName += ' (' + data.category + ')';
    }
    sourceLink.innerText = sourceName;
    source.appendChild(sourceLink);
    const date = document.createElement('div');
    info.appendChild(date);
    date.className = 'date';
    date.innerText = data.published.split(' ')[0];
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
    const stream = new EventSource('/stream');
    stream.addEventListener('message', evt => {
        const data = JSON.parse(evt.data);
        updates.insertBefore(createUpdate(data), updates.firstChild);
    });
}

window.onload = () => {
    const updates = document.querySelector('main');
    connect(updates);
};