from django.db import models


class Models(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='І\'мя Фамілія', max_length=255)
    img = models.ImageField(verbose_name='Фото обкладинки', upload_to='Models-Cover/Profile-Img/')
    profile_img = models.FileField(verbose_name='Інші фото', blank=True, null=True)
    info = models.TextField(verbose_name='Опис', blank=True, null=True)
    score = models.IntegerField(verbose_name='Кількість балів', blank=True, null=True, editable=False, default=0)

    def save(self, **kwargs):
        super(Models, self).save()

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Моделі'

