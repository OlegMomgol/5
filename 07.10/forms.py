from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class TaskForm(FlaskForm):
    title = StringField(
        'название',
        validators=[DataRequired(message='нужно написать название'),
                    Length(max=200)]
    )
    description = TextAreaField('описание')
    deadline = DateTimeLocalField(
        'Дедлайн',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired(message='укажите дедлайн')]
    )
    priority = SelectField(
        'Приоритет',
        choices=[('low', 'низкий'), ('medium', 'средний'), ('high', 'высокий')],
        default='medium'
    )
    submit = SubmitField('сохранить')

    def validate_deadline(self, field):
        if field.data and field.data < datetime.now() and not getattr(self, '_is_edit', False):
            raise ValidationError('дедлайн не может быть в прошлом')