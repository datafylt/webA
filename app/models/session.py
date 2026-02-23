"""
Session Model - Formation Électro
"""

from tortoise import fields

from .base import BaseModel, TimestampMixin


class Session(BaseModel, TimestampMixin):
    """
    Modèle Session de formation (cours planifié)
    """

    # Relation avec Programme
    program = fields.ForeignKeyField(
        "models.Program", related_name="sessions", on_delete=fields.CASCADE, description="Programme associé"
    )

    # Informations de base
    title = fields.CharField(max_length=200, description="Titre de la session", index=True)
    description = fields.TextField(null=True, description="Description/notes")

    # Dates
    start_date = fields.DateField(description="Date de début", index=True)
    end_date = fields.DateField(null=True, description="Date de fin")
    start_time = fields.TimeField(null=True, description="Heure de début")
    end_time = fields.TimeField(null=True, description="Heure de fin")

    # Lieu
    location_type = fields.CharField(max_length=20, default="in_person", description="Type: in_person, online, hybrid")
    location = fields.CharField(max_length=200, null=True, description="Lieu physique")
    online_link = fields.CharField(max_length=500, null=True, description="Lien Zoom/Teams")

    # Capacité
    max_participants = fields.IntField(default=15, description="Places maximum")
    min_participants = fields.IntField(default=1, description="Places minimum")

    # Prix (peut être différent du programme)
    price = fields.DecimalField(
        max_digits=10, decimal_places=2, null=True, description="Prix (null = prix du programme)"
    )

    # Statut
    status = fields.CharField(
        max_length=20,
        default="scheduled",
        description="Statut: scheduled, in_progress, completed, cancelled",
        index=True,
    )

    # Formateur
    instructor_name = fields.CharField(max_length=100, null=True, description="Nom du formateur")

    class Meta:
        table = "session"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} - {self.start_date}"


class SessionEnrollment(BaseModel, TimestampMixin):
    """
    Inscription d'un étudiant à une session
    """

    session = fields.ForeignKeyField("models.Session", related_name="enrollments", on_delete=fields.CASCADE)
    student = fields.ForeignKeyField("models.Student", related_name="enrollments", on_delete=fields.CASCADE)

    # Statut inscription
    status = fields.CharField(
        max_length=20, default="enrolled", description="Statut: enrolled, completed, cancelled, no_show"
    )

    # Paiement
    payment_status = fields.CharField(max_length=20, default="pending", description="Paiement: pending, paid, refunded")
    amount_paid = fields.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Notes
    notes = fields.TextField(null=True)

    # Date inscription
    enrolled_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "session_enrollment"
        unique_together = (("session", "student"),)

    def __str__(self):
        return f"Enrollment {self.id}"
