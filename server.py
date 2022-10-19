from flask import Flask, request, redirect
import random

app = Flask(__name__)

next_id = 4
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'},
]

def get_contents():
    liTags = ''
    for topic in topics:
        liTags += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return liTags

def template(contents, content, id=None):
    context_ui = ''
    if id != None:
        context_ui = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''

    return f'''
    <!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {context_ui}
            </ul>
        </body>
    </html>
    '''

@app.route('/')
def index():
    liTags = get_contents()

    return template(liTags, '<h2>Welcome</h2>Hello, Web')

@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(get_contents(), f'<h2>{title}</h2>{body}', id)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(get_contents(), content)
    elif request.method == "POST":
        global next_id
        new_topic = {
            'id': next_id,
            'title': request.form['title'],
            'body': request.form['body']
        }
        topics.append(new_topic)
        url = f'/read/{next_id}/'
        next_id += 1
        return redirect(url)
        

@app.route('/update/<int:id>/', methods=["GET", "POST"])
def update(id):
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value={title}></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(get_contents(), content, id)
    elif request.method == "POST":
        title = request.form['title'] 
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = f'/read/{id}/'
        return redirect(url)


@app.route('/delete/<int:id>/', methods=["POST"])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)