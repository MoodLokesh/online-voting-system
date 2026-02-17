from django.db import models


class Voter(models.Model):
    full_name = models.CharField(max_length=100)
    govt_voter_id = models.CharField(max_length=50, unique=True)

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    gender = models.CharField(max_length=10)
    constituency = models.CharField(max_length=100)
    dob = models.DateField()

    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.username})"


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    constituency = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vote(models.Model):
    voter = models.OneToOneField(
        Voter,
        on_delete=models.CASCADE,
        related_name="vote"
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    voted_at = models.DateTimeField(auto_now_add=True)
