from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Question(models.Model):
    statement = models.TextField()
    enable = models.BooleanField(default=False)
    options = models.JSONField()
    answer = models.IntegerField(choices=[
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D'),
    ])

    def __str__(self):
        return self.statement


class Reply(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['player', 'question'], name='unique_answer')
        ]
