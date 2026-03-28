from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField,
    BooleanField, SubmitField
)
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class BlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=300)])

    summary = TextAreaField("Summary", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])

    author_name = StringField("Author Name", validators=[DataRequired()])

    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])

    featured_image = FileField(
        "Featured Image",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp"], "Images only")]
    )

    is_published = BooleanField("Publish now")

    submit = SubmitField("Save Blog")
