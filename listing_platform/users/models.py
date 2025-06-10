from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wiadomość od {self.sender} do {self.recipient}"

class UserRating(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    score = models.PositiveSmallIntegerField()  # 1 to 5
    comment = models.TextField(blank=True)  # <-- nowy komentarz
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'rated_user')

    def __str__(self):
        return f"{self.reviewer.username} rated {self.rated_user.username} ({self.score}/5)"

