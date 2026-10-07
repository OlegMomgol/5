from flask import Flask, session, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-me'


@app.route('/')
def index():
    session['visits'] = session.get('visits', 0) + 1
    return render_template('index.html', visits=session['visits'])


@app.route('/reset')
def reset():
    session['visits'] = 0
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)