from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField,
    BooleanField, SubmitField, HiddenField, PasswordField, DateField,
    DecimalField
)
from wtforms.validators import DataRequired, InputRequired, Length, Optional, ValidationError
from flask_wtf.file import FileField, FileAllowed

from models import DOCUMENT_TYPE_CHOICES, PROJECT_STATUS_CHOICES


class BlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=300)])

    summary = TextAreaField("Summary", validators=[DataRequired()])
    content = HiddenField("Content")
    author_name = StringField("Author Name", validators=[DataRequired()])

    category_id = SelectField('Category', coerce=str, validators=[DataRequired()])

    featured_image = FileField(
        "Featured Image",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp"], "Images only")]
    )
    featured_image_alt = StringField(
        "Featured Image Alt Text",
        validators=[Optional(), Length(max=255)]
    )

    # ── SEO ──
    seo_title = StringField(
        "SEO Title",
        validators=[Optional(), Length(max=255)]
    )
    seo_description = TextAreaField(
        "Meta Description",
        validators=[Optional(), Length(max=300)]
    )
    seo_keywords = TextAreaField(
        "Focus Keywords",
        validators=[Optional()]
    )

    is_published = BooleanField("Publish now")

    submit = SubmitField("Save Blog")


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=256)])
    submit = SubmitField("Login")


class DeleteForm(FlaskForm):
    pass


class ProjectPaymentForm(FlaskForm):
    amount = DecimalField("Payment Amount", places=2, validators=[InputRequired()])
    paid_on = DateField("Payment Date", validators=[DataRequired()])
    note = StringField("Note", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Add Payment")

    def validate_amount(self, field):
        if field.data is not None and field.data <= 0:
            raise ValidationError("Payment amount must be greater than zero.")


class ProjectForm(FlaskForm):
    name = StringField("Project Name", validators=[DataRequired(), Length(max=180)])
    client_name = StringField("Client Name", validators=[DataRequired(), Length(max=180)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=3000)])
    start_date = DateField("Start Date", validators=[DataRequired()])
    expected_end_date = DateField("Expected End Date", validators=[Optional()])
    actual_completion_date = DateField("Actual Completion Date", validators=[Optional()])
    next_payment_due_date = DateField("Next Payment Due Date", validators=[Optional()])
    status = SelectField("Project Status", choices=PROJECT_STATUS_CHOICES, validators=[DataRequired()])
    total_value = DecimalField("Total Project Value", places=2, validators=[InputRequired()])
    advance_received = DecimalField("Advance Received", places=2, validators=[InputRequired()])
    document_type = SelectField("Document Type", choices=DOCUMENT_TYPE_CHOICES, validators=[Optional()])
    document_file = FileField(
        "Upload Document",
        validators=[FileAllowed(["pdf", "doc", "docx", "jpg", "jpeg", "png", "webp"], "Supported documents only")]
    )
    submit = SubmitField("Save Project")

    def validate_expected_end_date(self, field):
        if field.data and self.start_date.data and field.data < self.start_date.data:
            raise ValidationError("Expected end date cannot be before the start date.")

    def validate_actual_completion_date(self, field):
        if field.data and self.start_date.data and field.data < self.start_date.data:
            raise ValidationError("Actual completion date cannot be before the start date.")

    def validate_total_value(self, field):
        if field.data is not None and field.data < 0:
            raise ValidationError("Total project value cannot be negative.")

    def validate_advance_received(self, field):
        if field.data is not None and field.data < 0:
            raise ValidationError("Advance received cannot be negative.")

        if field.data is not None and self.total_value.data is not None and field.data > self.total_value.data:
            raise ValidationError("Advance received cannot exceed total project value.")
