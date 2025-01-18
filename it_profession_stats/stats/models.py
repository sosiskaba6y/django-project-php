from django.db import models

class PageCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PageContent(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(PageCategory, on_delete=models.CASCADE, related_name='contents')
    image = models.ImageField(upload_to='graphs/', null=True, blank=True)  # Путь для загрузки графиков
    table_content = models.TextField(blank=True)  # Текстовое поле для таблицы (можно использовать HTML)

    def __str__(self):
        return self.title