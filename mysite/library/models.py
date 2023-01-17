import uuid as uuid
from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(verbose_name='Pavadinimas', max_length=200, help_text='Iveskite knygos zanra, pvz "detektyvas"')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Zanras'
        verbose_name_plural = 'Zanrai'

class Book(models.Model):
    title = models.CharField(verbose_name='Pavadinimas', max_length=200)
    summary = models.TextField(verbose_name='Aprasymas', max_length=1000)
    isbn = models.CharField(verbose_name='ISBN', max_length=13)
    author = models.ForeignKey(to='Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(to='Genre')

    def display_genre(self):
        sujungta = ''
        zanrai = self.genre.all()
        for zanras in zanrai:
            sujungta += zanras.name + ', '
        return sujungta

    display_genre.short_description = "Zanras"

    def __str__(self):
        return f'"{self.title}" {self.author}'

    class Meta:
        verbose_name = 'Knyga'
        verbose_name_plural = 'Knygos'

class Author(models.Model):
    first_name = models.CharField(verbose_name='Vardas', max_length=100)
    last_name = models.CharField(verbose_name='Pavarde', max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Autorius'
        verbose_name_plural = 'Autoriai'

class BookInstance(models.Model):
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE)
    uuid = models.UUIDField(verbose_name='UUID', default= uuid.uuid4, help_text= 'Unikalus ID knygos kopijai')
    due_back = models.DateField(verbose_name='Bus prieinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Statusas',
    )

    def __str__(self):
        return  f'{self.book} - {self.uuid}'

    class Meta:
        verbose_name = 'Uzsakyta preke'
        verbose_name_plural = 'Uzsakytos prekes'