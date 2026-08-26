from flask import Blueprint, abort, current_app, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from models import (
    BlogPost,
    Category,
    ContactLead,
    Project,
    ProjectDocument,
    ProjectPayment,
    ensure_contact_leads_table,
    ensure_project_tables,
    format_money,
    signed_project_document_url,
    upload_project_document,
    upload_blog_image,
)
from .forms import AdminLoginForm, BlogForm, DeleteForm, ProjectForm, ProjectPaymentForm
from .utils import generate_unique_slug
from security_utils import admin_ip_login_limiter, admin_login_limiter, login_ip_key, login_rate_key
import re
import os
from datetime import date, datetime, timedelta
from decimal import Decimal
from extensions import db
from sqlalchemy.orm import selectinload
from werkzeug.utils import secure_filename

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ALLOWED_PROJECT_DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx", "jpg", "jpeg", "png", "webp"}
PROJECTS_PER_PAGE = 20
_ADMIN_CONTENT_TABLES_READY_FOR = None


@admin_bp.before_request
def require_admin_user():
    if request.endpoint == "admin.login":
        return None

    if not current_user.is_authenticated:
        return redirect(url_for("admin.login"))

    if not getattr(current_user, "is_admin", False):
        abort(403)

    return None

# ============================
# LOGIN
# ============================
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        rate_key = login_rate_key("admin", form.username.data, request.remote_addr)
        ip_rate_key = login_ip_key("admin", request.remote_addr)
        if admin_login_limiter.is_limited(rate_key) or admin_ip_login_limiter.is_limited(ip_rate_key):
            flash("Too many login attempts. Please try again later.", "error")
            return render_template("admin/login.html", form=form), 429

        if verify_admin_credentials(form.username.data, form.password.data):
            from app import AdminUser
            session.clear()
            login_user(AdminUser())
            admin_login_limiter.reset(rate_key)
            admin_ip_login_limiter.reset(ip_rate_key)
            return redirect(url_for("admin.dashboard"))

        admin_login_limiter.record_failure(rate_key)
        admin_ip_login_limiter.record_failure(ip_rate_key)
        flash("Invalid credentials", "error")

    return render_template("admin/login.html", form=form)


def verify_admin_credentials(username, password):
    expected_username = os.getenv("ADMIN_USERNAME")
    plaintext_password = os.getenv("ADMIN_PASSWORD")

    if username != expected_username:
        return False

    return bool(plaintext_password) and password == plaintext_password


def flash_database_error(error, message="Sorry, there was a database problem. Please try again."):
    current_app.logger.exception("Admin database error: %s", error)
    flash(message, "error")


def ensure_admin_content_tables():
    global _ADMIN_CONTENT_TABLES_READY_FOR

    database_key = str(db.engine.url)
    if _ADMIN_CONTENT_TABLES_READY_FOR == database_key:
        return

    auto_migrate = os.getenv("ADMIN_AUTO_MIGRATE", "").lower() in {"1", "true", "yes", "on"}
    if db.engine.dialect.name != "sqlite" and not auto_migrate:
        _ADMIN_CONTENT_TABLES_READY_FOR = database_key
        return

    Category.__table__.create(bind=db.engine, checkfirst=True)
    BlogPost.__table__.create(bind=db.engine, checkfirst=True)
    for table in (Category.__table__, BlogPost.__table__):
        for index in table.indexes:
            index.create(bind=db.engine, checkfirst=True)

    _ADMIN_CONTENT_TABLES_READY_FOR = database_key

# ============================
# LOGOUT
# ============================
@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/#")

# ============================
# DASHBOARD
# ============================
@admin_bp.route("/")
@login_required
def dashboard():
    ensure_admin_content_tables()
    ensure_contact_leads_table()
    ensure_project_tables()
    today = date.today()
    period = request.args.get("period", "6m")
    if period not in {"6m", "12m", "year"}:
        period = "6m"

    projects = Project.query.options(selectinload(Project.payments)).order_by(Project.created_at.desc()).all()
    current_month = today.replace(day=1)
    previous_month = add_months(current_month, -1)
    next_month = add_months(current_month, 1)

    def in_month(value, month_start, month_end):
        if value is None:
            return False
        value = value.date() if isinstance(value, datetime) else value
        return month_start <= value < month_end

    new_projects_this_month = len([
        project for project in projects
        if in_month(project.created_at, current_month, next_month)
    ])
    new_projects_last_month = len([
        project for project in projects
        if in_month(project.created_at, previous_month, current_month)
    ])
    completed_this_month = len([
        project for project in projects
        if in_month(project.actual_completion_date, current_month, next_month)
    ])
    new_leads_this_month = ContactLead.query.filter(
        ContactLead.created_at >= datetime.combine(current_month, datetime.min.time()),
        ContactLead.created_at < datetime.combine(next_month, datetime.min.time()),
    ).count()
    new_leads_last_month = ContactLead.query.filter(
        ContactLead.created_at >= datetime.combine(previous_month, datetime.min.time()),
        ContactLead.created_at < datetime.combine(current_month, datetime.min.time()),
    ).count()
    project_count = len(projects)
    active_project_count = len([project for project in projects if project.status == "active"])
    completed_project_count = len([project for project in projects if project.status == "completed"])
    total_value = sum((decimal_value(project.total_value) for project in projects), Decimal("0.00"))
    revenue_collected = sum((project.collected_amount for project in projects), Decimal("0.00"))
    outstanding = sum((project.remaining_amount for project in projects), Decimal("0.00"))
    monthly_revenue = build_monthly_revenue(period, today, projects=projects)
    monthly_revenue_by_month = {item["month"]: item["amount"] for item in monthly_revenue}
    revenue_this_month = monthly_revenue_by_month.get(current_month, Decimal("0.00"))
    revenue_last_month = monthly_revenue_by_month.get(previous_month, Decimal("0.00"))
    status_distribution = build_status_distribution(projects)
    active_statuses = {"active", "on_hold"}

    def change_label(current, previous):
        if previous == 0:
            return "New this month" if current > 0 else "No change this month"
        change = round(((current - previous) / abs(previous)) * 100)
        sign = "+" if change > 0 else ""
        return f"{sign}{change}% vs last month"

    return render_template(
        "admin/dashboard.html",
        blog_count=BlogPost.query.count(),
        category_count=Category.query.count(),
        project_count=project_count,
        active_project_count=active_project_count,
        completed_project_count=completed_project_count,
        total_project_value=format_money(total_value),
        revenue_collected=format_money(revenue_collected),
        outstanding_amount=format_money(outstanding),
        lead_count=ContactLead.query.count(),
        project_change=change_label(new_projects_this_month, new_projects_last_month),
        active_project_change=f"{new_projects_this_month} new this month",
        completed_project_change=f"{completed_this_month} completed this month",
        lead_change=change_label(new_leads_this_month, new_leads_last_month),
        total_value_change="Portfolio total",
        revenue_change=change_label(revenue_this_month, revenue_last_month),
        outstanding_change="Balance due",
        content_change="Content library",
        recent_leads=ContactLead.query.order_by(ContactLead.created_at.desc()).limit(5).all(),
        recent_projects=projects[:5],
        projects_due_soon=[project for project in projects if project.is_due_soon(today)][:5],
        overdue_projects=[project for project in projects if project.is_overdue(today)][:5],
        payments_due_soon=[
            project for project in projects
            if project.status in active_statuses and project.is_payment_due_soon(today)
        ][:5],
        monthly_revenue=monthly_revenue,
        monthly_revenue_max=max([item["amount"] for item in monthly_revenue] or [Decimal("0.00")]),
        status_distribution=status_distribution,
        period=period,
    )


@admin_bp.route("/leads")
@login_required
def lead_list():
    ensure_contact_leads_table()
    leads = ContactLead.query.order_by(ContactLead.created_at.desc()).all()
    return render_template("admin/lead_list.html", leads=leads, delete_form=DeleteForm())


@admin_bp.route("/leads/<int:lead_id>/delete", methods=["POST"])
@login_required
def delete_lead(lead_id):
    ensure_contact_leads_table()
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Lead delete action could not be verified. Please try again.", "error")
        return redirect(url_for("admin.lead_list"))

    lead = ContactLead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    flash("Lead deleted.", "success")
    return redirect(url_for("admin.lead_list"))


def apply_project_payment_filter(query, payment_filter):
    if payment_filter == "paid":
        paid_ids = [
            project.id
            for project in Project.query.options(selectinload(Project.payments)).all()
            if project.payment_status == "paid"
        ]
        return query.filter(Project.id.in_(paid_ids or [-1]))

    if payment_filter == "partial":
        partial_ids = [
            project.id
            for project in Project.query.options(selectinload(Project.payments)).all()
            if project.payment_status == "partial"
        ]
        return query.filter(Project.id.in_(partial_ids or [-1]))

    if payment_filter == "unpaid":
        unpaid_ids = [
            project.id
            for project in Project.query.options(selectinload(Project.payments)).all()
            if project.payment_status == "unpaid"
        ]
        return query.filter(Project.id.in_(unpaid_ids or [-1]))

    return query


def project_outstanding_filter(query):
    return query.filter(db.or_(Project.total_value <= 0, Project.advance_received < Project.total_value))


def sum_project_column(column):
    return db.session.query(db.func.coalesce(db.func.sum(column), 0)).scalar() or 0


def sum_project_outstanding_amount():
    return sum(
        (project.remaining_amount for project in Project.query.options(selectinload(Project.payments)).all()),
        Decimal("0.00"),
    )


def decimal_value(value):
    if value is None:
        return Decimal("0.00")
    return Decimal(value).quantize(Decimal("0.01"))


def add_months(value, months):
    month = value.month - 1 + months
    year = value.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)


def reporting_months(period, today):
    if period == "12m":
        count = 12
        start = add_months(today.replace(day=1), -11)
    elif period == "year":
        start = date(today.year, 1, 1)
        count = today.month
    else:
        count = 6
        start = add_months(today.replace(day=1), -5)

    return [add_months(start, offset) for offset in range(count)]


def build_monthly_revenue(period, today, projects=None):
    months = reporting_months(period, today)
    revenue_by_month = {month: Decimal("0.00") for month in months}
    if not months:
        return []

    if projects is None:
        projects = Project.query.options(selectinload(Project.payments)).all()

    for project in projects:
        for payment in project.payments:
            if payment.paid_on < months[0]:
                continue
            month = payment.paid_on.replace(day=1)
            if month in revenue_by_month:
                revenue_by_month[month] += decimal_value(payment.amount)

    # Legacy projects only contribute when no payment rows exist for that project.
    for project in projects:
        if project.advance_received <= 0:
            continue
        if project.payments:
            continue
        month_source = project.start_date or project.created_at.date()
        month = month_source.replace(day=1)
        if month in revenue_by_month:
            revenue_by_month[month] += decimal_value(project.advance_received)

    return [
        {
            "month": month,
            "label": month.strftime("%b %Y"),
            "amount": amount,
            "amount_label": format_money(amount),
        }
        for month, amount in revenue_by_month.items()
    ]


def build_status_distribution(projects):
    labels = {
        "active": "Active",
        "completed": "Completed",
        "on_hold": "On Hold",
        "cancelled": "Cancelled",
    }
    total = len(projects) or 1
    distribution = []
    start = 0
    colors = {
        "active": "#21c7a8",
        "completed": "#2f6fed",
        "on_hold": "#f59e0b",
        "cancelled": "#dc2626",
    }
    for status, label in labels.items():
        count = len([project for project in projects if project.status == status])
        percent = round((count / total) * 100, 1) if projects else 0
        end = start + percent
        distribution.append({
            "status": status,
            "label": label,
            "count": count,
            "percent": percent,
            "color": colors[status],
            "range": f"{start}% {end}%",
        })
        start = end
    return distribution


@admin_bp.route("/projects")
@login_required
def project_list():
    ensure_project_tables()
    status_filter = request.args.get("status", "").strip()
    payment_filter = request.args.get("payment", "").strip()
    page = request.args.get("page", 1, type=int)
    query = Project.query.options(selectinload(Project.payments))

    if status_filter:
        query = query.filter(Project.status == status_filter)

    if payment_filter:
        query = apply_project_payment_filter(query, payment_filter)

    pagination = query.order_by(Project.created_at.desc()).paginate(
        page=page,
        per_page=PROJECTS_PER_PAGE,
        error_out=False,
    )

    return render_template(
        "admin/project_list.html",
        projects=pagination.items,
        pagination=pagination,
        status_filter=status_filter,
        payment_filter=payment_filter,
        delete_form=DeleteForm(),
    )


@admin_bp.route("/projects/dashboard")
@login_required
def project_dashboard():
    ensure_project_tables()
    today = date.today()
    month_start = today.replace(day=1)
    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month_start = month_start.replace(month=month_start.month + 1)

    projects = Project.query.options(selectinload(Project.payments)).order_by(Project.created_at.desc()).all()

    return render_template(
        "admin/project_dashboard.html",
        total_projects=Project.query.count(),
        active_projects=Project.query.filter_by(status="active").count(),
        completed_projects=Project.query.filter_by(status="completed").count(),
        on_hold_projects=Project.query.filter_by(status="on_hold").count(),
        cancelled_projects=Project.query.filter_by(status="cancelled").count(),
        awaiting_payment_count=project_outstanding_filter(Project.query).count(),
        completed_pending_count=project_outstanding_filter(Project.query.filter_by(status="completed")).count(),
        monthly_projects=Project.query
            .filter(Project.start_date >= month_start)
            .filter(Project.start_date < next_month_start)
            .count(),
        total_value=format_money(sum((decimal_value(project.total_value) for project in projects), Decimal("0.00"))),
        collected_amount=format_money(sum((project.collected_amount for project in projects), Decimal("0.00"))),
        outstanding_amount=format_money(sum((project.remaining_amount for project in projects), Decimal("0.00"))),
        recent_projects=projects[:6],
    )


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def create_project():
    ensure_project_tables()
    form = ProjectForm()

    if request.method == "GET":
        form.start_date.data = date.today()
        form.status.data = "active"
        form.total_value.data = 0
        form.advance_received.data = 0

    if form.validate_on_submit():
        project = Project(
            name=form.name.data.strip(),
            client_name=form.client_name.data.strip(),
            description=(form.description.data or "").strip() or None,
            start_date=form.start_date.data,
            expected_end_date=form.expected_end_date.data,
            actual_completion_date=form.actual_completion_date.data,
            next_payment_due_date=form.next_payment_due_date.data,
            status=form.status.data,
            total_value=form.total_value.data,
            advance_received=form.advance_received.data,
        )

        try:
            db.session.add(project)
            db.session.flush()
            create_initial_project_payment(project, form.advance_received.data, form.start_date.data)
            save_project_document(project, form)
            db.session.commit()
            flash("Project created successfully.", "success")
            return redirect(url_for("admin.project_list"))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
        except Exception as e:
            db.session.rollback()
            flash_database_error(e)

    return render_template("admin/project_form.html", form=form, is_edit=False, project=None)


@admin_bp.route("/projects/<int:project_id>")
@login_required
def project_detail(project_id):
    ensure_project_tables()
    project = Project.query.options(selectinload(Project.payments)).filter_by(id=project_id).first_or_404()
    payment_form = ProjectPaymentForm()
    payment_form.paid_on.data = date.today()
    return render_template(
        "admin/project_detail.html",
        project=project,
        delete_form=DeleteForm(),
        payment_form=payment_form,
    )


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    ensure_project_tables()
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        project.name = form.name.data.strip()
        project.client_name = form.client_name.data.strip()
        project.description = (form.description.data or "").strip() or None
        project.start_date = form.start_date.data
        project.expected_end_date = form.expected_end_date.data
        project.actual_completion_date = form.actual_completion_date.data
        project.next_payment_due_date = form.next_payment_due_date.data
        project.status = form.status.data
        project.total_value = form.total_value.data
        project.advance_received = form.advance_received.data

        try:
            save_project_document(project, form)
            db.session.commit()
            flash("Project updated.", "success")
            return redirect(url_for("admin.project_detail", project_id=project.id))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
        except Exception as e:
            db.session.rollback()
            flash_database_error(e)

    return render_template("admin/project_form.html", form=form, is_edit=True, project=project)


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    ensure_project_tables()
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Project delete action could not be verified. Please try again.", "error")
        return redirect(url_for("admin.project_list"))

    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("admin.project_list"))


@admin_bp.route("/projects/<int:project_id>/payments", methods=["POST"])
@login_required
def create_project_payment(project_id):
    ensure_project_tables()
    project = Project.query.get_or_404(project_id)
    form = ProjectPaymentForm()
    if not form.validate_on_submit():
        flash("Payment could not be saved. Check the amount and date.", "error")
        return redirect(url_for("admin.project_detail", project_id=project.id))

    payment = ProjectPayment(
        project=project,
        amount=form.amount.data,
        paid_on=form.paid_on.data,
        note=(form.note.data or "").strip() or None,
    )
    db.session.add(payment)
    db.session.commit()
    flash("Payment added.", "success")
    return redirect(url_for("admin.project_detail", project_id=project.id))


@admin_bp.route("/projects/<int:project_id>/payments/<int:payment_id>/delete", methods=["POST"])
@login_required
def delete_project_payment(project_id, payment_id):
    ensure_project_tables()
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Payment delete action could not be verified. Please try again.", "error")
        return redirect(url_for("admin.project_detail", project_id=project_id))

    payment = ProjectPayment.query.filter_by(id=payment_id, project_id=project_id).first_or_404()
    db.session.delete(payment)
    db.session.commit()
    flash("Payment deleted.", "success")
    return redirect(url_for("admin.project_detail", project_id=project_id))


@admin_bp.route("/projects/<int:project_id>/documents/<int:document_id>/delete", methods=["POST"])
@login_required
def delete_project_document(project_id, document_id):
    ensure_project_tables()
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Document delete action could not be verified. Please try again.", "error")
        return redirect(url_for("admin.project_detail", project_id=project_id))

    document = ProjectDocument.query.filter_by(id=document_id, project_id=project_id).first_or_404()
    db.session.delete(document)
    db.session.commit()
    flash("Project document removed.", "success")
    return redirect(url_for("admin.project_detail", project_id=project_id))


@admin_bp.route("/projects/<int:project_id>/documents/<int:document_id>/download")
@login_required
def download_project_document(project_id, document_id):
    ensure_project_tables()
    document = ProjectDocument.query.filter_by(id=document_id, project_id=project_id).first_or_404()
    expires_at = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
    signed_url = signed_project_document_url(document, expires_at)

    if not signed_url:
        flash("This document is unavailable. Please upload it again.", "error")
        return redirect(url_for("admin.project_detail", project_id=project_id))

    return redirect(signed_url)


def save_project_document(project, form):
    if not form.document_file.data:
        return

    file = form.document_file.data
    file_name = secure_filename(file.filename or "project-document")
    validate_project_document_file(file, file_name)
    upload_result = upload_project_document(file)

    if not upload_result:
        return

    document = ProjectDocument(
        project=project,
        document_type=form.document_type.data or "supporting",
        file_name=file_name,
        file_url=upload_result.get("secure_url") or "",
        cloudinary_public_id=upload_result.get("public_id"),
        cloudinary_resource_type=upload_result.get("resource_type") or "raw",
        cloudinary_delivery_type=upload_result.get("type") or "private",
    )
    db.session.add(document)


def create_initial_project_payment(project, amount, paid_on):
    amount = decimal_value(amount)
    if amount <= 0:
        return

    db.session.add(ProjectPayment(
        project=project,
        amount=amount,
        paid_on=paid_on or date.today(),
        note="Initial advance",
    ))


def validate_project_document_file(file, file_name):
    extension = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
    if extension not in ALLOWED_PROJECT_DOCUMENT_EXTENSIONS:
        raise ValueError("Unsupported project document type.")

    header = file.stream.read(16)
    file.stream.seek(0)

    valid_signatures = {
        "pdf": header.startswith(b"%PDF-"),
        "png": header.startswith(b"\x89PNG\r\n\x1a\n"),
        "jpg": header.startswith(b"\xff\xd8\xff"),
        "jpeg": header.startswith(b"\xff\xd8\xff"),
        "webp": header.startswith(b"RIFF") and header[8:12] == b"WEBP",
        "doc": header.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"),
        "docx": header.startswith(b"PK\x03\x04"),
    }

    if not valid_signatures.get(extension, False):
        raise ValueError("Uploaded document content does not match the selected file type.")

# ============================
# BLOG LIST
# ============================
@admin_bp.route("/blogs")
@login_required
def blog_list():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template("admin/blog_list.html", blogs=posts)

# ============================
# CREATE BLOG 
# ============================
@admin_bp.route("/blogs/new", methods=["GET", "POST"])
@login_required
def create_blog():
    form = BlogForm()
    # Populate category choices
    form.category_id.choices = [
        (str(c.id), c.name) for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():
        content = request.form.get('content', '').strip()
        # Strip all HTML tags and check there is actual visible text
        if not re.sub(r'<[^>]+>', '', content).strip():
            flash("Blog content cannot be empty.", "error")
            return render_template("admin/blog_form.html", form=form, is_edit=False)

        # Handle Image Upload
        image_url = None
        if form.featured_image.data:
            image_url = upload_blog_image(form.featured_image.data)

        # Create the new record
        post = BlogPost(
            title=form.title.data,
            slug=generate_unique_slug(form.title.data),
            summary=form.summary.data,
            content=content,
            author_name=form.author_name.data,
            category_id=form.category_id.data,
            featured_image=image_url,
            featured_image_alt=form.featured_image_alt.data or None,
            seo_title=form.seo_title.data or None,
            seo_description=form.seo_description.data or None,
            seo_keywords=form.seo_keywords.data or None,
            is_published=form.is_published.data,
            published_at=db.func.now() if form.is_published.data else None,
        )

        try:
            db.session.add(post)
            db.session.commit()
            flash("Blog created successfully!", "success")
            return redirect(url_for("admin.blog_list"))
        except Exception as e:
            db.session.rollback()
            flash_database_error(e)

    else:
        print("VALIDATION FAILED!")
        print(form.errors)

    
    return render_template("admin/blog_form.html", form=form, is_edit=False)

# ============================
# EDIT BLOG
# ============================
@admin_bp.route("/blogs/<int:blog_id>/edit", methods=["GET", "POST"])
@login_required
def edit_blog(blog_id):
    post = BlogPost.query.get_or_404(blog_id)
    form = BlogForm(obj=post)

    form.category_id.choices = [
        (str(c.id), c.name) for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():
        content = request.form.get('content', '').strip()
        if not re.sub(r'<[^>]+>', '', content).strip():
            flash("Blog content cannot be empty.", "error")
            return render_template("admin/blog_form.html", form=form, is_edit=True)

        post.title = form.title.data
        post.slug = generate_unique_slug(form.slug.data, post_id=post.id)
        post.summary = form.summary.data
        post.content = content
        post.author_name = form.author_name.data
        post.category_id = form.category_id.data
        post.featured_image_alt = form.featured_image_alt.data or None
        post.seo_title = form.seo_title.data or None
        post.seo_description = form.seo_description.data or None
        post.seo_keywords = form.seo_keywords.data or None
        post.is_published = form.is_published.data

        if form.is_published.data and not post.published_at:
            post.published_at = db.func.now()

        if form.featured_image.data:
            post.featured_image = upload_blog_image(form.featured_image.data)

        db.session.commit()
        flash("Blog updated", "success")
        return redirect(url_for("admin.blog_list"))

    return render_template("admin/blog_form.html", form=form, is_edit=True)

# ============================
# DELETE BLOG
# ============================
@admin_bp.route("/blogs/<int:blog_id>/delete", methods=["POST"])
@login_required
def delete_blog(blog_id):
    blog = BlogPost.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash("Blog deleted", "success")
    return redirect(url_for("admin.blog_list"))

@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
def manage_categories():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()

        if not name:
            flash("Category name required", "error")
            return redirect(url_for("admin.manage_categories"))

        existing = Category.query.filter(db.func.lower(Category.name) == name.lower()).first()
        if existing:
            flash("Category already exists", "error")
            return redirect(url_for("admin.manage_categories"))

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()

        flash("Category added", "success")
        return redirect(url_for("admin.manage_categories"))

    categories = Category.query.all()
    return render_template("admin/categories.html", categories=categories)


@admin_bp.route("/categories/inline", methods=["POST"])
@login_required
def create_category_inline():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify({"error": "Enter a category name."}), 400

    existing = Category.query.filter(db.func.lower(Category.name) == name.lower()).first()
    if existing:
        return jsonify({"error": "Category already exists."}), 409

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify({"id": str(category.id), "name": category.name}), 201

@admin_bp.route("/categories/<uuid:id>/delete", methods=["POST"])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)

    if category.posts:
        flash("Cannot delete category with blogs", "error")
        return redirect(url_for("admin.manage_categories"))

    db.session.delete(category)
    db.session.commit()

    flash("Category deleted", "success")
    return redirect(url_for("admin.manage_categories"))

# ============================
# QUILL IMAGE UPLOAD (AJAX)
# ============================
@admin_bp.route("/upload-image", methods=["POST"])
@login_required
def upload_image():
    """Upload an image from the Quill editor to Cloudinary."""
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image provided"}), 400

    try:
        url = upload_blog_image(file)
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

