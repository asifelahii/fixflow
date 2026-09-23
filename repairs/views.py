from django.shortcuts import get_object_or_404, redirect, render

from .forms import TrackingForm
from .models import RepairTicket


def home(request):
    form = TrackingForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        tracking_code = form.cleaned_data["tracking_code"]

        ticket_exists = RepairTicket.objects.filter(
            tracking_code=tracking_code,
        ).exists()

        if not ticket_exists:
            form.add_error(
                "tracking_code",
                "Ticket not found. Please check the tracking code.",
            )
        else:
            return redirect(
                "repairs:ticket_detail",
                tracking_code=tracking_code,
            )

    return render(
        request,
        "repairs/home.html",
        {
            "form": form,
        },
    )


def ticket_detail(request, tracking_code):
    normalized_code = tracking_code.strip().upper()

    if tracking_code != normalized_code:
        return redirect(
            "repairs:ticket_detail",
            tracking_code=normalized_code,
        )

    ticket = get_object_or_404(
        RepairTicket.objects.select_related("device"),
        tracking_code=normalized_code,
    )

    status_history = ticket.status_history.order_by(
        "created_at"
    )

    safe_history = [
        {
            "from_status": (
                history.get_from_status_display()
                if history.from_status
                else ""
            ),
            "to_status": history.get_to_status_display(),
            "customer_note": history.customer_note,
            "created_at": history.created_at,
        }
        for history in status_history
    ]

    public_ticket = {
        "tracking_code": ticket.tracking_code,
        "device_label": (
            f"{ticket.device.brand} "
            f"{ticket.device.model_name}"
        ),
        "status": ticket.get_status_display(),
        "expected_completion_date": (
            ticket.expected_completion_date
        ),
        "customer_visible_note": (
            ticket.customer_visible_note
        ),
        "history": safe_history,
    }

    return render(
        request,
        "repairs/ticket_detail.html",
        {
            "ticket": public_ticket,
        },
    )