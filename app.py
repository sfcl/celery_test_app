# -*- coding:utf-8 -*-


from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from celery import Celery


app = Flask(__name__)
#app.config.from_systemctl start redis-serverobject("config")
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']


client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)

mail = Mail(app)

@client.task
def send_mail(data):
    """ Function to send emails.
    """
    with app.app_context():
        msg = Message("Ping!",
                    sender="admin.ping",
                    recipients=[data['email']])
        msg.body = data['message']
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        data = {}
        data['email'] = request.form['email']
        data['first_name'] = request.form['first_name']
        data['last_name'] = request.form['last_name']
        data['message'] = request.form['message']
        duration = int(request.form['duration'])
        duration_unit = request.form['duration_unit']

        if duration_unit == 'minutes':
            duration *= 60
        elif duration_unit == 'hours':
            duration *= 3600
        elif duration_unit == 'days':
            duration *= 86400

        send_mail.apply_async(args=[data], countdown=duration)
        mes = 'Email will be sent to {email} in {duration} {duration_unit}'.format(email=data["email"], 
                                                                                   duration=request.form["duration"],
                                                                                   duration_unit=duration_unit)
        flash(mes)
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)

